from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import requests

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
AZURE_MAP_KEY = os.getenv("AZURE_MAP_KEY")


def convertGeometryToPoint(row: pd.core.series.Series) -> Point:
    if row.get("geometry"):
        return gpd.GeoSeries(Point())

    query = row["address"]
    url = f"https://atlas.microsoft.com/geocode?api-version=2022-02-01-preview&subscription-key={AZURE_MAP_KEY}&query={query}"
    response = requests.get(url)
    geojson = response.json()
    coordinates = geojson["features"][0]["geometry"]["coordinates"]

    if len(coordinates):
        return Point(coordinates[0], coordinates[1])
    else:
        return Point()
