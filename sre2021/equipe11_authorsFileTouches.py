import csv
from pydriller import Repository


"""
Ce script analyse les fichiers .csv générés par CollectFiles.py. En utilisant PyDriller, on cherche le nom d'auteur
et la date de modification de chaque fichier. Un fichier *_author_date.csv est généré pour chaque repo afin d'afficher
le nom du développeur et la date de modification. Ce fichier est utile pour générer le graphe de nuage de points.
"""
lstFiles = ['rootbeer.csv',
            'backpack.csv',
            'gpslogger.csv',
            'k-9.csv']

lstRepos = ['https://github.com/scottyab/rootbeer.git',
            'https://github.com/Skyscanner/backpack.git',
            'https://github.com/mendhak/gpslogger.git',
            'https://github.com/k9mail/k-9.git']
index = 0
for sourceFile in lstFiles:
    while index < len(lstRepos):
        with open(sourceFile, newline='') as csvfile:
            file = sourceFile.split('.')[0]
            fileOutput = file + '_author_date.csv'
            rows = ["Author", "Date"]
            fileCSV = open(fileOutput, 'w')
            writer = csv.writer(fileCSV)
            writer.writerow(rows)
            reader = csv.DictReader(csvfile)
            for row in reader:
                for commit in Repository(lstRepos[index], filepath=row['Filename']).traverse_commits():
                    rows = [commit.author.name, commit.author_date]
                    writer.writerow(rows)  # Ajouter le nom d'auteur et la date de modification dans le fichier csv
            fileCSV.close()
        index += 1
