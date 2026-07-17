import geopandas as gpd

file = "../data/geo/mys_admin_boundaries/mys_admin1.geojson"

gdf = gpd.read_file(file)

print(gdf["adm1_name"].tolist())