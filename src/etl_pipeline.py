# Banking Data Intelligence Platform
# Purpose: Reusable ETL pipeline with automatic data validation

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT / "data" / "PS_20174392719_1491204439457_log.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "paysim_processed.csv"
)

CHUNK_SIZE = 100_000

EXPECTED_TYPES = {
    "CASH_IN",
    "CASH_OUT",
    "DEBIT",
    "PAYMENT",
    "TRANSFER",
}


def main():
    """Transform PaySim data in chunks and validate the output."""

    print("Starting ETL Pipeline...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    missing_cells = 0
    negative_amounts = 0
    invalid_amounts = 0

    transaction_types = set()
    fraud_flags = set()
    flagged_fraud_values = set()

    # Read, transform, validate, and save the data in chunks.
    for chunk_number, chunk in enumerate(
        pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE),
        start=1,
    ):
        chunk.columns = chunk.columns.str.strip().str.lower()

        required_columns = {
            "type", "amount", "isfraud", "isflaggedfraud"
        }

        missing_columns = required_columns - set(chunk.columns)

        if missing_columns:
            raise ValueError(
                f"Required columns missing: {sorted(missing_columns)}"
            )

        chunk["type"] = chunk["type"].str.strip().str.upper()

        chunk["amount"] = pd.to_numeric(
            chunk["amount"], errors="coerce"
        )

        # Count missing values and validate transaction amounts.
        missing_cells += int(chunk.isna().sum().sum())
        negative_amounts += int((chunk["amount"] < 0).sum())
        invalid_amounts += int(chunk["amount"].isna().sum())

        transaction_types.update(chunk["type"].dropna().unique())
        fraud_flags.update(chunk["isfraud"].dropna().unique())
        flagged_fraud_values.update(
            chunk["isflaggedfraud"].dropna().unique()
        )

        # Write the first chunk with a header; append the rest.
        chunk.to_csv(
            OUTPUT_FILE,
            index=False,
            mode="w" if chunk_number == 1 else "a",
            header=(chunk_number == 1),
        )

        total_rows += len(chunk)
        print(f"Rows processed: {total_rows:,}")

    # Validate the complete ETL run.
    types_valid = transaction_types == EXPECTED_TYPES
    fraud_valid = fraud_flags == {0, 1}
    flagged_valid = flagged_fraud_values == {0, 1}
    amounts_valid = negative_amounts == 0 and invalid_amounts == 0
    missing_valid = missing_cells == 0

    print("\n========== ETL VALIDATION ==========")
    print("Total rows processed:", total_rows)
    print("Total columns:", len(pd.read_csv(OUTPUT_FILE, nrows=0).columns))
    print("Missing cells:", missing_cells)
    print("Negative amounts:", negative_amounts)
    print("Invalid or missing amounts:", invalid_amounts)
    print("Transaction types valid:", types_valid)
    print("Fraud flags valid:", fraud_valid)
    print("Flagged fraud values valid:", flagged_valid)
    print("Output file exists:", OUTPUT_FILE.exists())

    all_valid = (
        total_rows == 6_362_620
        and missing_valid
        and amounts_valid
        and types_valid
        and fraud_valid
        and flagged_valid
        and OUTPUT_FILE.exists()
    )

    print("Overall validation:", "PASSED" if all_valid else "FAILED")

    if not all_valid:
        raise ValueError("ETL validation failed. Review the results above.")

    print("====================================")
    print("ETL Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()