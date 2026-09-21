#!/usr/bin/env python3
"""Delete finished phase rows older than the chart window. In-progress rows stay."""

from phases import Store

if __name__ == "__main__":
    removed = Store().prune()
    print(f"pruned {removed}")
