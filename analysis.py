# Retail Sales Analytics - EDA Script
# Usage: python src/analysis.py
# Outputs cleaned dataset and charts into /data/processed and /reports

import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def main():
    data_path = os.path.join(BASE_DIR, "data", "raw", "retail_sales.csv")
    df = pd.read_csv(data_path, parse_dates=["order_date"])

    # Basic cleaning
    df = df.dropna()
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

    # Save processed
    processed_path = os.path.join(BASE_DIR, "data", "processed", "retail_sales_processed.csv")
    df.to_csv(processed_path, index=False)

    # KPIs
    kpis = {}
    kpis["Total Sales"] = float(df["sales"].sum())
    kpis["Total Profit"] = float(df["profit"].sum())
    kpis["Total Orders"] = int(df["order_id"].nunique())
    kpis["Avg Order Value (AOV)"] = float(df.groupby("order_id")["sales"].sum().mean())
    kpis["Profit Margin (%)"] = float((df["profit"].sum() / df["sales"].sum()) * 100)

    # Save KPI summary
    kpi_lines = ["# KPI Summary\n"]
    for k, v in kpis.items():
        if isinstance(v, float):
            kpi_lines.append(f"- {k}: {v:,.2f}")
        else:
            kpi_lines.append(f"- {k}: {v:,.0f}")
    with open(os.path.join(BASE_DIR, "reports", "kpi_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(kpi_lines))

    # Charts (matplotlib, default colors)
    # 1) Monthly Sales Trend
    ms = df.groupby("month")["sales"].sum().reset_index()
    plt.figure()
    plt.plot(ms["month"], ms["sales"])
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "reports", "monthly_sales_trend.png"))
    plt.close()

    # 2) Sales by Category
    sc = df.groupby("category")["sales"].sum().sort_values(ascending=False)
    plt.figure()
    sc.plot(kind="bar")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "reports", "sales_by_category.png"))
    plt.close()

    # 3) Sales by Region
    sr = df.groupby("region")["sales"].sum().sort_values(ascending=False)
    plt.figure()
    sr.plot(kind="bar")
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "reports", "sales_by_region.png"))
    plt.close()

if __name__ == "__main__":
    main()
