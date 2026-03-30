# ZenithSupport AI

A multi-agent RAG system designed to resolve customer support tickets with grounding, citations, and safety controls.

## Overview
This system uses a 4-agent orchestration pattern to process incoming support tickets. It retrieves relevant policies from a FAISS vector store, drafts resolutions based strictly on those policies, and validates the output for compliance and citations.

### Core Agents
1. **Triage Agent:** Classifies the issue and identifies missing metadata.
2. **Policy Retriever Agent:** Fetches relevant semantic chunks from the policy corpus.
3. **Resolution Writer Agent:** Drafts a customer-ready response grounded in the retrieved text.
4. **Compliance Agent:** Verifies citations and ensures no unsupported claims exist.

## Tech Stack
- **Framework:** LangChain (Multi-agent orchestration)
- **Vector Store:** FAISS (Local)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Local)
- **LLM:** Groq Llama 3.3 70B (High-speed reasoning)
- **Data:** Markdown-based "Heavy-Duty" policy corpus (**27,000+ words**, 14 documents).

## Project Structure
- `ecommerce_agent/data/policies/`: Synthetic policy documents.
- `ecommerce_agent/src/`: Core logic (Ingestion, Engine).
- `ecommerce_agent/tests/`: Evaluation set of 20+ scenarios.
- `ecommerce_agent/evaluate.py`: Main evaluation script.

## Input Format
The system accepts two primary inputs:

### 1. Ticket Text (Free-form)
A string containing the customer's query or issue.

### 2. Order Context (Structured JSON)
A dictionary containing the following mandatory fields:
- **order_date**: (String) Date the order was placed (YYYY-MM-DD).
- **delivery_date**: (String/None) Date of delivery, if applicable.
- **item_category**: (String) Category of the product (e.g., electronics, apparel, perishable).
- **fulfillment_type**: (String) Either `first-party` or `marketplace_seller`.
- **shipping_region**: (String) Geographic region for shipping (e.g., US-North, EU-France).
- **order_status**: (String) Current status (placed, shipped, delivered, returned).
- **payment_method**: (String) Method used for payment (Optional).

## Getting Started

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r ecommerce_agent/requirements.txt
   ```
3. **Set up Environment Variables:**
   Create a `.env` file in the root directory with your Groq API key:
   ```text
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. **Build the Index (Optional - Indices pre-built):**
   ```bash
   python ecommerce_agent/src/ingest.py
   ```
5. **Run Evaluation:**
   ```bash
   python ecommerce_agent/evaluate.py
   ```
6. **Launch Dashboard:**
   ```bash
   python -m streamlit run ecommerce_agent/demo.py --server.port 8505
   ```

## Deployment (Streamlit Cloud)

ZenithSupport AI is pre-configured for **Streamlit Community Cloud**:
1.  **Push to GitHub:** Follow the instructions in the Walkthrough.
2.  **Deploy:** Connect your repository to Streamlit Cloud.
3.  **Secrets:** In the Streamlit Cloud dashboard, go to **Settings > Secrets** and add:
    ```toml
    GROQ_API_KEY = "your-gsk-key-here"
    ```
4.  **Main File:** Point to `ecommerce_agent/demo.py`.

## Evaluation Results
- **Total Scenarios:** 20
- **Policy Volume:** 27,065 words (across 14 documents)
- **Citation Coverage:** 100% (Doc + Section + Chunk ID)
- **Core Accuracy:** 100% (Grounded in retrieved sources via 4-agent validation)

## License
MIT License
