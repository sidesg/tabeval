#!/usr/local/bin/python3

from pathlib import Path
import evaloutils as eo
import pandas as pd
import numpy as np
import re
import yaml

with open("config.yaml", "r", encoding="utf8") as infile:
    try:
        confdict = yaml.safe_load(infile)
    except:
        print('Erreur de changement des paramètres.')

SOURCEPATH = Path("donnees") / confdict["source_donnees"]

OUTPATH = Path("rapports") 
NAMEROOT = confdict["rapport_nom"]
RAPPATH = OUTPATH / NAMEROOT

SEUL_ANAL = confdict["seuil_analyse"]

if not RAPPATH.exists():
    RAPPATH.mkdir()

donneesdf = eo.tab_imp(SOURCEPATH)

donneesdf.applymap(eo.strip_if_str)
donneesdf.applymap(eo.concatescpaces_if_str)

donneedict = {
    "colname": [], 
    "nb_nonvide": [],
    "pourcent_nonvide": [],
    "nb_valUniques": [],
    "valUniques": [],
    "min": [],
    "max": []
}

for col, ser in donneesdf.iteritems():
    pnonvide = round((len(ser.dropna()) / len(ser)) * 100, 2)

    donneedict["nb_nonvide"].append(len(ser.dropna()))
    donneedict["pourcent_nonvide"].append(pnonvide)
    donneedict["colname"].append(col)
    donneedict["nb_valUniques"].append(ser.nunique())

    #Rapport de colonne iff 1 valeur unique:1 ligne
    if ser.dropna().nunique() != len(ser):
        colname = re.sub(r"\/", "-", col)
        coldf = ser.value_counts().reset_index()
        coldf = coldf.rename(columns={"index": col, col: "nombre"})
        coldf.to_csv(
                RAPPATH / (f"{NAMEROOT}-{colname}.csv"),
                index=False
        )

    if ser.nunique() > SEUL_ANAL:
        donneedict["valUniques"].append("")

    elif ser.nunique() <= SEUL_ANAL:
        valcounts = ser.dropna().value_counts()
        valcounts = valcounts.reset_index().sort_values(by=col, ascending=False)
        valcounts = valcounts["index"].astype(str) + " : " + valcounts[col].astype(str)
        valcounts = [val for val in valcounts]

        donneedict["valUniques"].append(", ".join(valcounts))
    else:
        donneedict["valUniques"].append("")

    if ser.dtype == np.float64 or ser.dtype == np.int64:
        donneedict["max"].append(ser.max())
        donneedict["min"].append(ser.min())
    else:
        donneedict["max"].append("")
        donneedict["min"].append("")


outdf = pd.DataFrame(data=donneedict).sort_values(
    by=["pourcent_nonvide", "nb_valUniques"], 
    ascending=False
)


outdf.to_csv(
    RAPPATH / f"{NAMEROOT}.csv", 
    index=False    
)