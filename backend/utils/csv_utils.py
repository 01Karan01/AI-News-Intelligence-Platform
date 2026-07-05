from pathlib import Path

import pandas as pd


def read_csv_safely(path, **kwargs):
    csv_path = Path(path)
    if not csv_path.is_absolute():
        csv_path = Path(__file__).resolve().parent.parent / csv_path

    df = pd.read_csv(
        csv_path,
        engine="python",
        skipinitialspace=True,
        on_bad_lines="skip",
        encoding="utf-8",
        quotechar='"',
        **kwargs,
    )

    df.columns = [col.strip() for col in df.columns]
    return df
