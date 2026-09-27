from pathlib import Path
from datetime import datetime

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Configuration
# ============================================================

BATCH_SIZE = 100_000

# Project scope:
# August 2025 through July 2026
#
# Start is inclusive.
# End is exclusive.
PROJECT_START = pa.scalar(
    datetime(2025, 8, 1),
    type=pa.timestamp("us")
)

PROJECT_END = pa.scalar(
    datetime(2026, 8, 1),
    type=pa.timestamp("us")
)


# ============================================================
# Base columns
# ============================================================

BASE_COLUMNS = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
]


# ============================================================
# Process one batch
# ============================================================

def process_batch(table):

    pickup = table["tpep_pickup_datetime"]
    dropoff = table["tpep_dropoff_datetime"]

    # --------------------------------------------------------
    # Time features
    # --------------------------------------------------------

    pickup_date = pc.cast(
        pickup,
        pa.date32()
    )

    pickup_hour = pc.hour(pickup)

    pickup_day = pc.day(pickup)

    pickup_month = pc.month(pickup)

    pickup_year = pc.year(pickup)

    day_of_week = pc.strftime(
        pickup,
        format="%A"
    )

    # --------------------------------------------------------
    # Weekend flag
    # --------------------------------------------------------

    is_weekend = pc.is_in(
        day_of_week,
        value_set=pa.array([
            "Saturday",
            "Sunday"
        ])
    )

    # --------------------------------------------------------
    # Trip duration
    # --------------------------------------------------------

    pickup_microseconds = pc.cast(
        pickup,
        pa.int64()
    )

    dropoff_microseconds = pc.cast(
        dropoff,
        pa.int64()
    )

    duration_microseconds = pc.subtract(
        dropoff_microseconds,
        pickup_microseconds
    )

    trip_duration_minutes = pc.divide(
        duration_microseconds,
        60_000_000
    )

    # --------------------------------------------------------
    # Fare per mile
    # --------------------------------------------------------

    fare_per_mile = pc.if_else(
        pc.greater(
            table["trip_distance"],
            0
        ),
        pc.divide(
            table["fare_amount"],
            table["trip_distance"]
        ),
        pa.scalar(
            None,
            type=pa.float64()
        )
    )

    # --------------------------------------------------------
    # Tip percentage
    # --------------------------------------------------------

    tip_percentage = pc.if_else(
        pc.greater(
            table["fare_amount"],
            0
        ),
        pc.multiply(
            pc.divide(
                table["tip_amount"],
                table["fare_amount"]
            ),
            100
        ),
        pa.scalar(
            None,
            type=pa.float64()
        )
    )

    # --------------------------------------------------------
    # Duration validation
    #
    # Keep trips between 0 minutes and 24 hours.
    # --------------------------------------------------------

    valid_duration = pc.and_kleene(
        pc.greater_equal(
            trip_duration_minutes,
            0
        ),
        pc.less_equal(
            trip_duration_minutes,
            24 * 60
        )
    )

    # --------------------------------------------------------
    # Project date scope
    #
    # August 1, 2025 inclusive
    # August 1, 2026 exclusive
    # --------------------------------------------------------

    in_project_scope = pc.and_kleene(
        pc.greater_equal(
            pickup,
            PROJECT_START
        ),
        pc.less(
            pickup,
            PROJECT_END
        )
    )

    # --------------------------------------------------------
    # Combine filters
    # --------------------------------------------------------

    valid_rows = pc.and_kleene(
        valid_duration,
        in_project_scope
    )

    table = table.filter(
        valid_rows
    )

    if table.num_rows == 0:
        return None

    # --------------------------------------------------------
    # Recalculate derived features after filtering
    # --------------------------------------------------------

    pickup = table["tpep_pickup_datetime"]
    dropoff = table["tpep_dropoff_datetime"]

    pickup_date = pc.cast(
        pickup,
        pa.date32()
    )

    pickup_hour = pc.hour(pickup)

    pickup_day = pc.day(pickup)

    pickup_month = pc.month(pickup)

    pickup_year = pc.year(pickup)

    day_of_week = pc.strftime(
        pickup,
        format="%A"
    )

    is_weekend = pc.is_in(
        day_of_week,
        value_set=pa.array([
            "Saturday",
            "Sunday"
        ])
    )

    pickup_microseconds = pc.cast(
        pickup,
        pa.int64()
    )

    dropoff_microseconds = pc.cast(
        dropoff,
        pa.int64()
    )

    duration_microseconds = pc.subtract(
        dropoff_microseconds,
        pickup_microseconds
    )

    trip_duration_minutes = pc.divide(
        duration_microseconds,
        60_000_000
    )

    fare_per_mile = pc.if_else(
        pc.greater(
            table["trip_distance"],
            0
        ),
        pc.divide(
            table["fare_amount"],
            table["trip_distance"]
        ),
        pa.scalar(
            None,
            type=pa.float64()
        )
    )

    tip_percentage = pc.if_else(
        pc.greater(
            table["fare_amount"],
            0
        ),
        pc.multiply(
            pc.divide(
                table["tip_amount"],
                table["fare_amount"]
            ),
            100
        ),
        pa.scalar(
            None,
            type=pa.float64()
        )
    )

    # --------------------------------------------------------
    # Add derived columns
    # --------------------------------------------------------

    table = table.append_column(
        "pickup_date",
        pickup_date
    )

    table = table.append_column(
        "pickup_hour",
        pickup_hour
    )

    table = table.append_column(
        "pickup_day",
        pickup_day
    )

    table = table.append_column(
        "pickup_month",
        pickup_month
    )

    table = table.append_column(
        "pickup_year",
        pickup_year
    )

    table = table.append_column(
        "day_of_week",
        day_of_week
    )

    table = table.append_column(
        "is_weekend",
        is_weekend
    )

    table = table.append_column(
        "trip_duration_minutes",
        trip_duration_minutes
    )

    table = table.append_column(
        "fare_per_mile",
        fare_per_mile
    )

    table = table.append_column(
        "tip_percentage",
        tip_percentage
    )

    return table


