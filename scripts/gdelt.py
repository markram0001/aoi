import requests
import os
import pandas as pd
from zipfile import ZipFile
from io import BytesIO

BASE_URL = "http://data.gdeltproject.org/gdeltv2"
DATA_DIR = "data/gdelt_raw"
NROWS = 100

os.makedirs(DATA_DIR, exist_ok=True)

# Get latest GKG file
resp = requests.get(f"{BASE_URL}/lastupdate.txt", timeout=30)
resp.raise_for_status()

gkg_url = None
for line in resp.text.strip().split("\n"):
    if ".gkg.csv.zip" in line.lower():
        gkg_url = line.split(" ")[2]
        break

if gkg_url is None:
    raise RuntimeError("No GKG file found")

zip_resp = requests.get(gkg_url, timeout=60)
zip_resp.raise_for_status()

zip_path = os.path.join(DATA_DIR, os.path.basename(gkg_url))
with open(zip_path, "wb") as f:
    f.write(zip_resp.content)

# Extract first 100 rows
with ZipFile(BytesIO(zip_resp.content)) as z:
    csv_name = z.namelist()[0]
    with z.open(csv_name) as f:
        df = pd.read_csv(
            f,
            sep="\t",
            header=None,
            nrows=NROWS,
            low_memory=False
        )

out_csv = zip_path.replace(".zip", f".first_{NROWS}.csv")
df.to_csv(out_csv, index=False)

print("Saved sample:", out_csv)
print("Shape:", df.shape)
