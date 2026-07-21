"""
mapping.py — Power BI / Notion / Stripe Style Business Intelligence Sidebar Construction.
Renders clean Business Intelligence Logo and 100% Vietnamese navigation menus with clear icons.
"""

import pandas as pd
import os
import streamlit as st

def load_sme_mapping(mapping_file="data/mapping/sme_role_to_occupation.csv"):
    """
    Loads SME role to O*NET occupation mapping file.
    """
    if os.path.exists(mapping_file):
        return pd.read_csv(mapping_file)
    else:
        return pd.DataFrame(columns=["sme_role", "sme_category", "onet_occupation", "description"])

def filter_tasks_by_sme_profile(df_scored, selected_categories=None, selected_roles=None, mapping_file="data/mapping/sme_role_to_occupation.csv"):
    """
    Filters scored tasks based on selected SME business categories and roles.
    """
    df_map = load_sme_mapping(mapping_file)

    if selected_categories:
        df_map = df_map[df_map["sme_category"].isin(selected_categories)]
        
    if selected_roles:
        df_map = df_map[df_map["sme_role"].isin(selected_roles)]

    target_occupations = df_map["onet_occupation"].unique()

    if len(target_occupations) > 0:
        df_filtered = df_scored[df_scored["occupation"].isin(target_occupations)].copy()
        df_filtered = df_filtered.merge(df_map[["onet_occupation", "sme_role", "sme_category"]], left_on="occupation", right_on="onet_occupation", how="left")
        return df_filtered
    else:
        return df_scored.copy()

def _on_categories_change():
    """
    Callback to handle smooth category selection.
    """
    cats = st.session_state.get("sb_categories_select", [])
    prev_cats = st.session_state.get("prev_raw_categories_input", [])
    all_tag = "🌐 Tất cả lĩnh vực"

    if all_tag in cats and all_tag not in prev_cats:
        st.session_state["sb_categories_select"] = [all_tag]
    elif all_tag in cats and len(cats) > 1:
        st.session_state["sb_categories_select"] = [c for c in cats if c != all_tag]
    elif not cats:
        st.session_state["sb_categories_select"] = [all_tag]

    st.session_state["prev_raw_categories_input"] = st.session_state["sb_categories_select"]

