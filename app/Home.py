import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("app"))

from utils import load_processed_data
from mapping import render_common_sidebar_filters
from components.ui_components import inject_custom_css, render_mockup_banner, render_mockup_kpi
from chatbot_widget import render_floating_chatbot

st.set_page_config(page_title="SME Strategy Advisor — Business Intelligence Platform", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
st.session_state["current_page_name"] = "Overview"

# ── Load raw data ──
df_scored = load_processed_data("data/processed/tasks_scored.csv")

# ── Sidebar Filters ──
df_profile, df_recalc, selected_category, selected_single_job = render_common_sidebar_filters(df_scored)

# ── 1. Top Hero Banner ──
render_mockup_banner(
    title="Tổng quan chiến lược AI Agent",
    subtitle="Hệ thống tư vấn định hướng và chiến lược triển khai tối ưu cho doanh nghiệp SME"
)

if df_profile.empty:
    st.info("Vui lòng chọn vị trí công việc ở thanh Sidebar.")
    st.stop()

# ── 2. 6 KPI Cards Row ──
n = len(df_profile)
n_pilot = len(df_profile[df_profile["risk_category"] == "ideal_pilot"])
n_risk = len(df_profile[df_profile["risk_category"].isin(["risk_resistance", "risk_expectation"])])
avg_p = df_profile["priority_score"].mean()
total_roi = df_profile["roi_savings_usd"].sum()
n_sensitive = int(df_profile["is_sensitive"].sum())

pct_pilot = (n_pilot / n * 100) if n > 0 else 0
pct_risk = (n_risk / n * 100) if n > 0 else 0
pct_sensitive = (n_sensitive / n * 100) if n > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: render_mockup_kpi("Tổng tác vụ", f"{n}", "tác vụ", "#8B5CF6")
with c2: render_mockup_kpi("Điểm ưu tiên TB", f"{avg_p:.1f}", "/ 100", "#8B5CF6")
with c3: render_mockup_kpi("ROI ước tính", f"${total_roi:,.0f}", "/năm", "#22C55E")
with c4: render_mockup_kpi("Thí điểm ngay", f"{n_pilot}", f"{pct_pilot:.0f}% tổng", "#0284C7")
with c5: render_mockup_kpi("Rủi ro cao", f"{n_risk}", f"{pct_risk:.1f}% tổng", "#EF4444")
with c6: render_mockup_kpi("Nhạy cảm", f"{n_sensitive}", "tác vụ", "#F59E0B")

st.markdown("<br>", unsafe_allow_html=True)

# ── 3. Middle 3-Column Section ──
col1, col2, col3 = st.columns([3.2, 3.8, 3])

role_col = "sme_role" if "sme_role" in df_profile.columns else "occupation"

# ── Cột 1: Khoảng cách Kỳ vọng vs Năng lực AI ──
with col1:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Khoảng cách kỳ vọng vs Năng lực AI</div>
<div class="mockup-card-subtitle">Gap = Mong muốn (D) − Năng lực AI (C). Thanh xanh = NV muốn nhiều hơn AI làm được. Thanh đỏ = AI sẵn sàng nhưng NV chưa muốn.</div>""", unsafe_allow_html=True)

    df_gap = df_profile.copy()
    df_gap["gap"] = df_gap["norm_desire"] - df_gap["norm_capability"]
    gap_by_role = df_gap.groupby(role_col)["gap"].mean().sort_values()

    gap_vals = gap_by_role.values * 100
    colors = ['#EF4444' if v < 0 else '#34D399' for v in gap_vals]

    fig_gap = go.Figure(go.Bar(
        y=gap_by_role.index,
        x=gap_vals,
        orientation='h',
        marker_color=colors,
        text=[f"{v:+.1f}" for v in gap_vals],
        textposition='outside',
        textfont=dict(size=10, color="#1E293B")
    ))
    fig_gap.add_vline(x=0, line_dash="solid", line_color="#94A3B8", line_width=1.5)

    fig_gap.update_layout(
        height=320,
        template="plotly_white",
        margin=dict(l=10, r=40, t=10, b=30),
        xaxis_title="Khoảng cách (D - C)",
        yaxis=dict(categoryorder="total ascending")
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    st.markdown("""<div style="font-size:0.75rem; display:flex; gap:15px; justify-content:center; margin-top:0.3rem;">
<span><span style="color:#EF4444;">●</span> AI sẵn sàng nhưng NV chưa muốn</span>
<span><span style="color:#34D399;">●</span> NV muốn nhiều hơn AI làm được</span>
</div></div>""", unsafe_allow_html=True)

# ── Cột 2: Ma trận 4 góc phần tư ──
with col2:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Ma trận 4 góc phần tư</div>
<div class="mockup-card-subtitle">Trục X = Năng lực AI (C). Trục Y = Mong muốn (D). Kích thước = ROI ($). Màu = Nhóm chiến lược.</div>""", unsafe_allow_html=True)

    fig_quad = px.scatter(
        df_profile, x="norm_capability", y="norm_desire",
        size="roi_savings_usd", color="risk_flag",
        color_discrete_map={
            "🟢 Thí điểm Ngay": "#34D399",
            "🟡 Rủi ro Phản kháng Nội bộ": "#F59E0B",
            "🟠 Rủi ro Kỳ vọng vượt Năng lực": "#EF4444",
            "⚪ Ưu tiên Thấp": "#A78BFA"
        },
        labels={"norm_capability": "Năng lực AI (C)", "norm_desire": "Mong muốn (D)"},
        template="plotly_white", size_max=28
    )

    for thresh in [0.5]:
        fig_quad.add_vline(x=thresh, line_dash="dot", line_color="#CBD5E1")
        fig_quad.add_hline(y=thresh, line_dash="dot", line_color="#CBD5E1")

    fig_quad.add_annotation(x=0.85, y=0.85, text="Thí điểm Ngay", showarrow=False, font=dict(size=10, color="#059669"), bgcolor="rgba(240,253,244,0.8)")
    fig_quad.add_annotation(x=0.15, y=0.85, text="Ưu tiên Thấp", showarrow=False, font=dict(size=10, color="#6D28D9"), bgcolor="rgba(245,243,255,0.8)")
    fig_quad.add_annotation(x=0.15, y=0.15, text="Rủi ro / Cần chú ý", showarrow=False, font=dict(size=10, color="#DC2626"), bgcolor="rgba(254,242,242,0.8)")
    fig_quad.add_annotation(x=0.85, y=0.15, text="Mở rộng & Tối ưu", showarrow=False, font=dict(size=10, color="#475569"), bgcolor="rgba(248,250,252,0.8)")

    fig_quad.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=20),
        xaxis=dict(range=[-0.02, 1.02]), yaxis=dict(range=[-0.02, 1.02]),
        showlegend=False
    )
    st.plotly_chart(fig_quad, use_container_width=True)

    st.markdown("""<div style="font-size:0.75rem; display:flex; gap:12px; justify-content:center; margin-top:0.3rem;">
<span><span style="color:#34D399;">●</span> Thí điểm ngay</span>
<span><span style="color:#A78BFA;">●</span> Ưu tiên thấp</span>
<span><span style="color:#F59E0B;">●</span> Rủi ro</span>
<span><span style="color:#94A3B8;">●</span> Mở rộng</span>
</div></div>""", unsafe_allow_html=True)

