# Technical debt at scale

This is a project for the HPI Summersemester 2020. It uses python and jupyter notebooks.

## Organization

In the analysis folder you will find all scripts related to analysing the data. Most importantly there is one for:

- Data cleaning
  - will put out a cleaned data csv. For reference of available fields look at the section cleaned data.
- Covariance analysis
  - Makes a similarity analysis for all countable properties of a commit
- Principal Component Analysis
  - Makes a PCA analysis which outputs 4 graphs for looking into the data
- Prediction
  - Makes predictions for a certain debt metric. Per default it is the "Debt Indicator". If you want to change that, please append the metric in quotes to the command e.g. : `python3 prediction.py "SQALE Delta"` For availabe metrics use the section cleaned data.

In the crwaler folder you will find the crawler. Appending an org with the repo will let you crwal that repo like so: `python3 crawler.py [Sonarqubetoken] rzwitserloot/lombok` adding multiple will crawl all of them like: `python3 [Sonarqubetoken] crawler.py rzwitserloot/lombok apache/spark`.

The literature folder holds all research done. The summary of all of this is the definition.md.

The misc folder holds all presentations held for this topic during this seminar.

Notebooks and visualizations were only for the scouting phase of the project. Those are used with a connection to the github database scheme.

## Setup

First of all you need a normal connection to the database and execute the follwing command to get a materialized view:

```
CREATE MATERIALIZED VIEW crm20.tech_debt_projects AS
SELECT ght.projects.id, ght.projects.url, ght.projects.name, ght.projects.language, ght.commits.sha, ght.commits.created_at, raw.message, raw.additions, raw.deletions
FROM ght.projects
RIGHT JOIN ght.commits ON ght.projects.id=ght.commits.project_id
INNER JOIN (select * from ght.raw_commits where message like '%technical debt%' and deletions > 100 and additions > 100) as raw ON raw.sha=ght.commits.sha;
```

Now you can spinup a jupyter notebook and open the visualization notebook to get a broad data overview. The connection string for the database is in the very top cell. Edit it to your needs. The very last cell does not get visualized as there are no needs for it.

If you want to start crawling data navigate int to the crawler folder. Before starting ensure the following. Did you install all dependcies with pip or conda: `pip install -r requirements.txt`. Additionally have an instance of sonarqube running on you localhost at port 9000. The easiest way to do this is to run a docker container: `docker run --name sonarqube -p 9000:9000 sonarqube`. If you did that install the [sonarqube cli](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/), log into the sonarqube instance with and username admin and password admin. Then create a project named "sonarqube" and generate a sonarqube token. An explanation can be found [here](https://docs.sonarqube.org/latest/setup/get-started-2-minutes/). Then execute the crawler like such: `python3 [Sonarqubetoken] crawler.py rzwitserloot/lombok apache/spark [.. more repos on github]`.
This will put out a data.csv with data to be written out.

Now you can switch to the analysis folder and let the cleaning run with `python3 cleaning.py`. Make sure you installed all requirements again using `pip install -r requirements.txt`. NOw you can run all analysis after that.

## Cleaned data

The cleaned data file contains the following data points per commit:

- project - The name of the project
- hash - The commit hash
- msg - The commit message
- author - The author email
- committer - The committer email
- author_date - The author date
- commit_date - The commit date
  DMM stands for Delta Maintainability Model and is provieded by pydriller
- dmm_unit_size - Method length in lines of code
- dmm_unit_complexity - Method cyclomatic complexity
- dmm_unit_interfacing - Method number of parameters
- \# Churn - Deleted lines + Added Lines since last commit
- \# Churn (over 3) - Deleted lines + Added Lines in the last three commits, excluding the last one
- \# Churn (over 5) - Deleted lines + Added Lines in the last five commits, excluding the last three commits
- \# Lines added - Added Lines in the last commit
- \# Lines added (over 3) - Added Lines in the last last three commits, excluding the last one
- \# Lines added (over 5) - Added Lines in the last five commits, excluding the last three commits
- \# Lines removed - Deleted lines in the last commit
- \# Lines removed (over 3) - Deleted lines in the last three commits, excluding the last one
- \# Lines removed (over 5) - Deleted lines in the last five commits, excluding the last three commits
- \# Hunks count - How many code bloacks have been chaged since the last commit
- \# Files committed - In the last commit
- \# Contributors committed (over 3) - in the last three commits, excluding the last one
- \# Contributors committed (over 5) -in the last five commits, excluding the last three commits
- Complexity - Calculated cognitive complexity from sonarqube
- % Comments - Calculated lines by sonarqube
- % Duplicated lines - Calculated by sonarqube
- SQALE - Code Dabt metric calculated by sonarqube
- Coverage - Testcoverage as caluclated by sonarqube
- SQALE Delta - SQALE change in this commit
- Complexity Delta - Complexity change in this commit
- % Comments Delta - Comments change in this commit
- % Duplicated lines Delta - Duplaicated lines changed in this commit
- Debt Indicator - -1 SQALE lower as before, 0 equal and 1 higher as before
