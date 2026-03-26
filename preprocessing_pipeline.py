from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class Paths:
    # project root = folder containing this script
    project_root: Path = Path(__file__).resolve().parent
    data_path: Path = project_root / "data" / "processed" / "milan_telecom_agg_all.parquet"
    out_dir: Path = project_root / "results" / "preprocessing"


ACTIVITY_COLS = ["sms_in", "sms_out", "call_in", "call_out", "internet_traffic"]


def ensure_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "datetime" not in df.columns:
        df = df.copy()
        df["datetime"] = pd.to_datetime(df["time_interval"], unit="ms")
    return df


def build_hourly_weekday_weekend_mean_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build 240 features per square:
      weekday/weekend × hour(0-23) × 5 channels
    Aggregation: mean.

    Returns a DataFrame with columns: square_id + 240 features.
    """
    df = ensure_datetime(df).copy()

    df["hour"] = df["datetime"].dt.hour
    df["weekday"] = df["datetime"].dt.weekday
    df["is_weekend"] = df["weekday"].isin([5, 6])
    df["regime"] = np.where(df["is_weekend"], "weekend", "weekday")

    grp = (
        df.groupby(["square_id", "regime", "hour"], as_index=False)[ACTIVITY_COLS]
        .mean()
    )

    wide = grp.pivot(index="square_id", columns=["regime", "hour"], values=ACTIVITY_COLS)

    wide.columns = [
        f"{reg}_hour_{hour:02d}_{chan}_mean" for chan, reg, hour in wide.columns
    ]

    X = wide.reset_index()

    # sanity: no missing
    if X.isna().any().any():
        raise ValueError("Feature matrix contains missing values. Check temporal coverage.")

    return X


def save_square_split(df: pd.DataFrame, out_dir: Path, random_state: int = 42) -> None:
    square_ids = df["square_id"].unique()
    train_squares, holdout_squares = train_test_split(
        square_ids, test_size=0.2, random_state=random_state
    )
    out_path = out_dir / "square_id_split.npz"
    np.savez(out_path, train_squares=train_squares, holdout_squares=holdout_squares)


def make_variants_and_save(
    X: pd.DataFrame, out_dir: Path, random_state: int = 42
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save full features
    full_path = out_dir / "features_hourly_weekday_weekend_mean_FULL.parquet"
    X.to_parquet(full_path, index=False)

    id_col = "square_id"
    feature_cols = [c for c in X.columns if c != id_col]
    X_raw = X[feature_cols].values

    # Variant A: StandardScaler(raw)
    scaler_A = StandardScaler()
    Z_A = scaler_A.fit_transform(X_raw)

    Z_A_df = pd.DataFrame(Z_A, columns=feature_cols)
    Z_A_df.insert(0, "square_id", X[id_col].values)

    out_A = out_dir / "features_FULL_standardscaled.parquet"
    Z_A_df.to_parquet(out_A, index=False)

    scaler_A_path = out_dir / "scaler_variant_A_standard.joblib"
    joblib.dump(scaler_A, scaler_A_path)

    # Variant B: log1p + StandardScaler
    X_log = np.log1p(X_raw)

    scaler_B = StandardScaler()
    Z_B = scaler_B.fit_transform(X_log)

    Z_B_df = pd.DataFrame(Z_B, columns=feature_cols)
    Z_B_df.insert(0, "square_id", X[id_col].values)

    out_B = out_dir / "features_FULL_log1p_standardscaled.parquet"
    Z_B_df.to_parquet(out_B, index=False)

    scaler_B_path = out_dir / "scaler_variant_B_log1p_standard.joblib"
    joblib.dump(scaler_B, scaler_B_path)

    # quick sanity prints (optional)
    mean_A = Z_A_df.drop(columns=["square_id"]).mean().mean()
    std_A = Z_A_df.drop(columns=["square_id"]).std(ddof=0).mean()

    mean_B = Z_B_df.drop(columns=["square_id"]).mean().mean()
    std_B = Z_B_df.drop(columns=["square_id"]).std(ddof=0).mean()

    print("Saved artifacts to:", out_dir.resolve())
    print("Variant A mean/std:", mean_A, std_A)
    print("Variant B mean/std:", mean_B, std_B)


def main():
    paths = Paths()
    df = pd.read_parquet(paths.data_path)
    df = ensure_datetime(df)

    paths.out_dir.mkdir(parents=True, exist_ok=True)
    save_square_split(df, paths.out_dir, random_state=42)

    X = build_hourly_weekday_weekend_mean_features(df)
    make_variants_and_save(X, paths.out_dir, random_state=42)


if __name__ == "__main__":
    main()