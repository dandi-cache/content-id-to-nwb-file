# syntax=docker/dockerfile:1

# The pinned runtime environment for this cache.
#
# Everything shared comes from the base image: Debian, git-annex, the virtual environment, the
# `dandi_cache_utils` library that `code/update.py` imports, and the vendored `update_pipeline.sh`
# that CI extracts and runs on the runner.
#
# This cache has no processing dependencies of its own. It reads one JSON Lines file and filters
# it, which the standard library and the base image already cover, so there is nothing to install
# here beyond what the base provides.
#
# The image holds only the environment, not this cache's code. The code is mounted at run time, so
# a single image serves any revision of it.
FROM ghcr.io/dandi-cache/dandi-cache-utils:latest

# The source label associates the image on the GitHub Container Registry with this repository.
LABEL org.opencontainers.image.source="https://github.com/dandi-cache/content-id-to-nwb-file"
LABEL org.opencontainers.image.description="The pinned runtime environment for the DANDI Cache content-id-to-nwb-file update pipeline."

CMD ["python", "--version"]
