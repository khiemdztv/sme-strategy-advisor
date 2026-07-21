import pandas as pd
import os
import ast


def _parse_skill_list(val):
    """Parse skill column from string like "['A', 'B']" to a Python list."""
    if pd.isna(val) or not isinstance(val, str):
        return []
    val = val.strip()
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list):
            return [s.strip() for s in parsed if isinstance(s, str) and s.strip()]
        return [str(parsed).strip()]
    except (ValueError, SyntaxError):
        cleaned = val.strip("[]'\"")
        if cleaned:
            return [s.strip().strip("'\"") for s in cleaned.split(",") if s.strip()]
        return []


# Short reason column names for easier downstream use
REASON_RENAME = {
    "Reasons for Automation Desire - Free Time": "reason_auto_free_time",
    "Reasons for Automation Desire - Repetitive": "reason_auto_repetitive",
    "Reasons for Automation Desire - Human Error": "reason_auto_human_error",
    "Reasons for Automation Desire - Stress": "reason_auto_stress",
    "Reasons for Automation Desire - Difficulty": "reason_auto_difficulty",
    "Reasons for Automation Desire - Scale": "reason_auto_scale",
    "Reasons for Human Agency - Physical": "reason_human_physical",
    "Reasons for Human Agency - Control": "reason_human_control",
    "Reasons for Human Agency - Domain Knowledge": "reason_human_domain",
    "Reasons for Human Agency - Empathy": "reason_human_empathy",
    "Reasons for Human Agency - Quality Oversight": "reason_human_quality",
    "Reasons for Human Agency - Dynamic": "reason_human_dynamic",
    "Reasons for Human Agency - Ethical": "reason_human_ethical",
}

# Human-readable labels for Vietnamese UI
REASON_LABELS_VI = {
    "reason_auto_free_time": "Tiết kiệm thời gian rảnh",
    "reason_auto_repetitive": "Tính chất lặp đi lặp lại",
    "reason_auto_human_error": "Tránh lỗi sai con người",
    "reason_auto_stress": "Giảm bớt căng thẳng",
    "reason_auto_difficulty": "Giảm độ khó công việc",
    "reason_auto_scale": "Xử lý quy mô dữ liệu lớn",
    "reason_human_physical": "Yêu cầu thao tác vật lý",
    "reason_human_control": "Nhu cầu kiểm soát",
    "reason_human_domain": "Kiến thức chuyên môn sâu",
    "reason_human_empathy": "Sự thấu cảm con người",
    "reason_human_quality": "Giám sát chất lượng",
    "reason_human_dynamic": "Tình huống linh hoạt",
    "reason_human_ethical": "Ràng buộc đạo đức",
}

AUTO_REASONS = [k for k in REASON_LABELS_VI if k.startswith("reason_auto_")]
HUMAN_REASONS = [k for k in REASON_LABELS_VI if k.startswith("reason_human_")]


def load_and_merge_raw_data(raw_dir="data/raw"):
    """
    Reads raw CSV files from WORKBank dataset and merges them on Task ID.
    """
    worker_file = os.path.join(raw_dir, "domain_worker_desires.csv")
    expert_file = os.path.join(raw_dir, "expert_rated_technological_capability.csv")
    meta_file = os.path.join(raw_dir, "task_statement_with_metadata.csv")

    if not (os.path.exists(worker_file) and os.path.exists(expert_file) and os.path.exists(meta_file)):
        raise FileNotFoundError("One or more raw WORKBank CSV files missing in " + raw_dir)

    # 1. Read metadata
    df_meta = pd.read_csv(meta_file)
    df_meta["Task ID"] = df_meta["Task ID"].astype(str)

    # 2. Read worker desires and aggregate
    df_worker = pd.read_csv(worker_file)
    df_worker["Task ID"] = df_worker["Task ID"].astype(str)

    worker_agg_cols = {
        "Automation Desire Rating": "worker_desire_score",
        "Time": "worker_time_score",
        "Core Skill Rating": "worker_skill_score",
        "Job Security Rating": "worker_security_score",
        "Enjoyment Rating": "worker_enjoyment_score"
    }

    df_worker_agg = df_worker.groupby("Task ID").agg({
        col: "mean" for col in worker_agg_cols.keys() if col in df_worker.columns
    }).rename(columns=worker_agg_cols).reset_index()

    # Calculate boolean reason percentages if available
    reason_cols = [c for c in df_worker.columns if "Reasons for" in c]
    if reason_cols:
        for c in reason_cols:
            df_worker[c] = df_worker[c].astype(str).str.lower().isin(["true", "1", "yes"])
        df_reasons = df_worker.groupby("Task ID")[reason_cols].mean() * 100
        df_worker_agg = df_worker_agg.merge(df_reasons, on="Task ID", how="left")

    # 3. Read expert capability and aggregate
    df_expert = pd.read_csv(expert_file)
    df_expert["Task ID"] = df_expert["Task ID"].astype(str)

    expert_agg_cols = {
        "Automation Capacity Rating": "capability_score",
        "Physical Action Requirement": "expert_physical_score",
        "Involved Uncertainty": "expert_uncertainty_score",
        "Domain Expertise Requirement": "expert_domain_score",
        "Interpersonal Communication Requirement": "expert_interpersonal_score",
        "Human Agency Scale Rating": "expert_agency_score"
    }

    df_expert_agg = df_expert.groupby("Task ID").agg({
        col: "mean" for col in expert_agg_cols.keys() if col in df_expert.columns
    }).rename(columns=expert_agg_cols).reset_index()

    # 4. Merge all into master dataframe
    df_merged = df_meta.merge(df_worker_agg, on="Task ID", how="left")
    df_merged = df_merged.merge(df_expert_agg, on="Task ID", how="left")

    # Rename columns for clarity
    rename_map = {
        "Occupation (O*NET-SOC Title)": "occupation",
        "Task": "task_statement",
        "Task Type": "task_type",
        "Occupation Mean Annual Wage": "annual_wage",
        "Occupation Employment": "employment",
    }
    # Add reason renames for any present columns
    for old_name, new_name in REASON_RENAME.items():
        if old_name in df_merged.columns:
            rename_map[old_name] = new_name

    df_merged.rename(columns=rename_map, inplace=True)

    # Parse Skill column
    skill_raw_col = None
    for candidate in ["Skill (O*NET Work Activity)", "Skill"]:
        if candidate in df_merged.columns:
            skill_raw_col = candidate
            break

    if skill_raw_col:
        df_merged["skill_list"] = df_merged[skill_raw_col].apply(_parse_skill_list)
        # Keep first skill as primary for non-exploded views
        df_merged["skill_primary"] = df_merged["skill_list"].apply(
            lambda lst: lst[0] if lst else "Unknown"
        )
    else:
        df_merged["skill_list"] = [[] for _ in range(len(df_merged))]
        df_merged["skill_primary"] = "Unknown"

    # Coerce numeric values
    numeric_fields = ["worker_desire_score", "capability_score", "annual_wage", "employment"]
    for field in numeric_fields:
        if field in df_merged.columns:
            df_merged[field] = pd.to_numeric(df_merged[field], errors="coerce")

    return df_merged


if __name__ == '__main__':
    df = load_and_merge_raw_data()
    print(f"ETL completed: {len(df)} merged tasks.")
    print(f"Columns: {list(df.columns)}")
    print(f"Skill primary sample: {df['skill_primary'].value_counts().head(5).to_dict()}")
