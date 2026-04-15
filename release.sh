#!/usr/bin/env bash

TOOL_RUN="uv run"

function bump {
  NEW_VERSION="$(${TOOL_RUN} bump-my-version show --increment "$1" new_version)"
  ${TOOL_RUN} cz changelog --file-name changelog.md --unreleased-version="v${NEW_VERSION}"
  git add changelog.md && git commit -m "Update changelog.md for v${NEW_VERSION}"
  ${TOOL_RUN} bump-my-version bump "$1" --allow-dirty
}


bump $@