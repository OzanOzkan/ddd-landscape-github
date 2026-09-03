import time
import subprocess
import json
import os
import git
import utils.logger as logger
import utils.requestmanager as requestmanager
import utils.databasemanager as databasemanager
from datetime import datetime
import chardet  # Add this at the top

def clone_repository(repo, output_dir):
    name = repo['name']
    owner = repo['owner']['login']
    clone_dir = os.path.join(output_dir, name)

    logger.print_with_timestamp(f"Clonning repository {name} to {clone_dir}")

    # Construct the GitHub repository URL
    repo_url = f'https://github.com/{owner}/{name}.git'

    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, clone_dir], 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.STDOUT)

    logger.print_with_timestamp(f"Clonning repository {name} complete.")
    
    return clone_dir

def calculate_loc(repo, repo_dir, conn):
    logger.print_with_timestamp(f"Calculating LoC for {repo_dir}")   

    # Run cloc command to calculate Lines of Code
    result = subprocess.run(['cloc', repo_dir, '--json', '--exclude-dir=.git'], capture_output=True, text=True)
    
    try:
        # Parse the JSON output to get LoC information
        loc_data = json.loads(result.stdout)
        
        # Remove 'header' and 'SUM'
        if 'header' in loc_data:
            del loc_data['header']
        if 'SUM' in loc_data:
            del loc_data['SUM']

        # Save LoC data to database
        databasemanager.save_repository_loc_data(conn, repo, loc_data)
    except json.decoder.JSONDecodeError as e:
        # Log error information
        logger.print_with_timestamp(f"Error parsing JSON for {repo['name']}: {str(e)}")

def process_file_names_with_directories_and_content(repo, repo_dir, conn):
    logger.print_with_timestamp(f"Getting files and directories for {repo_dir}")   

    file_infos = []
    binary_extensions = {
        'exe', 'dll', 'so', 'bin', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico', 'pdf', 'zip', 'tar', 'gz', '7z', 'rar',
        'mp3', 'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'ogg', 'class', 'jar', 'pyc', 'pyo', 'o', 'a', 'lib', 'obj'
    }
    min_confidence = 0.5  # threshold for chardet confidence

    for foldername, subfolders, filenames in os.walk(repo_dir):
        # Skip .git directory
        if ".git" in foldername:
            continue

        relative_foldername = foldername.replace(repo_dir, '', 1).lstrip('/')

        for filename in filenames:
            relative_filename = os.path.join(relative_foldername, filename)
            file_path = os.path.join(foldername, filename)
            file_ext = os.path.splitext(filename)[1].lstrip('.').lower()
            file_info = {'path': relative_filename, 'content': None, 'encoding': None, 'file_type': file_ext}
            try:
                # Skip known binary extensions
                if file_ext in binary_extensions:
                    continue
                with open(file_path, 'rb') as f:
                    raw = f.read()
                    result = chardet.detect(raw)
                    encoding = result['encoding'] or 'utf-8'
                    confidence = result.get('confidence', 0)
                    # Skip if chardet is not confident (likely binary)
                    if confidence < min_confidence:
                        continue
                    try:
                        content = raw.decode(encoding)
                    except Exception:
                        content = raw.decode('utf-8', errors='replace')
                        encoding = 'utf-8'
                    # Heuristic: skip if too many replacement chars (likely binary)
                    if content.count('\ufffd') > 10:
                        continue
                    file_info['content'] = content
                    file_info['encoding'] = encoding
            except Exception:
                # If file can't be read as text, skip content
                pass
            file_infos.append(file_info)

    databasemanager.save_repository_file_names_with_directories_and_content(conn, repo, file_infos)

