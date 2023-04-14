# Tabeval
Outil pour produire des rapports sur la distributions de valeurs dans des données tabulaires.

Le script prend les paramètres suivants :
* `source_donnees` : le chemin vers le fichier de données tabulaire à analyser.
* `rapport_nom` : le nom à donner au dossier qui contiendra les rapports générés.
* `seuil_analyse` (facultatif) : Pour chaque colonne du fichier à analyser, le rapport principal en énumère toutes les valeurs uniques si le nombre de valeurs uniques égales à ou en-dessous de ce chiffre. La valeur par défaur est 15.

Par exemple, la commande `python -m tabeval fichiertabulaire.csv fichiertabulaire -sa 10` analyserait le fichier `donnees/fichiertabulaire.csv`, produisant les rapports dans le répertoire `rapports/fichiertabulaire`, énumérant les valeurs uniques de chaque colonne avec 10 valeurs ou moins.