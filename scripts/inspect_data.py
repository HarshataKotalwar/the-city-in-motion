from pathlib import Path
import pyarrow.parquet as pq

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

files = sorted(RAW_DIR.glob("yellow_tripdata_*.parquet"))

print("=" * 70)
print("THE CITY IN MOTION — FULL FILE CHECK")
print("=" * 70)

print(f"\nFound {len(files)} Parquet files.\n")

total_rows = 0

for i, file in enumerate(files, 1):

    print(f"[{i}/{len(files)}] {file.name}")

    size_mb = file.stat().st_size / (1024 * 1024)
    pf = pq.ParquetFile(file)

    rows = pf.metadata.num_rows
    row_groups = pf.metadata.num_row_groups

    total_rows += rows

    print(f"    Size:       {size_mb:.2f} MB")
    print(f"    Rows:       {rows:,}")
    print(f"    Row groups: {row_groups}")
    print()

print("=" * 70)
print(f"TOTAL ROWS: {total_rows:,}")
print("=" * 70)

print("\nChecking schema consistency...")

first_schema = pq.ParquetFile(files[0]).schema_arrow

schemas_match = True

for file in files[1:]:
    schema = pq.ParquetFile(file).schema_arrow

    if schema != first_schema:
        schemas_match = False
        print(f"Different schema: {file.name}")

if schemas_match:
    print("All 12 files have the same schema. ✓")
else:
    print("WARNING: Schema differences detected.")

print("\nInspection complete.")