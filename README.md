<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.x-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq_AI-Llama_3.3_70B-F55036?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/RAG-WORKBank_Paper-8B5CF6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" />
</p>

<h1 align="center">📊 SME Strategy Advisor</h1>
<h3 align="center">Business Intelligence Platform for AI Agent Adoption in SMEs</h3>

<p align="center">
  <em>Hệ thống tư vấn chiến lược triển khai AI Agent cho doanh nghiệp vừa & nhỏ — dựa trên bộ dữ liệu nghiên cứu WORKBank (Stanford SALT Lab & Harvard)</em>
</p>

---

## 📋 Mục Lục

- [Tổng Quan](#-tổng-quan)
- [Demo & Screenshots](#-demo--screenshots)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Quy Trình Dữ Liệu (Data Pipeline)](#-quy-trình-dữ-liệu-data-pipeline)
- [Workflow Ứng Dụng](#-workflow-ứng-dụng)
- [Cấu Trúc Thư Mục](#-cấu-trúc-thư-mục)
- [Kỹ Thuật Sử Dụng](#-kỹ-thuật-sử-dụng)
- [Cài Đặt & Chạy](#-cài-đặt--chạy)
- [Biến Môi Trường](#-biến-môi-trường)
- [Dashboard Chi Tiết](#-dashboard-chi-tiết)
- [AI Chatbot Advisor](#-ai-chatbot-advisor)
- [Deploy Lên Streamlit Cloud / Vercel](#-deploy)
- [Tài Liệu Tham Khảo](#-tài-liệu-tham-khảo)
- [License](#-license)

---

## 🎯 Tổng Quan

**SME Strategy Advisor** là hệ thống Business Intelligence Dashboard giúp doanh nghiệp vừa & nhỏ (SME) tại Việt Nam đưa ra quyết định **dựa trên dữ liệu** (Data-Driven Decision Making) khi triển khai AI Agent tự động hóa công việc.

### Vấn đề cần giải quyết

| Thách thức | Giải pháp |
|---|---|
| SME không biết nên tự động hóa tác vụ nào trước | Ma trận 4 Góc phần tư phân loại 180 tác vụ |
| Không ước lượng được ROI tiết kiệm | Mô hình tính ROI = Thời gian × Lương × C |
| Lo ngại nhân viên phản đối thay đổi | Bản đồ Tâm lý 4 nhóm cảm xúc + Change Management |
| Nhà quản trị không đọc được biểu đồ | AI Chatbot RAG giải thích insight 24/7 |

### Tính năng nổi bật

- 🏢 **5 trang Dashboard** phong cách Power BI / Notion / Stripe
- 📊 **7 metrics định lượng** với công thức toán học rõ ràng
- 🤖 **AI Chatbot Floating** (Llama-3.3-70B + RAG) tư vấn chiến lược trực tiếp trên Dashboard
- 🎛️ **3 bộ lọc tương tác** (Ngành nghề, Vị trí, Focus Job) cập nhật real-time
- 📈 **5 loại biểu đồ** Plotly tương tác: Diverging Bar, Scatter Quadrant, Bubble, Heatmap, Histogram
- 🗂️ **Bảng dữ liệu gốc**: WORKBank Research Dataset (Stanford SALT Lab, arXiv:2506.06576v3)

---

## 🖼️ Demo & Screenshots

### Trang Chủ — Tổng Quan Dashboard
![Overview Dashboard](docs/screenshots/home_overview.png)

### Ma Trận Chiến Lược 4 Góc Phần Tư
![Strategic Quadrant](docs/screenshots/strategic_matrix.png)

### Bản Đồ Tâm Lý Nhân Viên
![Employee Psychology](docs/screenshots/employee_insights.png)

### AI Chatbot Advisor
![AI Chatbot](docs/screenshots/chatbot_demo.png)

---

## 🏗️ Kiến Trúc Hệ Thống

```mermaid
graph TB
    subgraph "📂 Data Layer"
        A1[("domain_worker_desires.csv<br/>180 tác vụ × 7,451 NLĐ")] 
        A2[("expert_rated_capability.csv<br/>180 tác vụ × 453 chuyên gia")]
        A3[("task_statement_metadata.csv<br/>Nghề nghiệp + Thời gian")]
        A4[("sme_role_to_occupation.csv<br/>18 vị trí × 8 ngành SME")]
    end

    subgraph "⚙️ ETL Pipeline"
        B1["etl.py<br/>Merge + Clean + Rename"]
        B2["scoring.py<br/>Normalize + Score + Flag"]
        B3["mapping.py<br/>O*NET → SME Mapping"]
    end

    subgraph "📊 Presentation Layer"
        C1["Home.py — Tổng Quan"]
        C2["1_Chiến_Lược_Triển_Khai.py"]
        C3["2_Tâm_Lý_Nhân_Viên.py"]
        C4["3_Chi_Tiết_và_So_Sánh.py"]
        C5["4_Khuyến_Nghị.py"]
    end

    subgraph "🎨 UI Engine"
        D1["ui_components.py<br/>CSS Injection + KPI + Banner"]
        D2["insights.py<br/>Auto-generated Insight Panels"]
    end

    subgraph "🤖 AI Layer"
        E1["rag_advisor.py<br/>RAG Context Retrieval"]
        E2["chatbot_widget.py<br/>Floating Chat UI"]
        E3[("Groq Cloud API<br/>Llama-3.3-70B")]
        E4[("workbank_paper_text.txt<br/>Paper Knowledge Base")]
    end

    A1 & A2 & A3 --> B1 --> B2 --> B3
    B3 --> |"tasks_scored.csv"| C1 & C2 & C3 & C4 & C5
    D1 --> C1 & C2 & C3 & C4 & C5
    D2 --> C2 & C3 & C4
    E4 --> E1 --> E2
    E2 --> E3
    E2 --> C1 & C2 & C3 & C4 & C5

    style A1 fill:#DBEAFE,stroke:#2563EB
    style A2 fill:#DBEAFE,stroke:#2563EB
    style A3 fill:#DBEAFE,stroke:#2563EB
    style A4 fill:#DBEAFE,stroke:#2563EB
    style B1 fill:#FEF3C7,stroke:#D97706
    style B2 fill:#FEF3C7,stroke:#D97706
    style B3 fill:#FEF3C7,stroke:#D97706
    style E3 fill:#F3E8FF,stroke:#7C3AED
```

---

## 🔄 Quy Trình Dữ Liệu (Data Pipeline)

```mermaid
flowchart LR
    subgraph "1️⃣ RAW DATA"
        R1["worker_desires.csv<br/>D score + 13 lý do"]
        R2["expert_capability.csv<br/>C score + 6 yếu tố"]
        R3["task_metadata.csv<br/>occupation + time"]
    end

    subgraph "2️⃣ ETL"
        E1["Merge trên<br/>task_statement"]
        E2["Rename cột<br/>13 lý do → short names"]
        E3["Parse skills<br/>ast.literal_eval"]
    end

    subgraph "3️⃣ SCORING"
        S1["Min-Max Normalize<br/>C, D → [0, 1]"]
        S2["Priority Score<br/>P = (0.5×C + 0.5×D) × 100"]
        S3["ROI Savings<br/>wage × C × 0.20"]
        S4["Risk Flag<br/>4 quadrants"]
        S5["Sensitive Flag<br/>keyword scan"]
    end

    subgraph "4️⃣ MAPPING"
        M1["O*NET occupation<br/>→ sme_role"]
        M2["sme_role<br/>→ sme_category"]
    end

    subgraph "5️⃣ OUTPUT"
        O1[("tasks_scored.csv<br/>180 rows × 35+ cols")]
    end

    R1 & R2 & R3 --> E1 --> E2 --> E3 --> S1 --> S2 --> S3 --> S4 --> S5 --> M1 --> M2 --> O1

    style R1 fill:#DBEAFE
    style R2 fill:#DBEAFE
    style R3 fill:#DBEAFE
    style O1 fill:#DCFCE7,stroke:#16A34A
```

### Công thức Scoring chi tiết

| Metric | Công thức | Thang đo |
|---|---|---|
| Normalized C | `(c_raw − 1.0) / (5.0 − 1.0)` | 0.00 – 1.00 |
| Normalized D | `(d_raw − 1.0) / (5.0 − 1.0)` | 0.00 – 1.00 |
| Priority Score | `(0.5 × C + 0.5 × D) × 100` | 0 – 100 |
| ROI Savings | `annual_wage × C × 0.20` | USD/năm |
| Technical Complexity | `(phys×0.3 + unc×0.35 + dom×0.35) / 5.0 × 10` | 0 – 10 |
| Time Saving | `C × 40%` | % |

### Phân loại 4 Vùng Chiến Lược (Risk Flag)

| Vùng | Điều kiện | Mô hình AI | Số tác vụ |
|---|---|---|---|
| 🟢 Thí điểm Ngay | D ≥ 0.5 & C ≥ 0.5 | Full Automation | 95 (52.8%) |
| 🟡 Phản kháng Nội bộ | C > 0.7 & D < 0.4 | Copilot | 16 (8.9%) |
| 🟠 Kỳ vọng vượt Năng lực | D > 0.7 & C < 0.4 | RAG Agent | 0 (0%) |
| ⚪ Ưu tiên Thấp | Còn lại | Chưa ưu tiên | 69 (38.3%) |

---

## 🔁 Workflow Ứng Dụng

```mermaid
flowchart TD
    START(("👤 User truy cập<br/>localhost:8501")) --> SIDEBAR

    subgraph SIDEBAR["🎛️ Sidebar Navigation"]
        F1["Chọn Ngành SME<br/>(8 ngành)"]
        F2["Chọn Vị trí công việc<br/>(18 vị trí)"]
        F3["Focus Job<br/>(chi tiết 1 vị trí)"]
        F1 --> F2 --> F3
    end

    SIDEBAR --> LOAD["📂 Load tasks_scored.csv<br/>+ Filter theo selection"]

    LOAD --> PAGE{"📄 Chọn trang?"}

    PAGE -->|"Tổng quan"| P1["🏠 Overview<br/>6 KPI + Gap Bar + Quadrant<br/>+ Strategy Summary"]
    PAGE -->|"Chiến lược"| P2["📈 Strategic Quadrant<br/>Scatter 4 vùng + Insight Panel"]
    PAGE -->|"Tâm lý"| P3["👥 Employee Psychology<br/>Bubble Chart 4 cảm xúc"]
    PAGE -->|"Chi tiết"| P4["🔍 Heatmap Analysis<br/>13 lý do × 18 vị trí"]
    PAGE -->|"Khuyến nghị"| P5["🎯 Action Cards<br/>Top 5 Quick Wins"]

    P1 & P2 & P3 & P4 & P5 --> CHATBOT

    subgraph CHATBOT["🤖 AI Chatbot Advisor"]
        CB1["Floating Button<br/>+ Callout Badge"]
        CB2["Chat Window mở ra<br/>4 Quick Questions"]
        CB3["User nhập câu hỏi"]
        CB4["RAG trích xuất<br/>WORKBank context"]
        CB5["Groq Llama-3.3-70B<br/>sinh câu trả lời"]
        CB6["Hiển thị Executive<br/>Report trên chat"]
        CB1 --> CB2 --> CB3 --> CB4 --> CB5 --> CB6
    end

    style START fill:#8B5CF6,color:#FFF
    style CHATBOT fill:#F0FDF4,stroke:#16A34A
    style SIDEBAR fill:#EFF6FF,stroke:#2563EB
```

### User Flow chi tiết

```mermaid
sequenceDiagram
    actor User
    participant Sidebar
    participant Dashboard
    participant Insights
    participant Chatbot
    participant Groq as Groq AI (Llama-3.3-70B)
    participant RAG as RAG Engine

    User->>Sidebar: Chọn Ngành + Vị trí
    Sidebar->>Dashboard: Filter dữ liệu real-time
    Dashboard->>Dashboard: Render 6 KPI Cards
    Dashboard->>Dashboard: Render biểu đồ Plotly
    Dashboard->>Insights: Tính insight tự động
    Insights->>Dashboard: Panel 3 mục (Proof + Cause + Report)
    
    User->>Chatbot: Click "Hỏi AI Trợ Lý"
    Chatbot->>RAG: get_paper_summary_context()
    RAG-->>Chatbot: WORKBank paper excerpts
    Chatbot->>Chatbot: Inject page_type + KPI stats
    Chatbot->>Groq: POST /chat/completions
    Groq-->>Chatbot: Executive analysis (150-220 words)
    Chatbot->>User: Hiển thị phân tích chiến lược
```

---

## 📁 Cấu Trúc Thư Mục

```
SME-Strategy-Advisor/
│
├── 📄 README.md                          # Documentation (file này)
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .streamlit/
│   └── config.toml                       # Streamlit theme config
│
├── 📂 app/                               # ── PRESENTATION LAYER ──
│   ├── Home.py                           # 🏠 Trang Chủ (Tổng Quan Dashboard)
│   ├── components/
│   │   └── ui_components.py              # 🎨 CSS Injection + KPI Cards + Banners
│   └── pages/
│       ├── 1_Chiến_Lược_Triển_Khai.py    # 📈 Ma Trận 4 Góc Phần Tư
│       ├── 2_Tâm_Lý_Nhân_Viên.py        # 👥 Bản Đồ Tâm Lý Nhân Viên
│       ├── 3_Chi_Tiết_và_So_Sánh.py      # 🔍 Heatmap Phân Bố Lý Do
│       └── 4_Khuyến_Nghị.py              # 🎯 Recommendation Cards
│
├── 📂 src/                               # ── BUSINESS LOGIC LAYER ──
│   ├── etl.py                            # 🔄 Extract-Transform-Load pipeline
│   ├── scoring.py                        # 📐 Scoring + Risk Flag + ROI
│   ├── mapping.py                        # 🗺️ O*NET → SME Role Mapping + Sidebar
│   ├── insights.py                       # 💡 Auto-generated Insight Engine
│   ├── utils.py                          # 🛠️ Utility functions (load data)
│   ├── rag_advisor.py                    # 📚 RAG Engine (WORKBank paper)
│   └── chatbot_widget.py                 # 🤖 Floating AI Chatbot Widget
│
├── 📂 data/                              # ── DATA LAYER ──
│   ├── domain_worker_desires.csv         # Worker desire scores (7,451 ratings)
│   ├── expert_rated_technological_capability.csv  # Expert capability scores (453 experts)
│   ├── task_statement_with_metadata.csv  # Task metadata (occupation, time, wage)
│   ├── workbank_paper_text.txt           # WORKBank paper text for RAG
│   ├── mapping/
│   │   └── sme_role_to_occupation.csv    # 18 SME roles → O*NET occupations
│   └── processed/
│       └── tasks_scored.csv              # ⭐ Final scored dataset (180 × 35+ cols)
│
└── 📂 docs/                              # ── DOCUMENTATION ──
    └── screenshots/                      # Dashboard screenshots for README
```

---

## 🛠️ Kỹ Thuật Sử Dụng

### Tech Stack

| Layer | Technology | Vai trò |
|---|---|---|
| **Frontend** | Streamlit 1.35+ | Web framework, multipage routing |
| **UI/UX** | Custom CSS Injection | Power BI / Notion / Stripe design system |
| **Charts** | Plotly 5.x (Express + Graph Objects) | Interactive visualizations |
| **Icons** | Font Awesome 6.5 (CDN) | Navigation + KPI icons |
| **Backend** | Python 3.10+ | Data processing + API calls |
| **Data** | Pandas + NumPy | ETL pipeline + statistical computation |
| **AI Model** | Llama-3.3-70B-Versatile | Chatbot response generation |
| **AI Infra** | Groq Cloud API | Ultra-fast LLM inference (~200ms) |
| **RAG** | Custom text retrieval | WORKBank paper knowledge extraction |
| **Report** | python-docx | Automated Word report generation |

### Kỹ Thuật Trực Quan Hóa

| Biểu đồ | Thư viện | Kỹ thuật | Mục đích |
|---|---|---|---|
| Diverging Bar Chart | `plotly.graph_objects.Bar` | Horizontal bar, dual-color encoding | So sánh Gap (D−C) giữa 18 vị trí |
| Scatter Quadrant | `plotly.express.scatter` | Size = ROI, Color = Risk Flag | Phân loại 4 vùng chiến lược |
| Bubble Chart | `plotly.express.scatter` | Size = time, Color = % pilot | Bản đồ 4 nhóm cảm xúc |
| Heatmap | `plotly.express.imshow` | RdYlGn color scale | Phân bố 13 lý do × 18 vị trí |
| Histogram | `plotly.express.histogram` | Bin distribution | Phân bố Priority Score |

### Kỹ Thuật UI/UX Nâng Cao

- **CSS Injection**: Toàn bộ giao diện Streamlit được override bằng `st.markdown()` với `unsafe_allow_html=True` — tạo ra Sidebar 4 vùng cố định, KPI Cards bo tròn có viền màu, Hero Banner gradient, và layout responsive
- **Glassmorphism**: Background sidebar sử dụng `backdrop-filter: blur()` tạo hiệu ứng kính mờ
- **Micro-animations**: CSS `@keyframes` cho Float Bounce (chatbot badge), Pulse Glow (chat button), Shimmer (KPI cards)
- **Font Awesome Integration**: Nhúng CDN Font Awesome 6.5 để render 20+ icon chuyên nghiệp

### Kỹ Thuật AI/ML

- **RAG (Retrieval-Augmented Generation)**: Module `rag_advisor.py` đọc toàn văn bài báo WORKBank → trích xuất ngữ cảnh 3,500 + 2,500 ký tự → inject vào system prompt
- **Context-Aware Chatbot**: Mỗi trang truyền `page_type`, `job_name`, `category_name`, `stats_summary` → AI hiểu đang nói về trang nào, vị trí nào
- **Conversation Memory**: Lưu 6 tin nhắn gần nhất trong `st.session_state` cho multi-turn dialog
- **Prompt Engineering**: System prompt dài ~800 token, role-play Senior Strategy Advisor, output format C-Level Executive Report

---

## 🚀 Cài Đặt & Chạy

### Yêu cầu hệ thống

- Python ≥ 3.10
- pip (Python package manager)
- Trình duyệt web hiện đại (Chrome, Firefox, Edge)

### Cài đặt

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/sme-strategy-advisor.git
cd sme-strategy-advisor

# 2. Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Thiết lập biến môi trường
export GROQ_API_KEY="gsk_your_api_key_here"    # Linux/Mac
set GROQ_API_KEY=gsk_your_api_key_here         # Windows CMD
$env:GROQ_API_KEY="gsk_your_api_key_here"      # Windows PowerShell
```

### Chạy ứng dụng

```bash
# Chạy Streamlit development server
streamlit run app/Home.py --server.port 8501

# Mở trình duyệt tại:
# http://localhost:8501
```

### Requirements

```txt
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
groq>=0.4.0
python-docx>=0.8.11
openpyxl>=3.1.0
```

---

## 🔐 Biến Môi Trường

| Biến | Bắt buộc | Mô tả |
|---|---|---|
| `GROQ_API_KEY` | ✅ Có (cho Chatbot) | API key từ [console.groq.com](https://console.groq.com) |

> **Lưu ý**: Dashboard hoạt động bình thường mà không cần API key. Chỉ tính năng AI Chatbot yêu cầu Groq API key.

---

## 📊 Dashboard Chi Tiết

### Trang 1: Tổng Quan (Overview)

| Thành phần | Mô tả |
|---|---|
| Hero Banner | Gradient navy → blue, tiêu đề + phụ đề |
| 6 KPI Cards | Tổng tác vụ · Điểm ưu tiên TB · ROI · Thí điểm · Rủi ro · Nhạy cảm |
| Gap Analysis | Diverging Bar — khoảng cách D−C theo 18 vị trí |
| Strategic Quadrant | Scatter 4 góc — C vs D, size = ROI |
| Strategy Summary | Bullet points tự động tính từ dữ liệu |
| Action Cards | 3 thẻ khuyến nghị chiến lược |

### Trang 2: Chiến Lược Triển Khai

| Thành phần | Mô tả |
|---|---|
| Expanded Quadrant | Scatter 450px, hover tooltip chi tiết |
| Insight Panel | 3 mục: Bằng chứng + Nguyên nhân + Đề xuất |

### Trang 3: Tâm Lý Nhân Viên

| Thành phần | Mô tả |
|---|---|
| Bubble Chart | Enjoyment (X) vs Security (Y), size = time |
| 4 Nhóm | Sẵn sàng · Lo lắng · Mâu thuẫn · Gắn bó |

### Trang 4: Chi Tiết & So Sánh

| Thành phần | Mô tả |
|---|---|
| Heatmap | 13 lý do × 18 vị trí, RdYlGn scale |
| Cross-Industry | So sánh mức sẵn sàng giữa 8 ngành |

### Trang 5: Khuyến Nghị Hành Động

| Thành phần | Mô tả |
|---|---|
| Top 5 Cards | Recommendation cards xếp hạng ROI |
| Quick Wins | 3 kịch bản: Quick Wins · Copilot · Approval |

---

## 🤖 AI Chatbot Advisor

### Kiến Trúc RAG 3 Lớp

```mermaid
graph LR
    A["📄 WORKBank Paper<br/>workbank_paper_text.txt"] -->|"Retrieval"| B["🧠 RAG Engine<br/>rag_advisor.py"]
    C["📊 Page Context<br/>KPI + Filters"] -->|"Injection"| B
    D["💬 User Question"] -->|"Input"| B
    B -->|"System Prompt<br/>~800 tokens"| E["🦙 Groq Cloud<br/>Llama-3.3-70B"]
    E -->|"Response<br/>150-220 words"| F["📋 Executive<br/>Report Output"]

    style A fill:#DBEAFE
    style E fill:#F3E8FF,stroke:#7C3AED
    style F fill:#DCFCE7
```

### Tính năng Chatbot

- ✅ Context-Aware: Nhận biết trang đang mở + bộ lọc đang chọn
- ✅ Multi-turn: Lưu 6 tin nhắn gần nhất cho hội thoại liên tục
- ✅ Quick Questions: 4 phím tắt câu hỏi thường gặp
- ✅ RAG Knowledge: Trích xuất tri thức từ bài báo WORKBank
- ✅ Executive Style: Output theo format báo cáo quản trị cấp cao

---

## 🌐 Deploy

### Option 1: Streamlit Community Cloud (Khuyến nghị)

```bash
# 1. Push code lên GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Truy cập https://share.streamlit.io
# 3. Connect GitHub repo
# 4. Main file path: app/Home.py
# 5. Thêm GROQ_API_KEY vào Secrets
```

**Cấu hình Streamlit Cloud:**
- Main file: `app/Home.py`
- Python version: 3.10
- Secrets: `GROQ_API_KEY = "gsk_..."`

### Option 2: Vercel (via Serverless)

> ⚠️ **Lưu ý**: Vercel không hỗ trợ native Streamlit. Để deploy lên Vercel, cần chuyển sang framework web khác (Next.js/Flask) hoặc sử dụng Docker wrapper.

**Cách deploy Streamlit qua Docker trên Vercel:**

1. Tạo `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Tạo `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "Dockerfile",
      "use": "@vercel/static-build"
    }
  ]
}
```

3. Hoặc deploy qua **Vercel + Docker** platforms khác:
```bash
# Railway (khuyến nghị thay Vercel cho Streamlit)
railway login
railway init
railway up

# Hoặc Render
# Tạo Web Service → Docker → Connect GitHub repo
```

### Option 3: Docker Local

```bash
# Build image
docker build -t sme-advisor .

# Run container
docker run -p 8501:8501 -e GROQ_API_KEY="gsk_..." sme-advisor
```

### Chuẩn bị `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
~$*

# Reports (optional — exclude large Word files)
*.docx
*.pdf

# Data cache
data/processed/__pycache__/
```

---

## 📚 Tài Liệu Tham Khảo

| Tài liệu | Link |
|---|---|
| WORKBank Paper | [arXiv:2506.06576v3](https://arxiv.org/abs/2506.06576v3) |
| Stanford SALT Lab | [salt.stanford.edu](https://salt.stanford.edu) |
| O*NET Database | [onetonline.org](https://www.onetonline.org) |
| Streamlit Docs | [docs.streamlit.io](https://docs.streamlit.io) |
| Plotly Python | [plotly.com/python](https://plotly.com/python) |
| Groq API | [console.groq.com](https://console.groq.com) |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>SME Strategy Advisor</strong> — Data-Driven AI Adoption for Vietnamese SMEs
  <br/>
  <em>Built with ❤️ using Streamlit + Plotly + Groq AI</em>
</p>
