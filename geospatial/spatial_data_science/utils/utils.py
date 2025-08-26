from shapely.geometry import Point
import geopandas as gpd
import pandas as pd


def replace_column_by_geometry_column(
    df: pd.DataFrame, coord_columns: list
) -> gpd.GeoDataFrame:
    # Create a GeoDataFrame from the original DataFrame
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[coord_columns[0]], df[coord_columns[1]])
    )
    # Drop the original coordinate columns
    gdf = gdf.drop(columns=coord_columns)
    return gdf
