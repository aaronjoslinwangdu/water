#!/bin/bash

set -euo pipefail
cd "$(dirname "$0")/.."
uv run mpremote cp -r ./src/ :
uv run mpremote cp ./.env :
