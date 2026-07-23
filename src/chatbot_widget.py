"""
chatbot_widget.py — Executive Strategy Advisor Floating Widget (Enhanced Visibility & Guidance)
Renders a highly visible, engaging AI Chatbot Floating Button & Callout Badge to prompt user queries on page insights.
"""

import streamlit as st
import os
from groq import Groq
from rag_advisor import get_paper_summary_context, get_groq_api_key


def query_chatbot_groq(messages_history, page_type, job_name, category_name, stats_summary):
    """
    Queries Groq with conversation history + WORKBank paper RAG + page context.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return "⚠️ **Chưa tìm thấy Groq API Key**: Vui lòng nhập API Key ở ô cài đặt bên trên để kích hoạt AI Advisor."

    try:
        client = Groq(api_key=api_key)
        
        last_user_msg = ""
        for m in reversed(messages_history):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")
                break
                
        search_query = f"{job_name} {category_name} {page_type} {last_user_msg} desire capability automation worker expert human agency risk"
        paper_context = get_paper_summary_context(query_text=search_query, top_k=4)

        system_prompt = (
            "Bạn là Cố Vấn Chiến Lược Doanh Nghiệp Cấp Cao (Senior Strategy Advisor), chuyên tư vấn phân tích dữ liệu vận hành và hoạch định tự động hóa cho các doanh nghiệp vừa & nhỏ (SME) dựa trên nghiên cứu WORKBank (Stanford SALT Lab, arXiv:2506.06576v3).\n\n"
            f"📍 TRANG PHÂN TÍCH HIỆN TẠI: {page_type}\n"
            f"🏢 NGÀNH SME: {category_name} | 🎯 JOB FOCUS: {job_name}\n"
            f"📊 DỮ LIỆU ĐỊNH LƯỢNG HỆ THỐNG:\n{stats_summary}\n\n"
            f"📚 TRI THỨC TRUY XUẤT ĐỘNG (Dynamic RAG Context):\n{paper_context}\n\n"
            "QUY TẮC PHẢN HỒI:\n"
            "- Trình bày chuyên nghiệp theo phong cách báo cáo quản trị cấp cao (C-Level Executive Report).\n"
            "- Ngôn từ súc tích, mạch lạc (khoảng 150-220 từ), có gạch đầu dòng rõ ràng, tập trung vào chiến lược, ROI và quản trị thay đổi."
        )

        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages_history[-6:]:
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=formatted_messages,
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Không thể kết nối Cố vấn AI: {str(e)}"


def render_floating_chatbot(page_type, job_name, category_name, stats_summary):
    """
    Renders a highly visible, modern Executive Strategy AI Advisor floating pop-up widget.
    Fully collapses the Streamlit element container wrapper to 0px height to prevent any bottom white bar.
    """
    st.markdown("""
    <style>
        /* Pulse Animation for Chatbot Glow */
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.5); }
            70% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
            100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }

        @keyframes floatBounce {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-4px); }
        }

        /* ── 1. COLLAPSE STWRAPPER CONTAINER TO 0PX TO PREVENT BOTTOM BAR ── */
        div[data-testid="stElementContainer"]:has(div[data-testid="stPopover"]),
        div[data-testid="stElementContainer"]:has(button[data-testid="stBaseButton-popover"]),
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            width: 0px !important;
            height: 0px !important;
            min-height: 0px !important;
            max-height: 0px !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
            z-index: 999999 !important;
            overflow: visible !important;
        }

        /* ── FLOATING CALLOUT BADGE (TOP PILL) ── */
        .chat-callout-badge-v3 {
            position: fixed !important;
            bottom: 75px !important;
            right: 25px !important;
            z-index: 999998 !important;
            background: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px !important;
            padding: 5px 14px !important;
            font-size: 0.82rem !important;
            font-weight: 700 !important;
            color: #1E3A8A !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
            display: flex !important;
            align-items: center !important;
            gap: 7px !important;
            white-space: nowrap !important;
            animation: floatBounce 2.5s infinite ease-in-out !important;
        }

        /* ── 2. FLOATING POPOVER BUTTON STYLING (WHITE PILL LIKE SCREENSHOT) ── */
        html body div.stApp div[data-testid="stPopover"] button,
        html body div.stApp button[data-testid="stBaseButton-popover"],
        html body div.stApp div[data-testid="stPopoverButton"] button,
        html body div.stApp button[aria-haspopup="dialog"],
        div[data-testid="stPopover"] > button {
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            z-index: 999999 !important;
            width: auto !important;
            height: auto !important;
            white-space: nowrap !important;
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 12px !important;
            padding: 0.55rem 1.1rem !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.1) !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        html body div.stApp div[data-testid="stPopover"] button:hover,
        html body div.stApp button[data-testid="stBaseButton-popover"]:hover,
        div[data-testid="stPopover"] > button:hover {
            background: #F8FAFC !important;
            background-color: #F8FAFC !important;
            border-color: #94A3B8 !important;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        html body div.stApp div[data-testid="stPopover"] button *,
        html body div.stApp button[data-testid="stBaseButton-popover"] *,
        div[data-testid="stPopover"] > button * {
            color: #1E293B !important;
            fill: #1E293B !important;
            font-weight: 700 !important;
        }

        /* ── 3. POP-UP DIALOG WINDOW STYLING (OVERRIDE INLINE BASEWEB LEFT OFFSET) ── */
        [data-baseweb="portal"] [data-baseweb="popover"],
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-testid="stPopoverBody"],
        html body div[data-testid="stPopoverBody"] {
            position: fixed !important;
            bottom: 85px !important;
            right: 20px !important;
            left: auto !important;
            top: auto !important;
            transform: none !important;
            margin: 0 !important;
            width: 420px !important;
            max-width: calc(100vw - 30px) !important;
            max-height: calc(100vh - 100px) !important;
            border-radius: 18px !important;
            box-shadow: 0 25px 50px rgba(15, 23, 42, 0.35) !important;
            border: 1.5px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            padding: 0.85rem !important;
            z-index: 9999999 !important;
            overflow-y: auto !important;
        }

        /* Ensure dropdown menus (selectbox/multiselect) retain normal positioning */
        [data-baseweb="portal"] [data-baseweb="popover"]:has([data-baseweb="menu"]),
        div[data-baseweb="popover"]:has(ul[role="listbox"]) {
            position: absolute !important;
            bottom: auto !important;
            right: auto !important;
            width: auto !important;
        }

        /* Quick Suggestion Chips (Fitted Compact Style) */
        div[data-testid="stPopoverBody"] div[data-testid="column"] button {
            min-height: 32px !important;
            height: 32px !important;
            border-radius: 8px !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            padding: 0.15rem 0.3rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: nowrap !important;
            border: 1px solid #E2E8F0 !important;
            background-color: #F8FAFC !important;
            color: #334155 !important;
        }
        div[data-testid="stPopoverBody"] div[data-testid="column"] button:hover {
            border-color: #2563EB !important;
            color: #2563EB !important;
            background-color: #EFF6FF !important;
        }

        .chat-header-v2 {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
            color: #FFFFFF;
            padding: 0.6rem 0.85rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }
        .chat-header-v2 .icon-box {
            width: 34px;
            height: 34px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            color: #60A5FA;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .chat-header-v2 .title { font-weight: 800; font-size: 0.88rem; color: #FFFFFF !important; }
        .chat-header-v2 .subtitle { font-size: 0.72rem; color: #93C5FD; font-weight: 500; margin-top: 1px; }
        .chat-header-v2 .status { font-size: 0.68rem; color: #4ADE80; font-weight: 600; margin-top: 1px; display: flex; align-items: center; gap: 6px; }
    </style>
    """, unsafe_allow_html=True)

    history_key = f"chat_history_{page_type}"
    if history_key not in st.session_state:
        st.session_state[history_key] = [
            {
                "role": "assistant",
                "content": f"👋 **Xin chào Quản lý!** Tôi là **Trợ Lý Chiến Lược AI Agent**.\n"
                           f"Tôi sẵn sàng giải đáp thắc mắc về dữ liệu & chiến lược trang **{page_type}** cho hồ sơ **{job_name}**."
            }
        ]

    # ── FLOATING CALLOUT BADGE & POPOVER BUTTON (MATCHING USER SCREENSHOT) ──
    st.markdown("""
    <div class="chat-callout-badge-v3">
        <i class="fa-solid fa-user-tie" style="color: #1E3A8A; font-size: 0.9rem;"></i>
        <span>Cố Vấn Chiến Lược SME</span>
    </div>
    """, unsafe_allow_html=True)

    with st.popover("💼  Hỏi Cố Vấn Chiến Lược", use_container_width=False):
        st.markdown(f"""
        <div class="chat-header-v2">
            <div class="icon-box"><i class="fa-solid fa-headset"></i></div>
            <div>
                <div class="title">Cố Vấn AI — Giải Đáp Dữ Liệu Trang Hiện Tại</div>
                <div class="subtitle">Hệ thống RAG tri thức WORKBank & Analytics</div>
                <div class="status"><span class="chat-callout-dot"></span> Đang kết nối: Trang {page_type} | {job_name[:20]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 1. CHAT MESSAGES HISTORY (PERFECT COMPACT HEIGHT: 180PX) ──
        chat_container = st.container(height=180)
        with chat_container:
            for msg in st.session_state[history_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # ── 2. QUICK SUGGESTION CHIPS ──
        st.markdown("<div style='margin-top: 4px; margin-bottom: 2px; font-size: 0.72rem; color: #64748B; font-weight: 600;'>💡 Gợi ý câu hỏi nhanh:</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        q_clicked = None
        with col1:
            if st.button("📊 Insight cốt lõi trang này?", key=f"q1_{page_type}", use_container_width=True):
                q_clicked = f"Tóm tắt 3 Insight số liệu quan trọng nhất trên trang {page_type} cho vị trí {job_name}."
            if st.button("⚠️ Rủi ro & rào cản nhân sự?", key=f"q2_{page_type}", use_container_width=True):
                q_clicked = f"Phân tích rào cản tâm lý và rủi ro phản kháng của nhân sự vị trí {job_name}."
        with col2:
            if st.button("🎯 Tác vụ thí điểm trước?", key=f"q3_{page_type}", use_container_width=True):
                q_clicked = f"Đề xuất danh sách các tác vụ Quick Wins có ROI cao nên thí điểm ngay cho {job_name}."
            if st.button("📋 Lộ trình Action Plan?", key=f"q4_{page_type}", use_container_width=True):
                q_clicked = f"Tư vấn lộ trình Action Plan 4 bước triển khai AI Agent tối ưu cho {job_name}."

        # ── 3. CHAT INPUT ──
        user_input = st.chat_input(f"Hỏi AI thắc mắc về trang {page_type}...", key=f"chat_input_{page_type}")
        prompt_to_process = q_clicked or user_input

        if prompt_to_process:
            st.session_state[history_key].append({"role": "user", "content": prompt_to_process})

            with st.spinner("Đang truy xuất dữ liệu WORKBank & phân tích câu hỏi..."):
                reply = query_chatbot_groq(
                    st.session_state[history_key],
                    page_type, job_name, category_name, stats_summary
                )

            st.session_state[history_key].append({"role": "assistant", "content": reply})
            st.rerun()




