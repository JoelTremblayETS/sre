import csv
from datetime import datetime as dt, timedelta


"""
Code inspiré à partir du lien:
https://stackoverflow.com/questions/30067772/how-to-find-earliest-and-latest-dates-from-a-csv-file-python
Ce script permet de trouver la première date et la date la plus récente dans chacun des fichiers csv.
Une fois que le nombre de semaines est trouvé, on génère un graphe de nuage de points.
"""
with open('rootbeer_author_date.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    first = next(reader)
    earliest = dt.strptime(first['Date'].split(' ')[0], "%Y-%m-%d")
    latest = dt.strptime(first['Date'].split(' ')[0], "%Y-%m-%d")
    for row in reader:
        date = row['Date'].split(' ')[0]
        date = dt.strptime(date, "%Y-%m-%d")
        if date < earliest:
            earliest = date
        if date > latest:
            latest = date
        monday1 = (earliest - timedelta(days=earliest.weekday()))
        monday2 = (latest - timedelta(days=latest.weekday()))
        print('Weeks:', (monday2 - monday1).days / 7)
    print("Earliest date:", earliest)
    print("Latest date:", latest)
    # Le code ci-dessus est emprunté du lien :
    # https://stackoverflow.com/questions/14191832/how-to-calculate-difference-between-two-dates-in-weeks-in-python
    # Ceci permet de trouver le nombre de semaines entre la première date et la plus récente
    monday1 = (earliest - timedelta(days=earliest.weekday()))
    monday2 = (latest - timedelta(days=latest.weekday()))
    print('Weeks:', (monday2 - monday1).days / 7)
