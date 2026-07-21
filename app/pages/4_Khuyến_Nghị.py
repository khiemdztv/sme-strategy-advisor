import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("app"))

from utils import load_processed_data
from mapping import render_common_sidebar_filters
from components.ui_components import inject_custom_css, render_mockup_banner, render_mockup_kpi
from chatbot_widget import render_floating_chatbot

st.set_page_config(page_title="Khuyến Nghị Hành Động", page_icon="🎯", layout="wide")
inject_custom_css()
st.session_state["current_page_name"] = "Recommendations"

df_scored = load_processed_data("data/processed/tasks_scored.csv")
df_profile, df_recalc, selected_category, selected_single_job = render_common_sidebar_filters(df_scored)

job_label = selected_single_job if selected_single_job != "Tất cả vị trí đã chọn" else selected_category

render_mockup_banner(
    "Danh Sách Khuyến Nghị Hành Động & Action Plan",
    f"Thẻ khuyến nghị tự động hóa chi tiết, phân loại ưu tiên Quick Wins và Playbook quản trị thay đổi cho SME — [{job_label}]"
)

if df_profile.empty:
    st.info(f"Không tìm thấy tác vụ nào cho [{job_label}]. Vui lòng chọn vị trí ở thanh Sidebar.")
    st.stop()

df_pilot = df_profile[df_profile["risk_category"] == "ideal_pilot"].sort_values("priority_score", ascending=False)
df_risk_table = df_profile[df_profile["risk_category"].isin(["risk_resistance", "risk_expectation"])]

n = len(df_profile)
n_pilot = len(df_pilot)
n_risk = len(df_risk_table)
pilot_roi = df_pilot["roi_savings_usd"].sum() if not df_pilot.empty else 0
avg_p = df_profile["priority_score"].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: render_mockup_kpi("Tổng tác vụ", f"{n}", "tác vụ", "#8B5CF6")
with c2: render_mockup_kpi("Thí điểm ngay", f"{n_pilot}", "Quick Wins", "#22C55E")
with c3: render_mockup_kpi("ROI Thí điểm", f"${pilot_roi:,.0f}", "/năm", "#22C55E")
with c4: render_mockup_kpi("Tác vụ rủi ro", f"{n_risk}", "cần Copilot", "#EF4444")
with c5: render_mockup_kpi("Priority Score", f"{avg_p:.1f}", "/ 100", "#8B5CF6")
with c6: render_mockup_kpi("Độ an toàn", "94%", "Human-in-loop", "#0284C7")

st.markdown("<br>", unsafe_allow_html=True)

col_cards, col_quickwins = st.columns([3.5, 2.5])

role_col = "sme_role" if "sme_role" in df_profile.columns else "occupation"

with col_cards:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Top Khuyến Nghị Thí Điểm (Recommendation Cards)</div>
<div class="mockup-card-subtitle">Được xếp hạng theo Điểm Ưu Tiên & Tiềm Năng ROI</div>""", unsafe_allow_html=True)

    if not df_pilot.empty:
        for idx, row in df_pilot.head(5).iterrows():
            roi_val = f"${row['roi_savings_usd']:,.0f}/năm"
            score_val = f"{row['priority_score']:.0f}đ"
            task_txt = row['task_statement']
            arch = row.get('recommended_architecture', 'Full Automation')
            role_txt = row.get(role_col, row['occupation'])

            card_html = f"""<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:1rem; margin-bottom:0.8rem; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
<div style="font-size:0.92rem; font-weight:700; color:#0F172A;">{task_txt[:80]}…</div>
<span style="background:#DCFCE7; color:#15803D; font-size:0.72rem; font-weight:700; padding:0.2rem 0.5rem; border-radius:12px;">High ROI</span>
</div>
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; background:#F8FAFC; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
<div><span style="color:#64748B;">VỊ TRÍ:</span> <b>{role_txt[:18]}</b></div>
<div><span style="color:#64748B;">SCORE:</span> <b style="color:#2563EB;">{score_val}</b></div>
<div><span style="color:#64748B;">ROI:</span> <b style="color:#15803D;">{roi_val}</b></div>
<div><span style="color:#64748B;">MÔ HÌNH:</span> <b>{arch}</b></div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("Không có tác vụ nào thuộc diện Thí điểm ngay với bộ lọc hiện tại.")

    st.markdown("</div>", unsafe_allow_html=True)

with col_quickwins:
    quickwin_html = f"""<div class="insight-panel-v2">
<div class="mockup-card-title">Danh Sách Quick Wins & Cảnh Báo</div>
<div class="insight-item-box">
<div class="insight-item-title" style="color:#15803D;"><i class="fa-solid fa-circle-check"></i> Quick Wins (Thắng Nhanh)</div>
<div class="insight-item-body">Tập trung các tác vụ công việc lặp lại, tốn nhiều thời gian nhưng nhân sự sẵn sàng giao phó cho công nghệ tự động hóa.</div>
</div>
<div class="insight-item-box">
<div class="insight-item-title" style="color:#2563EB;"><i class="fa-solid fa-handshake"></i> Kịch Bản Copilot Đồng Hành</div>
<div class="insight-item-body">Đối với tác vụ có rào cản tâm lý lo ngại mất việc, áp dụng giao diện Copilot để nhân sự làm chủ công nghệ thay vì thay thế hoàn toàn.</div>
</div>
<div class="insight-item-box">
<div class="insight-item-title" style="color:#D97706;"><i class="fa-solid fa-lock"></i> Quy Chế Chữ Ký Phê Duyệt</div>
<div class="insight-item-body">Các tác vụ nhạy cảm liên quan đến tài chính, hợp đồng pháp lý bắt buộc phải đi qua luồng phê duyệt từ Quản lý.</div>
</div>
</div>"""
    st.markdown(quickwin_html, unsafe_allow_html=True)

stats_summary = (
    f"- Vị trí / Ngành đang chọn: {job_label}\n"
    f"- Số tác vụ Thí điểm ngay: {n_pilot}\n"
    f"- ROI Thí điểm: ${pilot_roi:,.0f}/năm\n"
)
render_floating_chatbot("Trang 4: Khuyến Nghị", job_label, selected_category, stats_summary)
