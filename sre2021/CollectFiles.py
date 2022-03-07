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
lstRepos = ['Skyscanner/backpack',
            'mendhak/gpslogger',
            'k9mail/k-9']

# put your tokens here
lstTokens = ['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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
             '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',
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
