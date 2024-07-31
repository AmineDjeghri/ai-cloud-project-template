# ai-project-template
Template for a new AI project using streamlit, fastapi, cloud AI tools Azure OpenAI &amp; more.
If you want an on-premise template which supports GPU,
check this [ai-on-premise-project-template](https://github.com/AmineDjeghri/ai-on-premise-project-template)

# 1. Description
Template for a new AI project :
- streamlit
- fastapi
- azure openai
- docker
- pre-commit hooks / ruff
- makefile
- .env file
- logging
- tests
- github workflows
- ggshield

Additional features:
- [Pull requests templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [Emojis in commits](https://gitmoji.dev/)
- [Emojis in GitHub](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md)

Additional MLOps templates:
- https://github.com/fmind/mlops-python-package

## 1.1. Local installation
### 1.1.1. Local Prerequisites
- Ubuntu 22.04 (latest)
- Python 3.11
- git clone the repository
- Create a ``.env`` file *(take a look at the ``.env.example`` file)*:

### 1.1.2. Installation

1. run ``make install`` *(this will install the requirements)*,
2. edit `.env` file,

### 1.1.3. Run app
- Locally: Start the application with `` make run_all``,

## 1.2. Docker installation
- Set the environment variables (in the system or in a .env file)
- Run docker with the right port bindings.
- Since the app is running in docker and using streamlit, the Internal and External URL addresses won't work. You need to access the app with localhost:forwarded_port


## 1.5. Contributing
The following files are used in the contribution pipeline:
- ``.pre-commit-config.yaml``: pre-commit hooks configuration file
- ``ruff.toml``: ruff configuration file used by ruff in pre-commit hooks
- ``log_config.py``: logging configuration file for the project. This logger is used in the backend and can be used in the frontend.
- ``Makefile``: contains the commands to run the app locally.
- ``.env`` : contains the environment variables used by the app.

### 1.5.1. How to contribute
Before you start working on an issue, please comment on (or create) the issue and wait for it to be assigned to you. If someone has already been assigned but didn't have the time to work on it lately, please communicate with them and ask if they're still working on it. This is to avoid multiple people working on the same issue.
Once you have been assigned an issue, you can start working on it. When you are ready to submit your changes, open a pull request. For a detailed pull request tutorial, see this guide.

1. Create a branch from the dev branch and respect the naming convention: `feature/your-feature-name` or `bugfix/your-bug-name`.
2. Install pre-commit hooks by running ``pre-commit install``
3. Before commiting your code :
    - Run ``make test`` to run the tests
    - Run ``make pre-commit`` to check the code style & linting
    - Manually, merge dev branch into your branch to solve and avoid any conflicts. Merging strategy: merge : dev → your_branch
    - After merging, run ``make test`` and ``make pre-commit`` again to ensure that the tests are still passing.
    - (if your project is a python package) Update the package’s version, in pyproject.toml & build the wheel

4. Create a pull request. If the GitHub actions pass, the PR will be accepted and merged to dev.

#### 1.5.1.1. For repository admins: Merging strategies & GitHub actions guidelines
- Once the dev branch is tested, the pipeline is green, and the PR has been accepted, you can merge with a 'merge' strategy.
- Then, you should create a merge from dev to main with Squash strategy.
- The status of the ticket will change then to 'done.'
