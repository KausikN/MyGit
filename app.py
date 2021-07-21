"""
Stream lit GUI for hosting MyGit
"""

# Imports
from datetime import datetime
import os
import pickle
import functools
import streamlit as st
import json

import MyGit
# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
CACHE_PATH = 'StreamLitGUI/CacheData/Cache.json'

REPO_TYPES = ["All", "Private Repos", "Public Repos"]

# Util Vars
GITHUB_CLIENT = None
USER_ME = None

CACHE = {}

# Util Functions
def Str_to_DateTime(data):
    dateTimeList = list(map(int, data.split("-")))
    dateTime = datetime(dateTimeList[0], dateTimeList[1], dateTimeList[2], dateTimeList[3], dateTimeList[4], dateTimeList[5])
    return dateTime

def DateTime_to_Str(dateTime, format="%d-%b-%Y (%H:%M:%S)"):
    return dateTime.strftime(format) # Another format => '%Y-%m-%dT%H:%M:%S'

def LoadClientData():
    global GITHUB_CLIENT
    global USER_ME
    GITHUB_CLIENT = MyGit.GITHUB_CLIENT
    USER_ME = MyGit.GetCurrentUser()

def GetNames(data_list):
    names = []
    for data in data_list:
        names.append(data['name'])
    return names

def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, 'r'))

def SaveCache():
    json.dump(CACHE, open(CACHE_PATH, 'w'), indent=4)

def GetBadgeCode(a, b, color):
    return "[![Generic badge](https://img.shields.io/badge/{}-{}-{}.svg)]()".format(a, b, color)

# Main Functions


# UI Functions
def UI_SelectRepoMode(REPOS_DETAILS, user):
    USERINPUT_ColabForkReposAlso = st.checkbox("Include Colabbed and Forked Repos?", True)
    REPOS_DETAILS_PRUNED = REPOS_DETAILS
    if not USERINPUT_ColabForkReposAlso:
        REPOS_DETAILS_PRUNED = [repo for repo in REPOS_DETAILS if repo["name"].startswith(user.name.replace(" ", ""))]

    USERINPUT_SelectMode = st.selectbox("Select Repo Type", REPO_TYPES)
    if USERINPUT_SelectMode == "All":
        return REPOS_DETAILS_PRUNED
    elif USERINPUT_SelectMode == "Private Repos":
        return [repo for repo in REPOS_DETAILS_PRUNED if repo['private']]
    elif USERINPUT_SelectMode == "Public Repos":
        return [repo for repo in REPOS_DETAILS_PRUNED if not repo['private']]
    return REPOS_DETAILS_PRUNED

def UI_LoadReposData(user, excludes):
    REPOS = MyGit.GetAllRepos(user)
    repoCount = len(REPOS)
    st.markdown("User ***" + user.name + "***" + " has " + str(repoCount) + " repos.")

    LoaderText = st.empty()
    REPOS_DETAILS = []
    i = 0
    for repo in REPOS:
        repoDetails = MyGit.GetRepoDetails(repo, excludes)
        REPOS_DETAILS.append(repoDetails)
        i += 1
        LoaderText.markdown("[" + str(i) + " / " + str(repoCount) + "] Loaded " + repoDetails['name'])
    LoaderText.markdown("All " + str(repoCount) + " repo details loaded!")
    return REPOS_DETAILS

