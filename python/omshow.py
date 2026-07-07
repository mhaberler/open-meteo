# pip install omfiles
from omfiles import OmFileReader
import sys
from datetime import datetime, timezone

def main(file_path):
    with OmFileReader(file_path) as reader:
        print("Shape:", reader.shape)
        print("Chunks:", reader.chunks)
        ntime = reader.shape[-1] if len(reader.shape) > 1 else 0
        print("Timesteps:", ntime)

    # ICON global chunk calc (approx; adjust divisor per model)
    try:
        chunk_id = int(file_path.split('chunk_')[-1].split('.')[0])
        # Typical divisor ~7 days in seconds for rolling chunks
        divisor = 7 * 24 * 3600
        start_ts = chunk_id * divisor
        start_dt = datetime.fromtimestamp(start_ts, tz=timezone.utc)
        end_dt = datetime.fromtimestamp(start_ts + ntime * 3600, tz=timezone.utc)  # hourly
        print(f"Approx start: {start_dt}")
        print(f"Approx end: {end_dt}")
    except:
        print("Chunk ID parse failed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_om.py chunk_1958.om")
        sys.exit(1)
    main(sys.argv[1])
    