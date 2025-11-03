"""Train a YOLO model for cattle detection.

This script is intentionally verbose and heavily commented so it can be
used as teaching material in a machine learning course.  The implementation
relies on the `ultralytics` Python package, which provides a friendly API
for training YOLOv8 models.

The high-level workflow is:

1. Parse the command-line arguments provided by the user (model checkpoint,
   dataset configuration, training hyperparameters, output location).
2. Validate the inputs so that students can see what can go wrong early.
3. Instantiate a `YOLO` object pointing to the chosen weights.
4. Launch the training job via `model.train(...)`.
5. Print a didactic summary explaining where to find the results.

You can execute the script inside the Docker container with something like::

    python src/train.py --data-config configs/cattle.yaml --epochs 50

The provided `configs/cattle.yaml` expects the dataset to be stored in the
`data/` directory following the standard YOLO format.  See the README for
instructions on how to prepare the dataset.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments with helpful descriptions."""

    parser = argparse.ArgumentParser(
        description=(
            "Train a YOLO model specialised in counting cattle. "
            "All arguments have informative defaults so the script is easy to run."
        )
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help=(
            "Path to the pretrained checkpoint to start from. "
            "You may use Ultralytics' YAMLs (e.g. yolov8n.pt) or a custom path."
        ),
    )
    parser.add_argument(
        "--data-config",
        type=str,
        default="configs/cattle.yaml",
        help=(
            "Path to the dataset configuration file (YOLO format). "
            "The default assumes you prepared data/cattle following the README."
        ),
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs. Start small (e.g. 10) for quick experiments.",
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=640,
        help="Image size used for training. Typical YOLO values are 640 or 512.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size per iteration. Adjust to fit your GPU memory.",
    )
    parser.add_argument(
        "--project",
        type=str,
        default="outputs/training_runs",
        help=(
            "Directory where Ultralytics will store training artefacts "
            "(checkpoints, TensorBoard logs, images)."
        ),
    )
    parser.add_argument(
        "--run-name",
        type=str,
        default="cattle_detection",
        help="Sub-directory name used to namespace this specific training run.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help=(
            "Device used for training. Options: 'cpu', 'cuda', 'cuda:0', etc. "
            "'auto' lets Ultralytics pick automatically."
        ),
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.01,
        help="Initial learning rate; tweak to stabilise training if needed.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of dataloader worker processes. Reduce if using modest CPUs.",
    )

    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> Dict[str, Any]:
    """Ensure inputs exist and create output directories as needed.

    Returning a dictionary with resolved paths keeps the main function tidy and
    explicitly communicates what was validated.
    """

    resolved: Dict[str, Any] = {}

    data_config_path = Path(args.data_config)
    if not data_config_path.exists():
        raise FileNotFoundError(
            f"Could not find the dataset configuration file at {data_config_path.resolve()}"
        )
    resolved["data_config"] = data_config_path

    project_dir = Path(args.project)
    project_dir.mkdir(parents=True, exist_ok=True)
    resolved["project"] = project_dir

    # The model path can be either local or a named Ultralytics checkpoint.
    # We do not enforce existence to keep the experience smooth when using the
    # built-in names (e.g. 'yolov8n.pt'), which Ultralytics downloads on demand.

    return resolved


def main() -> None:
    """Run the training routine with the provided arguments."""

    args = parse_args()
    validated = validate_inputs(args)

    print("[INFO] Loading YOLO model...")
    model = YOLO(args.model)

    print("[INFO] Starting training. This may take a while depending on the dataset size.")
    model.train(
        data=str(validated["data_config"]),
        epochs=args.epochs,
        imgsz=args.img_size,
        batch=args.batch_size,
        project=str(validated["project"]),
        name=args.run_name,
        lr0=args.learning_rate,
        device=args.device,
        workers=args.workers,
    )

    output_dir = validated["project"] / args.run_name
    print("\n[SUCCESS] Training finished!")
    print(
        "You can find the resulting checkpoints, metrics, and visualisations at: "
        f"{output_dir.resolve()}"
    )
    print(
        "To resume training later, point the --model flag to the best.pt checkpoint "
        "inside that directory."
    )


if __name__ == "__main__":
    main()
