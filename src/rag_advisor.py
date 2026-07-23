"""
rag_advisor.py — Dynamic RAG Engine using WORKBank Paper (2506.06576v3) & Groq LLM.
Retrieves relevant context dynamically from extracted paper chunks using TF-IDF / Vector similarity.
"""

import os
import streamlit as st
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PAPER_TEXT_PATH = "data/workbank_paper_text.txt"


def get_groq_api_key():
    """
    Retrieves Groq API key from multiple sources in order of priority:
    1. Session state (entered by user in UI)
    2. Environment variables (os.environ or .env)
    3. Streamlit secrets (st.secrets)
    """
    if st.session_state.get("user_groq_api_key"):
        return st.session_state["user_groq_api_key"]

    env_key = os.environ.get("GROQ_API_KEY", "")
    if env_key:
        return env_key

    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GROQ_API_KEY="):
                        k = line.split("=", 1)[1].strip().strip("'\"")
                        if k:
                            return k
        except Exception:
            pass

    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
        if "groq" in st.secrets and "api_key" in st.secrets["groq"]:
            return st.secrets["groq"]["api_key"]
    except Exception:
        pass

    return ""


GROQ_API_KEY = get_groq_api_key()


@st.cache_resource
def load_and_index_paper():
    """
    Loads full text extracted from arXiv:2506.06576v3.pdf, chunks it, and builds TF-IDF vector index for RAG.
    """
    if not os.path.exists(PAPER_TEXT_PATH):
        return [], None, None

    try:
        with open(PAPER_TEXT_PATH, "r", encoding="utf-8") as f:
            full_text = f.read().strip()
        if not full_text or len(full_text) < 100:
            return [], None, None

        # Split text into meaningful paragraph chunks (~600-1000 characters)
        raw_paras = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 50]
        chunks = []
        curr = ""
        for p in raw_paras:
            if len(curr) + len(p) < 900:
                curr += "\n" + p if curr else p
            else:
                if curr:
                    chunks.append(curr)
                curr = p
        if curr:
            chunks.append(curr)

        if not chunks:
            return [], None, None

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(chunks)
        return chunks, vectorizer, tfidf_matrix

    except Exception:
        return [], None, None


def get_paper_summary_context(query_text=None, top_k=4):
    """
    Dynamic Retrieval Function: Searches indexed paper chunks for content most relevant to query_text.
    """
    chunks, vectorizer, tfidf_matrix = load_and_index_paper()

    if vectorizer and tfidf_matrix is not None and chunks:
        if query_text and len(query_text.strip()) > 2:
            try:
                q_vec = vectorizer.transform([query_text])
                sims = cosine_similarity(q_vec, tfidf_matrix).flatten()
                top_indices = sims.argsort()[-top_k:][::-1]
                retrieved = [chunks[i] for i in top_indices if sims[i] > 0.02]
                if retrieved:
                    return f"--- DYNAMIC RAG CONTEXT EXTRACTED FROM WORKBANK PAPER (arXiv:2506.06576v3) [Query: '{query_text}'] ---\n\n" + "\n\n[...Excerpt...]\n\n".join(retrieved)
            except Exception:
                pass
        
        # Fallback to top foundational chunks if query is empty or failed
        return "--- FOUNDATIONAL RAG CONTEXT FROM WORKBANK PAPER (arXiv:2506.06576v3) ---\n\n" + "\n\n[...Excerpt...]\n\n".join(chunks[:top_k])

    # Fallback summary if file is missing
    return """
    WORKBank Research Paper Summary (arXiv:2506.06576v3 - Stanford SALT Lab & Harvard):
    - Study: Comprehensive audit of AI Task Automation (2,053 tasks across 832 O*NET occupations).
    - Ratings: Evaluated by 7,451 workers (Automation Desire D, 13 reasons) and 453 AI experts (Technological Capability C, 6 factors).
    - Perception Gap: Significant gap between worker desire (D) and technological readiness (C). Tasks requiring high human agency (ethical, empathy, physical) need human-in-the-loop regardless of capability.
    - AI Architecture Framework: Full Automation (High D & High C), Copilot (High C & Low D), RAG Knowledge Agent (High D & Low C), Low Priority (Low D & Low C).
    """


