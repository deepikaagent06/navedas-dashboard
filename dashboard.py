import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta

def show_dashboard():

    st.set_page_config(
        page_title="Navedas Intelligence",
        layout="wide"
    )

    # ==============================
    # SESSION TIMEOUT CONTROL
    # ==============================

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()

    if datetime.now() - st.session_state.last_activity > timedelta(minutes=15):
        st.warning("Session expired due to inactivity. Please reload dashboard.")
        st.stop()

    st.session_state.last_activity = datetime.now()

    # ==============================
    # AUDIT LOG STORAGE
    # ==============================

    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []

    def log_event(event):
        st.session_state.audit_log.append({
            "timestamp": datetime.now(),
            "event": event
        })

    # ==============================
    # SIDEBAR NAVIGATION
    # ==============================

    st.sidebar.title("Navigation")

    page = st.sidebar.selectbox(
        "Select View",
        [
            "Dashboard Overview",
            "COO Insights",
            "Risk & Governance",
            "Ticket Intelligence"
        ]
    )

    # ==============================
    # HEADER
    # ==============================

    col1, col2 = st.columns([1,8])

    with col1:
        st.image("governance_logo.jpg", width=1000)

    with col2:
        st.title("Navedas Intelligence")

    st.divider()

    # ==============================
    # DATA UPLOAD
    # ==============================

    st.subheader("AI Ticket Intelligence")

    col1, col2 = st.columns([2,1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload Support Ticket File",
            type=["csv","xlsx"]
        )

    with col2:
        run_ai = st.button("Run AI Analysis")

    st.divider()

    if uploaded_file is None:
        st.info("Upload a ticket dataset to begin AI analysis")
        return

    log_event("Dataset uploaded")

    # ==============================
    # LOAD DATA
    # ==============================

    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # ==============================
    # SAFE INITIALIZATION
    # ==============================

    if "Revenue_Leakage_Risk" not in df.columns:
        df["Revenue_Leakage_Risk"] = False

    if "Escalation_Failure" not in df.columns:
        df["Escalation_Failure"] = False

    if "Brand_Threat" not in df.columns:
        df["Brand_Threat"] = False

    if "ticket_value" not in df.columns:
        df["ticket_value"] = 100

    if "customer_lifetime_value" not in df.columns:
        df["customer_lifetime_value"] = 500

    # ==============================
    # AI BATCH PROCESSING
    # ==============================

    if run_ai:

        log_event("AI analysis started")

        batch_size = 50
        total_batches = (len(df) // batch_size) + 1

        progress_bar = st.progress(0)

        for batch in range(total_batches):

            start = batch * batch_size
            end = start + batch_size

            batch_df = df.iloc[start:end]

            if len(batch_df) == 0:
                continue

            df.loc[start:end, "Revenue_Leakage_Risk"] = (
                (batch_df["customer_sentiment"] == "negative") &
                (batch_df["churn_risk_score"] > 0.7)
            )

            df.loc[start:end, "Escalation_Failure"] = (
                (batch_df["prior_escalations_count"] > 0) &
                (batch_df["customer_sentiment"] == "negative")
            )

            df.loc[start:end, "Brand_Threat"] = (
                (batch_df["customer_sentiment"] == "very_negative") |
                (batch_df["csat_score"] < 2)
            )

            progress = (batch + 1) / total_batches
            progress_bar.progress(progress)

            st.write(f"Processing Batch {batch + 1} / {total_batches}")

            time.sleep(0.2)

        log_event("AI analysis completed")

        st.success("AI Detection Engine Completed")

    # ==============================
    # EXECUTIVE ROI CALCULATIONS
    # ==============================

    leakage_cases = df["Revenue_Leakage_Risk"].sum()

    revenue_risk = df[df["Revenue_Leakage_Risk"]]["ticket_value"].sum()

    clv_risk = df[df["Revenue_Leakage_Risk"]]["customer_lifetime_value"].sum()

    revenue_recovery = revenue_risk * 0.6

    # ==============================
    # POST RESOLUTION ESCALATION DETECTION
    # ==============================

    post_resolution_cases = df[
        (df["customer_sentiment"] == "negative") &
        (df["prior_escalations_count"] > 0)
    ]

    # ==============================
    # DASHBOARD OVERVIEW
    # ==============================

    if page == "Dashboard Overview":

        st.subheader("Executive Overview")

        total_tickets = len(df)
        escalation_cases = df["Escalation_Failure"].sum()
        brand_threats = df["Brand_Threat"].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Tickets Analyzed", total_tickets)
        col2.metric("🔴 Revenue Leakage Risk", leakage_cases)
        col3.metric("⚠ Escalation Failures", escalation_cases)
        col4.metric("⚠ Brand Threats", brand_threats)

        st.divider()

        st.subheader("Executive ROI Intelligence")

        col1, col2, col3 = st.columns(3)

        col1.metric("Revenue at Risk ($)", int(revenue_risk))
        col2.metric("Customer Lifetime Value at Risk ($)", int(clv_risk))
        col3.metric("Recoverable Revenue Opportunity ($)", int(revenue_recovery))

        st.divider()

        st.subheader("Customer Sentiment Distribution")

        sentiment_counts = df["customer_sentiment"].value_counts()

        st.bar_chart(sentiment_counts)

        st.divider()

        st.subheader("AI Executive Insight")

        st.info(
            f"""
AI detected **{leakage_cases} potential revenue leakage cases**.

These cases represent approximately **${int(revenue_risk)} in revenue risk**.

Customer lifetime value exposure is **${int(clv_risk)}**.

If escalation automation is implemented, the organization could recover approximately **${int(revenue_recovery)} annually**.
"""
        )

    # ==============================
    # COO INSIGHTS
    # ==============================

    if page == "COO Insights":

        st.subheader("Operational Signals")

        total_tickets = len(df)

        ai_handled = df["ai_handled_flag"].sum()
        human_cases = total_tickets - ai_handled
        churn_risk_cases = (df["churn_risk_score"] > 0.7).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("AI Handled Tickets", ai_handled)
        col2.metric("Human Intervention", human_cases)
        col3.metric("⚠ High Churn Risk", churn_risk_cases)

        st.divider()

        st.subheader("Revenue Leakage Intelligence")

        negative_sentiment = (df["customer_sentiment"] == "negative").sum()
        escalation_cases = df["Escalation_Failure"].sum()

        funnel_data = pd.DataFrame({
            "Stage": [
                "Total Tickets",
                "Negative Sentiment",
                "Escalation Failures",
                "Revenue Leakage Risk"
            ],
            "Count": [
                total_tickets,
                negative_sentiment,
                escalation_cases,
                leakage_cases
            ]
        })

        fig = px.funnel(
            funnel_data,
            x="Count",
            y="Stage"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("Post Resolution Escalation Cases")

        st.metric(
            "Detected Post-Resolution Escalations",
            len(post_resolution_cases)
        )

    # ==============================
    # RISK & GOVERNANCE
    # ==============================

    if page == "Risk & Governance":

        st.subheader("Governance Monitoring")

        low_confidence_cases = (df["ai_confidence_score"] < 0.5).sum()
        repeat_escalations = (df["prior_escalations_count"] > 1).sum()
        high_churn_cases = (df["churn_risk_score"] > 0.8).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("⚠ Low AI Confidence", low_confidence_cases)
        col2.metric("⚠ Repeat Escalations", repeat_escalations)
        col3.metric("🔴 High Churn Risk", high_churn_cases)

        st.divider()

        st.subheader("Risk Distribution")

        risk_data = {
            "Low AI Confidence": low_confidence_cases,
            "Repeat Escalations": repeat_escalations,
            "High Churn Risk": high_churn_cases
        }

        risk_df = pd.DataFrame(
            list(risk_data.items()),
            columns=["Risk Type","Cases"]
        )

        st.bar_chart(risk_df.set_index("Risk Type"))

        st.divider()

        st.subheader("Flagged Risk Tickets")

        risk_cases = df[
            (df["Revenue_Leakage_Risk"]) |
            (df["Escalation_Failure"]) |
            (df["Brand_Threat"])
        ]

        st.dataframe(risk_cases)

        st.download_button(
            label="Export Risk Cases (CSV)",
            data=risk_cases.to_csv(index=False),
            file_name="navedas_risk_cases.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("Audit Log")

        audit_df = pd.DataFrame(st.session_state.audit_log)

        st.dataframe(audit_df)

    # ==============================
    # TICKET INTELLIGENCE
    # ==============================

    if page == "Ticket Intelligence":

        st.subheader("Ticket Dataset")

        batch_size = 50
        total_batches = (len(df) // batch_size) + 1

        batch_number = st.selectbox(
            "Select Ticket Batch",
            list(range(1, total_batches + 1))
        )

        start = (batch_number - 1) * batch_size
        end = start + batch_size

        batch_df = df.iloc[start:end]

        st.write(f"Showing Tickets {start + 1} - {min(end, len(df))}")


        st.dataframe(batch_df)

