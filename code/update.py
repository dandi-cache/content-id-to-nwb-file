"""Update the content-id-to-nwb-file DANDI cache.

Subset the upstream `content-id-to-usage-dandiset-path` cache to the entries whose asset path
names an NWB file. This is a pure filter over its input with nothing to resume, so it recomputes
the whole subset each run rather than accumulating.

Everything shared with the other caches -- the argument parsing, the logging, the batch cap, the
output paths, and testing mode -- comes from `dandi_cache_utils`, which the runtime image carries.
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
    dataset, arguments = dandi_cache.open_dataset()
    usage_dandiset_paths = dataset.read_input()

    dandi_cache.run_full_rebuild(
        dataset,
        build=lambda: [record for record in usage_dandiset_paths if names_an_nwb_file(record)],
        limit=dandi_cache.effective_limit(testing=dataset.testing, limit=arguments.limit),
    )


if __name__ == "__main__":
    main()
