import time
import boto3
import base64
import random
import string
import pyogrio
import pandas as pd
import geopandas as gpd
from fastapi import FastAPI
from fastapi_cors import CORS
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://www.gpkgtogeojson.com",
    "https://gpkgtogeojson.com",
    "https://www.gpkgtogeojson.com/gpkg",
    "https://gpkgtogeojson.com/gpkg",
    "https://gpkgtogeojson-frontend.fly.dev",
    #"*" # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GPKG(BaseModel):
    name: str
    base64src: str


@app.post("/gpkg")
async def create_item(gpkg: GPKG):
    decoded_bytes = base64.b64decode(gpkg.base64src)
    with open("src.gpkg", "wb") as f:
        f.write(decoded_bytes)

    layernames = [
        layername for layername, _ in pyogrio.list_layers("src.gpkg")
    ]
    dfs = [gpd.read_file("src.gpkg", layer=layername) for layername in layernames]
    united = gpd.GeoDataFrame(
        pd.concat([df.to_crs(4326) if df.crs is not None else df for df in dfs])
    )
    united.to_file("dst.geojson", driver="GeoJSON", engine="pyogrio")

    return FileResponse("dst.geojson")


@app.get("/")
async def read_root():
    return FileResponse("index.html")
