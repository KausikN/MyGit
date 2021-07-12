'''
Python tool to view details of git repositories and profile
'''

# Imports
import base64
import json
from github import Github

# Main Vars
GITHUB_CLIENT = Github(json.load(open('.accesstoken/secret_config.json'))["secret_token"])

# Main Functions
def GetUser(username):
    global GITHUB_CLIENT
    user = GITHUB_CLIENT.get_user(username)
    return user

def GetCurrentUser():
    global GITHUB_CLIENT
    user = GITHUB_CLIENT.get_user()
    return user

def GetRepos(user):
    return list(user.get_repos())

def GetRepoDetails(repo):
    # Get License Safely
    repoLicense = None
    try:
        repoLicense = base64.b64decode(repo.get_license().content.encode()).decode()
    except:
        pass

    # Get Other Details
    repoDetails = {
        'name': repo.full_name,
        'description': repo.description,
        'language': repo.language,
        'time_creation': repo.created_at,
        'time_push_last': repo.pushed_at,
        'home_page': repo.homepage,
        'n_forks': repo.forks,
        'n_stars': repo.stargazers_count,
        'contents': repo.get_contents(""),
        'license': repoLicense,
    }
    return repoDetails
    

# Driver Code
# Params
userName = "KausikN"
# Params

# RunCode
# Get User
USER = GetCurrentUser()
# Get Repos Details
REPOS = GetRepos(USER)
print("Available Repos:", len(REPOS))
# Get Repo Details
for repo in REPOS[:1]:                   
    print(GetRepoDetails(repo))
    print()