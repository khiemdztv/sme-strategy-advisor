"""
chatbot_widget.py — Executive Strategy Advisor Floating Widget (Enhanced Visibility & Guidance)
Renders a highly visible, engaging AI Chatbot Floating Button & Callout Badge to prompt user queries on page insights.
"""

import streamlit as st
import os
from groq import Groq
from rag_advisor import get_paper_summary_context, GROQ_API_KEY


def query_chatbot_groq(messages_history, page_type, job_name, category_name, stats_summary):
    """
    Queries Groq with conversation history + WORKBank paper RAG + page context.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        paper_context = get_paper_summary_context()

        system_prompt = (
            "Bạn là Cố Vấn Chiến Lược Doanh Nghiệp Cấp Cao (Senior Strategy Advisor), chuyên tư vấn phân tích dữ liệu vận hành và hoạch định tự động hóa cho các doanh nghiệp vừa & nhỏ (SME) dựa trên nghiên cứu WORKBank (Stanford SALT Lab).\n\n"
            f"📍 TRANG PHÂN TÍCH HIỆN TẠI: {page_type}\n"
            f"🏢 NGÀNH SME: {category_name} | 🎯 JOB FOCUS: {job_name}\n"
            f"📊 DỮ LIỆU ĐỊNH LƯỢNG HỆ THỐNG:\n{stats_summary}\n\n"
            f"📚 NỀN TẢNG TRI THỨC WORKBANK:\n{paper_context}\n\n"
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
    Renders a highly visible, modern Executive Strategy AI Advisor pop-up widget.
    """
    st.markdown("""
    <style>
        /* Pulse Animation for Chatbot Glow */
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.5); }
            70% { box-shadow: 0 0 0 14px rgba(37, 99, 235, 0); }
            100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }

        @keyframes floatBounce {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-4px); }
        }

        /* Floating Chatbot Button Position & Prevent Full-Width Container */
        div[data-testid="stElementContainer"]:has(div[data-testid="stPopover"]),
        div[data-testid="stPopover"],
        .stPopover {
            position: fixed !important;
            bottom: 75px !important;
            right: 25px !important;
            width: auto !important;
            max-width: fit-content !important;
            min-width: unset !important;
            z-index: 999999 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Executive High-Visibility Gradient Button */
        div[data-testid="stPopover"] > button {
            background: linear-gradient(135deg, #1E40AF 0%, #2563EB 60%, #3B82F6 100%) !important;
            color: #FFFFFF !important;
            border-radius: 50px !important;
            padding: 0.95rem 1.7rem !important;
            border: 2px solid rgba(255, 255, 255, 0.6) !important;
            font-weight: 800 !important;
            font-size: 1.02rem !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.45) !important;
            animation: pulseGlow 2.8s infinite !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: auto !important;
        }
        div[data-testid="stPopover"] > button:hover {
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%) !important;
            transform: translateY(-3px) scale(1.03) !important;
            box-shadow: 0 14px 35px rgba(37, 99, 235, 0.6) !important;
        }
        div[data-testid="stPopover"] > button p {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1.02rem !important;
            margin: 0 !important;
        }

        /* Callout Badge (Bong Bóng Hướng Dẫn) */
        .chat-callout-badge {
            position: fixed !important;
            bottom: 145px !important;
            right: 25px !important;
            width: auto !important;
            max-width: 320px !important;
            background: #FFFFFF !important;
            color: #0F172A !important;
            padding: 0.6rem 1.1rem !important;
            border-radius: 14px !important;
            font-size: 0.83rem !important;
            font-weight: 700 !important;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15) !important;
            border: 1.5px solid #2563EB !important;
            z-index: 999998 !important;
            pointer-events: none !important;
            animation: floatBounce 3s infinite ease-in-out !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        .chat-callout-badge::after {
            content: '';
            position: absolute;
            bottom: -9px;
            right: 35px;
            width: 0;
            height: 0;
            border-left: 9px solid transparent;
            border-right: 9px solid transparent;
            border-top: 9px solid #2563EB;
        }
        .chat-callout-dot {
            width: 9px;
            height: 9px;
            background-color: #22C55E;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #22C55E;
        }

        /* Pop-up Window Dimensions & Style */
        div[data-testid="stPopoverBody"] {
            width: 490px !important;
            max-height: 680px !important;
            border-radius: 18px !important;
            box-shadow: 0 25px 50px rgba(15, 23, 42, 0.25) !important;
            border: 1px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            padding: 1.2rem !important;
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
    
    <div class="chat-callout-badge">
        <span class="chat-callout-dot"></span>
        <span>💡 Thắc mắc về trang này? <strong>Hỏi AI Advisor</strong> ngay!</span>
    </div>
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

    with st.popover("💬 Hỏi AI Trợ Lý Về Trang Này"):
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

        st.caption("💡 Câu hỏi gợi ý nhanh cho trang này:")
        col1, col2 = st.columns(2)
        q_clicked = None
        with col1:
            if st.button("📊 Insight cốt lõi trang này?", key=f"q1_{page_type}", type="primary", use_container_width=True):
                q_clicked = f"Tóm tắt 3 Insight số liệu quan trọng nhất trên trang {page_type} cho vị trí {job_name}."
            if st.button("⚠️ Rủi ro & rào cản nhân sự?", key=f"q2_{page_type}", use_container_width=True):
                q_clicked = f"Phân tích rào cản tâm lý và rủi ro phản kháng của nhân sự vị trí {job_name}."
        with col2:
            if st.button("🎯 Tác vụ nào nên thí điểm trước?", key=f"q3_{page_type}", use_container_width=True):
                q_clicked = f"Đề xuất danh sách các tác vụ Quick Wins có ROI cao nên thí điểm ngay cho {job_name}."
            if st.button("📋 Action Plan 4 bước triển khai?", key=f"q4_{page_type}", use_container_width=True):
                q_clicked = f"Tư vấn lộ trình Action Plan 4 bước triển khai AI Agent tối ưu cho {job_name}."

        st.markdown("---")

        chat_container = st.container(height=380)
        with chat_container:
            for msg in st.session_state[history_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

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
