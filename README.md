![CI](https://github.com/ltpitt/python-playwright-fastapi-9292-data-fetcher/workflows/CI/badge.svg)
[![GitHub Issues](https://img.shields.io/github/issues-raw/ltpitt/python-playwright-fastapi-9292-data-fetcher)](https://github.com/ltpitt/python-playwright-fastapi-9292-data-fetcher/issues)
![Total Commits](https://img.shields.io/github/last-commit/ltpitt/python-playwright-fastapi-9292-data-fetcher)
![GitHub commit activity](https://img.shields.io/github/commit-activity/4w/ltpitt/python-playwright-fastapi-9292-data-fetcher?foo=bar)
[![License](https://img.shields.io/badge/license-GPL-blue.svg)](https://opensource.org/licenses/GPL-3.0)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

# 9292 Travel Data Fetcher
> An API built with FastAPI and Playwright to fetch travel data from [9292.nl](https://9292.nl).

## Pre-requisites
* Python: [installation instructions](https://www.python.org/downloads/).
* Python Pip: it should be available in your Python install. If not, here's [installation instructions](https://pip.pypa.io/en/stable/installing/).
* Node.js and npm: required for Playwright. Install from [here](https://nodejs.org/).

## How to install

Once Python, Pip, and Node.js are installed:

```bash
$ git clone https://github.com/ltpitt/python-playwright-fastapi-9292-data-fetcher.git
$ cd python-playwright-fastapi-9292-data-fetcher
$ pip install -r requirements.txt
$ python -m playwright install
```

## How to run

To run the FastAPI app:

```bash
$ uvicorn app.main:app --reload
```

Then access the API's Swagger at `http://127.0.0.1:8000/docs`.

Data can be fetched with from the API at `http://127.0.0.1:8000/travel-data?start=START&start_id=START_ID&destination=DESTINATION&destination_id=DESTINATION_ID`

Replace `START`, `START_ID`, `DESTINATION`, and `DESTINATION_ID` with actual values retrieved from 9292.nl.

## Usage

Here's how to use the API:

```bash
$ curl -X 'GET' \
  'http://127.0.0.1:8000/travel-data?start=Amsterdam&start_id=amsterdam_central&destination=Utrecht&destination_id=utrecht_central' \
  -H 'accept: application/json'
```

## Contribution guidelines

* If you have any ideas or suggestions, contact the Repo Owner

## Who do I talk to?

* ltpitt: Repo Owner
