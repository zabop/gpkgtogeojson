#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

python3 main.py
tippecanoe -o dst.mbtiles -zg layersUnited*.geojson
gcloud storage cp dst.mbtiles gs://gpkgviz/dst.mbtiles