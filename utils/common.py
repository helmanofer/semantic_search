import glob
from pathlib import Path
from typing import List


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent


def list_all_files(directory, extension: str):
    """
    dir: directory with * in the pattern
    """
    return glob.glob(f"{directory}/*.{extension}")


def split_list_to_lists_w_overlapping(list_: list, group_size: int, overlap_size: int) -> List[list]:
    return [
        list_[i: i + group_size]
        for i in range(0, len(list_), group_size - overlap_size)
    ]


def lambda_x_x(x):
    return x
