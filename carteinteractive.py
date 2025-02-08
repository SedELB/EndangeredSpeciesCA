from pygbif import species
from pygbif import occurrences
import pandas as pd


dfanimaux = pd.read_csv('animals.csv', encoding='ISO-8859-1', skiprows=2)
dfanimaux = dfanimaux.drop(dfanimaux.columns[[4,5,6,7,9,10]], axis='columns')
dfanimaux = dfanimaux.dropna()

def obtenir_carte(index):
    taxon = species.name_backbone(name=dfanimaux['Nom scientifique'].iloc[index])
    taxon_id = taxon.get("usageKey", None)


