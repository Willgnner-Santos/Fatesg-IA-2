import pandas as pd
import logging

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Normalizando colunas...")
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    numeric_cols = ["runtime", "rate", "meta_score", "imdb_votes"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["rate"], inplace=True)

    logging.info("DataFrame limpo e tipado!")
    return df
