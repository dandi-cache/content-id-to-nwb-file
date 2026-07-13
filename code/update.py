import argparse
import json
import pathlib


def _run(base_directory: pathlib.Path, limit: int | None) -> None:
    # Subset the upstream content-id-to-usage-dandiset-path cache to the entries whose asset
    # path is an NWB file. The upstream records are `{content_id: {dandiset_id: path}}`; a
    # path is considered an NWB file when `.nwb` is one of its suffixes, which also keeps
    # multi-suffix variants such as `.nwb.zarr`.
    #
    # `limit` caps the number of input records scanned in a single invocation. Production
    # runs leave it unset and recompute the full subset; it exists to keep test and debug
    # runs fast and bounded.
    input_file_path = (
        base_directory
        / "sourcedata"
        / "content-id-to-usage-dandiset-path"
        / "derivatives"
        / "content_id_to_usage_dandiset_path.jsonl"
    )

    records: list[dict] = []
    with input_file_path.open(mode="r") as input_stream:
        for scanned, line in enumerate(input_stream):
            if limit is not None and scanned >= limit:
                break
            record = json.loads(line)
            ((_content_id, usage_dandiset_path),) = record.items()
            ((_dandiset_id, path),) = usage_dandiset_path.items()
            if ".nwb" in pathlib.PurePosixPath(path).suffixes:
                records.append(record)

    derivatives_directory = base_directory / "derivatives"
    derivatives_directory.mkdir(parents=True, exist_ok=True)

    output_file_path = derivatives_directory / "content_id_to_nwb_file.jsonl"
    with output_file_path.open(mode="w") as file_stream:
        file_stream.writelines(f"{json.dumps(record)}\n" for record in records)


if __name__ == "__main__":
    default_base_directory = pathlib.Path(__file__).parent.parent

    parser = argparse.ArgumentParser(description="Update the content-id-to-nwb-file DANDI cache.")
    parser.add_argument(
        "--base-directory",
        type=pathlib.Path,
        default=default_base_directory,
        help=(
            "The directory containing the `sourcedata` and `derivatives` directories. "
            "Set to the mounted dataset path when run inside the pipeline container; "
            "defaults to the repository root."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Optional cap on the number of input records scanned in this run. Intended for "
            "fast, bounded test and debug runs; production runs leave it unset and recompute "
            "the full subset."
        ),
    )
    args = parser.parse_args()

    _run(base_directory=args.base_directory, limit=args.limit)
