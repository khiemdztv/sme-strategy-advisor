"""
export_individual_charts.py — Exports high-resolution individual chart images (PNG, 300 DPI)
for embedded academic Word report generation.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set global matplotlib style matching BI Dashboard aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Segoe UI', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.edgecolor'] = '#E2E8F0'
plt.rcParams['axes.linewidth'] = 1.0

def export_all_charts(data_file="data/processed/tasks_scored.csv", output_dir="data/reports/charts"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_file)
    
    role_col = "sme_role" if "sme_role" in df.columns else "occupation"

    # ═══════════════════════════════════════════════════════════════
    # CHART 1: Diverging Gap Bar Chart (Mong muốn D - Năng lực C)
    # ═══════════════════════════════════════════════════════════════
    df_gap = df.copy()
    df_gap["gap"] = df_gap["norm_desire"] - df_gap["norm_capability"]
    gap_by_role = (df_gap.groupby(role_col)["gap"].mean() * 100).sort_values()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    colors = ['#EF4444' if v < 0 else '#10B981' for v in gap_by_role.values]
    bars = ax.barh(gap_by_role.index, gap_by_role.values, color=colors, height=0.65)
    
    ax.axvline(0, color='#94A3B8', linewidth=1.5, linestyle='-')
    ax.set_title("Khoảng Cách Kỳ Vọng (D) vs Năng Lực AI (C) Theo Vị Trí SME", fontsize=13, fontweight='bold', pad=15, color='#0F172A')
    ax.set_xlabel("Khoảng cách Gap (%) = Mong muốn (D) - Năng lực AI (C)", fontsize=10, fontweight='bold', color='#475569')
    ax.grid(axis='x', linestyle='--', alpha=0.4, color='#CBD5E1')
    
    for bar in bars:
        w = bar.get_width()
        offset = 1.5 if w >= 0 else -4.5
        ax.text(w + offset, bar.get_y() + bar.get_height()/2, f"{w:+.1f}%", 
                va='center', fontsize=9, fontweight='bold', color='#1E293B')

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "chart_1_gap_analysis.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print("Saved:", chart1_path)

    # ═══════════════════════════════════════════════════════════════
    # CHART 2: Strategic Quadrant Scatter Plot (C vs D)
    # ═══════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    
    color_map = {
        "🟢 Thí điểm Ngay": "#10B981",
        "🟡 Rủi ro Phản kháng Nội bộ": "#F59E0B",
        "🟠 Rủi ro Kỳ vọng vượt Năng lực": "#EF4444",
        "⚪ Ưu tiên Thấp": "#8B5CF6"
    }

    for flag, group in df.groupby("risk_flag"):
        c = color_map.get(flag, "#64748B")
        sizes = np.clip(group["roi_savings_usd"] / 1000 * 4, 30, 400)
        ax.scatter(group["norm_capability"], group["norm_desire"], s=sizes, color=c, alpha=0.7, edgecolors='white', linewidth=1, label=flag)

    ax.axvline(0.5, color='#94A3B8', linestyle='--', linewidth=1.2)
    ax.axhline(0.5, color='#94A3B8', linestyle='--', linewidth=1.2)
    
    # Add quadrant labels
    ax.text(0.75, 0.75, "🟢 THÍ ĐIỂM NGAY\n(Ideal Pilot)", fontsize=11, fontweight='bold', color='#065F46', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#A7F3D0'))
    ax.text(0.25, 0.75, "⚪ ƯU TIÊN THẤP\n(Low Priority)", fontsize=11, fontweight='bold', color='#5B21B6', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#F5F3FF', edgecolor='#DDD6FE'))
    ax.text(0.25, 0.25, "🟠 RỦI RO KỲ VỌNG\n(Over Expectation)", fontsize=11, fontweight='bold', color='#991B1B', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF2F2', edgecolor='#FCA5A5'))
    ax.text(0.75, 0.25, "🟡 PHẢN KHÁNG NỘI BỘ\n(Internal Resistance)", fontsize=11, fontweight='bold', color='#92400E', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFBEB', edgecolor='#FDE68A'))

    ax.set_title("Ma Trận 4 Góc Phần Tư Phân Loại Tác Vụ Chiến Lược", fontsize=13, fontweight='bold', pad=15, color='#0F172A')
    ax.set_xlabel("Năng Lực Công Nghệ AI (Capability - C)", fontsize=10, fontweight='bold', color='#475569')
    ax.set_ylabel("Mong Muốn Tự Động Hóa (Desire - D)", fontsize=10, fontweight='bold', color='#475569')
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "chart_2_strategic_quadrant.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print("Saved:", chart2_path)

    # ═══════════════════════════════════════════════════════════════
    # CHART 3: Worker Psychology Bubble Chart (Enjoyment vs Security)
    # ═══════════════════════════════════════════════════════════════
    psych_cols = ["worker_enjoyment_score", "worker_security_score", "worker_time_score"]
    if all(c in df.columns for c in psych_cols):
        df_psych = df.groupby(role_col).agg(
            avg_enjoyment=("worker_enjoyment_score", "mean"),
            avg_security=("worker_security_score", "mean"),
            avg_time=("worker_time_score", "mean")
        ).reset_index().dropna()

        fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
        sizes = df_psych["avg_time"] * 120
        scatter = ax.scatter(df_psych["avg_enjoyment"], df_psych["avg_security"], s=sizes, c=df_psych["avg_enjoyment"], cmap='Spectral', alpha=0.8, edgecolors='#334155', linewidth=1.5)

        med_x = df_psych["avg_enjoyment"].median()
        med_y = df_psych["avg_security"].median()
        ax.axvline(med_x, color='#94A3B8', linestyle='--', linewidth=1.2)
        ax.axhline(med_y, color='#94A3B8', linestyle='--', linewidth=1.2)

        for _, r in df_psych.iterrows():
            ax.text(r["avg_enjoyment"], r["avg_security"] + 0.06, r[role_col][:16], fontsize=8.5, fontweight='bold', color='#1E293B', ha='center')

        ax.text(med_x - 0.4, med_y - 0.4, "🟢 SẮN SÀNG\n(Thí điểm tối ưu)", fontsize=10, fontweight='bold', color='#065F46', ha='center', bbox=dict(boxstyle='round', facecolor='#ECFDF5', alpha=0.8))
        ax.text(med_x - 0.4, med_y + 0.4, "🔴 LO LẮNG\n(Sợ mất việc)", fontsize=10, fontweight='bold', color='#991B1B', ha='center', bbox=dict(boxstyle='round', facecolor='#FEF2F2', alpha=0.8))
        ax.text(med_x + 0.4, med_y + 0.4, "🟠 MÂU THUẪN\n(Thích + Lo lắng)", fontsize=10, fontweight='bold', color='#92400E', ha='center', bbox=dict(boxstyle='round', facecolor='#FFFBEB', alpha=0.8))
        ax.text(med_x + 0.4, med_y - 0.4, "🔵 GẮN BÓ\n(Chống đối cao)", fontsize=10, fontweight='bold', color='#1E40AF', ha='center', bbox=dict(boxstyle='round', facecolor='#EFF6FF', alpha=0.8))

        ax.set_title("Bản Đồ Phân Tích Tâm Lý Nhân Viên (4 Vùng Cảm Xúc)", fontsize=13, fontweight='bold', pad=15, color='#0F172A')
        ax.set_xlabel("Mức Độ Yêu Thích Công Việc (Enjoyment Score)", fontsize=10, fontweight='bold', color='#475569')
        ax.set_ylabel("Mức Độ Lo Ngại An Toàn (Security Score)", fontsize=10, fontweight='bold', color='#475569')
        ax.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        chart3_path = os.path.join(output_dir, "chart_3_worker_psychology.png")
        plt.savefig(chart3_path, dpi=300)
        plt.close()
        print("Saved:", chart3_path)

    # ═══════════════════════════════════════════════════════════════
    # CHART 4: Top 10 ROI Tasks Bar Chart
    # ═══════════════════════════════════════════════════════════════
    df_top_roi = df.sort_values("roi_savings_usd", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    task_labels = [t[:45] + "…" for t in df_top_roi["task_statement"]]
    bars = ax.barh(task_labels[::-1], (df_top_roi["roi_savings_usd"] / 1000)[::-1], color='#2563EB', height=0.6)
    
    ax.set_title("Top 10 Tác Vụ Đem Lại Giá Trị ROI Tiết Kiệm Chi Phí Cao Nhất ($/năm)", fontsize=12, fontweight='bold', pad=15, color='#0F172A')
    ax.set_xlabel("Giá trị ROI ước tính (Nghìn USD / năm)", fontsize=10, fontweight='bold', color='#475569')
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1, bar.get_y() + bar.get_height()/2, f"${w:,.1f}K", va='center', fontsize=9, fontweight='bold', color='#1E293B')

    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "chart_4_top_roi_tasks.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print("Saved:", chart4_path)

    # ═══════════════════════════════════════════════════════════════
    # CHART 5: Priority Score Distribution Histogram
    # ═══════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    n_counts, bins, patches = ax.hist(df["priority_score"], bins=20, color='#8B5CF6', edgecolor='white', alpha=0.85)
    
    ax.axvline(df["priority_score"].mean(), color='#EF4444', linestyle='--', linewidth=2, label=f'Trung bình: {df["priority_score"].mean():.1f}đ')
    ax.set_title("Phân Bố Mật Độ Điểm Ưu Tiên Chiến Lược (Priority Score Distribution)", fontsize=12, fontweight='bold', pad=15, color='#0F172A')
    ax.set_xlabel("Điểm Ưu Tiên Chiến Lược P (0 - 100 điểm)", fontsize=10, fontweight='bold', color='#475569')
    ax.set_ylabel("Số lượng tác vụ", fontsize=10, fontweight='bold', color='#475569')
    ax.legend(loc='upper right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "chart_5_priority_distribution.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print("Saved:", chart5_path)

if __name__ == "__main__":
    export_all_charts()
