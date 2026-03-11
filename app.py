import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# ---------------------------
# AI CLIENT
# ---------------------------

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="AffiNexa Insurance AI", layout="wide")

# ---------------------------
# LOGIN SYSTEM
# ---------------------------

PASSWORD = "affinexa123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("🔐 AffiNexa Insurance AI Demo Login")

    password = st.text_input("Enter Demo Password", type="password")

    if st.button("Login"):

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("Incorrect password")

    st.stop()

# ---------------------------
# PAGE TITLE
# ---------------------------

st.title("🚀 AffiNexa Insurance AI – Advisor Operating System")

# ---------------------------
# SAMPLE DATA
# ---------------------------

data = {
    "Client":[
        "Rajesh Sharma",
        "Anita Gupta",
        "Suresh Jain",
        "Vikas Verma",
        "Rohan Mehta",
        "Priya Singh"
    ],
    "Policy":[
        "LIC Life",
        "Health Insurance",
        "Motor Insurance",
        "LIC Life",
        "Health Insurance",
        "LIC Life"
    ],
    "Premium":[25000,18000,9000,32000,21000,27000],
    "Expiry":[
        "2026-04-12",
        "2026-04-18",
        "2026-04-25",
        "2026-04-30",
        "2026-05-05",
        "2026-05-20"
    ],
    "Interest":[
        "Term Insurance",
        "Health Upgrade",
        "Motor Renewal",
        "Child Plan",
        "Term Insurance",
        "Health Insurance"
    ]
}

df = pd.DataFrame(data)

# ---------------------------
# KPI DASHBOARD
# ---------------------------

st.subheader("📊 Advisor Dashboard")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Total Clients", len(df))
col2.metric("Active Policies", len(df))
col3.metric("Upcoming Renewals", 3)
col4.metric("Monthly Premium", f"₹{df['Premium'].sum():,}")
col5.metric("Conversion Rate", "34%")

st.divider()

# ---------------------------
# RENEWAL TRACKER
# ---------------------------

st.subheader("📅 Renewal Tracker")

st.dataframe(df)

st.divider()

# ---------------------------
# PREMIUM ANALYTICS
# ---------------------------

st.subheader("💰 Premium Analytics")

fig = px.bar(
    df,
    x="Client",
    y="Premium",
    color="Policy",
    title="Premium Distribution"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ---------------------------
# CLIENT PROFILE
# ---------------------------

st.subheader("👤 Client Profile")

selected = st.selectbox("Select Client", df["Client"])

profile = df[df["Client"]==selected].iloc[0]

colA,colB = st.columns(2)

colA.write(f"Policy: {profile['Policy']}")
colA.write(f"Premium: ₹{profile['Premium']}")
colA.write(f"Expiry: {profile['Expiry']}")

colB.write(f"Interested Product: {profile['Interest']}")
colB.write("Next Follow-up: 15 days")

st.divider()

# ---------------------------
# AI SALES INSIGHTS
# ---------------------------

st.subheader("📈 AI Sales Insights")

high_value = df[df["Premium"] > 25000]

st.write("High Value Clients")

st.dataframe(high_value)

st.write("Cross-Sell Opportunities")

cross_sell = df[df["Interest"]=="Term Insurance"]

st.dataframe(cross_sell)

st.divider()

# ---------------------------
# AI ADVISOR COPILOT
# ---------------------------

st.subheader("🤖 AI Advisor Copilot")

question = st.text_input("Ask AI about your clients")

if question:

    prompt=f"""
You are an intelligent insurance advisor assistant.

Dataset:
{df.to_string()}

Answer advisor questions and suggest opportunities.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[{"role":"user","content":prompt}]
    )

    answer = response.choices[0].message.content

    st.success(answer)