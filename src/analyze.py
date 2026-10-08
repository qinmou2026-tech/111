"""读取模拟经济数据并计算简单指标；仅使用 Python 标准库。"""

import csv
from pathlib import Path
from statistics import mean


def main():
    # 从脚本位置定位数据，因此不依赖终端当前所在的目录。
    data_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_economy.csv"
    with data_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("数据文件至少需要一行记录。")

    incomes = []
    consumptions = []
    consumption_shares = []
    real_incomes = []

    for row in rows:
        income = float(row["income"])
        consumption = float(row["consumption"])
        cpi = float(row["cpi"])
        if income <= 0 or cpi <= 0 or consumption < 0:
            raise ValueError("收入和 CPI 必须大于零，消费不能为负。")
        incomes.append(income)
        consumptions.append(consumption)
        consumption_shares.append(consumption / income)
        # CPI 使用同一个固定基期，基期 = 100。
        real_incomes.append(income / (cpi / 100))

    print(f"模拟数据：{len(rows)} 期（{rows[0]['month']} 至 {rows[-1]['month']}）")
    print(f"平均名义收入：{mean(incomes):.2f} 元/月")
    print(f"平均消费：{mean(consumptions):.2f} 元/月")
    print(f"各期消费占收入比例的平均值：{mean(consumption_shares):.2%}")
    print(f"平均实际收入（基期价格）：{mean(real_incomes):.2f} 元/月")


if __name__ == "__main__":
    main()
