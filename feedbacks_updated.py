import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
DATA_FILE = "peer_feedback.csv"

st.set_page_config(
    page_title="Team Impact 2025 - Mohamed",
    page_icon="💠",
    layout="wide"
)

# =========================
# LOAD / INIT DATA
# =========================
if "peer_comments" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.peer_comments = pd.read_csv(DATA_FILE).to_dict("records")
    else:
        st.session_state.peer_comments = []

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
}
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.main-header {
    background: white;
    padding: 40px;
    border-radius: 24px;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    margin-bottom: 30px;
    border: 1px solid #E2E8F0;
}
.main-title {
    color: #0F172A;
    font-weight: 800;
    font-size: 2.5rem;
    margin:0;
}
.sub-title {
    color: #3B82F6;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.feedback-card {
    background: rgba(255,255,255,0.95);
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.dept-badge {
    background-color: #EFF6FF;
    color: #1D4ED8;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}
.tech-tag {
    background: #0F172A;
    color: white;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
}
.comment-text {
    color: #334155;
    font-size: 1rem;
    line-height: 1.6;
    padding: 15px;
    background: #F8FAFC;
    border-radius: 12px;
    margin-top: 15px;
    border-left: 4px solid #3B82F6;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("### 🏢 MERCADIA")
    st.markdown("#### 👤 MOHAMED")
    st.caption("IT Support Technician | 2025")
    st.markdown("---")
    st.write("Internal IT Impact Registry")

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-header">
    <p class="sub-title">Internal Collaboration Portal</p>
    <p class="main-title">Team Impact Wall 🤝</p>
    <p style="color:#64748B;">Permanent record of IT assistance across departments.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col_form, col_wall = st.columns([1, 1.4], gap="large")

# =========================
# FORM
# =========================
with col_form:
    st.markdown("### 📥 Log Feedback")

    colleague_data = {
        "Merieme Dissi": "Chargé D'approvisionnement",
        "Bennis Hassan": "Chargé des opérations comptables et d’analyse financière",
        "Abichry Adil": "Store Center Manager",
        "Nafie Ikram": "Assistance Administrative",
        "El Aboudi Abdelmonim": "Responsable De Magasin",
        "Benmira Mourad": "Responsable De Magasin",
        "Zif Zakaria": "Responsable De Magasin",
        "Benali Abdeladem": "Responsable De Magasin",
        "Other (Manual Entry)": "External"
    }

    with st.form("impact_form", clear_on_submit=True):
        name_select = st.selectbox("Identify Yourself:", colleague_data.keys())

        final_name = name_select
        final_dept = colleague_data[name_select]

        if name_select == "Other (Manual Entry)":
            final_name = st.text_input("Full Name")
            final_dept = st.text_input("Department / Position")

        st.markdown("---")
        support_mode = st.radio(
            "Service Provided:",
            ["All Technical Assistance", "Specific IT Project"],
            horizontal=True
        )

        specific_task = ""
        if support_mode == "Specific IT Project":
            specific_task = st.text_input("Task Detail")

        feedback_note = st.text_area("Observations")

        submit = st.form_submit_button("PUBLISH TO WALL")

        if submit:
            if final_name and feedback_note:
                tag = specific_task if support_mode == "Specific IT Project" else support_mode

                new_entry = {
                    "name": final_name,
                    "dept": final_dept,
                    "tag": tag,
                    "note": feedback_note,
                    "time": pd.Timestamp.now().strftime("%H:%M | %d %b %Y")
                }

                st.session_state.peer_comments.append(new_entry)

                # SAVE TO FILE (PERSISTENCE)
                pd.DataFrame(st.session_state.peer_comments).to_csv(DATA_FILE, index=False)

                st.success("Feedback saved permanently ✔")
            else:
                st.error("Name and observation are required.")

# =========================
# WALL
# =========================
with col_wall:
    st.markdown("### 🌐 Live Feedback Stream")

    if not st.session_state.peer_comments:
        st.info("No feedback registered yet.")
    else:
        for c in reversed(st.session_state.peer_comments):
            st.markdown(f"""
            <div class="feedback-card">
                <div style="display:flex;justify-content:space-between;">
                    <span class="dept-badge">🏢 {c['dept']}</span>
                    <small>{c['time']}</small>
                </div>
                <p style="font-size:1.4rem;font-weight:800;">{c['name']}</p>
                <span class="tech-tag">⚡ {c['tag']}</span>
                <div class="comment-text">"{c['note']}"</div>
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