# Repo Based Functions
def view_my_repos():
    global CACHE

    # Title
    st.header("View My Repos")

    LoadClientData()
    LoadCache()
    REPOS_DETAILS = []
    if USER_ME.name in CACHE["REPOS_DETAILS"].keys():
        REPOS_DETAILS = CACHE["REPOS_DETAILS"][USER_ME.name]

    # Load Inputs
    st.markdown("User ***" + USER_ME.name + "***" + " has " + str(len(REPOS_DETAILS)) + " repos.")

    REPOS_DETAILS_PRUNED = UI_SelectRepoMode(REPOS_DETAILS, USER_ME)
    REPOS_NAMES = GetNames(REPOS_DETAILS_PRUNED)
    
    st.markdown("Loaded ***" + str(len(REPOS_NAMES)) + "***" + " repos.")
    USERINPUT_RepoNameChoice = st.selectbox("Select Repo", REPOS_NAMES)

    # Process Inputs
    USERINPUT_RepoChoiceIndex = -1
    if USERINPUT_RepoNameChoice is not None: USERINPUT_RepoChoiceIndex = REPOS_NAMES.index(USERINPUT_RepoNameChoice)
    if USERINPUT_RepoChoiceIndex == -1: return
    USERINPUT_RepoChoice = REPOS_DETAILS_PRUNED[USERINPUT_RepoChoiceIndex]

    # Display Outputs
    st.markdown("## " + USERINPUT_RepoChoice['name'])

    col1, col2, col3, col4 = st.beta_columns([2, 4, 1, 1])
    Repo_public = ":ballot_box_with_check:" if not USERINPUT_RepoChoice['private'] else ":x:"
    col1.markdown("Public:")
    col2.markdown(Repo_public)
    Repo_nforks = USERINPUT_RepoChoice['n_forks']
    Badge_nforks = GetBadgeCode("forks", str(Repo_nforks), "blue")
    col3.markdown(Badge_nforks)
    Repo_nstars = USERINPUT_RepoChoice['n_stars']
    Badge_nstars = GetBadgeCode("stars", str(Repo_nstars), "orange")
    col4.markdown(Badge_nstars)

    detailSizeRatio = [1, 3]
    col1, col2 = st.beta_columns(detailSizeRatio)
    Repo_desc = USERINPUT_RepoChoice['description'] if USERINPUT_RepoChoice['description'] is not None else "No Description"
    col1.markdown("Description:")
    col2.markdown("```\n" + Repo_desc)

    col1, col2 = st.beta_columns(detailSizeRatio)
    Repo_lang = USERINPUT_RepoChoice['language'] if USERINPUT_RepoChoice['language'] is not None else "No Language"
    col1.markdown("Language:")
    col2.markdown("```\n" + Repo_lang)

    col1, col2 = st.beta_columns(detailSizeRatio)
    Repo_timestr_created = USERINPUT_RepoChoice['time_creation'] if USERINPUT_RepoChoice['time_creation'] is not None else "Time of Creation not found"
    Repo_timestr_created = DateTime_to_Str(Str_to_DateTime(Repo_timestr_created))
    col1.markdown("Time of Creation:")
    col2.markdown("```\n" + Repo_timestr_created)

    col1, col2 = st.beta_columns(detailSizeRatio)
    Repo_timestr_lastpush = USERINPUT_RepoChoice['time_push_last'] if USERINPUT_RepoChoice['time_push_last'] is not None else "Time of Last Push not found"
    Repo_timestr_lastpush = DateTime_to_Str(Str_to_DateTime(Repo_timestr_lastpush))
    col1.markdown("Time of Last Push:")
    col2.markdown("```\n" + Repo_timestr_lastpush)

    col1, col2 = st.beta_columns(detailSizeRatio)
    Repo_homepage = USERINPUT_RepoChoice['home_page']
    col1.markdown("Home Page:")
    if Repo_homepage is None:
        col2.markdown("Home Page not found", unsafe_allow_html=True)
    else:
        col2.markdown('<a href="' + Repo_homepage + '">' + Repo_homepage + '</a>', unsafe_allow_html=True)

def settings():
    global CACHE

    # Title
    st.header("Settings")

    LoadClientData()
    LoadCache()

    # Load Inputs
    st.markdown("## Repository Settings")
    USERINPUT_GetContents = st.checkbox("Load Repo Contents", False)
    USERINPUT_GetLicense = st.checkbox("Load Repo License", False)
    if st.button("Reload Repos"):
        REPOS_DETAILS = UI_LoadReposData(USER_ME, {"contents": not USERINPUT_GetContents, "license": not USERINPUT_GetLicense})

        # Update Cache
        CACHE["REPOS_DETAILS"][USER_ME.name] = REPOS_DETAILS
        SaveCache()

    # Process Inputs

    # Display Outputs

    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()