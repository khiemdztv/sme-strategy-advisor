import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("app"))

from utils import load_processed_data
from mapping import render_common_sidebar_filters
from etl import AUTO_REASONS, HUMAN_REASONS, REASON_LABELS_VI
from insights import worker_psychology_insight, butterfly_insight
from components.ui_components import inject_custom_css, render_mockup_banner, render_mockup_kpi, render_report_insight
from chatbot_widget import render_floating_chatbot

st.set_page_config(page_title="Tâm Lý Nhân Viên", page_icon="👥", layout="wide")
inject_custom_css()
st.session_state["current_page_name"] = "Employee Insights"

df_scored = load_processed_data("data/processed/tasks_scored.csv")
df_profile, df_recalc, selected_category, selected_single_job = render_common_sidebar_filters(df_scored)

job_label = selected_single_job if selected_single_job != "Tất cả vị trí đã chọn" else selected_category

render_mockup_banner(
    "Phân Tích Tâm Lý Nhân Viên & Quản Trị Thay Đổi",
    f"Giải mã cảm xúc, động lực và rào cản nội bộ đối với tự động hóa công việc — [{job_label}]"
)

if df_profile.empty:
    st.info(f"Không tìm thấy tác vụ nào cho [{job_label}]. Vui lòng chọn vị trí ở thanh Sidebar.")
    st.stop()

n = len(df_profile)
n_pilot = len(df_profile[df_profile["risk_category"] == "ideal_pilot"])
n_risk = len(df_profile[df_profile["risk_category"].isin(["risk_resistance", "risk_expectation"])])
total_roi = df_profile["roi_savings_usd"].sum()
enjoyment_score = df_profile["worker_enjoyment_score"].mean() if "worker_enjoyment_score" in df_profile.columns else 0.0
security_score = df_profile["worker_security_score"].mean() if "worker_security_score" in df_profile.columns else 0.0

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: render_mockup_kpi("Tổng tác vụ", f"{n}", "tác vụ", "#8B5CF6")
with c2: render_mockup_kpi("Điểm Enjoyment", f"{enjoyment_score:.2f}", "/ 5.0", "#8B5CF6")
with c3: render_mockup_kpi("Điểm Security", f"{security_score:.2f}", "/ 5.0", "#22C55E")
with c4: render_mockup_kpi("Thí điểm ngay", f"{n_pilot}", f"{n_pilot/n*100:.0f}%", "#0284C7")
with c5: render_mockup_kpi("Rủi ro cao", f"{n_risk}", f"{n_risk/n*100:.1f}%", "#EF4444")
with c6: render_mockup_kpi("ROI tiết kiệm", f"${total_roi:,.0f}", "/năm", "#F59E0B")

st.markdown("<br>", unsafe_allow_html=True)

col_chart, col_insight = st.columns([3.5, 2.5])

role_col = "sme_role" if "sme_role" in df_profile.columns else "occupation"

