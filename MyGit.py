'''
Python tool to view details of git repositories and profile
'''

# Imports
import base64
import json
from github import Github

# Main Vars
GITHUB_CLIENT = Github() # Github(json.load(open('.accesstoken/secret_config.json'))["secret_token"])

# Main Functions
def GetUser(username):
    global GITHUB_CLIENT
    user = GITHUB_CLIENT.get_user(username)
    return user

def GetCurrentUser():
    global GITHUB_CLIENT
    user = GITHUB_CLIENT.get_user()
    return user

def GetAllRepos(user):
    return list(user.get_repos())

def SearchRepos(user, query):
    return list(user.search_repositories(query))

# Repo Details Functions
def GetRepoLicense(repo):
    repoLicense = None
    try: repoLicense = base64.b64decode(repo.get_license().content.encode()).decode()
    except: pass
    return repoLicense

def GetRepoContents(repo):
    repoContents = []
    try: repoContents = list(repo.get_contents(""))
    except: pass
    return repoContents

def GetRepoDetails(repo, excludes={"contents": False, "license": False}):
    # Get Other Details
    repoDetails = {
        'name': repo.full_name,
        'description': repo.description,
        'language': repo.language,
        'time_creation': repo.created_at.strftime('%Y-%m-%d-%H-%M-%S'),
        'time_push_last': repo.pushed_at.strftime('%Y-%m-%d-%H-%M-%S'),
        'home_page': repo.homepage,
        'n_forks': repo.forks,
        'n_stars': repo.stargazers_count,
        'private': repo.private
    }
    if not excludes['contents']: repoDetails['contents'] = GetRepoContents(repo)
    if not excludes['license']: repoDetails['license'] = GetRepoLicense(repo)

    return repoDetails

# Driver Code
# # Params
# userName = "KausikN"
# # Params

# # RunCode
# # Get User
# USER = GetCurrentUser()
# # Get Repos Details
# REPOS = GetAllRepos(USER)
# print("Available Repos:", len(REPOS))
# # Get Repo Details
# for repo in REPOS[:1]:                   
#     print(GetRepoDetails(repo))
#     print()