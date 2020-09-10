# Workflow

## Thanks for helping us parse the minutes of the BoE!
We're glad you're here and ready to help. 

## Basic order of operations
### 0. Clone the repo and check it out 
Please start by looking around and getting to know the code base a bit. A great place to start is to clone the repo and run the `tabulator.ipynb` notebook, which is designed to give collaborators a look into the workings of the code. It also helps to read a few pages from the Board of Estimates .pdf files, just to get the flavor of the input data. 

### 1. Submit an issue
Once you feel like you've spotted a way for the repo to be improved, head to our [Issues page](https://github.com/department-of-general-services/BOE_tabulator/issues) and create a new issue. When creating an issue, apply one of the following mutually exclusive labels:

- __Bug__. "I've found something that is broken and my branch will fix it." 
- __Discovery__. "I will conduct research, and my branch will add my findings (as text) to the /discovery directory."
- __Feature__. "My branch will add a new functionality to the repo."
- __Improvement__. "The existing code isn't broken, but could be improved. My branch will improve it."
- __Documentation__. "My branch will add docstrings, comments, or improve the Markdown documents in the repo."
- __Question__. "There's something about the repo that I don't understand or want to ask the group about."

Issues should correspond to medium-sized tasks of about a few hours of work each. Fixing a typo is too small; re-doing the web scraping section is too big. If there are a number of related smaller tasks that need to be done, please try to merge them into one issue.

### 2. Create a branch associated with your issue and code your solution
A preferred approach is to name the branch to match the issue. So if the issue number is 12, the branch will be called "issue_12." This enforces a one-to-one relationship between issues and branches, which keeps things tidy in general. 

Please commit often. DGS would rather see too many commits than two few. 

> Whenever you add a new feature that's worth commiting, commit. You added a working method? Commit. You fixed a typo? Commit. You fixed a file wrong indentation? Commit. There's nothing wrong commiting small changes, as soon as the commit is relevant. [ht](https://softwareengineering.stackexchange.com/a/74893)

Push to remote as often as you like. 

Bonus round: Automatically close your issue when your code is merged by making the final commit message read "closes #12" (but with the number of your git issue in place of 12)

### 3. Request merging your branch to master  
If there's a specific person who you know if familiar with the issue (for example, Billy Daly if your branch concerns unit testing), assign your pull request to that person for review. 

It's OK if you leave your PR unassigned. The next available reviewer will take it. You can expect to get some comments on your PR. Then your PR will either be approved and merged, or sent back to you with a request for changes. 

