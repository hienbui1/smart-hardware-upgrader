import streamlit as st
import google.generativeai as genai
import os
import psycopg2
from dotenv import load_dotenv

# 1. Load configuration
load_dotenv()

# Setup API Key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Database Helper Function
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# UI Setup
st.set_page_config(page_title="Smart Hardware Upgrader", page_icon="💻")
st.title("💻 Smart Hardware Upgrader (v2 - RDS Powered)")

# Inputs
st.markdown("### Your Current Setup")
col1, col2 = st.columns(2)
with col1:
    current_cpu = st.selectbox("Current CPU", ["Ryzen 5 5600X", "Ryzen 7 7800X3D", "Core i7-13700K", "Core i5-12400F"])
with col2:
    current_gpu = st.selectbox("Current GPU", ["RTX 3070", "RTX 4090", "RX 7800 XT", "RX 6700 XT"])

st.markdown("### Your Target Goals")
col3, col4 = st.columns(2)
with col3:
    target_game = st.text_input("Target Game", value="Counter-Strike 2")
with col4:
    upgrade_budget = st.number_input("Upgrade Budget ($ USD)", min_value=0, step=50, value=550)

if st.button("Analyze & Recommend", type="primary"):
    with st.spinner("Fetching live prices from AWS RDS and analyzing..."):
        try:
            # 3. Fetch data from your Cloud Memory
            conn = get_db_connection()
            cur = conn.cursor()

            # Get all parts that fit the budget
            cur.execute("SELECT component_name, current_price FROM hardware_pricing WHERE current_price <= %s", (upgrade_budget,))
            affordable_parts = cur.fetchall()

            cur.close()
            conn.close()

            # Format the DB data for the AI
            pricing_context = "\n".join([f"- {name}: ${price}" for name, price in affordable_parts])

            # 4. The Augmented Prompt (RAG)
            prompt = f"""
            You are a master PC builder. 
            User Current Setup: {current_cpu} and {current_gpu}.
            Target Game: {target_game}.
            Budget: ${upgrade_budget}.
            
            CRITICAL: Use ONLY the following real-time pricing data from my database for your recommendation:
            {pricing_context}
            
            Analyze the bottleneck. Recommend ONE specific component from the list above that provides the best value. 
            Explain the performance gain.
            """

            response = model.generate_content(prompt)
            st.success("Analysis Complete (Grounded in RDS Data)")
            st.markdown("---")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error connecting to cloud memory: {e}")