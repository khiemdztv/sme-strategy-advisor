"""
insights.py — Dynamic 3-part Report-Ready Insight Generation.
Generates for each chart:
1. Proof Text   (Bằng chứng số liệu - Formatted with clear line breaks per group)
2. Cause Text   (Giải thích nguyên nhân cốt lõi)
3. Report Excerpt (Đoạn văn mẫu trích xuất cho Báo cáo / Slide)
"""
import pandas as pd


def _pct(n, total):
    if total == 0:
        return 0
    return round(n / total * 100, 1)


def _fmt_usd(v):
    return f"${v:,.0f}"


# ═══════════════════════════════════════════════════════════════
# HOME — Executive Summary
# ═══════════════════════════════════════════════════════════════

def executive_summary(df, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ["Chưa có dữ liệu phù hợp. Hãy chọn ít nhất 1 vị trí SME."]

    total = len(df)
    pilot = len(df[df["risk_category"] == "ideal_pilot"])
    resist = len(df[df["risk_category"] == "risk_resistance"])
    expect = len(df[df["risk_category"] == "risk_expectation"])
    sensitive = df["is_sensitive"].sum()

    avg_d = df["norm_desire"].mean() * 100
    avg_c = df["norm_capability"].mean() * 100
    total_roi = df["roi_savings_usd"].sum()

    role_col = "sme_role" if "sme_role" in df.columns else "occupation"
    top_role = df.groupby(role_col)["roi_savings_usd"].sum().idxmax() if role_col in df.columns else "N/A"
    top_role_roi = df.groupby(role_col)["roi_savings_usd"].sum().max() if role_col in df.columns else 0

    bullets = [
        f"**Phạm vi Case Study ngành [{category_name}]**: Tổng số **{total} tác vụ** được phân tích chi tiết định lượng.",
        f"**Mức độ khả thi công nghệ & ủng hộ**: Điểm năng lực công nghệ trung bình đạt **{avg_c:.1f}%**, mức sẵn sàng người lao động đạt **{avg_d:.1f}%**.",
        f"**Tác vụ thí điểm khả thi nhất**: Có **{pilot} tác vụ ({_pct(pilot, total)}%)** thuộc nhóm 🟢 **Thí điểm ngay**, hứa hẹn thu hồi **{_fmt_usd(total_roi)}/năm** cho doanh nghiệp.",
        f"**Vị trí trọng điểm đóng góp ROI lớn nhất**: Vị trí **{top_role}** đóng góp **{_fmt_usd(top_role_roi)}/năm**.",
        f"**Quản trị rủi ro & Bảo mật**: Ghi nhận **{resist} tác vụ rủi ro phản kháng nội bộ** và **{int(sensitive)} tác vụ chứa từ khóa nhạy cảm** cần áp dụng quy chế phê duyệt giám sát (Human Approval Loop)."
    ]
    return bullets


# ═══════════════════════════════════════════════════════════════
# HOME — Gap Analysis  (D − C  by role)
# ═══════════════════════════════════════════════════════════════

def gap_insight(df, role_col, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    df = df.copy()
    df["gap"] = df["norm_desire"] - df["norm_capability"]
    gap_by_role = df.groupby(role_col)["gap"].mean().sort_values()

    n_resist = int((gap_by_role < -0.05).sum())
    n_expect = int((gap_by_role > 0.05).sum())

    most_resist = gap_by_role.index[0]
    most_resist_val = gap_by_role.iloc[0]
    most_expect = gap_by_role.index[-1]
    most_expect_val = gap_by_role.iloc[-1]

    proof = (
        f"Phân tích khoảng cách D−C cho ngành **{category_name}**:<br>"
        f"• **Vị trí Gap âm (AI sẵn sàng nhưng NV chưa muốn)**: **{n_resist} vị trí** (lớn nhất là **{most_resist}** với gap = **{most_resist_val:+.2f}**)<br>"
        f"• **Vị trí Gap dương (NV muốn nhưng AI chưa đủ giỏi)**: **{n_expect} vị trí** (lớn nhất là **{most_expect}** với gap = **{most_expect_val:+.2f}**)"
    )

    cause = (
        f"Vị trí {most_resist} có gap âm lớn nhất do tính chất công việc đòi hỏi sự kiểm soát "
        f"và trách nhiệm cá nhân cao, khiến nhân viên e ngại dù công nghệ đã sẵn sàng. "
        f"Ngược lại, vị trí {most_expect} có gap dương lớn nhất do áp lực thời gian và khối lượng "
        f"công việc lặp lại cao, thúc đẩy mong muốn tự động hóa vượt xa năng lực AI hiện tại."
    )

    report = (
        f"Biểu đồ khoảng cách D−C chỉ ra chiến lược triển khai phân hóa cho ngành {category_name}: "
        f"Với các vị trí gap âm (đặc biệt {most_resist}), ưu tiên chiến dịch truyền thông nội bộ "
        f"và thí điểm Copilot đồng hành. Với các vị trí gap dương (đặc biệt {most_expect}), "
        f"cần quản lý kỳ vọng và triển khai RAG Agent hỗ trợ từng bước thay vì hứa hẹn thay thế hoàn toàn."
    )

    return proof, cause, report


# ═══════════════════════════════════════════════════════════════
# PAGE 1 — Quadrant Strategic Map  (D vs C)
# ═══════════════════════════════════════════════════════════════

def quadrant_insight(df, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    pilot = df[df["risk_category"] == "ideal_pilot"]
    resist = df[df["risk_category"] == "risk_resistance"]
    expect = df[df["risk_category"] == "risk_expectation"]
    low = df[df["risk_category"] == "low_priority"]
    total = len(df)

    pilot_roi = pilot["roi_savings_usd"].sum()
    resist_roi = resist["roi_savings_usd"].sum()

    proof = (
        f"Trong tổng số {total} tác vụ thuộc ngành **{category_name}**:<br>"
        f"• **Nhóm 🟢 Thí điểm Ngay**: chiếm **{_pct(len(pilot), total)}%** ({len(pilot)} tác vụ, ROI ước tính {_fmt_usd(pilot_roi)}/năm)<br>"
        f"• **Nhóm 🟡 Phản kháng Nội bộ**: chiếm **{_pct(len(resist), total)}%** ({len(resist)} tác vụ, ROI {_fmt_usd(resist_roi)}/năm)<br>"
        f"• **Nhóm 🟠 Kỳ vọng vượt Năng lực**: chiếm **{_pct(len(expect), total)}%** ({len(expect)} tác vụ)<br>"
        f"• **Nhóm ⚪ Ưu tiên Thấp**: chiếm **{_pct(len(low), total)}%** ({len(low)} tác vụ)"
    )

    cause = (
        f"Sự tập trung lớn ở vùng 🟢 Thí điểm Ngay phản ánh công nghệ LLM và AI Agent hiện tại "
        f"đã đạt độ chín rất cao trong việc xử lý các tác vụ số hóa văn bản, tra cứu dữ liệu và "
        f"lập báo cáo. Tuy nhiên, các tác vụ nằm ở vùng 🟡 Phản kháng chịu ảnh hưởng từ tâm lý "
        f"lo ngại về tính an toàn bảo mật và nỗi sợ bị thay thế công việc của nhân sự nghiệp vụ."
    )

    report = (
        f"Kết quả phân tích ma trận 4 góc phần tư cho ngành {category_name} chỉ ra chiến lược "
        f"phân bổ nguồn lực tối ưu: Doanh nghiệp SME cần ưu tiên triển khai ngay {len(pilot)} "
        f"tác vụ vùng Thí điểm Ngay để thu hồi vốn {_fmt_usd(pilot_roi)}/năm. Đồng thời đối với "
        f"{len(resist)} tác vụ vùng Phản kháng, cần triển khai kịch bản Copilot đóng vai trò "
        f"Trợ lý đồng hành nhằm giảm thiểu sự chống đối từ nội bộ."
    )

    return proof, cause, report


# ═══════════════════════════════════════════════════════════════
# PAGE 2 — Worker Psychology Bubble  (Enjoyment × Security)
# ═══════════════════════════════════════════════════════════════

def worker_psychology_insight(df, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    cols_needed = ["worker_enjoyment_score", "worker_security_score"]
    if not all(c in df.columns for c in cols_needed):
        return ("Thiếu dữ liệu tâm lý.", "Thiếu dữ liệu tâm lý.", "Thiếu dữ liệu tâm lý.")

    med_enjoy = df["worker_enjoyment_score"].median()
    med_security = df["worker_security_score"].median()
    total = len(df)

    q_ready = df[(df["worker_enjoyment_score"] <= med_enjoy) & (df["worker_security_score"] <= med_security)]
    q_worry = df[(df["worker_enjoyment_score"] <= med_enjoy) & (df["worker_security_score"] > med_security)]
    q_conflict = df[(df["worker_enjoyment_score"] > med_enjoy) & (df["worker_security_score"] > med_security)]
    q_attach = df[(df["worker_enjoyment_score"] > med_enjoy) & (df["worker_security_score"] <= med_security)]

    proof = (
        f"Phân tích tâm lý {total} tác vụ ngành **{category_name}**:<br>"
        f"• **Nhóm 'Sẵn sàng'**: **{_pct(len(q_ready), total)}%** (không thích + không lo mất việc)<br>"
        f"• **Nhóm 'Lo lắng'**: **{_pct(len(q_worry), total)}%** (không thích + lo mất việc)<br>"
        f"• **Nhóm 'Mâu thuẫn'**: **{_pct(len(q_conflict), total)}%** (thích + lo mất việc)<br>"
        f"• **Nhóm 'Gắn bó'**: **{_pct(len(q_attach), total)}%** (thích + không lo → sẽ phản kháng)"
    )

    cause = (
        f"Nhóm 'Sẵn sàng' ({_pct(len(q_ready), total)}%) đại diện cho các tác vụ hành chính lặp lại "
        f"mà nhân viên không có gắn kết cảm xúc — đây là mục tiêu thí điểm AI tối ưu nhất. "
        f"Nhóm 'Gắn bó' ({_pct(len(q_attach), total)}%) đáng lo ngại nhất vì nhân viên yêu thích "
        f"công việc và không lo mất việc, nên sẽ chống đối mạnh nhất khi bị 'tước' task yêu thích."
    )

    report = (
        f"Bản đồ tâm lý nhân viên ngành {category_name} chỉ ra 4 nhóm tác vụ đòi hỏi 4 chiến lược "
        f"tiếp cận khác nhau: Triển khai ngay với nhóm 'Sẵn sàng', cam kết không sa thải với nhóm "
        f"'Lo lắng', đối thoại trực tiếp với nhóm 'Mâu thuẫn', và tuyệt đối không ép buộc nhóm "
        f"'Gắn bó' mà nên để AI đóng vai trò hỗ trợ bổ sung."
    )

    return proof, cause, report


# ═══════════════════════════════════════════════════════════════
# PAGE 2 — Butterfly  (Auto Reasons vs Human Reasons)
# ═══════════════════════════════════════════════════════════════

def butterfly_insight(df, auto_cols, human_cols, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    auto_means = df[auto_cols].mean().sort_values(ascending=False)
    human_means = df[human_cols].mean().sort_values(ascending=False)

    top_auto = auto_means.index[0] if len(auto_means) > 0 else "N/A"
    top_auto_val = auto_means.iloc[0] if len(auto_means) > 0 else 0
    top_human = human_means.index[0] if len(human_means) > 0 else "N/A"
    top_human_val = human_means.iloc[0] if len(human_means) > 0 else 0

    proof = (
        f"Đối chiếu động lực vs rào cản nhân sự:<br>"
        f"• **Động lực tự động hóa lớn nhất**: **'{top_auto}'** với **{top_auto_val:.1f}%** sự đồng thuận.<br>"
        f"• **Rào cản/yêu cầu con người lớn nhất**: **'{top_human}'** đạt **{top_human_val:.1f}%** sự đồng thuận."
    )

    cause = (
        f"Nhân sự trong ngành {category_name} mong muốn giải phóng bản thân khỏi áp lực thời gian "
        f"và sự lặp lại thủ công. Tuy nhiên, họ vẫn giữ sự cẩn trọng đối với yếu tố chuyên môn "
        f"và trách nhiệm giải trình (Accountability) mà máy móc chưa thể chịu trách nhiệm pháp lý."
    )

    report = (
        f"Phân tích tâm lý học tổ chức cho thấy thông điệp truyền thông nội bộ hiệu quả nhất cho "
        f"ngành {category_name} là: 'AI Agent giúp tạo thêm thời gian rảnh và loại bỏ sai sót thủ "
        f"công', kết hợp với việc thiết lập quy trình kiểm soát chất lượng con người để giải tỏa "
        f"rào cản '{top_human}'."
    )

    return proof, cause, report


# ═══════════════════════════════════════════════════════════════
# PAGE 3 — Heatmap  (Reasons × Roles)
# ═══════════════════════════════════════════════════════════════

def heatmap_insight(df, reason_cols, role_col, category_name="Tất cả lĩnh vực"):
    if df.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    grouped = df.groupby(role_col)[reason_cols].mean()
    if grouped.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    max_val = grouped.max().max()
    max_reason = grouped.max().idxmax()
    max_role = grouped[max_reason].idxmax()

    proof = (
        f"Ma trận phân bố lý do theo vị trí:<br>"
        f"• **Vị trí thể hiện rõ nhất**: Vị trí **{max_role}** tập trung đậm nét nhất ở lý do **'{max_reason}'** với tỷ lệ đạt **{max_val:.1f}%**."
    )

    cause = (
        f"Sự khác biệt giữa các vị trí xuất phát từ bản chất đặc thù nghiệp vụ. Các vị trí "
        f"chuyên môn sâu đòi hỏi sự thấu cảm hay thẩm định chất lượng cao hơn hẳn so với "
        f"các vị trí thuần túy xử lý tác vụ hành chính."
    )

    report = (
        f"Dữ liệu Heatmap lý do cung cấp cơ sở để thiết kế ma trận truyền thông phân hóa "
        f"theo vị trí trong ngành {category_name}. Các chính sách đào tạo và áp dụng công nghệ "
        f"cần được tùy chỉnh riêng cho từng nhóm vai trò thay vì áp dụng một công thức "
        f"chung toàn công ty."
    )

    return proof, cause, report


# ═══════════════════════════════════════════════════════════════
# PAGE 3 — Cross-Industry Comparison
# ═══════════════════════════════════════════════════════════════

def cross_industry_insight(df_cross):
    """Expects a DataFrame already merged with sme_category + gap column."""
    if df_cross.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    industry_stats = df_cross.groupby("sme_category").agg(
        total_tasks=("task_statement", "count"),
        pct_pilot=("risk_category", lambda x: (x == "ideal_pilot").sum() / len(x) * 100),
    ).sort_values("pct_pilot", ascending=False)

    if industry_stats.empty:
        return ("Chưa có dữ liệu.", "Chưa có dữ liệu.", "Chưa có dữ liệu.")

    best = industry_stats.index[0]
    best_pct = industry_stats.iloc[0]["pct_pilot"]
    worst = industry_stats.index[-1]
    worst_pct = industry_stats.iloc[-1]["pct_pilot"]

    proof = (
        f"So sánh chỉ số sẵn sàng giữa {len(industry_stats)} ngành SME:<br>"
        f"• **Ngành dẫn đầu**: Ngành **{best}** có tỷ lệ thí điểm cao nhất đạt **{best_pct:.1f}%**.<br>"
        f"• **Ngành rủi ro nhất**: Ngành **{worst}** đạt **{worst_pct:.1f}%**."
    )

    cause = (
        f"Ngành {best} dẫn đầu nhờ tập trung nhiều tác vụ hành chính có quy tắc rõ ràng "
        f"và khối lượng xử lý tài liệu lớn — vốn là thế mạnh cốt lõi của AI Agent hiện tại. "
        f"Ngành {worst} tụt hạng do yêu cầu chuyên môn sâu và trách nhiệm pháp lý cao "
        f"trong phần lớn tác vụ."
    )

    report = (
        f"Bản đồ so sánh liên ngành khuyến nghị doanh nghiệp SME đa ngành ưu tiên triển "
        f"khai AI Agent tại bộ phận {best} trước, tạo case study thành công làm đòn bẩy "
        f"mở rộng sang các ngành còn lại theo lộ trình từ dễ đến khó."
    )

    return proof, cause, report
