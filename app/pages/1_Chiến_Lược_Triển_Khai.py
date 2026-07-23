import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("app"))

from utils import load_processed_data
from mapping import render_common_sidebar_filters
from insights import quadrant_insight
from components.ui_components import inject_custom_css, render_mockup_banner, render_mockup_kpi, render_report_insight
from chatbot_widget import render_floating_chatbot

st.set_page_config(page_title="Chiến Lược Triển Khai", page_icon="📊", layout="wide")
inject_custom_css()
st.session_state["current_page_name"] = "Strategy"

df_scored = load_processed_data("data/processed/tasks_scored.csv")
df_profile, df_recalc, selected_category, selected_single_job = render_common_sidebar_filters(df_scored)

job_label = selected_single_job if selected_single_job != "Tất cả vị trí đã chọn" else selected_category

render_mockup_banner(
    "Ma Trận Chiến Lược Triển Khai",
    f"Phân loại tác vụ theo 4 vùng chiến lược dựa trên Mong muốn (D) và Năng lực AI (C) — [{job_label}]"
)

if df_profile.empty:
    st.info(f"Không tìm thấy tác vụ nào cho [{job_label}]. Vui lòng chọn vị trí ở thanh Sidebar.")
    st.stop()

n = len(df_profile)
n_pilot = len(df_profile[df_profile["risk_category"] == "ideal_pilot"])
n_risk = len(df_profile[df_profile["risk_category"].isin(["risk_resistance", "risk_expectation"])])
avg_p = df_profile["priority_score"].mean()
total_roi = df_profile["roi_savings_usd"].sum()
n_sensitive = int(df_profile["is_sensitive"].sum())

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: render_mockup_kpi("Tổng tác vụ", f"{n}", "tác vụ", "#8B5CF6")
with c2: render_mockup_kpi("Điểm ưu tiên TB", f"{avg_p:.1f}", "/ 100", "#8B5CF6")
with c3: render_mockup_kpi("ROI ước tính", f"${total_roi:,.0f}", "/năm", "#22C55E")
with c4: render_mockup_kpi("Thí điểm ngay", f"{n_pilot}", f"{n_pilot/n*100:.0f}%", "#0284C7")
with c5: render_mockup_kpi("Rủi ro cao", f"{n_risk}", f"{n_risk/n*100:.1f}%", "#EF4444")
with c6: render_mockup_kpi("Nhạy cảm", f"{n_sensitive}", "tác vụ", "#F59E0B")

st.markdown("<br>", unsafe_allow_html=True)

col_chart, col_insight = st.columns([3.5, 2.5])

with col_chart:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Ma Trận 4 Góc Phần Tư (Strategic Quadrant)</div>
<div class="mockup-card-subtitle">Trục X = Năng lực AI (C) | Trục Y = Mong muốn Người lao động (D)</div>""", unsafe_allow_html=True)

    color_map = {
        "🟢 Thí điểm Ngay": "#34D399",
        "🟡 Rủi ro Phản kháng Nội bộ": "#F59E0B",
        "🟠 Rủi ro Kỳ vọng vượt Năng lực": "#EF4444",
        "⚪ Ưu tiên Thấp": "#A78BFA"
    }

    fig = px.scatter(
        df_profile, x="norm_capability", y="norm_desire",
        size="roi_savings_usd", color="risk_flag",
        color_discrete_map=color_map,
        hover_data={"occupation": True, "task_statement": True, "priority_score": ":.1f"},
        labels={"norm_capability": "Năng lực AI (C)", "norm_desire": "Mong muốn (D)", "roi_savings_usd": "ROI ước tính ($)", "risk_flag": "Nhóm chiến lược", "occupation": "Nghề nghiệp", "task_statement": "Tác vụ", "priority_score": "Điểm ưu tiên"},
        template="plotly_white", size_max=32
    )

    for thresh in [0.4, 0.7]:
        fig.add_vline(x=thresh, line_dash="dot", line_color="#CBD5E1")
        fig.add_hline(y=thresh, line_dash="dot", line_color="#CBD5E1")

    fig.update_layout(height=450, margin=dict(l=10, r=10, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_insight:
    proof, cause, report = quadrant_insight(df_profile, category_name=job_label)
    render_report_insight(proof, cause, report)

stats_summary = (
    f"- Vị trí / Ngành đang chọn: {job_label}\n"
    f"- Số tác vụ phân tích: {n}\n"
    f"- Thí điểm ngay: {n_pilot} ({n_pilot/n*100:.1f}%)\n"
    f"- Tác vụ rủi ro: {n_risk}\n"
)
render_floating_chatbot("Trang 1: Chiến Lược", job_label, selected_category, stats_summary)
