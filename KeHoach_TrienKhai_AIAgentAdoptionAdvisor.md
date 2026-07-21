# Kế hoạch triển khai chi tiết
## Đề tài: AI Agent Adoption Advisor — Công cụ tư vấn triển khai AI Agent cho doanh nghiệp SME

> Học phần: Trực quan hoá dữ liệu · Chủ đề 1 — Kinh doanh, Tài chính và Quản trị Tổ chức
> Công cụ: Python, Streamlit · Dữ liệu: WORKBank (SALT-NLP, Stanford)

---

## 1. Tổng quan dự án

| Mục | Nội dung |
|---|---|
| Sản phẩm cuối | Dashboard Streamlit tương tác + báo cáo docx + slide 10–15 trang |
| Người dùng mục tiêu | Chủ/quản lý SME cân nhắc triển khai AI Agent |
| Nguồn dữ liệu | 3 file CSV từ `SALT-NLP/WORKBank` (Hugging Face) |
| Thời lượng | 6 tuần |
| Quy mô nhóm | 4–5 sinh viên, 4 vai trò |

**Đầu ra cốt lõi:** người dùng chọn ngành + vị trí công việc → hệ thống trả về (1) bảng xếp hạng tác vụ nên thí điểm AI Agent, (2) ước tính thời gian tiết kiệm, (3) cảnh báo tác vụ rủi ro.

---

## 2. Kiến trúc tổng thể

```
data/
 ├─ raw/                        # 3 file CSV gốc tải từ Hugging Face
 │   ├─ domain_worker_desires.csv
 │   ├─ expert_rated_technological_capability.csv
 │   └─ task_statement_with_metadata.csv
 ├─ mapping/
 │   └─ sme_role_to_occupation.csv   # bảng ánh xạ tự xây (thủ công)
 └─ processed/
     └─ tasks_scored.parquet     # dữ liệu đã gộp + tính chỉ số

src/
 ├─ etl.py            # load, clean, merge 3 nguồn dữ liệu
 ├─ scoring.py         # công thức tính Priority Score & Risk Flag
 ├─ mapping.py         # xử lý ánh xạ vị trí SME ↔ occupation
 └─ utils.py

app/
 ├─ Home.py                        # trang chọn hồ sơ doanh nghiệp
 ├─ pages/
 │   ├─ 1_Bang_khuyen_nghi.py
 │   ├─ 2_Bieu_do_tong_quan.py
 │   └─ 3_Canh_bao_rui_ro.py
 └─ components/                    # biểu đồ, thẻ KPI tái sử dụng

reports/
 ├─ bao_cao_nhom.docx
 └─ slide_trinh_bay.pptx
```

**Tech stack:** Python 3.11, Pandas, Streamlit, Plotly (biểu đồ tương tác), `datasets` (tải WORKBank từ Hugging Face), Parquet (lưu dữ liệu đã xử lý để dashboard load nhanh).

---

## 3. Pipeline xử lý dữ liệu (chi tiết)

### Bước 3.1 — Tải & khảo sát dữ liệu gốc
- Tải 3 file bằng `datasets.load_dataset("SALT-NLP/WORKBank", data_files=...)`.
- Đọc **Code Book** (`codebook.pdf` trong repo GitHub `SALT-NLP/workbank`) để xác nhận chính xác tên cột, thang đo (ví dụ thang mong muốn 1–5, thang năng lực 1–5, mã occupation theo O*NET-SOC).
- Kiểm tra: số dòng, giá trị thiếu, trùng lặp `task_id`.

### Bước 3.2 — Gộp dữ liệu (merge)
- Khoá gộp: `task_id` (hoặc cặp `occupation_code` + `task_statement` nếu không có id chung — cần đối chiếu codebook).
- Kết quả: mỗi dòng = 1 tác vụ, gồm: `occupation`, `task_statement`, `desire_score` (trung bình đánh giá người lao động), `capability_score` (trung bình đánh giá chuyên gia), và metadata ngành/nhóm nghề.

### Bước 3.3 — Xây bảng ánh xạ vị trí SME ↔ occupation
Vì WORKBank dùng danh mục nghề nghiệp O*NET (104 nghề, khá chi tiết), nhóm cần tự xây bảng ánh xạ thủ công cho các vị trí SME phổ biến, ví dụ:

| Vị trí công việc trong SME | Occupation gần nhất (WORKBank/O*NET) |
|---|---|
| Kế toán | Accountants and Auditors |
| Chăm sóc khách hàng | Customer Service Representatives |
| Nhân sự | Human Resources Specialists |
| Marketing nội bộ | Marketing Specialists |
| Trợ lý hành chính | Secretaries and Administrative Assistants |
| Bán hàng | Retail Salespersons / Sales Representatives |

