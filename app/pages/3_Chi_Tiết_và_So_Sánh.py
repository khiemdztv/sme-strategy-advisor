import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("app"))

from utils import load_processed_data
from mapping import render_common_sidebar_filters, load_sme_mapping
from etl import AUTO_REASONS, HUMAN_REASONS, REASON_LABELS_VI
from insights import heatmap_insight, cross_industry_insight
from components.ui_components import inject_custom_css, render_mockup_banner, render_mockup_kpi, render_report_insight
from chatbot_widget import render_floating_chatbot

st.set_page_config(page_title="Chi Tiết & So Sánh", page_icon="🔍", layout="wide")
inject_custom_css()
st.session_state["current_page_name"] = "Analysis"

df_scored = load_processed_data("data/processed/tasks_scored.csv")
df_profile, df_recalc, selected_category, selected_single_job = render_common_sidebar_filters(df_scored)

job_label = selected_single_job if selected_single_job != "Tất cả vị trí đã chọn" else selected_category

render_mockup_banner(
    "Phân Tích Chi Tiết Theo Vị Trí & So Sánh Liên Ngành",
    f"Heatmap phân bố lý do động lực/rào cản và bản đồ so sánh mức sẵn sàng giữa 8 ngành SME — [{job_label}]"
)

if df_profile.empty:
    st.info(f"Không tìm thấy tác vụ nào cho [{job_label}]. Vui lòng chọn vị trí ở thanh Sidebar.")
    st.stop()

n = len(df_profile)
n_pilot = len(df_profile[df_profile["risk_category"] == "ideal_pilot"])
n_risk = len(df_profile[df_profile["risk_category"].isin(["risk_resistance", "risk_expectation"])])
avg_p = df_profile["priority_score"].mean()
total_roi = df_profile["roi_savings_usd"].sum()
role_count = len(df_profile["sme_role"].unique()) if "sme_role" in df_profile.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: render_mockup_kpi("Tổng tác vụ", f"{n}", "tác vụ", "#8B5CF6")
with c2: render_mockup_kpi("Số Vị Trí SME", f"{role_count}", "vị trí", "#8B5CF6")
with c3: render_mockup_kpi("ROI Tiết Kiệm", f"${total_roi:,.0f}", "/năm", "#22C55E")
with c4: render_mockup_kpi("Thí điểm ngay", f"{n_pilot}", f"{n_pilot/n*100:.0f}%", "#0284C7")
with c5: render_mockup_kpi("Rủi ro cao", f"{n_risk}", f"{n_risk/n*100:.1f}%", "#EF4444")
with c6: render_mockup_kpi("Priority Score", f"{avg_p:.1f}", "/ 100", "#F59E0B")

st.markdown("<br>", unsafe_allow_html=True)

col_chart, col_insight = st.columns([3.5, 2.5])

role_col = "sme_role" if "sme_role" in df_profile.columns else "occupation"
auto_present = [c for c in AUTO_REASONS if c in df_profile.columns]
human_present = [c for c in HUMAN_REASONS if c in df_profile.columns]
all_reasons = auto_present + human_present
vi_labels = [REASON_LABELS_VI.get(c, c) for c in all_reasons]

with col_chart:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Heatmap Phân Bố Lý Do Theo Vị Trí SME</div>
<div class="mockup-card-subtitle">Đỏ = % Đồng ý cao | Xanh = % Đồng ý thấp</div>""", unsafe_allow_html=True)

    if all_reasons and not df_profile.empty:
        grouped = df_profile.groupby(role_col)[all_reasons].mean()
        if not grouped.empty:
            fig_hm = px.imshow(
                grouped.values, x=vi_labels, y=grouped.index.tolist(),
                color_continuous_scale="RdYlGn", aspect="auto",
                labels=dict(x="Lý do", y="Vị trí SME", color="% Đồng ý")
            )
            fig_hm.update_layout(height=max(320, len(grouped) * 40 + 80), margin=dict(l=10, r=10, t=10, b=20))
            st.plotly_chart(fig_hm, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_insight:
    proof1, cause1, report1 = heatmap_insight(df_profile, all_reasons, role_col, category_name=job_label)
    for eng, vi in REASON_LABELS_VI.items():
        proof1 = proof1.replace(eng, vi)
        cause1 = cause1.replace(eng, vi)
        report1 = report1.replace(eng, vi)
    render_report_insight(proof1, cause1, report1)

stats_summary = (
    f"- Vị trí / Ngành đang chọn: {job_label}\n"
    f"- Điểm Ưu tiên TB: {avg_p:.1f}/100\n"
    f"- ROI Tổng: ${total_roi:,.0f}/năm\n"
)
render_floating_chatbot("Trang 3: Chi Tiết & So Sánh", job_label, selected_category, stats_summary)