# ── Cột 3: Điểm nhấn chiến lược & Tóm tắt tổng quan ──
with col3:
    summary_html = f"""<div class="mockup-card">
<div class="mockup-card-title">Điểm nhấn chiến lược</div>
<div class="highlight-box">
<div class="highlight-item"><span style="color:#2563EB; font-weight:bold;">•</span> <span><b>{n_pilot} tác vụ</b> có thể thí điểm ngay, chiếm {pct_pilot:.0f}% tổng số.</span></div>
<div class="highlight-item"><span style="color:#2563EB; font-weight:bold;">•</span> <span>ROI ước tính đạt <b>${total_roi/1e6:.2f}M/năm</b> nếu triển khai toàn diện.</span></div>
<div class="highlight-item"><span style="color:#2563EB; font-weight:bold;">•</span> <span>Nhóm vị trí có khoảng cách rào cản lớn nhất cần tập trung truyền thông.</span></div>
<div class="highlight-item"><span style="color:#2563EB; font-weight:bold;">•</span> <span><b>{n_risk} tác vụ</b> có rủi ro cao cần rà soát và kiểm soát.</span></div>
</div>
<div class="mockup-card-title" style="margin-top: 1.2rem;">Tóm tắt tổng quan</div>
<div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#2563EB;">🔹</span> Tổng tác vụ phân tích</span><span class="summary-val-text">{n}</span></div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#10B981;">🔹</span> Điểm ưu tiên trung bình</span><span class="summary-val-text">{avg_p:.1f} /100</span></div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#10B981;">🔹</span> ROI ước tính</span><span class="summary-val-text">${total_roi:,.0f} /năm</span></div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#F59E0B;">🔸</span> Tác vụ thí điểm ngay</span><span class="summary-val-text">{n_pilot} ({pct_pilot:.0f}%)</span></div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#EF4444;">🔺</span> Rủi ro cao</span><span class="summary-val-text">{n_risk} ({pct_risk:.1f}%)</span></div>
<div class="summary-row"><span class="summary-label-text"><span style="color:#F59E0B;">🔸</span> Tác vụ nhạy cảm</span><span class="summary-val-text">{n_sensitive} ({pct_sensitive:.1f}%)</span></div>
</div>
</div>"""
    st.markdown(summary_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 4. Bottom Grid ──
b_col1, b_col2 = st.columns([3, 1])

with b_col1:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title" style="color:#15803D;">Khuyến nghị hành động</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top:0.8rem;">
<div class="rec-green-box">
<div class="rec-green-title">1. Ưu tiên triển khai</div>
<div class="rec-green-desc">Bắt đầu với nhóm Thí điểm ngay để tạo giá trị nhanh và chứng minh hiệu quả.</div>
</div>
<div class="rec-green-box">
<div class="rec-green-title">2. Quản trị rủi ro</div>
<div class="rec-green-desc">Rà soát các tác vụ rủi ro cao, xây dựng chính sách và cơ chế kiểm soát phù hợp.</div>
</div>
<div class="rec-green-box">
<div class="rec-green-title">3. Đào tạo & Truyền thông</div>
<div class="rec-green-desc">Tập trung đào tạo ở các mảng có khoảng cách lớn để giải tỏa lo ngại cho nhân sự.</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

with b_col2:
    st.markdown("""<div class="support-box">
<div>
<div style="font-size:0.95rem; font-weight:800; color:#0F172A; margin-bottom:0.4rem;">Bạn cần hỗ trợ?</div>
<div style="font-size:0.82rem; color:#64748B; line-height:1.5;">Đội ngũ tư vấn sẵn sàng đồng hành cùng doanh nghiệp SME của bạn.</div>
</div>
<div>
<a href="mailto:support@sme-advisor.com" class="support-btn" style="width:100%;">Liên hệ tư vấn</a>
</div>
</div>""", unsafe_allow_html=True)

# ── Floating Advisor Chatbot ──
stats_summary = (
    f"- Tổng tác vụ: {n}\n"
    f"- Thí điểm ngay: {n_pilot} ({pct_pilot:.0f}%)\n"
    f"- Priority Score TB: {avg_p:.1f}/100\n"
    f"- ROI Ước tính: ${total_roi:,.0f}/năm\n"
)
job_target_name = selected_single_job if selected_single_job != "Tất cả vị trí đã chọn" else f"Ngành {selected_category}"

render_floating_chatbot("Trang Chủ", job_target_name, selected_category, stats_summary)
