"""
rag_advisor.py — Balanced & Actionable RAG Engine using WORKBank Paper & Groq LLM.
API Key: Provided by user.
Model: llama-3.3-70b-versatile (Medium length, well-structured & insightful)
"""

import os
import streamlit as st
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

PAPER_TEXT_PATH = "data/workbank_paper_text.txt"


def get_paper_summary_context():
    """
    Returns curated knowledge base extracted from the WORKBank research paper.
    """
    if os.path.exists(PAPER_TEXT_PATH):
        try:
            with open(PAPER_TEXT_PATH, "r", encoding="utf-8") as f:
                full_text = f.read()
                return full_text[:3500] + "\n\n[...Excerpts on Worker vs Expert Ratings & Task Automation...]\n" + full_text[10000:12500]
        except Exception:
            pass

    return """
    WORKBank Research Paper Summary:
    - Study: Stanford SALT Lab comprehensive study on AI Task Automation (2,053 tasks across 832 O*NET occupations).
    - Ratings: Evaluated by 7,451 workers (desire D, 13 reasons) and 453 AI experts (technological capability C, physical action, uncertainty, domain expertise, interpersonal communication, human agency).
    - Key Findings: Perception gap (D vs C) exists between worker desire and actual technological readiness. Tasks requiring high human agency (ethical, empathy, physical) need human-in-the-loop regardless of capability score.
    - AI Agent Framework: Full Automation (High D & High C), Copilot (High C & Low D), RAG Agent (High D & Low C), Low Priority (Low D & Low C).
    """


def query_groq_rag(job_name, category_name, page_type, stats_summary, user_question=""):
    """
    Queries Groq Llama-3.3-70b model for balanced, clear, medium-length analysis.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        paper_context = get_paper_summary_context()

        system_prompt = (
            "Bạn là Chuyên gia Tư vấn Chuyển đổi số & AI Agent cho Doanh nghiệp SME (dựa trên bài báo khoa học WORKBank - Stanford SALT Lab).\n"
            "QUY TẮC TRÌNH BÀY: ĐỘ DÀI TRUNG BÌNH, MẠCH LẠC, ĐI THẲNG VÀO TRỌNG TÂM. "
            "Không chào hỏi rườm rà. Trình bày rõ ràng thành 3 mục cốt lõi, mỗi mục gồm 2-3 gạch đầu dòng phân tích có lập luận số liệu cụ thể và dễ hiểu.\n\n"
            f"Tri thức bài báo khoa học WORKBank (Context):\n{paper_context}"
        )

        prompt_body = f"""
🎯 PHÂN TÍCH ĐỐI TƯỢNG: [{job_name}] — Ngành [{category_name}] (Chuyên đề: {page_type})
📊 DỮ LIỆU ĐỊNH LƯỢNG WORKBANK:
{stats_summary}

{f"❓ NGUYỆN VỌNG THÊM: {user_question}" if user_question else ""}

YÊU CẦU ĐẦU RA (Trình bày mạch lạc, độ dài vừa phải 300–400 từ, có emoji):

1. 🎓 **Đối Chiếu Lý Thuyết WORKBank**:
- Liên hệ chỉ số Mong muốn (D), Năng lực (C) và khoảng cách Gap ($D-C$) của vị trí này với phát hiện trong bài báo WORKBank.
- Đánh giá mức độ sẵn sàng công nghệ thực tế và rào cản đặc thù.

2. 🔍 **Giải Mã Bản Chất Tâm Lý & Nghiệp Vụ**:
- Lý giải nguyên nhân tại sao người lao động ủng hộ hoặc e ngại tự động hóa (dựa trên 13 lý do và các yếu tố lo mất việc / áp lực thời gian).
- Nhận diện các điểm nghẽn về chuyên môn hoặc quy trình cần lưu ý.

3. 🚀 **Khuyến Nghị Lộ Trình Triển Khai AI Agent**:
- Chỉ định mô hình AI phù hợp (Copilot / RAG Knowledge Agent / Full Automation).
- Đề xuất 2-3 bước hành động thực tiễn cho doanh nghiệp SME (bao gồm cơ chế Human-in-the-Loop nếu có tác vụ rủi ro/nhạy cảm).
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_body}
            ],
            temperature=0.35,
            max_tokens=850,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ **Không thể kết nối với Groq API**: {str(e)}\nVui lòng kiểm tra lại API Key hoặc kết nối mạng."


def render_ai_advisor_widget(page_type, job_name, category_name, stats_summary):
    """
    Renders an interactive UI section for Groq RAG AI Analysis.
    """
    st.markdown("---")
    st.markdown("### 🤖 Groq AI Advisor — Phân Tích Chuyên Sâu Theo Bài Báo WORKBank")
    st.caption("Ứng dụng Llama-3.3-70b kết hợp RAG Tri thức bài báo WORKBank (Stanford SALT Lab) — Phân tích mạch lạc & giải pháp thực tiễn cho SME.")

    col_btn, col_q = st.columns([1, 2])
    with col_q:
        custom_q = st.text_input("Gửi câu hỏi cho AI (tùy chọn):", placeholder="Ví dụ: Làm sao để nhân viên vị trí này hợp tác dùng AI?", key=f"q_{page_type}")
    with col_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Bắt Đầu Phân Tích AI", key=f"btn_{page_type}", type="primary", use_container_width=True)

    session_key = f"ai_result_{page_type}_{job_name}"

    if analyze_btn:
        with st.spinner("🔍 Đang truy xuất tri thức bài báo WORKBank & tổng hợp phân tích Groq AI..."):
            res = query_groq_rag(job_name, category_name, page_type, stats_summary, user_question=custom_q)
            st.session_state[session_key] = res

    if session_key in st.session_state:
        st.markdown(f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #8b5cf6; border-radius: 12px; padding: 1.4rem 1.6rem; margin-top: 1rem; box-shadow: 0 4px 12px -2px rgba(15,23,42,.05);">', unsafe_allow_html=True)
        st.markdown(st.session_state[session_key])
        st.markdown('</div>', unsafe_allow_html=True)