def render_common_sidebar_filters(df_scored):
    """
    Renders 4-region SaaS Business Intelligence Sidebar matching Power BI / Notion specifications.
    """
    df_mapping = load_sme_mapping()
    all_real_categories = sorted(df_mapping["sme_category"].unique().tolist())
    all_categories_options = ["🌐 Tất cả lĩnh vực"] + all_real_categories

    # Determine current page for active navigation item styling
    current_page = st.session_state.get("current_page_name", "Overview")

    # ── REGION 1: HEADER (Non-truncated BI Logo & Sleek Typography) ──
    st.sidebar.markdown("""
    <div class="bi-sidebar-header">
        <div class="bi-logo-icon">
            <i class="fa-solid fa-chart-line"></i>
        </div>
        <div class="bi-brand-text-container">
            <div class="bi-brand-title">SME Strategy Advisor</div>
            <div class="bi-brand-subtitle">Business Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── REGION 2: NAVIGATION CARD (Fixed, 5 Vietnamese Menu Items with Icons) ──
    nav_overview_cls = "bi-nav-item active" if current_page == "Overview" else "bi-nav-item"
    nav_strat_cls = "bi-nav-item active" if current_page == "Strategy" else "bi-nav-item"
    nav_psych_cls = "bi-nav-item active" if current_page == "Employee Insights" else "bi-nav-item"
    nav_dtl_cls = "bi-nav-item active" if current_page == "Analysis" else "bi-nav-item"
    nav_rec_cls = "bi-nav-item active" if current_page == "Recommendations" else "bi-nav-item"

    st.sidebar.markdown(f"""
    <div class="bi-sidebar-nav">
        <a href="/" target="_self" class="{nav_overview_cls}">
            <i class="fa-solid fa-chart-pie"></i> Tổng quan
        </a>
        <a href="/Chiến_Lược_Triển_Khai" target="_self" class="{nav_strat_cls}">
            <i class="fa-solid fa-diagram-project"></i> Chiến lược triển khai
        </a>
        <a href="/Tâm_Lý_Nhân_Viên" target="_self" class="{nav_psych_cls}">
            <i class="fa-solid fa-users"></i> Tâm lý nhân viên
        </a>
        <a href="/Chi_Tiết_và_So_Sánh" target="_self" class="{nav_dtl_cls}">
            <i class="fa-solid fa-magnifying-glass-chart"></i> Chi tiết & so sánh
        </a>
        <a href="/Khuyến_Nghị" target="_self" class="{nav_rec_cls}">
            <i class="fa-solid fa-clipboard-list"></i> Khuyến nghị hành động
        </a>
    </div>
    <div class="bi-sidebar-divider"></div>
    <div class="bi-filter-header">CÀI ĐẶT PHÂN TÍCH</div>
    """, unsafe_allow_html=True)

    # ── REGION 3: SCROLLABLE FILTER AREA ──
    if "sb_categories_select" not in st.session_state or not st.session_state["sb_categories_select"]:
        st.session_state["sb_categories_select"] = ["🌐 Tất cả lĩnh vực"]
    if "prev_raw_categories_input" not in st.session_state:
        st.session_state["prev_raw_categories_input"] = st.session_state["sb_categories_select"]

    selected_categories_input = st.sidebar.multiselect(
        "Ngành nghề / Phân khúc SME",
        options=all_categories_options,
        key="sb_categories_select",
        on_change=_on_categories_change
    )

    curr_selected = st.session_state.get("sb_categories_select", ["🌐 Tất cả lĩnh vực"])

    if not curr_selected or "🌐 Tất cả lĩnh vực" in curr_selected:
        active_categories = all_real_categories
        selected_category_label = "Tất cả lĩnh vực"
    else:
        active_categories = [c for c in curr_selected if c != "🌐 Tất cả lĩnh vực"]
        if not active_categories:
            active_categories = all_real_categories
            selected_category_label = "Tất cả lĩnh vực"
        elif len(active_categories) == 1:
            selected_category_label = active_categories[0]
        else:
            selected_category_label = f"({len(active_categories)} ngành) " + ", ".join(active_categories)

    # Sub-roles Selection
    available_roles = df_mapping[df_mapping["sme_category"].isin(active_categories)]["sme_role"].unique().tolist()

    last_cats_tracker = "last_selected_categories_tracker"
    if last_cats_tracker not in st.session_state or st.session_state[last_cats_tracker] != active_categories:
        st.session_state["sb_roles_select"] = available_roles
        st.session_state[last_cats_tracker] = active_categories

    selected_roles = st.sidebar.multiselect(
        "Vị trí công việc",
        options=available_roles,
        key="sb_roles_select"
    )
    if not selected_roles:
        selected_roles = available_roles

    # Single Focus Job Selection
    single_job_options = ["Tất cả vị trí đã chọn"] + sorted(available_roles)
    if "sb_single_job_select" not in st.session_state or st.session_state["sb_single_job_select"] not in single_job_options:
        st.session_state["sb_single_job_select"] = "Tất cả vị trí đã chọn"

    selected_single_job = st.sidebar.selectbox(
        "Lọc Focus vào 1 Job cụ thể",
        options=single_job_options,
        key="sb_single_job_select"
    )

    # ── REGION 4: FOOTER (Fixed at bottom) ──
    st.sidebar.markdown("""
    <div class="bi-sidebar-footer">
        <div class="bi-footer-version">Version 2.0</div>
        <div>© 2026 SME Strategy Advisor</div>
    </div>
    """, unsafe_allow_html=True)

    # Risk recalculation
    from scoring import calculate_scores_and_flags
    df_recalc = calculate_scores_and_flags(df_scored, w1=0.5, w2=0.5, sme_size_factor=1.0)

    if selected_single_job != "Tất cả vị trí đã chọn":
        active_roles = [selected_single_job]
    else:
        active_roles = selected_roles

    df_profile = filter_tasks_by_sme_profile(df_recalc, selected_categories=active_categories, selected_roles=active_roles)

    st.session_state["df_profile"] = df_profile
    st.session_state["df_all_scored"] = df_recalc
    st.session_state["selected_categories"] = active_categories
    st.session_state["selected_category"] = selected_category_label
    st.session_state["selected_single_job"] = selected_single_job

    return df_profile, df_recalc, selected_category_label, selected_single_job
