import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# CONFIG
# =========================
DATA_FILE = "peer_feedback.csv"
DELETE_KEY = "MERCADIA2025"
ADMIN_KEY = "MERCADIA2025"

st.set_page_config(
    page_title="Team Impact 2025 - Mohamed",
    page_icon="💠",
    layout="wide"
)

# =========================
# ADMIN DETECTION (URL PARAM)
# =========================
query_params = st.query_params
IS_ADMIN = query_params.get("admin", "") == ADMIN_KEY

# =========================
# INIT CSV IF NOT EXISTS
# =========================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=["name", "dept", "tag", "note", "time"]
    ).to_csv(DATA_FILE, index=False)

# =========================
# LOAD DATA (SAFE)
# =========================
if "peer_comments" not in st.session_state:
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            st.session_state.peer_comments = pd.read_csv(DATA_FILE).to_dict("records")
        except pd.errors.EmptyDataError:
            st.session_state.peer_comments = []
    else:
        st.session_state.peer_comments = []

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #F8FAFC, #F1F5F9); }
.main-header { background: white; padding: 40px; border-radius: 24px; margin-bottom: 30px; border: 1px solid #E2E8F0; }
.feedback-card { background: white; padding: 24px; border-radius: 20px; border: 1px solid #E2E8F0; margin-bottom: 20px; }
.dept-badge { background: #EFF6FF; color: #1D4ED8; padding: 6px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; }
.tech-tag { background: #0F172A; color: white; padding: 5px 12px; border-radius: 6px; }
.comment-text { padding: 15px; background: #F8FAFC; border-radius: 12px; border-left: 4px solid #3B82F6; }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("### 🏢 MERCADIA")
    st.markdown("#### 👤 MOHAMED")
    st.caption("IT Support Technician | 2025")

    if IS_ADMIN:
        st.success("Admin mode enabled")

    # ADMIN DELETE
    if IS_ADMIN and st.session_state.peer_comments:
        st.markdown("---")
        st.markdown("### 🗑️ Delete Feedback")

        delete_key_input = st.text_input("Private Key", type="password")

        delete_index = st.selectbox(
            "Select feedback",
            range(len(st.session_state.peer_comments)),
            format_func=lambda i: f"{st.session_state.peer_comments[i]['name']} - {st.session_state.peer_comments[i]['time']}"
        )

        if st.button("DELETE"):
            if delete_key_input == DELETE_KEY:
                st.session_state.peer_comments.pop(delete_index)
                pd.DataFrame(st.session_state.peer_comments).to_csv(DATA_FILE, index=False)
                st.success("Feedback deleted")
                st.rerun()
            else:
                st.error("Invalid key")

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-header">
    <p style="color:#3B82F6;font-weight:600;">Internal Collaboration Portal</p>
    <h1>Team Impact Wall 🤝</h1>
    <p style="color:#64748B;">Permanent record of IT assistance</p>
</div>
""", unsafe_allow_html=True)

col_form, col_wall = st.columns([1, 1.4], gap="large")

# =========================
# FORM
# =========================
with col_form:
    st.markdown("### 📥 Log Feedback")

    colleague_data = {
        "Merieme Dissi": "Chargé D'approvisionnement",
        "Bennis Hassan": "Chargé des opérations comptables et d'analyse financière",
        "Abichry Adil": "Store Center Manager",
        "Other (Manual Entry)": "External"
    }

    with st.form("impact_form", clear_on_submit=True):
        name_select = st.selectbox("Identify Yourself:", colleague_data.keys())

        final_name = name_select
        final_dept = colleague_data[name_select]

        if name_select == "Other (Manual Entry)":
            final_name = st.text_input("Full Name")
            final_dept = st.text_input("Department / Position")

        support_mode = st.radio(
            "Service Provided:",
            ["All Technical Assistance", "Specific IT Project"],
            horizontal=True
        )

        specific_task = ""
        if support_mode == "Specific IT Project":
            specific_task = st.text_input("Task Detail")

        feedback_note = st.text_area("Observations")

        # =========================
        # ADMIN DATE/TIME OVERRIDE FIX
        # =========================
        if IS_ADMIN:
            st.markdown("### 🕒 Admin Time Override")
            
            if "custom_date" not in st.session_state:
                st.session_state.custom_date = datetime.now().date()
            if "custom_time" not in st.session_state:
                st.session_state.custom_time = datetime.now().time()
            
            st.session_state.custom_date = st.date_input(
                "Date",
                st.session_state.custom_date
            )
            st.session_state.custom_time = st.time_input(
                "Time",
                st.session_state.custom_time
            )
            
            final_datetime = datetime.combine(
                st.session_state.custom_date,
                st.session_state.custom_time
            )
        else:
            final_datetime = datetime.now()

        submit = st.form_submit_button("PUBLISH TO WALL")

        if submit:
            if final_name and feedback_note:
                tag = specific_task if support_mode == "Specific IT Project" else support_mode

                new_entry = {
                    "name": final_name,
                    "dept": final_dept,
                    "tag": tag,
                    "note": feedback_note,
                    "time": final_datetime.strftime("%H:%M | %d %b %Y")
                }

                st.session_state.peer_comments.append(new_entry)
                pd.DataFrame(st.session_state.peer_comments).to_csv(DATA_FILE, index=False)
                st.success("Feedback saved ✔")
            else:
                st.error("Name and observation are required")

# =========================
# WALL
# =========================
with col_wall:
    st.markdown("### 🌐 Live Feedback Stream")

    if not st.session_state.peer_comments:
        st.info("No feedback yet")
    else:
        for c in reversed(st.session_state.peer_comments):
            st.markdown(f"""
            <div class="feedback-card">
                <div style="display:flex;justify-content:space-between;">
                    <span class="dept-badge">🏢 {c['dept']}</span>
                    <small>{c['time']}</small>
                </div>
                <h3>{c['name']}</h3>
                <span class="tech-tag">⚡ {c['tag']}</span>
                <div class="comment-text">{c['note']}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# EXPORT
# =========================
if st.session_state.peer_comments:
    df = pd.DataFrame(st.session_state.peer_comments)
    st.sidebar.download_button(
        "📥 DOWNLOAD CSV REPORT",
        data=df.to_csv(index=False),
        file_name="mercadia_it_impact.csv"
    )
