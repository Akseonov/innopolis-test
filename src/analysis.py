import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import SAMPLE_PATH, FIGURES_DIR
from load_data import load_data

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

def iqr_outliers(s: pd.Series):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers_count = int(((s < lower_bound) | (s > upper_bound)).sum())
    return lower_bound, upper_bound, outliers_count

def z_score_outliers(s: pd.Series):
    s_mean = s.mean()
    s_std = s.std()
    lower_bound = s_mean - 3 * s_std
    upper_bound = s_mean + 3 * s_std
    outliers_count = int(((s.dropna() < lower_bound) | (s.dropna() > upper_bound)).sum())
    return lower_bound, upper_bound, outliers_count

def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    df = load_data(SAMPLE_PATH)

    # 1. Выведите описательную статистику для датасета
    print("!!!!! 1 !!!!!")
    print(df.describe().T.round(2))

    # 2. Постройте гистограммы для трех колонок, которые, на ваш взгляд,
    # могут содержать полезную информацию. Выясните, есть ли в этих
    # колонках выбросы и аномалии (значения, которые сильно отличаются
    # от остальных значений или кажутся странными/некорректными).
    print("!!!!! 2 !!!!!")
    hist_cols = ["age", "total_assets", "net_profit"] # возраст компании, баланс по 1 и 2 разделам и чистая прибыль
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

    # Гистограмма Возраста
    sns.histplot(data=df, x=hist_cols[0], kde=True, ax=axes[0], color='skyblue', edgecolor='black')
    axes[0].set_title(f'Гистограмма: {hist_cols[0]}')

    # Гистограмма Баланса
    lower_a = df['total_assets'].quantile(0.05)
    upper_a = df['total_assets'].quantile(0.95)
    sns.histplot(data=df[(df['total_assets'] >= lower_a) & (df['total_assets'] <= upper_a)], x=hist_cols[1], kde=True, ax=axes[1], color='skyblue', edgecolor='black')
    axes[1].set_title(f'Гистограмма: {hist_cols[1]}')

    # Гистограмма Прибыли
    lower_p = df['net_profit'].quantile(0.05)
    upper_p = df['net_profit'].quantile(0.95)
    sns.histplot(data=df[(df['net_profit'] >= lower_p) & (df['net_profit'] <= upper_p)], x=hist_cols[2], kde=True, ax=axes[2], color='skyblue', edgecolor='black')
    axes[2].set_title(f'Гистограмма: {hist_cols[2]}')

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "histograms.png", dpi=120)
    plt.close(fig)

    print("Выбросы по IQRб")
    for col in hist_cols:
        low, high, count = iqr_outliers(df[col])
        print(f"{col} Выбросы = {count}, Норма = от {low} до {high}")

    print("Выбросы по Z-score")
    for col in hist_cols:
        low, high, count = z_score_outliers(df[col])
        print(f"{col} Выбросы = {count}, Норма = от {low} до {high}")

    # 3. Вычислите и визуализируйте матрицу корреляции между всеми 20
    # колонками. Между какими колонками имеется высокая корреляция?
    # Что означает эта высокая корреляция и в чем может быть ее
    # причина?
    print("!!!!! 3 !!!!!")

    fig, axes = plt.subplots(1, 1, figsize=(26, 26))
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=axes, annot_kws={"size": 7})
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "correlation.png", dpi=110)
    plt.close(fig)

    pairs = corr.abs().unstack().drop_duplicates()
    pairs = pairs[pairs < 1.0]
    max_corr_value = pairs.max()
    max_corr_pair = pairs.idxmax()

    original_corr = corr.loc[max_corr_pair[0], max_corr_pair[1]]

    print(f"Самая сильная связь между: {max_corr_pair[0]} и {max_corr_pair[1]}")
    print(f"Коэффициент корреляции: {original_corr:.4f} (по модулю: {max_corr_value:.4f})")
    print("Возможно компании ведут очень убыточные политики ведения бизнеса")

    # 4. Постройте диаграмму рассеивания (scatter plot) между
    # коррелирующими колонками.
    print("!!!!! 4 !!!!!")
    plt.figure(figsize=(5, 5))
    sns.scatterplot(
        data=df[df["revenue"] > 0],
        x="revenue",
        y=df["cost_of_sales"].abs(),
        s=15
    )

    plt.plot([1, 1e9], [1, 1e9], "r--", lw=1, label="y = x")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Выручка и продажи")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "scatter.png", dpi=120)
    plt.close()

    # 5. Сделайте как минимум один вывод исходя из описательной
    # статистики, гистограмм, матрицы корреляции, диаграммы
    # рассеивания.
    print("!!!!! 5 !!!!!")
    print("Большинство компаний из малого бизнеса это молодые компании с минимальной выручкой и очень низкими активами")
    print("Так же присутствуют малое количество компаний со сверхдоходами")
    print("Между себестоимостью продажи и выручкой практически идеальная обратная корреляция")


if __name__ == "__main__":
    main()
