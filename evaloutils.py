import pandas as pd
from pathlib import Path
import re

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

def stripc(cell):
    if isinstance(cell, str):
        return cell.strip()
    else:
        return cell

def stripconcec(cell):
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