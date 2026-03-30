import os
import json
from typing import List, Dict, Any, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class TriageResult(BaseModel):
    issue_type: str = Field(description="The category of the issue (refund, shipping, etc.)")
    confidence: float = Field(description="Confidence score for the classification")
    missing_fields: List[str] = Field(description="Any missing information needed for resolution")
    clarifying_questions: List[str] = Field(description="Questions to ask the user if info is missing")

class ResolutionDraft(BaseModel):
    decision: str = Field(description="approve, deny, partial, or needs escalation")
    rationale: str = Field(description="Policy-based explanation for the decision")
    customer_response: str = Field(description="The final message to the customer")
    internal_notes: str = Field(description="Notes for the support team")

class ComplianceResult(BaseModel):
    is_compliant: bool = Field(description="Whether the response is compliant with policy and safety rules")
    issues: List[str] = Field(description="List of issues found (unsupported claims, missing citations, etc.)")
    suggested_fix: Optional[str] = Field(description="Suggested fix or rewrite instruction")
    should_escalate: bool = Field(description="Whether the issue must be escalated to a human")

class FinalResponse(BaseModel):
    classification: str = Field(description="issue type + confidence")
    clarifying_questions: List[str] = Field(description="max 3 questions if needed")
    decision: str = Field(description="approve/deny/partial/needs escalation")
    rationale: str = Field(description="policy-based explanation")
    citations: List[str] = Field(description="bullet list with doc + section/chunk id")
    customer_response: str = Field(description="customer-ready message")
    next_steps: str = Field(description="what the agent recommends support does next")

class EcommerceSupportEngine:
    def __init__(self, index_dir: str, groq_api_key: Optional[str] = None):
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                pass
                
        if not api_key:
            raise ValueError("GROQ_API_KEY must be provided, set in .env, or configured in Streamlit Secrets.")
            
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.load_local(index_dir, self.embeddings, allow_dangerous_deserialization=True)
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            api_key=api_key,
            temperature=0
        )

    def triage(self, ticket_text: str, order_context: Dict[str, Any]) -> TriageResult:
        prompt = ChatPromptTemplate.from_template("""
        You are an expert E-commerce Triage Agent. 
        Classify the following support ticket and identify any missing context fields.
        
        Ticket: {ticket_text}
        Context: {order_context}
        
        Available Categories: refund, shipping, payment, promo, fraud, other.
        """)
        chain = prompt | self.llm.with_structured_output(TriageResult)
        return chain.invoke({"ticket_text": ticket_text, "order_context": json.dumps(order_context)})

    def retrieve_policies(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        docs = self.vectorstore.similarity_search_with_relevance_scores(query, k=k)
        results = []
        for doc, score in docs:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "score": score
            })
        return results

    def write_resolution(self, ticket: str, context: Dict[str, Any], policies: List[Dict[str, Any]]) -> ResolutionDraft:
        policy_text = "\n\n".join([f"Source: {p['source']}\nContent: {p['content']}" for p in policies])
        prompt = ChatPromptTemplate.from_template("""
        You are a Resolution Writer. Draft a response based STRICTLY on the provided policies.
        Do not hallucinate policies. If the policy doesn't cover a request, escalate or deny with explanation.
        
        Ticket: {ticket}
        Context: {context}
        Policies:
        {policies}
        """)
        chain = prompt | self.llm.with_structured_output(ResolutionDraft)
        return chain.invoke({"ticket": ticket, "context": json.dumps(context), "policies": policy_text})

    def compliance_check(self, ticket: str, response: ResolutionDraft, policies: List[Dict[str, Any]]) -> ComplianceResult:
        policy_text = "\n\n".join([f"Source: {p['source']}\nContent: {p['content']}" for p in policies])
        prompt = ChatPromptTemplate.from_template("""
        You are a Compliance & Safety Agent. 
        Verify the drafted resolution against the retrieved policies.
        
        Check for:
        1. Unsupported statements (not found in policies).
        2. Missing/weak citations.
        3. Policy violations.
        4. Sensitive data leakage (PII).
        
        Ticket: {ticket}
        Draft: {draft}
        Policies:
        {policies}
        """)
        chain = prompt | self.llm.with_structured_output(ComplianceResult)
        return chain.invoke({"ticket": ticket, "draft": response.json(), "policies": policy_text})

    def run(self, ticket_text: str, order_context: Dict[str, Any]) -> FinalResponse:
        triage_info = self.triage(ticket_text, order_context)
        
        search_query = f"{triage_info.issue_type} {ticket_text}"
        policies = self.retrieve_policies(search_query)
        
        resolution = self.write_resolution(ticket_text, order_context, policies)
        
        compliance = self.compliance_check(ticket_text, resolution, policies)
        
        final_decision = resolution.decision
        if not compliance.is_compliant or compliance.should_escalate:
            final_decision = "needs escalation"
            
        citations = []
        for p in policies:
            doc_name = os.path.basename(p['source'])
            section = p.get('section', 'General')
            chunk_id = p.get('chunk_id', 'N/A')
            citations.append(f"{doc_name} - Section: {section} ({chunk_id})")
        
        seen = set()
        unique_citations = [x for x in citations if not (x in seen or seen.add(x))]
        
        return FinalResponse(
            classification=f"{triage_info.issue_type} (Confidence: {triage_info.confidence})",
            clarifying_questions=triage_info.clarifying_questions[:3] if triage_info.missing_fields else [],
            decision=final_decision,
            rationale=resolution.rationale if compliance.is_compliant else f"Compliance Issue: {', '.join(compliance.issues)}",
            citations=unique_citations,
            customer_response=resolution.customer_response if compliance.is_compliant else "This request requires manual review by a supervisor.",
            next_steps=resolution.internal_notes if compliance.is_compliant else f"ESCALATED: {compliance.suggested_fix}"
        )

if __name__ == "__main__":
    potential_index = os.path.join("ecommerce_agent", "data", "index")
    if os.path.exists(potential_index):
        INDEX_DIR = potential_index
    else:
        INDEX_DIR = os.path.join("data", "index")
    try:
        engine = EcommerceSupportEngine(INDEX_DIR)
        
        test_ticket = "My order arrived late and the cookies are melted. I want a full refund and to keep the item."
        test_context = {
            "order_date": "2026-03-20",
            "delivery_date": "2026-03-28",
            "item_category": "perishable",
            "shipping_region": "US-West",
            "shipping_method": "Standard"
        }
        
        response = engine.run(test_ticket, test_context)
        print(response.json(indent=2))
    except Exception as e:
        print(f"Engine failure: {e}")
