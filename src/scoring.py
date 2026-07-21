import pandas as pd
import numpy as np


def calculate_scores_and_flags(df, w1=0.5, w2=0.5, sme_size_factor=1.0, **kwargs):
    """
    Calculates normalised D/C, Priority Score, ROI estimate, Technical Complexity,
    Risk Flags (using original plan thresholds D>0.7/C<0.4), and recommended
    AI Agent architecture.
    """
    df = df.copy()

    min_d, max_d = 1.0, 5.0
    min_c, max_c = 1.0, 5.0

    # --- Normalise D and C to [0, 1] ---
    df["norm_desire"] = (df["worker_desire_score"] - min_d) / (max_d - min_d)
    df["norm_capability"] = (df["capability_score"] - min_c) / (max_c - min_c)
    df["norm_desire"] = df["norm_desire"].fillna(0.5).clip(0, 1)
    df["norm_capability"] = df["norm_capability"].fillna(0.5).clip(0, 1)

    # --- Priority Score (0 – 100) ---
    df["priority_score"] = (w1 * df["norm_desire"] + w2 * df["norm_capability"]) * 100

    # --- Estimated Time Saving (%, max 40%) ---
    df["time_saving_pct"] = df["norm_capability"] * 40.0

    # --- Economic ROI Savings ($ per year) ---
    wage_median = df["annual_wage"].median()
    if pd.isna(wage_median):
        wage_median = 65000
    wage_clean = df["annual_wage"].fillna(wage_median)
    df["roi_savings_usd"] = wage_clean * df["norm_capability"] * 0.20 * sme_size_factor

    # --- Technical Complexity Score (0 – 10) ---
    phys = df.get("expert_physical_score", pd.Series(2.0, index=df.index)).fillna(2.0)
    unc = df.get("expert_uncertainty_score", pd.Series(2.5, index=df.index)).fillna(2.5)
    dom = df.get("expert_domain_score", pd.Series(3.0, index=df.index)).fillna(3.0)
    df["technical_complexity"] = ((phys * 0.3 + unc * 0.35 + dom * 0.35) / 5.0) * 10.0

    # ------------------------------------------------------------------
    # Risk Flag — using ORIGINAL PLAN thresholds:
    #   Expectation risk:    D > 0.7  AND  C < 0.4
    #   Internal resistance: C > 0.7  AND  D < 0.4
    #   Ideal pilot:         D >= 0.5 AND  C >= 0.5  (and not in risk zones)
    #   Low priority:        everything else
    # ------------------------------------------------------------------
    def _categorise(row):
        d, c = row["norm_desire"], row["norm_capability"]
        if d > 0.7 and c < 0.4:
            return pd.Series([
                "risk_expectation",
                "🟠 Rủi ro Kỳ vọng vượt Năng lực",
                "RAG Agent (Truy xuất tri thức)",
                "Dùng mô hình RAG hỗ trợ tra cứu; không hứa hẹn thay thế hoàn toàn."
            ])
        if c > 0.7 and d < 0.4:
            return pd.Series([
                "risk_resistance",
                "🟡 Rủi ro Phản kháng Nội bộ",
                "Copilot (Trợ lý đồng hành)",
                "Triển khai Copilot gợi ý; giữ quyền phê duyệt cho nhân sự."
            ])
        if d >= 0.5 and c >= 0.5:
            return pd.Series([
                "ideal_pilot",
                "🟢 Thí điểm Ngay",
                "Full Automation Agent",
                "Kết nối API nghiệp vụ, tự động hóa quy trình end-to-end."
            ])
        return pd.Series([
            "low_priority",
            "⚪ Ưu tiên Thấp",
            "Chưa ưu tiên",
            "Duy trì quy trình thủ công; theo dõi tiến bộ công nghệ."
        ])

    df[["risk_category", "risk_flag", "recommended_architecture", "implementation_step"]] = \
        df.apply(_categorise, axis=1)

    # --- Sensitive task flag ---
    _sensitive = ["audit", "financial", "credit", "legal", "payroll",
                  "confidential", "compliance", "medical", "tax"]

    def _check_sensitive(task):
        if not isinstance(task, str):
            return False
        t = task.lower()
        return any(k in t for k in _sensitive)

    df["is_sensitive"] = df["task_statement"].apply(_check_sensitive)

    return df
