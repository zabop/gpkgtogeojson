import boto3

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="ams3",
    endpoint_url="https://ams3.digitaloceanspaces.com",
    aws_access_key_id="DO00YK8Y48BFHJCC7FHD",
    aws_secret_access_key="25wJqah30+32XsbMzVsZKa5MUY8iELfhwgU99lU1SGk",
)

client.upload_file("dst.mbtiles", "gpkgtogeojson", "usageviz/dst.mbtiles")