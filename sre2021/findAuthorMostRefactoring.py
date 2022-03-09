import csv
import json
from collections import defaultdict
from pydriller import Repository


"""
Ce script génère un fichier developer_most_refactorings.csv qui affiche les développeurs ayant effectué des
opérations de refactorings. On compte le nombre de fois que le nom d'un dévelopeur apparaît après chaque analyse
de commit avec PyDriller.
"""
with open('output.json') as json_file:
    data = json.load(json_file)
    rows = ["Developer", "Count"]
    fileCSV = open('developer_most_refactorings.csv', 'w')
    writer = csv.writer(fileCSV)
    writer.writerow(rows)
    name_dict = defaultdict(list)
    count_dict = defaultdict(int)

    for item in data['commits']:
        if item.get('refactorings'):
            for commit in Repository("https://github.com/hscrocha/jpacman.git",
                                     single=item.get('sha1')).traverse_commits():
                if commit.committer.name in name_dict.values():
                    count_dict[commit.committer.name] += 1
                else:
                    name_dict["developer"].append(commit.committer.name)
                    count_dict[commit.committer.name] += 1
    items = count_dict.items()
    for item in items:
        rows = [item[0], item[1]]
        writer.writerow(rows)
    fileCSV.close()