def get_repository_metadata_by_name(repo_name, token):
    logger.print_with_timestamp(f"Getting the repository metadata from GitHub: {repo_name}")
    repo_query = """
        query($name: String!, $owner: String!){
            repository(name: $name, owner: $owner) {
                id
                name
                nameWithOwner,
                owner {
                    login
                    id
                    __typename
                }
                stargazerCount
                forkCount
                watchers {
                    totalCount
                }
                issues(states: OPEN) {
                    totalCount
                }
                languages(first: 1, orderBy: {field: SIZE, direction: DESC}) {
                    nodes {
                        name
                    }
                }
                createdAt
                updatedAt
                pushedAt
                homepageUrl
                diskUsage
                defaultBranchRef {
                    name
                }
                isArchived
                description
                isFork
                repositoryTopics(first: 100) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges {
                        node {
                            topic {
                                name
                            }
                        }
                    }
                }
            }
        }
    """

    owner, name = repo_name.split('/', 1)  # Assuming the format is "owner/repo"
    variables = {
        "name": name,
        "owner": owner,
    }

    # Get the repository info and topics
    result = requestmanager.graphql_request(token, repo_query, variables)['data']['repository']

    # To not to exhaust the token
    time.sleep(1)

    logger.print_with_timestamp(f"Repository metadata obtained from GitHub: {repo_name}")

    return result

def process_repository_metadata_and_topics(repo, year, conn, main_topic=""):
    logger.print_with_timestamp(f"Processing the repository metadata: {repo['name']}")

    # Save repo data and topics
    databasemanager.save_repository_metadata(conn, year, repo, main_topic)
    databasemanager.save_repository_topics(conn, repo)

    logger.print_with_timestamp(f"Processing the repository metadata DONE: {repo['name']}")

# def process_repository_readme(repo, token, conn):
#     logger.print_with_timestamp(f"Processing the repository README: {repo['name']}")

#     # Supported readme files on GitHub
#     readme_filenames = ['README.md', 'README', 'README.rst', 'README.adoc', 'README.asciidoc', 'README.textile', 'README.txt',
#                         'readme.md', 'readme', 'readme.rst', 'readme.adoc', 'readme.asciidoc', 'readme.textile', 'readme.txt']
#     readme_found = False

