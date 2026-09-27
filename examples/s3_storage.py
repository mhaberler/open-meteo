#!/usr/bin/env python3
"""Sum object count and bytes under an anonymously readable S3 prefix.

Open-Meteo publishes the tree behind
https://openmeteo.s3.amazonaws.com/index.html#data/ at s3://openmeteo/data/.
ListObjects is unsigned, so no AWS account is required. A full walk is one
ListObjectsV2 request per 1000 keys. Ctrl-C prints the totals collected so far.

Usage:
    python3 s3_storage.py
    python3 s3_storage.py data/dwd_icon/
    python3 s3_storage.py --bucket openmeteo --prefix data/

Requires boto3 (pip install boto3).
"""

from __future__ import annotations

import argparse
import sys

UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")


def human(n: int) -> str:
    size = float(n)
    for unit in UNITS:
        if size < 1024 or unit == UNITS[-1]:
            if unit == "B":
                return f"{int(size)} B"
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{n} B"


def report(objects: int, size: int, *, partial: bool) -> None:
    label = "Partial" if partial else "Total"
    tebi = size / (1024**4)
    tera = size / (1000**4)
    print(f"{label} objects: {objects:,}")
    print(f"{label} size: {human(size)} ({tebi:.2f} TiB, {tera:.2f} TB)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prefix", nargs="?", default="data/", help="Key prefix (default: data/)")
    parser.add_argument("--bucket", default="openmeteo")
    parser.add_argument("--region", default="us-west-2", help="Bucket region (x-amz-bucket-region)")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10_000,
        metavar="N",
        help="Print a running total to stderr every N objects (0 disables)",
    )
    args = parser.parse_args()

    try:
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config
    except ImportError:
        print("boto3 is required: pip install boto3", file=sys.stderr)
        return 1

    client = boto3.client(
        "s3",
        region_name=args.region,
        config=Config(signature_version=UNSIGNED, retries={"max_attempts": 10, "mode": "standard"}),
    )
    paginator = client.get_paginator("list_objects_v2")

    total_size = 0
    total_objects = 0
    since_report = 0
    print(f"Calculating size for s3://{args.bucket}/{args.prefix} ...", file=sys.stderr)
    try:
        for page in paginator.paginate(Bucket=args.bucket, Prefix=args.prefix):
            for obj in page.get("Contents", []):
                total_size += obj["Size"]
                total_objects += 1
                since_report += 1
            if args.progress_every and since_report >= args.progress_every:
                since_report = 0
                print(f"{total_objects:,} objects, {human(total_size)}", file=sys.stderr, flush=True)
    except KeyboardInterrupt:
        print(file=sys.stderr)
        report(total_objects, total_size, partial=True)
        return 130

    report(total_objects, total_size, partial=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