# ============================================================
# Process one Parquet file
# ============================================================

def process_file(file_path):

    output_file = (
        OUTPUT_DIR
        / f"{file_path.stem.replace('_cleaned', '')}_features.parquet"
    )

    # --------------------------------------------------------
    # Skip existing feature file
    # --------------------------------------------------------

    if output_file.exists():

        print(
            f"Skipping {file_path.name} "
            f"(features already exist)"
        )

        return

    print()
    print("=" * 70)
    print(f"Processing: {file_path.name}")
    print(f"Output:    {output_file.name}")
    print("=" * 70)

    parquet_file = pq.ParquetFile(
        file_path
    )

    writer = None

    total_input_rows = 0
    total_output_rows = 0

    try:

        # ----------------------------------------------------
        # Process in batches
        # ----------------------------------------------------

        for batch in parquet_file.iter_batches(
            batch_size=BATCH_SIZE,
            columns=BASE_COLUMNS
        ):

            table = pa.Table.from_batches(
                [batch]
            )

            total_input_rows += table.num_rows

            processed_table = process_batch(
                table
            )

            if processed_table is None:
                continue

            total_output_rows += processed_table.num_rows

            # ------------------------------------------------
            # Create writer from first valid batch
            # ------------------------------------------------

            if writer is None:

                writer = pq.ParquetWriter(
                    output_file,
                    processed_table.schema,
                    compression="snappy"
                )

            writer.write_table(
                processed_table
            )

            # ------------------------------------------------
            # Progress
            # ------------------------------------------------

            if (
                total_input_rows % 1_000_000
                < BATCH_SIZE
            ):

                print(
                    f"Processed: {total_input_rows:,} rows | "
                    f"Kept: {total_output_rows:,} rows"
                )

    finally:

        if writer is not None:
            writer.close()

    print()
    print(
        f"Finished: {file_path.name}"
    )

    print(
        f"Input rows:  {total_input_rows:,}"
    )

    print(
        f"Output rows: {total_output_rows:,}"
    )


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("=" * 70)
    print("THE CITY IN MOTION")
    print("Feature Engineering")
    print("=" * 70)

    print()
    print("Project scope:")
    print("August 2025 through July 2026")
    print("Start: 2025-08-01")
    print("End:   2026-08-01 (exclusive)")
    print()

    cleaned_files = sorted(
        INPUT_DIR.glob("*_cleaned.parquet")
    )

    if not cleaned_files:

        print(
            "No cleaned Parquet files found."
        )

        return

    print(
        f"Found {len(cleaned_files)} cleaned files."
    )

    print()

    for file_path in cleaned_files:

        process_file(
            file_path
        )

    print()
    print("=" * 70)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()