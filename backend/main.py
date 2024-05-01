import time
import boto3
import base64
import random
import string
import geopandas as gpd
from fastapi import FastAPI
from fastapi_cors import CORS
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="ams3",
    endpoint_url="https://gpkgtogeojson.ams3.digitaloceanspaces.com",
    aws_access_key_id="DO00YK8Y48BFHJCC7FHD",
    aws_secret_access_key="25wJqah30+32XsbMzVsZKa5MUY8iELfhwgU99lU1SGk",
)

origins = [
    "https://www.gpkgtogeojson.com",
    "https://gpkgtogeojson.com",
    "https://www.gpkgtogeojson.com/gpkg",
    "https://gpkgtogeojson.com/gpkg",
    "https://gpkgtogeojson-frontend.fly.dev",
    # "http://localhost:5173" # local dev
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

    client.upload_file(
        "src.gpkg",
        "uploaded_files",
        f"src_{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}_{int(time.time()*1000)}.gpkg",
    )
    gpd.read_file("src.gpkg").to_file("dst.geojson", driver="GeoJSON", engine="pyogrio")

    return FileResponse("dst.geojson")


@app.get("/")
async def read_root():
    return FileResponse("index.html")
