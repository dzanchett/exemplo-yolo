"""Evaluate cattle-counting performance using ground-truth counts.

The goal of this script is not to provide state-of-the-art metrics, but rather
to demonstrate how students can quantify the quality of their counting model.
Given two CSV files (predictions and ground-truth counts) it computes:

* Mean Absolute Error (MAE)
* Mean Absolute Percentage Error (MAPE) when possible
* Aggregate totals and their difference

Both CSV files are expected to contain the columns:

* `image_path`: full or relative path to the image
* `cattle_count`: predicted or true number of animals in the frame

The script aligns rows by the basename of `image_path`, which keeps things
flexible even if the folders differ between training and evaluation time.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Dict, List


@dataclass
class CountEntry:
    """Simple container for the relevant information of each frame."""

    image_name: str
    count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare predicted cattle counts with ground-truth annotations."
    )
    parser.add_argument(
        "--predictions",
        type=str,
        required=True,
        help="CSV file produced by src/infer.py (cattle_count_report.csv).",
    )
    parser.add_argument(
        "--ground-truth",
        type=str,
        required=True,
        help="CSV file with manually verified cattle counts.",
    )

    return parser.parse_args()


def read_counts(csv_path: Path) -> List[CountEntry]:
    """Load counts from CSV while validating the presence of required columns."""

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    entries: List[CountEntry] = []
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required_columns = {"image_path", "cattle_count"}
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"CSV file {csv_path} is missing required columns: {sorted(missing)}"
            )

        for row in reader:
            try:
                count = int(row["cattle_count"])
            except ValueError as exc:
                raise ValueError(
                    f"Row in {csv_path} has a non-integer count: {row['cattle_count']}"
                ) from exc

            image_path = Path(row["image_path"]) if row["image_path"] else Path()
            entries.append(CountEntry(image_path.name, count))

    return entries


def align_by_image_name(entries: List[CountEntry]) -> Dict[str, CountEntry]:
    """Map each entry by the basename of the image path."""

    return {entry.image_name: entry for entry in entries}


def compute_errors(
    predictions: Dict[str, CountEntry], ground_truth: Dict[str, CountEntry]
) -> None:
    """Compute and print error metrics for the provided dictionaries."""

    absolute_errors: List[float] = []
    percentage_errors: List[float] = []

    missing_predictions = []
    for image_name, gt_entry in ground_truth.items():
        pred_entry = predictions.get(image_name)
        if pred_entry is None:
            missing_predictions.append(image_name)
            continue

        abs_error = abs(pred_entry.count - gt_entry.count)
        absolute_errors.append(abs_error)

        if gt_entry.count > 0:
            percentage_errors.append(abs_error / gt_entry.count)

        print(
            f"[DETAIL] {image_name}: predicted={pred_entry.count} | "
            f"ground_truth={gt_entry.count} | abs_error={abs_error}"
        )

    if missing_predictions:
        print(
            "\n[WARNING] No predictions were found for the following images: "
            + ", ".join(sorted(missing_predictions))
        )

    if not absolute_errors:
        print("[ERROR] Could not compute metrics because there are no matching entries.")
        return

    mae = mean(absolute_errors)
    mape = mean(percentage_errors) * 100 if percentage_errors else float("nan")

    total_pred = sum(entry.count for entry in predictions.values())
    total_gt = sum(entry.count for entry in ground_truth.values())

    print("\n[RESULTS]")
    print(f"Mean Absolute Error (MAE): {mae:.2f} animals")
    if percentage_errors:
        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    else:
        print("Mean Absolute Percentage Error (MAPE): undefined (zero animals in some frames)")
    print(f"Total predicted cattle: {total_pred}")
    print(f"Total ground-truth cattle: {total_gt}")
    print(f"Absolute difference: {abs(total_pred - total_gt)} animals")


def main() -> None:
    args = parse_args()
    predictions = read_counts(Path(args.predictions))
    ground_truth = read_counts(Path(args.ground_truth))

    compute_errors(align_by_image_name(predictions), align_by_image_name(ground_truth))


if __name__ == "__main__":
    main()
