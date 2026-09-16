# DANDI Cache: `content-id-to-nwb-file`

A one-to-one mapping from content IDs to a single `(dandiset ID, asset path)` pair, restricted to the assets that are NWB files.

This cache is the NWB subset of [`content-id-to-usage-dandiset-path`](https://github.com/dandi-cache/content-id-to-usage-dandiset-path): each record from that upstream cache is kept when `.nwb` is one of the suffixes of its asset path, which also retains multi-suffix variants such as `.nwb.zarr`.

Updated frequently.

Primarily for use by developers.

Each line of the derivatives is a JSON object of the form:

```json
{"<content_id>": {"<dandiset_id>": "<path>"}}
```



## One-time use

If you only plan to use this cache infrequently or from disparate locations, you can directly download the latest version of the cache as a compressed [JSON Lines](https://jsonlines.org/) file from the `dist` branch:

### Python API (recommended)

```python
import gzip
import json

import requests

url = "https://raw.githubusercontent.com/dandi-cache/content-id-to-nwb-file/refs/heads/dist/derivatives/content_id_to_nwb_file.jsonl.gz"
response = requests.get(url)
lines = gzip.decompress(data=response.content).decode("utf-8").splitlines()
content_id_to_nwb_file = [json.loads(line) for line in lines]
```

### Save to file

```bash
curl https://raw.githubusercontent.com/dandi-cache/content-id-to-nwb-file/refs/heads/dist/derivatives/content_id_to_nwb_file.jsonl.gz -o content_id_to_nwb_file.jsonl.gz
```



## Repeated use

If you plan on using this cache regularly, clone the `dist` branch of this repository:

```bash
git clone --branch dist https://github.com/dandi-cache/content-id-to-nwb-file.git
```

Or, if you prefer [DataLad](https://www.datalad.org/):

```bash
datalad clone https://github.com/dandi-cache/content-id-to-nwb-file.git --branch derivatives
```

Then set up a CRON on your system to pull the latest version of the cache at your desired frequency.

For example, through `crontab -e`, add:

```bash
0 0 * * * git -C /path/to/content-id-to-nwb-file pull
```

This will minimize data overhead by only loading the most recent changes.


## How this cache is built

The orchestration, the runtime library and the CI all come from elsewhere, so this repository holds only what is specific to this cache: `cache.toml` (what it is), `code/update.py` (the filter it applies), `envs/pyproject.toml` (its dependencies, of which it has none) and the schedule in `.github/workflows/update.yml`.

The pipeline is [`dandi-cache-utils`](https://github.com/dandi-cache/dandi-cache-utils), vendored into the runtime image this cache is built `FROM`, and the workflows call the shared actions in [`dandi-cache-action`](https://github.com/dandi-cache/dandi-cache-action).
A gap in any of them is fixed there, where every cache gets the fix, rather than worked around here.
