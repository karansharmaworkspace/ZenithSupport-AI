import streamlit as st
import json
from datetime import datetime
from ecommerce_agent.src.engine import EcommerceSupportEngine

st.set_page_config(page_title="ZenithSupport AI", layout="wide")


st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
    }
    .agent-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    .agent-title {
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("E-commerce Support Resolution Engine")
st.markdown("---")

with st.sidebar:
    st.header("Order Context")
    order_date = st.date_input("Order Date", datetime(2026, 3, 25))
    delivery_date = st.date_input("Delivery Date (Optional)", datetime(2026, 3, 27))
    item_category = st.selectbox("Item Category", ["apparel", "electronics", "perishable", "hygiene", "software", "toys", "home_decor"])
    fulfillment_type = st.radio("Fulfillment Type", ["first-party", "marketplace_seller"])
    shipping_region = st.text_input("Shipping Region", "US-North")
    order_status = st.selectbox("Order Status", ["placed", "shipped", "delivered", "returned"])
    payment_method = st.text_input("Payment Method", "Credit Card")
    
st.header("Customer Ticket")
ticket_text = st.text_area("Enter the customer's request here:", "I received the wrong size for my shirt. How can I return it?")

if st.button("Process Resolution"):
    if not ticket_text:
        st.error("Please enter a ticket description.")
    else:
        context = {
            "order_date": order_date.strftime("%Y-%m-%d"),
            "delivery_date": delivery_date.strftime("%Y-%m-%d") if delivery_date else None,
            "item_category": item_category,
            "fulfillment_type": fulfillment_type,
            "shipping_region": shipping_region,
            "order_status": order_status,
            "payment_method": payment_method
        }
        
        engine = EcommerceSupportEngine(index_dir="ecommerce_agent/data/index")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Agent Workflow Status")
            
            with st.status("Step 1: Triage Agent", expanded=True):
                st.write("Analyzing ticket intent and validating context...")
            
            with st.status("Step 2: Policy Retriever Agent", expanded=True):
                st.write("Searching FAISS index for relevant policy chunks...")
                
            with st.status("Step 3: Resolution Writer Agent", expanded=True):
                st.write("Drafting response using retrieved policy evidence...")
                
            with st.status("Step 4: Compliance Agent", expanded=True):
                st.write("Verifying citations and checking for safety violations...")

        try:
            result = engine.run(ticket_text, context)
            
            with col2:
                st.subheader("Final System Output (JSON)")
                st.json(result.model_dump())
                
                st.subheader("Customer-Facing Response")
                st.info(result.customer_response)
                
                if result.decision == "needs escalation":
                    st.warning("Action Required: This case has been escalated to a human supervisor.")
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")

st.markdown("---")
st.caption("Purple Merit Technologies - AI ML Engineer Assessment 2026")
