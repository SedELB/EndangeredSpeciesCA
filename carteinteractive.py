from pygbif import species
from pygbif import occurrences
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd

dfanimaux = pd.read_csv('animals.csv', encoding='ISO-8859-1', skiprows=2)
dfanimaux = dfanimaux.drop(dfanimaux.columns[[4, 5, 6, 7, 9, 10]], axis='columns')
dfanimaux = dfanimaux.dropna()

def obtenir_carte(index):
    nom_scientifique = dfanimaux['Nom scientifique'].iloc[index]
    
    taxon = species.name_backbone(name=nom_scientifique)
    taxon_id = taxon.get("usageKey", None)
    
    if not taxon_id:
        print(f"Taxon pour {nom_scientifique} non trouvé.")
        return
    
    obs = occurrences.search(taxonKey=taxon_id, country="CA", limit=100)
    
    df_observations = pd.DataFrame(obs["results"])
    
    if df_observations.empty:
        print(f"Aucune observation trouvée pour {nom_scientifique}.")
        return
    
    
    geometry = [Point(xy) for xy in zip(df_observations['decimalLongitude'], df_observations['decimalLatitude'])]
    
  
    gdf = gpd.GeoDataFrame(df_observations, geometry=geometry, crs="EPSG:4326")
    
  
    gdf = gdf.to_crs(epsg=3857)
    
  
    fig, ax = plt.subplots(figsize=(8, 8))
    

    ax.set_xlim(-1.5e7, -0.5e7)
    ax.set_ylim(5e6, 1.2e7)
    

    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=4)
    
    gdf.plot(ax=ax, marker='o', markersize=50, alpha=0.7, color='red')
    

    ax.set_title(f"Observations de {nom_scientifique} au Canada")
    
    ax.set_axis_off()
    
    plt.show()
