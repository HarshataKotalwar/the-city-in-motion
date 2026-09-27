from pathlib import Path
import json
import pyarrow.parquet as pq
import pyarrow.compute as pc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


FILES = sorted(
    PROCESSED_DIR.glob("yellow_tripdata_*_cleaned.parquet")
)


def analyze_file(file_path):

    parquet = pq.ParquetFile(file_path)

    total_rows = 0
    null_pickup = 0
    null_dropoff = 0
    null_distance = 0
    null_fare = 0
    null_total = 0

    zero_distance = 0
    zero_fare = 0
    zero_total = 0

    negative_distance = 0
    negative_fare = 0
    negative_total = 0

    for batch in parquet.iter_batches(
        batch_size=100_000,
        columns=[
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
        ],
    ):

        total_rows += batch.num_rows

        pickup = batch.column(
            batch.schema.get_field_index("tpep_pickup_datetime")
        )
        dropoff = batch.column(
            batch.schema.get_field_index("tpep_dropoff_datetime")
        )
        distance = batch.column(
            batch.schema.get_field_index("trip_distance")
        )
        fare = batch.column(
            batch.schema.get_field_index("fare_amount")
        )
        total = batch.column(
            batch.schema.get_field_index("total_amount")
        )

        # Null counts
        null_pickup += pc.sum(
            pc.is_null(pickup)
        ).as_py()

        null_dropoff += pc.sum(
            pc.is_null(dropoff)
        ).as_py()

        null_distance += pc.sum(
            pc.is_null(distance)
        ).as_py()

        null_fare += pc.sum(
            pc.is_null(fare)
        ).as_py()

        null_total += pc.sum(
            pc.is_null(total)
        ).as_py()

        # Zero counts
        zero_distance += pc.sum(
            pc.equal(distance, 0)
        ).as_py()

        zero_fare += pc.sum(
            pc.equal(fare, 0)
        ).as_py()

        zero_total += pc.sum(
            pc.equal(total, 0)
        ).as_py()

        # Negative counts
        negative_distance += pc.sum(
            pc.less(distance, 0)
        ).as_py()

        negative_fare += pc.sum(
            pc.less(fare, 0)
        ).as_py()

        negative_total += pc.sum(
            pc.less(total, 0)
        ).as_py()

    return {
        "clean_rows": total_rows,
        "null_pickup_datetime": null_pickup,
        "null_dropoff_datetime": null_dropoff,
        "null_trip_distance": null_distance,
        "null_fare_amount": null_fare,
        "null_total_amount": null_total,
        "zero_trip_distance": zero_distance,
        "zero_fare_amount": zero_fare,
        "zero_total_amount": zero_total,
        "negative_trip_distance": negative_distance,
        "negative_fare_amount": negative_fare,
        "negative_total_amount": negative_total,
    }


def main():

    print("=" * 70)
    print("THE CITY IN MOTION — DATA QUALITY REPORT")
    print("=" * 70)

    print(f"\nCleaned files found: {len(FILES)}")

    if len(FILES) != 12:
        print("WARNING: Expected 12 cleaned files.")

    results = {}

    total_clean_rows = 0
    total_raw_rows = 0

    for cleaned_file in FILES:

        month = cleaned_file.name.replace(
            "yellow_tripdata_", ""
        ).replace(
            "_cleaned.parquet", ""
        )

        raw_file = RAW_DIR / f"yellow_tripdata_{month}.parquet"

        print(f"\nAnalyzing: {month}")

        raw_rows = pq.ParquetFile(
            raw_file
        ).metadata.num_rows

        quality = analyze_file(cleaned_file)

        clean_rows = quality["clean_rows"]
        removed_rows = raw_rows - clean_rows

        removal_percentage = (
            removed_rows / raw_rows * 100
            if raw_rows > 0
            else 0
        )

        quality["raw_rows"] = raw_rows
        quality["removed_rows"] = removed_rows
        quality["removal_percentage"] = round(
            removal_percentage, 2
        )

        results[month] = quality

        total_raw_rows += raw_rows
        total_clean_rows += clean_rows

        print(f"  Raw rows:     {raw_rows:,}")
        print(f"  Clean rows:   {clean_rows:,}")
        print(f"  Removed:      {removed_rows:,}")
        print(f"  Removal rate: {removal_percentage:.2f}%")

    total_removed = total_raw_rows - total_clean_rows

    overall_removal = (
        total_removed / total_raw_rows * 100
        if total_raw_rows > 0
        else 0
    )

    report = {
        "project": "The City in Motion",
        "dataset": "NYC TLC Yellow Taxi Trip Records",
        "scope": "August 2025 through July 2026",
        "months": len(FILES),
        "total_raw_rows": total_raw_rows,
        "total_clean_rows": total_clean_rows,
        "total_removed_rows": total_removed,
        "overall_removal_percentage": round(
            overall_removal, 2
        ),
        "monthly_results": results,
    }

    output_file = REPORT_DIR / "data_quality_report.json"

    with open(output_file, "w") as f:
        json.dump(
            report,
            f,
            indent=4
        )

    print("\n" + "=" * 70)
    print("OVERALL DATA QUALITY")
    print("=" * 70)

    print(f"\nTotal raw rows:   {total_raw_rows:,}")
    print(f"Total clean rows: {total_clean_rows:,}")
    print(f"Total removed:    {total_removed:,}")
    print(f"Removal rate:     {overall_removal:.2f}%")

    print(f"\nReport saved to:")
    print(output_file)

    print("\n" + "=" * 70)
    print("DATA QUALITY ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()