def query_groq_rag(job_name, category_name, page_type, stats_summary, user_question=""):
    """
    Queries Groq Llama-3.3-70b model with dynamically retrieved WORKBank paper context.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return "⚠️ **Thiếu Groq API Key**: Vui lòng nhập API Key ở ô bên dưới hoặc lưu vào `.env` / `.streamlit/secrets.toml`."

    try:
        client = Groq(api_key=api_key)
        
        # Build search query for dynamic RAG retrieval
        search_query = f"{job_name} {category_name} {page_type} {user_question} desire capability automation worker expert human agency risk"
        paper_context = get_paper_summary_context(query_text=search_query, top_k=4)

        system_prompt = (
            "Bạn là Chuyên gia Tư vấn Chuyển đổi số & AI Agent cho Doanh nghiệp SME (dựa trên bài báo khoa học WORKBank - Stanford SALT Lab, arXiv:2506.06576v3).\n"
            "QUY TẮC TRÌNH BÀY: ĐỘ DÀI TRUNG BÌNH, MẠCH LẠC, ĐI THẲNG VÀO TRỌNG TÂM. "
            "Không chào hỏi rườm rà. Trình bày rõ ràng thành 3 mục cốt lõi, mỗi mục gồm 2-3 gạch đầu dòng phân tích có lập luận số liệu cụ thể và dễ hiểu.\n\n"
            f"Tri thức truy xuất động từ bài báo WORKBank (Dynamic RAG Context):\n{paper_context}"
        )

        prompt_body = f"""
🎯 PHÂN TÍCH ĐỐI TƯỢNG: [{job_name}] — Ngành [{category_name}] (Chuyên đề: {page_type})
📊 DỮ LIỆU ĐỊNH LƯỢNG WORKBANK:
{stats_summary}

{f"❓ NGUYỆN VỌNG THÊM: {user_question}" if user_question else ""}

YÊU CẦU ĐẦU RA (Trình bày mạch lạc, độ dài vừa phải 300–400 từ, có emoji):

1. 🎓 **Đối Chiếu Lý Thuyết WORKBank (Truy xuất từ bài báo arXiv:2506.06576v3)**:
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
    Renders an interactive UI section for Groq Dynamic RAG AI Analysis.
    """
    st.markdown("---")
    st.markdown("### 🤖 Groq Dynamic RAG AI Advisor — Phân Tích Chuyên Sâu Theo Bài Báo WORKBank")
    st.caption("Ứng dụng Llama-3.3-70b kết hợp RAG truy xuất động tri thức từ bài báo WORKBank (arXiv:2506.06576v3, Stanford SALT Lab).")

    col_btn, col_q = st.columns([1, 2])
    with col_q:
        custom_q = st.text_input("Gửi câu hỏi cho AI (tùy chọn):", placeholder="Ví dụ: Làm sao để nhân viên vị trí này hợp tác dùng AI?", key=f"q_{page_type}")
    with col_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Bắt Đầu Phân Tích AI", key=f"btn_{page_type}", type="primary", use_container_width=True)

    session_key = f"ai_result_{page_type}_{job_name}"

    if analyze_btn:
        with st.spinner("🔍 Đang truy xuất động tri thức bài báo WORKBank & tổng hợp phân tích Groq AI..."):
            res = query_groq_rag(job_name, category_name, page_type, stats_summary, user_question=custom_q)
            st.session_state[session_key] = res

    if session_key in st.session_state:
        st.markdown('<div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #8b5cf6; border-radius: 12px; padding: 1.4rem 1.6rem; margin-top: 1rem; box-shadow: 0 4px 12px -2px rgba(15,23,42,.05);">', unsafe_allow_html=True)
        st.markdown(st.session_state[session_key])
        st.markdown('</div>', unsafe_allow_html=True)