*(Nhóm bổ sung đủ 10–15 vị trí phổ biến theo 5–6 loại hình SME sẽ demo: kế toán dịch vụ, bán lẻ, agency marketing, phòng khám nhỏ, văn phòng luật nhỏ.)*

### Bước 3.4 — Tính chỉ số dẫn xuất

**Chuẩn hoá điểm về thang 0–1:**
```
D = (desire_score - min) / (max - min)        # mức mong muốn
C = (capability_score - min) / (max - min)    # mức năng lực công nghệ
```

**Priority Score (điểm ưu tiên đầu tư)** — công thức đề xuất, có thể chỉnh trọng số qua slider trên dashboard:
```
Priority = w1 * D + w2 * C
mặc định: w1 = 0.5, w2 = 0.5
```
> Ghi chú: nếu WORKBank/metadata có trường tần suất thực hiện tác vụ, bổ sung thêm trọng số `w3 * F` để phản ánh tác vụ càng lặp lại càng đáng đầu tư; nếu không có, ghi rõ giới hạn này trong báo cáo.

**Ước tính % thời gian tiết kiệm (giá trị minh hoạ, không phải số đo thực nghiệm):**
```
TimeSavingEstimate = C * K
K = hằng số quy đổi (ví dụ 40%), nêu rõ đây là giả định minh hoạ trong báo cáo
```

**Risk Flag (cờ rủi ro)** — 2 loại:
- *Rủi ro kỳ vọng vượt năng lực*: `D cao` (>0.7) và `C thấp` (<0.4) → dễ gây thất vọng nếu triển khai vội.
- *Rủi ro phản kháng nội bộ*: `C cao` (>0.7) và `D thấp` (<0.4) → cần truyền thông nội bộ trước khi tự động hoá.
- Gắn thêm nhãn thủ công "nhạy cảm cao" cho tác vụ thuộc nhóm tài chính/pháp lý/nhân sự nhạy cảm (dựa trên đọc mô tả tác vụ).

### Bước 3.5 — Lưu dữ liệu đã xử lý
- Xuất `tasks_scored.parquet` để dashboard load nhanh, tránh tính lại mỗi lần chạy.

---

## 4. Thiết kế chi tiết dashboard (Streamlit)

### Trang 1 — Chọn hồ sơ doanh nghiệp (`Home.py`)
- Input: dropdown chọn ngành SME, multi-select các vị trí công việc hiện có.
- Slider: trọng số `w1` (mong muốn) / `w2` (năng lực) để người dùng tự điều chỉnh khẩu vị rủi ro.
- Output: lưu lựa chọn vào `st.session_state` để các trang sau dùng chung.

### Trang 2 — Bảng khuyến nghị tác vụ
- Bảng (dataframe tương tác) xếp hạng tác vụ theo `Priority Score` giảm dần, cột: tác vụ, vị trí liên quan, D, C, Priority, % thời gian tiết kiệm ước tính.
- Bộ lọc: theo vị trí, theo ngưỡng Priority tối thiểu.
- Nút tải bảng dưới dạng CSV.

### Trang 3 — Biểu đồ tổng quan
- Scatter plot Plotly: trục X = Capability, trục Y = Desire, kích thước điểm = Priority Score, màu theo vị trí công việc.
- 4 góc phần tư được chú thích: "Nên thí điểm ngay", "Cần chuẩn bị truyền thông", "Cần chờ công nghệ", "Ưu tiên thấp".
- Tương tác: hover hiện tên tác vụ, click lọc bảng ở Trang 2 (tuỳ khả năng, nếu không kịp thì để hover là đủ).

### Trang 4 — Cảnh báo rủi ro
- Danh sách tác vụ bị gắn Risk Flag, kèm lý do (theo 2 loại đã định nghĩa ở Bước 3.4).
- Card tổng hợp: số lượng tác vụ rủi ro theo từng loại.

---

## 5. Kế hoạch theo tuần

### Tuần 1 — Chuẩn bị dữ liệu & môi trường
- [ ] Tạo repo Git, cấu trúc thư mục theo mục 2.
- [ ] Tải 3 file WORKBank, đọc Code Book, ghi chú tên cột chính xác.
- [ ] Viết `etl.py`: load + merge dữ liệu, kiểm tra chất lượng (thiếu/trùng).
- **Deliverable:** dữ liệu đã gộp ở dạng bảng sạch (`tasks_merged.parquet`).
- **Phụ trách:** Data Analyst.

