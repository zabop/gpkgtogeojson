import geopandas as gpd
import pandas as pd
import pyogrio
import boto3

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="ams3",
    endpoint_url="https://ams3.digitaloceanspaces.com",
    aws_access_key_id="DO00YK8Y48BFHJCC7FHD",
    aws_secret_access_key="25wJqah30+32XsbMzVsZKa5MUY8iELfhwgU99lU1SGk",
)

keys = [e["Key"] for e in client.list_objects_v2(Bucket="gpkgtogeojson")["Contents"]]

for i, key in enumerate(keys[-3:]):
    print(key)
    try:
        dst = key.split("/")[-1]
        client.download_file("gpkgtogeojson", key, dst)

        layernames = [
            layername for layername, _ in pyogrio.list_layers(dst)
        ]

        print(f"layernames: {layernames}")
        dfs = [gpd.read_file(dst, layername=layername) for layername in layernames]
        united=gpd.GeoDataFrame(pd.concat([df.to_crs(4326) for df in dfs]))
        united.to_file(f"layersUnited{i}.geojson",engine="pyogrio",layer_options={"COORDINATE_PRECISION": 8})
    except Exception as e:
        print(e)
    print("########")