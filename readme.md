# Tabeval
Outil pour produire des rapports sur la distributions de valeurs dans des données tabulaires.

Config.yaml contient les variables suivantes :
* `source_donnees` : le chemin vers le fichier de données tabulaire à analyser.
* `rapport_nom` : le nom à donner au dossier qui contiendra les rapports générés.
* `seuil_analyse` : Pour chaque colonne du fichier à analyser, le rapport principal en énumère toutes les valeurs uniques si le nombre de valeurs uniques en en-dessous de ce chiffre.