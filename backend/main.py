import base64
import geopandas as gpd
from fastapi import FastAPI
from fastapi_cors import CORS
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://www.gpkgtogeojson.com/","https://gpkgtogeojson.com/"]

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

    gpd.read_file("src.gpkg").to_file("dst.geojson",driver="GeoJSON",engine="pyogrio")

    return FileResponse("dst.geojson")

@app.get("/")
async def read_root():
    return FileResponse("index.html")
