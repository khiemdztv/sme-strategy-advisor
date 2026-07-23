"""
ui_components.py — Power BI / Notion / Stripe Style Business Intelligence Sidebar System.
Adjusts header top padding (65px) so "SME Strategy Advisor" is comfortably positioned.
"""

import streamlit as st
import re

def inject_custom_css():
    """
    Injects CSS for perfect layout, Vietnamese tabs, and fully visible non-clipped header title.
    """
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ── Global Reset ── */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            color: #111827 !important;
            background-color: #F8FAFC !important;
        }

        .stApp {
            background-color: #F8FAFC !important;
        }

        /* ── Main View Canvas Layout ── */
        [data-testid="stAppViewContainer"] {
            overflow-x: hidden !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
            z-index: 100 !important;
        }

        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stMain"],
        section.main {
            padding: 0 !important;
            margin: 0 !important;
        }

        .main .block-container,
        [data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
            width: 100% !important;
            padding: 1.8rem 2rem 3rem 2rem !important;
            box-sizing: border-box !important;
        }

        /* ── SIDEBAR OVERHAUL (Width: 320px) ── */
        [data-testid="stSidebar"] {
            width: 320px !important;
            min-width: 320px !important;
            max-width: 320px !important;
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
            padding: 0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        }

        /* Hide Streamlit default sidebar nav items & header to collapse top gap */
        [data-testid="stSidebarNav"],
        div[data-testid="stSidebarNav"],
        [data-testid="stSidebarHeader"] {
            display: none !important;
            height: 0px !important;
            min-height: 0px !important;
            padding: 0px !important;
            margin: 0px !important;
        }

        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebarContent"] {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }

        /* ── 1. HEADER (Positioned Flush at Top) ── */
        .bi-sidebar-header {
            flex: 0 0 auto;
            min-height: 70px !important;
            padding: 16px 20px 14px 20px !important;
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            border-bottom: 1px solid #F3F4F6 !important;
            background: #FFFFFF !important;
            margin-top: 0px !important;
        }
        .bi-logo-icon {
            width: 42px !important;
            height: 42px !important;
            background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
            border-radius: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            color: #FFFFFF !important;
            font-size: 1.2rem !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2) !important;
            flex-shrink: 0 !important;
        }
        .bi-brand-text-container {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            flex: 1 !important;
            min-width: 0 !important;
        }
        .bi-brand-title {
            font-size: 0.98rem !important;
            font-weight: 800 !important;
            color: #0F172A !important;
            line-height: 1.35 !important;
            letter-spacing: -0.01em !important;
            margin: 0 !important;
            padding: 0 !important;
            white-space: nowrap !important;
        }
        .bi-brand-subtitle {
            font-size: 0.74rem !important;
            color: #6B7280 !important;
            margin-top: 3px !important;
            font-weight: 500 !important;
            white-space: nowrap !important;
        }

        /* ── 2. NAVIGATION CARD (Fixed, 5 Vietnamese Menu Items) ── */
        .bi-sidebar-nav {
            flex: 0 0 auto;
            padding: 16px 16px 0 16px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .bi-nav-item {
            height: 44px;
            padding: 0 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-radius: 10px;
            font-size: 0.88rem;
            font-weight: 500;
            color: #374151;
            text-decoration: none !important;
            transition: all 0.15s ease;
        }
        .bi-nav-item:hover {
            background: #F3F4F6;
            color: #111827;
        }
        .bi-nav-item.active {
            background: #EFF6FF;
            color: #2563EB;
            font-weight: 600;
        }
        .bi-nav-item i {
            font-size: 1rem;
            width: 20px;
            text-align: center;
        }

        /* Divider */
        .bi-sidebar-divider {
            flex: 0 0 auto;
            margin: 16px 20px;
            border-top: 1px solid #E5E7EB;
        }

        /* ── 3. SCROLLABLE FILTER AREA ── */
        .bi-filter-header {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #9CA3AF;
            margin-bottom: 14px;
            padding: 0 20px;
        }

        /* Custom Multiselect Tag Styling (Blue Theme #EFF6FF / #2563EB) */
        [data-testid="stSidebar"] [data-baseweb="select"] {
            border-radius: 12px !important;
            border: 1px solid #E5E7EB !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background-color: #EFF6FF !important;
            color: #2563EB !important;
            border-radius: 8px !important;
            padding: 4px 10px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            border: 1px solid #DBEAFE !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] span {
            color: #2563EB !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] [role="button"] {
            color: #2563EB !important;
        }

        /* ── 4. FOOTER (Fixed at bottom) ── */
        .bi-sidebar-footer {
            flex: 0 0 auto;
            padding: 16px 20px;
            border-top: 1px solid #E5E7EB;
            font-size: 0.75rem;
            color: #9CA3AF;
            background: #FFFFFF;
        }
        .bi-footer-version {
            font-weight: 600;
            color: #6B7280;
            margin-bottom: 2px;
        }

        /* ── Top Hero Banner ── */
        .hero-banner-mockup {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
            border-radius: 16px;
            padding: 2.2rem 2.5rem;
            color: #FFFFFF !important;
            margin-bottom: 1.8rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
        }
        .hero-banner-mockup h1 {
            font-size: 1.85rem !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin: 0 0 0.4rem 0 !important;
            letter-spacing: -0.02em;
        }
        .hero-banner-mockup p {
            font-size: 1rem !important;
            color: #E2E8F0 !important;
            margin: 0 !important;
            font-weight: 400;
        }

        /* ── 6 KPI Cards ── */
        .kpi-card-mockup {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
            height: 115px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-title {
            font-size: 0.78rem;
            font-weight: 700;
            color: #64748B;
        }
        .kpi-value {
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            color: #0F172A !important;
            line-height: 1.1 !important;
            letter-spacing: -0.02em !important;
            white-space: nowrap !important;
        }
        .kpi-sub {
            font-size: 0.78rem;
            color: #64748B;
            font-weight: 500;
        }

        /* ── White Container Card ── */
        .mockup-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.3rem 1.5rem;
            height: 100%;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
        }
        .mockup-card-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 0.3rem;
        }
        .mockup-card-subtitle {
            font-size: 0.8rem;
            color: #64748B;
            margin-bottom: 1rem;
            line-height: 1.4;
        }

        /* ── Insight Panel ── */
        .insight-panel-v2 {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.3rem 1.5rem;
            height: 100%;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
        }
        .insight-item-box {
            margin-bottom: 1.1rem;
            padding-bottom: 0.9rem;
            border-bottom: 1px solid #F1F5F9;
        }
        .insight-item-box:last-child {
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }
        .insight-item-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.4rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .insight-item-body {
            font-size: 0.88rem;
            color: #334155;
            line-height: 1.75 !important;
        }

        /* Compact & Fitted Executive Inline Pill Badges */
        .badge-pill {
            display: inline-block;
            white-space: nowrap;
            padding: 1px 6px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.81rem;
            margin: 0 3px;
            vertical-align: middle;
            line-height: 1.35;
        }
        .badge-pilot      { background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; }
        .badge-resistance { background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
        .badge-expectation{ background: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; }
        .badge-low        { background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }
        .badge-ready      { background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; }
        .badge-anxious    { background: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; }
        .badge-conflict   { background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
        /* Global Chatbot Pop-up Window Positioning (Fitted & Compact for all screen heights) */
        [data-baseweb="portal"] [data-baseweb="popover"]:not(:has([data-baseweb="menu"])),
        div[data-baseweb="popover"]:not(:has(ul[role="listbox"])),
        div[data-testid="stPopoverBody"] {
            position: fixed !important;
            bottom: 80px !important;
            right: 25px !important;
            left: auto !important;
            top: auto !important;
            transform: none !important;
            margin: 0 !important;
            width: 430px !important;
            max-width: calc(100vw - 40px) !important;
            max-height: calc(100vh - 100px) !important;
            border-radius: 18px !important;
            box-shadow: 0 25px 50px rgba(15, 23, 42, 0.35) !important;
            border: 1.5px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            padding: 1rem !important;
            z-index: 9999999 !important;
        }

        /* Ensure dropdown menus (selectbox/multiselect) retain normal positioning */
        [data-baseweb="portal"] [data-baseweb="popover"]:has([data-baseweb="menu"]),
        div[data-baseweb="popover"]:has(ul[role="listbox"]) {
            position: absolute !important;
            bottom: auto !important;
            right: auto !important;
            width: auto !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_mockup_banner(title="Tổng quan chiến lược AI Agent", subtitle="Hệ thống tư vấn định hướng và chiến lược triển khai tối ưu cho doanh nghiệp SME"):
    st.markdown(f"""<div class="hero-banner-mockup"><h1>{title}</h1><p>{subtitle}</p></div>""", unsafe_allow_html=True)


def render_mockup_kpi(label, value, subtext="", border_color="#2563eb"):
    st.markdown(f"""<div class="kpi-card-mockup" style="border-left: 4px solid {border_color};"><div class="kpi-title">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{subtext}</div></div>""", unsafe_allow_html=True)


def render_banner(title, subtitle):
    render_mockup_banner(title, subtitle)

def render_hero_banner(title, subtitle, selected_industry="Tất cả lĩnh vực", selected_job="Tất cả vị trí"):
    render_mockup_banner(title, subtitle)

def render_kpi_v2(icon_class, label, value, subtext="", icon_bg="#EFF6FF", icon_color="#2563EB"):
    render_mockup_kpi(label, value, subtext, icon_color)


def format_pro_text(text):
    if not text:
        return ""
    
    res = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    res = res.replace("🟢 Thí điểm Ngay", '<span class="badge-pill badge-pilot">Thí điểm Ngay</span>')
    res = res.replace("🟢 Thí điểm ngay", '<span class="badge-pill badge-pilot">Thí điểm ngay</span>')
    res = res.replace("🟡 Rủi ro Phản kháng Nội bộ", '<span class="badge-pill badge-resistance">Phản kháng Nội bộ</span>')
    res = res.replace("🟡 Phản kháng Nội bộ", '<span class="badge-pill badge-resistance">Phản kháng Nội bộ</span>')
    res = res.replace("🟠 Rủi ro Kỳ vọng vượt Năng lực", '<span class="badge-pill badge-expectation">Kỳ vọng vượt Năng lực</span>')
    res = res.replace("🟠 Kỳ vọng vượt Năng lực", '<span class="badge-pill badge-expectation">Kỳ vọng vượt Năng lực</span>')
    res = res.replace("⚪ Ưu tiên Thấp", '<span class="badge-pill badge-low">Ưu tiên Thấp</span>')
    
    res = res.replace("🟢 'Sẵn sàng'", '<span class="badge-pill badge-ready">Sẵn sàng</span>')
    res = res.replace("'Sẵn sàng'", '<span class="badge-pill badge-ready">Sẵn sàng</span>')
    res = res.replace("🔴 'Lo lắng'", '<span class="badge-pill badge-anxious">Lo lắng</span>')
    res = res.replace("'Lo lắng'", '<span class="badge-pill badge-anxious">Lo lắng</span>')
    res = res.replace("🟠 'Mâu thuẫn'", '<span class="badge-pill badge-conflict">Mâu thuẫn</span>')
    res = res.replace("'Mâu thuẫn'", '<span class="badge-pill badge-conflict">Mâu thuẫn</span>')
    res = res.replace("🔵 'Gắn bó'", '<span class="badge-pill badge-engaged">Gắn bó</span>')
    res = res.replace("'Gắn bó'", '<span class="badge-pill badge-engaged">Gắn bó</span>')

    res = res.replace("🟢 ", "").replace("🟡 ", "").replace("🟠 ", "").replace("⚪ ", "").replace("🔴 ", "").replace("🔵 ", "")

    return res


def render_report_insight(proof_text, cause_text, report_excerpt):
    html_code = f"""<div class="insight-panel-v2">
<div class="insight-item-box">
<div class="insight-item-title" style="color:#0284C7;"><i class="fa-solid fa-chart-line"></i> Bằng Chứng Số Liệu Thống Kê</div>
<div class="insight-item-body">{format_pro_text(proof_text)}</div>
</div>
<div class="insight-item-box">
<div class="insight-item-title" style="color:#D97706;"><i class="fa-solid fa-magnifying-glass-chart"></i> Phân Tích Nguyên Nhân Cốt Lõi</div>
<div class="insight-item-body">{format_pro_text(cause_text)}</div>
</div>
<div class="insight-item-box">
<div class="insight-item-title" style="color:#15803D;"><i class="fa-solid fa-lightbulb"></i> Kết Luận & Đề Xuất Cho Doanh Nghiệp</div>
<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #16A34A; padding:0.85rem 1.1rem; border-radius:8px; font-size:0.88rem; color:#0F172A; line-height:1.75;">{format_pro_text(report_excerpt)}</div>
</div>
</div>"""
    st.markdown(html_code, unsafe_allow_html=True)


def render_executive_summary_card(highlights, top_opportunities, high_risks, estimated_roi, next_steps):
    html_code = f"""<div class="mockup-card" style="margin-top:1.5rem; border-left:5px solid #2563EB;">
<div class="mockup-card-title">Executive Summary & Strategic Roadmap</div>
<div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:0.8rem;">
<div>
<div style="font-size:0.8rem; font-weight:700; color:#64748B; text-transform:uppercase;">Key Highlights</div>
<div style="font-size:0.88rem; color:#334155; line-height:1.65; margin-top:0.3rem;">{format_pro_text(highlights)}</div>
</div>
<div>
<div style="font-size:0.8rem; font-weight:700; color:#64748B; text-transform:uppercase;">Estimated Annual Impact</div>
<div style="font-size:1.5rem; font-weight:800; color:#15803D; margin-top:0.2rem;">{estimated_roi}</div>
</div>
</div>
<hr style="margin:1rem 0; border:0; border-top:1px solid #E2E8F0;">
<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:15px;">
<div>
<div style="font-size:0.8rem; font-weight:700; color:#15803D;">Top Opportunities</div>
<div style="font-size:0.83rem; color:#334155; margin-top:0.2rem;">{format_pro_text(top_opportunities)}</div>
</div>
<div>
<div style="font-size:0.8rem; font-weight:700; color:#DC2626;">High Risk Areas</div>
<div style="font-size:0.83rem; color:#334155; margin-top:0.2rem;">{format_pro_text(high_risks)}</div>
</div>
<div>
<div style="font-size:0.8rem; font-weight:700; color:#2563EB;">Next Action Steps</div>
<div style="font-size:0.83rem; color:#334155; margin-top:0.2rem;">{format_pro_text(next_steps)}</div>
</div>
</div>
</div>"""
    st.markdown(html_code, unsafe_allow_html=True)
