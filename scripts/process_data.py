from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


COLUMNS = [
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


def process_file(file_path):

    print(f"\nProcessing: {file_path.name}", flush=True)

    parquet = pq.ParquetFile(file_path)

    output_file = (
        PROCESSED_DIR /
        f"{file_path.stem}_cleaned.parquet"
    )

    writer = None
    total_rows = 0
    batch_number = 0

    for batch in parquet.iter_batches(
        batch_size=100_000,
        columns=COLUMNS
    ):

        batch_number += 1

        table = pa.Table.from_batches([batch])

        mask = pc.is_valid(
            table["tpep_pickup_datetime"]
        )

        mask = pc.and_kleene(
            mask,
            pc.is_valid(table["tpep_dropoff_datetime"])
        )

        mask = pc.and_kleene(
            mask,
            pc.is_valid(table["trip_distance"])
        )

        mask = pc.and_kleene(
            mask,
            pc.is_valid(table["fare_amount"])
        )

        mask = pc.and_kleene(
            mask,
            pc.is_valid(table["total_amount"])
        )

        mask = pc.and_kleene(
            mask,
            pc.greater_equal(table["trip_distance"], 0)
        )

        mask = pc.and_kleene(
            mask,
            pc.greater_equal(table["fare_amount"], 0)
        )

        mask = pc.and_kleene(
            mask,
            pc.greater_equal(table["total_amount"], 0)
        )

        cleaned = table.filter(mask)

        if cleaned.num_rows == 0:
            continue

        if writer is None:
            writer = pq.ParquetWriter(
                output_file,
                cleaned.schema,
                compression="snappy"
            )

        writer.write_table(cleaned)

        total_rows += cleaned.num_rows

        print(
            f"  Batch {batch_number}: "
            f"{cleaned.num_rows:,} rows written",
            flush=True
        )

    if writer is not None:
        writer.close()

    print(f"  Clean rows: {total_rows:,}", flush=True)
    print(f"  Output: {output_file.name}", flush=True)


def main():

    files = sorted(
        RAW_DIR.glob("yellow_tripdata_*.parquet")
    )

    print("=" * 70)
    print("THE CITY IN MOTION — DATA PROCESSING")
    print("=" * 70)

    print(f"\nFiles found: {len(files)}")

    for file_path in files:
        process_file(file_path)

    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()