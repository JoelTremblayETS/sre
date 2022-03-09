import csv
from pydriller import Repository

# lstFiles = ['rootbeer.csv',
#             'backpack.csv',
#             'gpslogger.csv',
#             'k-9.csv']
lstFiles = ['k-9.csv']

# lstRepos = ['https://github.com/scottyab/rootbeer.git',
#             'https://github.com/Skyscanner/backpack.git',
#             'https://github.com/mendhak/gpslogger.git',
#             'https://github.com/k9mail/k-9.git']
lstRepos = ['https://github.com/k9mail/k-9.git']
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