### Tuần 2 — Ánh xạ & tính chỉ số
- [ ] Xây bảng ánh xạ vị trí SME ↔ occupation (10–15 vị trí, có giải thích căn cứ).
- [ ] Viết `scoring.py`: chuẩn hoá D, C; tính Priority Score, Risk Flag theo công thức mục 3.4.
- [ ] Xuất `tasks_scored.parquet`.
- **Deliverable:** dữ liệu đã tính điểm, sẵn sàng cho dashboard.
- **Phụ trách:** Data Analyst + 1 thành viên hỗ trợ ánh xạ nghiệp vụ.

### Tuần 3 — Dựng khung dashboard
- [ ] Dựng `Home.py`: input chọn ngành/vị trí + slider trọng số.
- [ ] Dựng Trang 2 (bảng khuyến nghị) với dữ liệu thật.
- [ ] Kết nối `session_state` giữa các trang.
- **Deliverable:** dashboard chạy được luồng chọn hồ sơ → xem bảng khuyến nghị.
- **Phụ trách:** Dashboard Developer.

### Tuần 4 — Biểu đồ & cảnh báo rủi ro
- [ ] Dựng Trang 3 (scatter plot 4 góc phần tư bằng Plotly).
- [ ] Dựng Trang 4 (danh sách cảnh báo rủi ro + card tổng hợp).
- [ ] Visualization & UX rà soát màu sắc, bố cục, khả năng đọc cho người không chuyên kỹ thuật.
- **Deliverable:** dashboard đầy đủ 4 trang, có thể demo end-to-end.
- **Phụ trách:** Dashboard Developer + Visualization & UX.

### Tuần 5 — Kiểm thử & tinh chỉnh
- [ ] Chạy thử với 3 kịch bản SME giả định (kế toán dịch vụ, bán lẻ, agency marketing).
- [ ] Ghi nhận điểm bất hợp lý (ví dụ: khuyến nghị không thực tế) → điều chỉnh công thức/ánh xạ.
- [ ] Kiểm tra hiệu năng tải dashboard, sửa lỗi giao diện.
- **Deliverable:** dashboard bản hoàn thiện, có ghi chú kết quả kiểm thử.
- **Phụ trách:** Cả nhóm.

### Tuần 6 — Báo cáo, slide & hoàn thiện nộp bài
- [ ] Viết báo cáo docx: mục tiêu, dữ liệu, phương pháp, biểu đồ, insight, khuyến nghị, giới hạn.
- [ ] Chuẩn bị slide 10–15 trang tóm tắt.
- [ ] Chụp ảnh màn hình / đóng gói file dashboard theo đúng yêu cầu nộp bài.
- [ ] Rà soát toàn bộ, nộp qua kênh quy định.
- **Deliverable:** bộ hồ sơ nộp đầy đủ (báo cáo + dashboard + slide).
- **Phụ trách:** Báo cáo & Trình bày (chủ trì), cả nhóm rà soát chéo.

---

## 6. Ma trận rủi ro dự án (không nhầm với Risk Flag trong dữ liệu)

| Rủi ro | Khả năng | Tác động | Phương án dự phòng |
|---|---|---|---|
| Không xác định được cột dữ liệu chính xác (thiếu đọc kỹ Code Book) | Trung bình | Cao | Dành riêng buổi đầu tuần 1 để cả nhóm cùng đọc Code Book, thống nhất tên cột trước khi code |
| Bảng ánh xạ SME ↔ occupation mang tính chủ quan | Cao | Trung bình | Ghi rõ căn cứ/giả định trong báo cáo, xin góp ý giảng viên sớm |
| Dashboard chậm khi tải dữ liệu | Thấp | Trung bình | Tiền xử lý và lưu Parquet, cache bằng `st.cache_data` |
| Trễ tiến độ do phân công không rõ | Trung bình | Cao | Họp ngắn cuối mỗi tuần để rà tiến độ theo bảng ở mục 5 |

---

## 7. Checklist nộp bài

- [ ] Báo cáo nhóm (.docx hoặc .pdf): mục tiêu, dữ liệu, biểu đồ, insight, đề xuất.
- [ ] File dashboard hoặc ảnh chụp dashboard theo đúng định dạng yêu cầu.
- [ ] Slide trình bày (10–15 trang).
- [ ] Nộp qua kênh duy nhất theo thông báo của Nhà trường.