with col_chart:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Bản Đồ Tâm Lý Nhân Viên — 4 Nhóm Cảm Xúc</div>
<div class="mockup-card-subtitle">X = Yêu thích công việc (Enjoyment) | Y = Lo ngại mất việc (Security)</div>""", unsafe_allow_html=True)

    psych_cols = ["worker_enjoyment_score", "worker_security_score", "worker_time_score"]
    if all(c in df_profile.columns for c in psych_cols):
        df_psych = df_profile.groupby(role_col).agg(
            avg_enjoyment=("worker_enjoyment_score", "mean"),
            avg_security=("worker_security_score", "mean"),
            avg_time=("worker_time_score", "mean"),
            pct_pilot=("risk_category", lambda x: (x == "ideal_pilot").sum() / len(x) * 100)
        ).reset_index().dropna(subset=["avg_enjoyment", "avg_security"])

        if not df_psych.empty:
            df_psych["size_time"] = df_psych["avg_time"].fillna(2.5).clip(lower=0.5)

            fig_psych = px.scatter(
                df_psych, x="avg_enjoyment", y="avg_security",
                size="size_time", color="pct_pilot",
                color_continuous_scale="RdYlGn",
                hover_name=role_col,
                labels={"avg_enjoyment": "Mức yêu thích (Enjoyment)", "avg_security": "Lo ngại mất việc (Security)", "size_time": "Thời gian TB", "pct_pilot": "% Thí điểm ngay"},
                template="plotly_white", size_max=40
            )

            for _, row in df_psych.iterrows():
                fig_psych.add_annotation(
                    x=row["avg_enjoyment"], y=row["avg_security"],
                    text=row[role_col][:18] + ("…" if len(row[role_col]) > 18 else ""),
                    showarrow=False, font=dict(size=9, color="#334155"), yshift=16
                )

            fig_psych.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=20))
            st.plotly_chart(fig_psych, use_container_width=True)
        else:
            st.info("Chưa có đủ dữ liệu tâm lý cho phân khúc đang chọn.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_insight:
    proof1, cause1, report1 = worker_psychology_insight(df_profile, category_name=job_label)
    render_report_insight(proof1, cause1, report1)

# ── Row 2: Butterfly Chart (Đối chiếu Động lực vs Rào cản) ──
st.markdown("<br>", unsafe_allow_html=True)
col_bf_chart, col_bf_insight = st.columns([3.5, 2.5])

auto_present = [c for c in AUTO_REASONS if c in df_profile.columns]
human_present = [c for c in HUMAN_REASONS if c in df_profile.columns]

with col_bf_chart:
    st.markdown("""<div class="mockup-card">
<div class="mockup-card-title">Biểu Đồ Bướm — Đối Chiếu Động Lực vs Rào Cản Tâm Lý</div>
<div class="mockup-card-subtitle">Xanh = % Muốn tự động hóa (Động lực) | Đỏ = % Yêu cầu con người (Rào cản)</div>""", unsafe_allow_html=True)

    if auto_present and human_present and not df_profile.empty:
        auto_means = df_profile[auto_present].mean()
        human_means = df_profile[human_present].mean()

        y_auto_labels = [REASON_LABELS_VI.get(c, c) for c in auto_means.index]
        y_human_labels = [REASON_LABELS_VI.get(c, c) for c in human_means.index]

        fig_bf = go.Figure()

        # Left side: Human reasons (negative values for diverging bar chart)
        fig_bf.add_trace(go.Bar(
            y=y_human_labels,
            x=[-v for v in human_means.values],
            orientation='h',
            name='Yêu cầu Con người (Rào cản)',
            marker_color='#EF4444',
            text=[f"{v:.1f}%" for v in human_means.values],
            textposition='outside',
            hoverinfo='y+text'
        ))

        # Right side: Auto reasons (positive values)
        fig_bf.add_trace(go.Bar(
            y=y_auto_labels,
            x=list(auto_means.values),
            orientation='h',
            name='Động lực Tự động hóa',
            marker_color='#22C55E',
            text=[f"{v:.1f}%" for v in auto_means.values],
            textposition='outside',
            hoverinfo='y+text'
        ))

        fig_bf.update_layout(
            barmode='overlay',
            height=380,
            template='plotly_white',
            margin=dict(l=10, r=40, t=10, b=20),
            xaxis=dict(title="% Đồng Ý Khảo Sát", zeroline=True, zerolinecolor="#94A3B8"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bf, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_bf_insight:
    proof_b, cause_b, report_b = butterfly_insight(df_profile, auto_present, human_present, category_name=job_label)
    for eng, vi in REASON_LABELS_VI.items():
        proof_b = proof_b.replace(eng, vi)
        cause_b = cause_b.replace(eng, vi)
        report_b = report_b.replace(eng, vi)
    render_report_insight(proof_b, cause_b, report_b)


stats_summary = (
    f"- Vị trí / Ngành đang chọn: {job_label}\n"
    f"- Điểm Enjoyment TB: {enjoyment_score:.2f}/5\n"
    f"- Điểm Security TB: {security_score:.2f}/5\n"
)
render_floating_chatbot("Trang 2: Tâm Lý Nhân Viên", job_label, selected_category, stats_summary)
