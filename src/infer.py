"""Run inference with a YOLO model and count cattle in each image/video.

This script is intentionally pedagogical: every major step includes comments
that explain what is happening and why.  The default configuration uses the
`yolov8n.pt` checkpoint trained on the COCO dataset, which already contains the
`cow` class.  You can swap the weights for a fine-tuned checkpoint to obtain
better accuracy on your specific ranch imagery.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List

from ultralytics import YOLO

TARGET_CLASS_NAMES = {"cow", "cattle", "bull"}


def parse_args() -> argparse.Namespace:
    """Create the argument parser with didactic defaults."""

    parser = argparse.ArgumentParser(
        description="Run YOLO inference and produce a cattle-counting report."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help=(
            "Checkpoint to use for inference. Use a fine-tuned .pt file for better accuracy."
        ),
    )
    parser.add_argument(
        "--source",
        type=str,
        default="images",
        help=(
            "File or directory with images/videos. Accepts glob patterns (e.g. images/*.jpg)."
        ),
    )
    parser.add_argument(
        "--save-dir",
        type=str,
        default="outputs/inference",
        help="Directory where annotated predictions and the CSV report will be stored.",
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=640,
        help="Inference image size. Higher values may increase accuracy but cost RAM/compute.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for filtering detections.",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.7,
        help="Intersection-over-Union threshold used for non-maximum suppression.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Compute device: 'cpu', 'cuda', 'cuda:0', etc. 'auto' tries GPU then CPU.",
    )
    parser.add_argument(
        "--class-names",
        type=str,
        nargs="*",
        default=list(TARGET_CLASS_NAMES),
        help=(
            "Custom class names to count. Useful if you trained on different labels. "
            "Defaults to common cattle-related names."
        ),
    )

    return parser.parse_args()


def normalise_class_names(class_names: Iterable[str]) -> List[str]:
    """Normalise class names so comparisons do not depend on capitalisation."""

    return [name.strip().lower() for name in class_names]


def ensure_output_directory(save_dir: Path) -> None:
    """Create the output directory if it does not already exist."""

    save_dir.mkdir(parents=True, exist_ok=True)


def create_model(model_path: str) -> YOLO:
    """Load the YOLO model while printing a friendly message."""

    print(f"[INFO] Loading model from '{model_path}'.")
    return YOLO(model_path)


def count_cattle(model: YOLO, args: argparse.Namespace) -> None:
    """Run inference and save both predictions and a CSV summary."""

    save_dir = Path(args.save_dir)
    ensure_output_directory(save_dir)

    target_names = set(normalise_class_names(args.class_names))

    print("[INFO] Running inference...")
    results = model.predict(
        source=args.source,
        imgsz=args.img_size,
        conf=args.conf,
        iou=args.iou,
        save=True,  # saves annotated images to disk inside the project directory
        save_txt=True,  # saves the raw detections to .txt files (YOLO format)
        project=str(save_dir),
        name="predictions",
        exist_ok=True,
        device=args.device,
    )

    report_rows = []
    for result in results:
        # `result.path` holds the original file name, while `result.boxes.cls`
        # contains the predicted class indices as a tensor.  We convert them to
        # a Python list for easier manipulation.
        class_indices = result.boxes.cls.tolist() if result.boxes is not None else []
        class_names = result.names

        # Convert class IDs to their human-readable names and normalise them.
        detected_names = [class_names[int(idx)].lower() for idx in class_indices]

        # Count how many detections correspond to cattle-related names.
        cattle_detections = sum(1 for name in detected_names if name in target_names)
        total_detections = len(class_indices)

        report_rows.append(
            {
                "image_path": str(Path(result.path).resolve()),
                "cattle_count": cattle_detections,
                "total_detections": total_detections,
            }
        )

        print(
            f"[RESULT] {Path(result.path).name}: "
            f"{cattle_detections} cattle / {total_detections} total detections"
        )

    if not report_rows:
        print("[WARNING] No results were produced. Double-check the --source argument.")
        return

    csv_path = save_dir / "cattle_count_report.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["image_path", "cattle_count", "total_detections"]
        )
        writer.writeheader()
        writer.writerows(report_rows)

    total_cattle = sum(row["cattle_count"] for row in report_rows)
    print("\n[SUCCESS] Inference complete!")
    print(f"Total cattle detected across all inputs: {total_cattle}")
    print(f"Detailed report saved to: {csv_path.resolve()}")
    print(
        "Annotated images and raw YOLO predictions are stored in the same directory."
    )


def main() -> None:
    args = parse_args()
    model = create_model(args.model)
    count_cattle(model, args)


if __name__ == "__main__":
    main()
