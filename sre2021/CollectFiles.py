import json
from pip._vendor import requests
import csv


# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            if ct == len(lstTokens):
                ct = 0
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/{repo}/commits?page={page}'.format(repo=repo, page=spage)
            tokenHeader = 'token {}'.format(lsttokens[ct])

            ct += 1
            content = requests.get(
                commitsUrl,
                headers={
                    'authorization': tokenHeader
                }
            )

            jsonCommits = json.loads(content.content)
            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in a page
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                if ct == len(lstTokens):
                    ct = 0
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/{repo}/commits/{sha}'.format(repo=repo, sha=sha)
                shaTokenHeader = 'token {}'.format(lsttokens[ct])

                ct += 1
                content = requests.get(
                    shaUrl,
                    headers={
                        'authorization': shaTokenHeader
                    }
                )
                shaDetails = json.loads(content.content)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if '/src/' in filename:
                        extensionList = ['.png', '.gif', '.xml', '.md', '.snap', '.ico', '.xcf', '.jar']
                        if not [ele for ele in extensionList if (ele in filename)]:
                            print(filename)
                            dictfiles[filename] = dictfiles.get(filename, 0) + 1
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


# lstRepos = ['scottyab/rootbeer',
#             'PeterIJia/android_xlight',
#             'Skyscanner/backpack',
#             'mendhak/gpslogger',
#             'k9mail/k-9']
lstRepos = ['mendhak/gpslogger',
            'k9mail/k-9']

# put your tokens here
lstTokens = ['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',
             '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']

for repo in lstRepos:
    dictfiles = dict()
    countfiles(dictfiles, lstTokens, repo)
    print('Total number of files: ' + str(len(dictfiles)))

    file = repo.split('/')[1]
    # change this to the path of your file
    fileOutput = file + '.csv'
    rows = ["Filename", "Touches"]
    fileCSV = open(fileOutput, 'w')
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        writer.writerow(rows)
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename
    fileCSV.close()
    print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
