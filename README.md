# BOE_tabulator
Reads PDFs from Baltimore's archive of minutes from the Board of Estimates and places the data in a searchable table.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Fetching the Data](#fetching-the-data)
- [Usage](#usage)
- [Contributing](#contributing)

## Overview
This is where the project overview will go  

## Getting Started
Follow the steps below to recreate the development environment necessary to start contributing to this project

### Prerequisites
- Python version 3.6 or later

In order to check which version of python you have installed, run the following command in your command line (for Mac/Linux)

>**NOTE:** in all of the code blocks below, lines preceded with `$` indicate commands you should enter in your command line (excluding the `$` itself), while lines preceded with `>` indicate the expected output from the previous command.

```
$ python --version
```
The output should look something like this:
```
> Python 3.7.7
```
If you don't have Python version 3.6 or later installed on your computer, consider using [pyenv](https://github.com/pyenv/pyenv) to install and manage multiple versions of Python concurrently.

### Installation
1. Fork the repo -- for more information about forking, reference [this guide](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/working-with-forks)
1. Clone your forked repo on your local machine:
   ```
   $ git clone https://github.com/YOUR_USERNAME/BOE_tabulator.git
   ```
1. Move into the directory created when you cloned the repo:
   ```
   $ cd BOE_tabulator/
   ```
1. [Configure the upstream repository](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork) for your local fork:
   ```
   $ git remote add upstream https://github.com/department-of-general-services/BOE_tabulator.git
   ```
1. Confirm that the upstream repo has been set correctly
   ```
   $ git remote -v
   > origin    https://github.com/YOUR_USERNAME/BOE_tabulator.git (fetch)
   > origin    https://github.com/YOUR_USERNAME/BOE_tabulator.git (push)
   > upstream  https://github.com/department-of-general-services/BOE_tabulator.git (fetch)
   > upstream  https://github.com/department-of-general-services/BOE_tabulator.git (push)
   ```
1. Create a new virtual environment in your local directory
   ```
   $ python -m venv env
   ```
1. Activate your virtual environment
   ```
   $ source env/bin/activate
   ```
1. Install necessary python packages
   ```
   $ pip install -r requirements.txt
   ```
1. Install pre-commit to enable pre-commit hooks (This step ensures that your code is formatted according the Black standard and is compliant with PEP8.)
   ```
   $ pre-commit install
   ````
After making the above command from within the repository's root directory, you should see the following output:
   ```
   pre-commit installed at .git/hooks/pre-commit
   ```
1. Run the tests and make sure everything passes
   ```
   $ pytest
   > =============== XX passed in XXs ===============
   ```

### Fetching the Data
1. Open up jupyter notebooks
   ```
   $ jupyter notebook
   ```
1. Open the `tabulator.ipynb` from the directory in the browser
1. Run each cell of the notebook
> **NOTE:** Running the notebook may take 10-20 minutes the first time as you download all of the pdf files from the Comptroller webpage

## Usage
This is where we will specify how to use the tool

## Contributing
James will add details around the workflow for contributing
