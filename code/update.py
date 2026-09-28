"""Update the content-id-to-nwb-file DANDI cache.

Subset the upstream `content-id-to-usage-dandiset-path` cache to the entries whose asset path
names an NWB file. It is a string test over a file already in hand: no network, no state, nothing
to resume, and the whole subset is recomputed in the time it takes to read the input.

That is why this cache declares no limit while every other one does. A limit says how much of a
backlog one run works through, and there is no backlog here -- each run does all of the work there
is. `--testing` therefore changes only where the output is written.

Everything shared with the other caches -- the argument parsing, the logging, the output paths,
and testing mode -- comes from `dandi_cache_utils`, which the runtime image carries.
"""

import dandi_cache_utils as dandi_cache


def names_an_nwb_file(record: dict, /) -> bool:
    """Whether one upstream record's asset path names an NWB file.

    The upstream records are `{content_id: {dandiset_id: path}}`, one per line.
    """
    ((_content_id, usage_dandiset_path),) = record.items()
    ((_dandiset_id, path),) = usage_dandiset_path.items()
    return dandi_cache.nwb.is_nwb_path(path)


def main() -> None:
    dataset, _arguments = dandi_cache.open_dataset()
    usage_dandiset_paths = dataset.read_input()

    dandi_cache.run_full_rebuild(
        dataset,
        build=lambda: [record for record in usage_dandiset_paths if names_an_nwb_file(record)],
    )


if __name__ == "__main__":
    main()
