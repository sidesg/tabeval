#!/usr/local/bin/python3

from pathlib import Path
import pandas as pd
import numpy as np
import re
import yaml


def main():
    confdict = ouvrir_config()

    SOURCEPATH = Path("donnees") / confdict["source_donnees"]

    OUTPATH = Path("rapports") 
    NAMEROOT = confdict["rapport_nom"]
    RAPPATH = OUTPATH / NAMEROOT

    SEUL_ANAL = confdict["seuil_analyse"]

    if not RAPPATH.exists():
        RAPPATH.mkdir()

    donneesdf = tab_imp(SOURCEPATH)

    donneesdf.applymap(strip_if_str)
    donneesdf.applymap(concatescpaces_if_str)

    donneedict = {
        "colname": [], 
        "nb_nonvide": [],
        "pourcent_nonvide": [],
        "nb_valUniques": [],
        "valUniques": [],
        "min": [],
        "max": []
    }

    for col, ser in donneesdf.items():
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


def tab_imp(path:Path) -> pd.DataFrame:
    '''
    Ouvrir un fichier de données tabulaires et rendre un DataFrame
    '''
    if not path.exists():
        print("Fichier n'existe pas.")
        exit()
        
    match path.suffix:
        case ".csv":
            try:
                return pd.read_csv(path)
            except:
                return pd.read_csv(path, sep=";")
        
        case ".tsv":
            try:
                return pd.read_csv(path, sep="\t")
            except:
                return pd.read_csv(path, sep="\t", encoding="cp1252")
        
        case ".xlsx":
            return pd.read_excel(path).applymap(excelnewline)
        
        case _:
            raise RuntimeError("Extention de fichier non reconnue.")

def strip_if_str(cell):
    if isinstance(cell, str):
        return cell.strip()
    else:
        return cell

def concatescpaces_if_str(cell):
    if isinstance(cell, str):
        return re.sub(r"\s+", " ", cell)
    else:
        return cell

def strlower(cell):
    if isinstance(cell, str):
        return cell.lower()
    else:
        return cell    

def excelnewline(cell):
    if isinstance(cell, str):
        return re.sub(r"_x000d_", "\n", cell)
    else:
        return cell

def ouvrir_config() -> dict | None:
    with open("config.yaml", "r", encoding="utf8") as infile:
        try:
            return yaml.safe_load(infile)
        except:
            print('Erreur de changement des paramètres.')


if __name__ == "__main__":
    main()