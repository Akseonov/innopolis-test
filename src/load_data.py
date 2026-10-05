from itertools import islice

import pandas as pd
from datasets import load_dataset

from config import YEAR, ROWS, DATA_DIR, RAW_PATH, SAMPLE_PATH

# колонки из анализа для из бухгалтерского анализа. наименования взяты в интернете с https://www.berator.ru/
COLUMNS = {
    "simplified": "simplified",  # 1 — упрощённая форма отчётности (малый бизнес)
    "age": "age",  # возраст компании, лет
    "line_1100": "noncurrent_assets",  # ИТОГО по разделу I
    "line_1150": "fixed_assets",  # Основные средства
    "line_1200": "current_assets",  # ИТОГО по разделу II
    "line_1210": "inventories",  # Запасы
    "line_1230": "receivables",  # Дебиторская задолженность
    "line_1250": "cash",  # Денежные средства и денежные эквиваленты
    "line_1300": "equity",  # ИТОГО по разделу III
    "line_1400": "longterm_liabilities",  # ИТОГО по разделу IV
    "line_1500": "shortterm_liabilities",  # ИТОГО по разделу V
    "line_1520": "payables",  # Кредиторская задолженность
    "line_1600": "total_assets",  # БАЛАНС (по разделу I и II)
    "line_2110": "revenue",  # Выручка
    "line_2120": "cost_of_sales",  # Себестоимость продаж
    "line_2100": "gross_profit",  # Валовая прибыль (убыток)
    "line_2200": "operating_profit",  # Прибыль (убыток) от продаж
    "line_2300": "pretax_profit",  # Прибыль (убыток) до налогообложения
    "line_2400": "net_profit",  # Чистая прибыль (убыток)
    "line_2410": "income_tax",  # Налог на прибыль
}

def download_raw() -> None:
    ds = (load_dataset(
        "irlspbru/RFSD",
        split="train", streaming=True,
        data_files=f"RFSD/year={YEAR}/*.parquet"
    ).filter(lambda row: row["filed"] == 1))  # filed - отчет сдан.

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(islice(ds, ROWS)).to_csv(RAW_PATH, index=False)

def prepare_sample() -> None:
    raw = pd.read_csv(RAW_PATH)
    raw[list(COLUMNS)].rename(columns=COLUMNS).to_csv(SAMPLE_PATH, index=False)

def load_data(path) -> pd.DataFrame:
    return pd.read_csv(path)

if __name__ == "__main__":
    if not RAW_PATH.exists():
        download_raw()
    prepare_sample()
    print("Полные данные:", load_data(RAW_PATH).shape, RAW_PATH)
    print("Выборка для анализа:", load_data(SAMPLE_PATH).shape, SAMPLE_PATH)
