#!/usr/local/bin/python3

from pathlib import Path
import pandas as pd
import numpy as np
import re
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Nom du fichier à analyser dans /donnees.", type=str)
    parser.add_argument("destination", help="Nom du dossier dans /rapports où l'analyse est enregistrée.", type=str)
    parser.add_argument("--seuil_analyse", "-sa", type=int)
    
    args = parser.parse_args()

    SOURCEPATH = Path("donnees") / args.source

    OUTPATH = Path("rapports") 
    NAMEROOT = args.destination
    RAPPATH = OUTPATH / NAMEROOT

    SEUL_ANAL = args.seuil_analyse if args.seuil_analyse else 15

    if not RAPPATH.exists():
        RAPPATH.mkdir()

    donneesdf = tab_imp(SOURCEPATH)

    donneesdf.applymap(strip_if_str)
    donneesdf.applymap(concatescpaces_if_str)

    donneedict = {
        "colname": [], 
        "nb_nonvide": [],
        "pourcent_nonvide": [],
        "min": [],
        "max": [],
        "nb_valUniques": [],
        "valUniques": []
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
        print("Ce fichier n'existe pas.")
        exit()
        
    match path.suffix:
        case ".csv":
            try:
                return pd.read_csv(path, low_memory=False)
            except:
                return pd.read_csv(path, sep=";", low_memory=False)
        
        case ".tsv":
            try:
                return pd.read_csv(path, sep="\t", low_memory=False)
            except:
                return pd.read_csv(path, sep="\t", encoding="cp1252", low_memory=False)
        
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

if __name__ == "__main__":
    main()