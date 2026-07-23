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
        .element-container:has(div[data-testid="stPopover"]) {
            position: fixed !important;
            bottom: 75px !important;
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

        /* ── 2. FLOATING POPOVER BUTTON STYLING (FLOATING AT BOTTOM-RIGHT) ── */
        html body div.stApp div[data-testid="stPopover"] button,
        html body div.stApp button[data-testid="stBaseButton-popover"],
        html body div.stApp div[data-testid="stPopoverButton"] button,
        html body div.stApp button[aria-haspopup="dialog"],
        div[data-testid="stPopover"] > button {
            position: fixed !important;
            bottom: 75px !important;
            right: 25px !important;
            z-index: 999999 !important;
            width: auto !important;
            height: auto !important;
            white-space: nowrap !important;
            background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1.5px solid rgba(255, 255, 255, 0.45) !important;
            border-radius: 30px !important;
            padding: 0.7rem 1.4rem !important;
            font-weight: 800 !important;
            font-size: 0.88rem !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45) !important;
            animation: floatBounce 2.5s infinite ease-in-out !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        html body div.stApp div[data-testid="stPopover"] button:hover,
        html body div.stApp button[data-testid="stBaseButton-popover"]:hover,
        div[data-testid="stPopover"] > button:hover {
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%) !important;
            background-color: #1D4ED8 !important;
            box-shadow: 0 12px 32px rgba(37, 99, 235, 0.6) !important;
            transform: translateY(-2px) scale(1.02) !important;
        }
        html body div.stApp div[data-testid="stPopover"] button *,
        html body div.stApp button[data-testid="stBaseButton-popover"] *,
        div[data-testid="stPopover"] > button * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            font-weight: 800 !important;
        }

        /* ── 3. POP-UP DIALOG WINDOW STYLING ── */
        div[data-testid="stPopoverBody"] {
            width: 490px !important;
            max-height: 680px !important;
            border-radius: 18px !important;
            box-shadow: 0 25px 50px rgba(15, 23, 42, 0.25) !important;
            border: 1px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            padding: 1.2rem !important;
        }

        /* Quick Suggestion Chips */
        div[data-testid="stPopoverBody"] div[data-testid="column"] button {
            min-height: 42px !important;
            height: 42px !important;
            border-radius: 10px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            padding: 0.2rem 0.5rem !important;
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
            padding: 1rem 1.2rem;
            border-radius: 14px;
            margin-bottom: 0.9rem;
            display: flex;
            align-items: center;
            gap: 14px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }
        .chat-header-v2 .icon-box {
            width: 44px;
            height: 44px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.35rem;
            color: #60A5FA;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .chat-header-v2 .title { font-weight: 800; font-size: 1rem; color: #FFFFFF !important; }
        .chat-header-v2 .subtitle { font-size: 0.78rem; color: #93C5FD; font-weight: 500; margin-top: 2px; }
        .chat-header-v2 .status { font-size: 0.73rem; color: #4ADE80; font-weight: 600; margin-top: 3px; display: flex; align-items: center; gap: 6px; }
    </style>
    """, unsafe_allow_html=True)

    history_key = f"chat_history_{page_type}"
    if history_key not in st.session_state:
        st.session_state[history_key] = [
            {
                "role": "assistant",
                "content": f"👋 Kính chào Quản lý! Tôi là **Trợ Lý Chiến Lược AI Agent**.\n\n"
                           f"Tôi sẵn sàng giải đáp mọi thắc mắc về dữ liệu & biểu đồ trên trang **{page_type}** "
                           f"cho hồ sơ **{job_name}** ({category_name}).\n\n"
                           f"Vui lòng bấm chọn các câu hỏi gợi ý nhanh bên dưới hoặc gõ thắc mắc của bạn!"
            }
        ]

    # ── SINGLE FLOATING PILL POPOVER BUTTON (BOTTOM RIGHT) ──
    with st.popover("💡  Thắc mắc về trang này? Hỏi AI Advisor ngay!", use_container_width=False):
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

        # ── 1. CHAT MESSAGES HISTORY ──
        chat_container = st.container(height=380)
        with chat_container:
            for msg in st.session_state[history_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # ── 2. QUICK SUGGESTION CHIPS ──
        st.markdown("<div style='margin-top: 6px; margin-bottom: 2px; font-size: 0.75rem; color: #64748B; font-weight: 600;'>💡 Gợi ý câu hỏi nhanh:</div>", unsafe_allow_html=True)
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



