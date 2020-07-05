from sys import argv
from pathlib import Path
from csv import writer
import requests
from requests.auth import HTTPBasicAuth
import os
import subprocess

from pydriller import RepositoryMining
from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from git import Repo, Git


def summarize(d):
    if d == None:
        return None
    return sum(list(d.values()))


def getValue(v):
    return next((metric["value"] for metric in sq if metric["metric"] == v), None)


def getCommit(commit, i):
    c = commit
    for x in range(i+1):
        try:
            c = c.parents[0]
        except:
            return False
    return c.hexsha


Path("./repo").mkdir(parents=True, exist_ok=True)

# Form github urls
urls = list(map(lambda u: "https://github.com/"+u+".git", argv[2:]))
# Setup CSV Writer
with open('data.csv', 'w', newline='', buffering=1) as csvfile:
    csv = writer(csvfile)
    csv.writerow(['project', 'hash', 'msg', 'author', 'committer', 'author_date', 'commit_date',
                  'dmm_unit_size', 'dmm_unit_complexity', 'dmm_unit_interfacing',
                  '# Churn', '# Churn (over 3)', '# Churn (over 5)',
                  '# Lines addded', '# Lines added (over 3)', '# Lines added (over 5)',
                  '# Lines removed', '# Lines removed (over 3)', '# Lines removed (over 5)',
                  '# Hunks count', '# Files committed', '# Contributors committed (over 3)', '# Contribuitors committed (over 5)',
                  'Complexity', '% Comments', '% Duplicated lines', 'SQALE', 'Coverage'
                  ])
    # Traverse commits
    project = argv[2].split("/")[1]
    for commit in RepositoryMining(urls, clone_repo_to="./repo").traverse_commits():
        c = Repo("./repo/"+commit.project_name).commit(commit.hash)
        previousCommit = getCommit(c, 1)
        thirdCommit = getCommit(c, 3)
        fifthCommit = getCommit(c, 5)
        print(commit.hash)
        print(previousCommit)
        print(thirdCommit)
        print(fifthCommit)
        g = Git("./repo/"+commit.project_name)
        g.checkout(commit.hash)
        churn = LinesCount(path_to_repo=commit.project_path, from_commit=previousCommit,
                           to_commit=commit.hash).count() if previousCommit else None
        churn3 = LinesCount(path_to_repo=commit.project_path,
                            from_commit=thirdCommit, to_commit=commit.hash).count() if thirdCommit else None
        churn5 = LinesCount(path_to_repo=commit.project_path,
                            from_commit=fifthCommit, to_commit=commit.hash).count() if fifthCommit else None
        added = LinesCount(path_to_repo=commit.project_path, from_commit=previousCommit,
                           to_commit=commit.hash).count_added() if previousCommit else None
        added3 = LinesCount(path_to_repo=commit.project_path,
                            from_commit=thirdCommit, to_commit=commit.hash).count_added() if thirdCommit else None
        added5 = LinesCount(path_to_repo=commit.project_path,
                            from_commit=fifthCommit, to_commit=commit.hash).count_added() if fifthCommit else None
        removed = LinesCount(path_to_repo=commit.project_path,
                             from_commit=previousCommit, to_commit=commit.hash).count_removed() if previousCommit else None
        removed3 = LinesCount(path_to_repo=commit.project_path,
                              from_commit=thirdCommit, to_commit=commit.hash).count_removed() if thirdCommit else None
        removed5 = LinesCount(path_to_repo=commit.project_path,
                              from_commit=fifthCommit, to_commit=commit.hash).count_removed() if fifthCommit else None
        hunks = HunksCount(path_to_repo=commit.project_path, from_commit=previousCommit,
                           to_commit=commit.hash).count() if previousCommit else None
        files = len(commit.modifications)
        contributors3 = ContributorsCount(
            path_to_repo=commit.project_path, from_commit=thirdCommit, to_commit=commit.hash).count() if thirdCommit else None
        contributors5 = ContributorsCount(
            path_to_repo=commit.project_path, from_commit=fifthCommit, to_commit=commit.hash).count() if fifthCommit else None
        # Execute sonarqube
        code = subprocess.run('sonar-scanner -D"sonar.projectKey=sonarqube" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login='+argv[1]+'"',
                              cwd="./repo/"+commit.project_name, shell=True)
        res = requests.get(
            "http://localhost:9000/api/measures/component?component=sonarqube&metricKeys=cognitive_complexity,comment_lines_density,duplicated_lines_density,sqale_index,coverage", auth=HTTPBasicAuth(argv[1], ""))
        sq = res.json()["component"]["measures"]
        complexity = getValue("cognitive_complexity")
        comments = getValue("comment_lines_density")
        lines = getValue("duplicated_lines_density")
        sqale = getValue("sqale_index")
        coverage = getValue("coverage")
        csv.writerow([commit.project_name, commit.hash, commit.msg, commit.author.email, commit.committer.email, commit.author_date, commit.committer_date,
                      commit.dmm_unit_size, commit.dmm_unit_complexity, commit.dmm_unit_interfacing,
                      summarize(churn), summarize(churn3), summarize(churn5),
                      summarize(added), summarize(added3), summarize(added5),
                      summarize(removed), summarize(
                          removed3), summarize(removed5),
                      summarize(hunks), files, summarize(
                          contributors3), summarize(contributors5),
                      complexity, comments, lines, sqale, coverage
                      ])
        project = commit.project_name
