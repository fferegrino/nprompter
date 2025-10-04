#!/usr/bin/env bash

TOOL_RUN="uv run"

function bump {
  NEW_VERSION=`${TOOL_RUN} bumpversion --allow-dirty --dry-run --list $1 | grep new_version | sed -r s,"^.*=",,`
  ${TOOL_RUN} cz changelog --file-name changelog.md --unreleased-version="v${NEW_VERSION}"
  git add changelog.md && git commit -m "Update changelog.md for v${NEW_VERSION}"
  ${TOOL_RUN} bumpversion $1
}


bump $@