#     for filename in readme_filenames:
#         readme_query = """
#             query($name: String!, $owner: String!, $expression: String!){
#                 repository(name: $name, owner: $owner) {
#                     defaultBranchRef {
#                         name
#                         target {
#                             ... on Commit {
#                                 repository {
#                                     object(expression: $expression) {
#                                         ... on Blob {
#                                             text
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         """

#         variables = {
#             "name": repo['name'],
#             "owner": repo['owner']['login'],
#             "expression": f"{repo['defaultBranchRef']['name']}:{filename}"
#         }

#         # Fetch the README content
#         result = requestmanager.graphql_request(token, readme_query, variables)

#         if ('errors' not in result 
#             and result['data']['repository']['defaultBranchRef']['target']['repository']['object'] is not None
#             and 'text' in result['data']['repository']['defaultBranchRef']['target']['repository']['object']):
#             readme_text = result['data']['repository']['defaultBranchRef']['target']['repository']['object']['text']
#             databasemanager.save_repository_readme(conn, repo, readme_text)
#             readme_found = True

#     if readme_found:
#         logger.print_with_timestamp(f"Processing the repository README DONE: {repo['name']}")
#     else:
#         logger.print_with_timestamp(f"Processing the repository README: Not Found. {repo['name']}")

#     time.sleep(1)

def process_repository_readme(repo, repo_dir, conn):
    logger.print_with_timestamp(f"Processing the repository README: {repo['name']}")

    readme_filenames = ['README.md', 'README', 'README.rst', 'README.adoc', 'README.asciidoc', 'README.textile', 'README.txt',
                        'readme.md', 'readme', 'readme.rst', 'readme.adoc', 'readme.asciidoc', 'readme.textile', 'readme.txt']

    readme_found = False

    for filename in readme_filenames:
        readme_path = os.path.join(repo_dir, filename)

        # Check if the README file exists in the repository
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8', errors='replace') as readme_file:
                readme_text = readme_file.read()
                databasemanager.save_repository_readme(conn, repo, readme_text)
                readme_found = True
                break  # Stop searching if a README is found

    if readme_found:
        logger.print_with_timestamp(f"Processing the repository README DONE: {repo['name']}")
    else:
        logger.print_with_timestamp(f"Processing the repository README: Not Found. {repo['name']}")

def process_repository_commits(repo, repo_dir, conn, batch_size=100):
    logger.print_with_timestamp(f"Processing the repository commits: {repo['name']}")

    local_repo = git.Repo(repo_dir)
    commit_batch = []

    for commit in local_repo.iter_commits(local_repo.head.reference.name, no_merges=True, reverse=True):
        commit_data = {
            'sha': commit.hexsha,
            'authorName': commit.author.name,
            'authorEmail': commit.author.email,
            'date': datetime.utcfromtimestamp(commit.authored_date).strftime('%Y-%m-%d %H:%M:%S'),
            'message': commit.message,
            'files_changed': len(commit.stats.files),
            'insertions': commit.stats.total['insertions'],
            'deletions': commit.stats.total['deletions']
        }

        commit_batch.append(commit_data)

        if len(commit_batch) >= batch_size:
            databasemanager.save_repository_commits(conn, repo, commit_batch)
            commit_batch = []

    # Process any remaining commits
    if commit_batch:
        databasemanager.save_repository_commits(conn, repo, commit_batch)

# # Entry point for processing repository commits, which queries GitHub to fetch the content.
# def process_repository_commits(repo, token, conn):
#     logger.print_with_timestamp(f"Processing the repository commits: {repo['name']}")

#     commits_query = """
#         query($name: String!, $owner: String!, $cursor: String){
#             repository(name: $name, owner: $owner) {
#                 defaultBranchRef {
#                     target {
#                         ... on Commit {
#                             history(first: 50, after: $cursor) {
#                                 pageInfo {
#                                     hasNextPage
#                                     endCursor
#                                 }
#                                 edges {
#                                     node {
#                                         oid
#                                         author {
#                                             name
#                                             email
#                                             date
#                                         }
#                                         message
#                                         additions
#                                         deletions
#                                         changedFiles
#                                     }
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     """

#     variables = {
#         "name": repo['name'],
#         "owner": repo['owner']['login'],
#     }

#     # Fetch and save all commits
#     variables["cursor"] = None
#     hasNextPage = True
#     while hasNextPage:
#         result = requestmanager.graphql_request(token, commits_query, variables)
#         databasemanager.save_repository_commits(conn, repo, result['data']['repository']['defaultBranchRef']['target']['history']['edges'])
#         hasNextPage = result['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']['hasNextPage']
#         variables["cursor"] = result['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']['endCursor']

#     time.sleep(1)
#     logger.print_with_timestamp(f"Processing the repository commits DONE: {repo['name']}")

# Entry point for processing repository pull requests and comments, which queries GitHub to fetch the content.
def process_repository_pull_requests_and_comments(repo, token, conn):
    logger.print_with_timestamp(f"Processing the repository pull requests and comments: {repo['name']}")

    pull_requests_query = """
        query($name: String!, $owner: String!, $prCursor: String){
            repository(name: $name, owner: $owner) {
                pullRequests(first: 50, after: $prCursor) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges {
                        node {
                            number
                            title
                            body
                            state
                            createdAt
                            updatedAt
                            closedAt
                            mergedAt
                            comments {
                                totalCount
                            }
                            author {
                                login
                                ... on User {
                                    id
                                }
                                ... on Organization {
                                    id
                                }
                                ... on Bot {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }
    """

    comments_query = """
        query($name: String!, $owner: String!, $number: Int!, $commentCursor: String){
            repository(name: $name, owner: $owner) {
                pullRequest(number: $number) {
                    comments(first: 50, after: $commentCursor) {
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        edges {
                            node {
                                id
                                bodyText
                                author {
                                    login
                                    ... on User {
                                        id
                                    }
                                    ... on Organization {
                                        id
                                    }
                                    ... on Bot {
                                        id
                                    }
                                }
                                createdAt
                                updatedAt
                            }
                        }
                    }
                }
            }
        }
    """

    variables = {
        "name": repo['name'],
        "owner": repo['owner']['login'],
    }

    # Fetch and save all pull requests
    variables["prCursor"] = None
    hasNextPage = True
    while hasNextPage:
        result = requestmanager.graphql_request(token, pull_requests_query, variables)
        databasemanager.save_repository_pull_requests(conn, repo, result['data']['repository']['pullRequests']['edges'])

        # For each pull request, fetch and save all comments
        for edge in result['data']['repository']['pullRequests']['edges']:
            pr = edge['node']
            variables["number"] = pr['number']
            variables["commentCursor"] = None
            hasCommentPage = True
            while hasCommentPage:
                comment_result = requestmanager.graphql_request(token, comments_query, variables)
                databasemanager.save_repository_pr_comments(conn, repo, pr['number'], comment_result['data']['repository']['pullRequest']['comments']['edges'])
                hasCommentPage = comment_result['data']['repository']['pullRequest']['comments']['pageInfo']['hasNextPage']
                variables["commentCursor"] = comment_result['data']['repository']['pullRequest']['comments']['pageInfo']['endCursor']

        hasNextPage = result['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
        variables["prCursor"] = result['data']['repository']['pullRequests']['pageInfo']['endCursor']

    logger.print_with_timestamp(f"Processing the repository pull requests and comments DONE: {repo['name']}")
    time.sleep(1)

# Entry point for processing repository issues and comments, which queries GitHub to fetch the content.
def process_repository_issues_and_comments(repo, token, conn):
    logger.print_with_timestamp(f"Processing the repository issues and comments: {repo['name']}")

    issues_query = """
        query($name: String!, $owner: String!, $issueCursor: String){
            repository(name: $name, owner: $owner) {
                issues(first: 50, after: $issueCursor) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges {
                        node {
                            number
                            title
                            body
                            state
                            createdAt
                            updatedAt
                            closedAt
                            comments {
                                totalCount
                            }
                            author {
                                login
                                ... on User {
                                    id
                                }
                                ... on Organization {
                                    id
                                }
                                ... on Bot {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }
    """

    comments_query = """
        query($name: String!, $owner: String!, $number: Int!, $commentCursor: String){
            repository(name: $name, owner: $owner) {
                issue(number: $number) {
                    comments(first: 50, after: $commentCursor) {
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        edges {
                            node {
                                id
                                bodyText
                                author {
                                    login
                                    ... on User {
                                        id
                                    }
                                    ... on Organization {
                                        id
                                    }
                                    ... on Bot {
                                        id
                                    }
                                }
                                createdAt
                                updatedAt
                            }
                        }
                    }
                }
            }
        }
    """

    variables = {
        "name": repo['name'],
        "owner": repo['owner']['login'],
    }

    # Fetch and save all issues
    variables["issueCursor"] = None
    hasNextPage = True
    while hasNextPage:
        result = requestmanager.graphql_request(token, issues_query, variables)
        databasemanager.save_repository_issues(conn, repo, result['data']['repository']['issues']['edges'])

        # For each issue, fetch and save all comments
        for edge in result['data']['repository']['issues']['edges']:
            issue = edge['node']
            variables["number"] = issue['number']
            variables["commentCursor"] = None
            hasCommentPage = True
            while hasCommentPage:
                comment_result = requestmanager.graphql_request(token, comments_query, variables)
                databasemanager.save_repository_issue_comments(conn, repo, issue['number'], comment_result['data']['repository']['issue']['comments']['edges'])
                hasCommentPage = comment_result['data']['repository']['issue']['comments']['pageInfo']['hasNextPage']
                variables["commentCursor"] = comment_result['data']['repository']['issue']['comments']['pageInfo']['endCursor']

        hasNextPage = result['data']['repository']['issues']['pageInfo']['hasNextPage']
        variables["issueCursor"] = result['data']['repository']['issues']['pageInfo']['endCursor']

    logger.print_with_timestamp(f"Processing the repository issues and comments DONE: {repo['name']}")
    time.sleep(1)