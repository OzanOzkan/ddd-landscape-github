import sqlite3
import utils.logger as logger
from sqlite3 import Error

# Creates a database table.
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Creates database connection for the given database file.
def create_connection(db_file):
    conn = None;
    try:
        conn = sqlite3.connect(db_file)       
        return conn
    except Error as e:
        print(e)

# Creates required database tables for the given database connection.
def create_database_tables(conn):
    # Create tables
    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS repositories (
            ID text PRIMARY KEY, 
            Year integer, 
            Name text, 
            NameWithOwner text, 
            Owner text,
            OwnerId text,
            OwnerType text, 
            StargazersCount integer, 
            ForksCount integer, 
            WatchersCount integer, 
            OpenIssuesCount integer, 
            Language text, 
            CreatedAt text, 
            UpdatedAt text, 
            PushedAt text, 
            Homepage text, 
            Size integer, 
            DefaultBranch text, 
            Archived text, 
            Description text, 
            ContributorCount integer,
            isFork integer,
            QueryTopic text 
        )''')

    create_table(conn, '''CREATE TABLE IF NOT EXISTS topics (
                 ID integer PRIMARY KEY AUTOINCREMENT, 
                 repository_id text, 
                 topic text, 
                 FOREIGN KEY(repository_id) REFERENCES repositories(ID)
                 )''')
    
    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS readme (
            ID integer PRIMARY KEY AUTOINCREMENT,
            repository_id text, 
            content text, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )
    ''')

    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS commits (
            ID integer PRIMARY KEY AUTOINCREMENT, 
            repository_id text,
            commit_id text, 
            author_email text, 
            author text, 
            commit_date text, 
            message text, 
            files_changed integer,
            insertions integer, 
            deletions integer,
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )''')
    
    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS pull_requests (
            ID integer PRIMARY KEY, 
            repository_id text, 
            pr_number integer, 
            pr_title text,
            pr_body text, 
            pr_status text, 
            created_at text, 
            updated_at text, 
            closed_at text, 
            merged_at text, 
            comments integer, 
            AuthorID text, 
            AuthorName text, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )''')

    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS pull_request_comments (
            ID integer PRIMARY KEY AUTOINCREMENT, 
            repository_id text, 
            pr_number integer, 
            comment_id integer, 
            comment_body text, 
            commenter_id text, 
            commenter_login text, 
            created_at text, 
            updated_at text, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )''')
    
    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS issues (
            ID integer PRIMARY KEY, 
            repository_id text, 
            issue_number integer, 
            issue_title text, 
            issue_body text,
            issue_status text, 
            created_at text, 
            updated_at text, 
            closed_at text, 
            comments integer, 
            AuthorID text, 
            AuthorName text, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )
    ''')

    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS issue_comments (
            ID integer PRIMARY KEY AUTOINCREMENT, 
            repository_id text, 
            issue_number integer, 
            comment_id integer, 
            comment_body text, 
            commenter_id text, 
            commenter_login text, 
            created_at text, 
            updated_at text, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )
    ''')

    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS loc_data (
            ID integer PRIMARY KEY AUTOINCREMENT, 
            repository_id text, 
            language text, 
            nFiles integer, 
            blank integer, 
            comment integer, 
            code integer, 
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )
    ''')

    create_table(conn, '''
        CREATE TABLE IF NOT EXISTS files (
            ID integer PRIMARY KEY AUTOINCREMENT, 
            repository_id text, 
            file text, 
            content text,          
            encoding text,         
            file_type text,        
            FOREIGN KEY(repository_id) REFERENCES repositories(ID)
        )
    ''')

# Saves repository metadata to the database.
def save_repository_metadata(conn, year, repo, main_topic):
    logger.print_with_timestamp(f"Saving repository info: {repo['name']} - {repo['id']}")

    repo_data = (
            repo['id'],
            year,
            repo['name'],
            repo['nameWithOwner'],
            repo['owner']['login'],
            repo['owner']['id'],
            repo['owner']['__typename'],
            repo['stargazerCount'],
            repo['forkCount'],
            repo['watchers']['totalCount'],
            repo['issues']['totalCount'],
            repo['languages']['nodes'][0]['name'] if repo['languages']['nodes'] else None,
            repo['createdAt'],
            repo['updatedAt'],
            repo['pushedAt'],
            repo['homepageUrl'],
            repo['diskUsage'],
            repo['defaultBranchRef']['name'] if repo['defaultBranchRef'] is not None and repo['defaultBranchRef']['name'] is not None else None, # Some repositories might be empty, therefore, no branch.
            repo['isArchived'],
            repo['description'],
            repo['isFork'],
            main_topic
        )
    sql = '''
        INSERT INTO repositories(ID, Year, Name, NameWithOwner, Owner, OwnerId, OwnerType, StargazersCount, ForksCount, WatchersCount, OpenIssuesCount, Language, CreatedAt, UpdatedAt, PushedAt, Homepage, Size, DefaultBranch, Archived, Description, isFork, QueryTopic)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
    '''
    cur = conn.cursor()
    cur.execute(sql, repo_data)
    conn.commit()

    return cur.lastrowid

# Saves repository topics to the database.
def save_repository_topics(conn, repo):
    logger.print_with_timestamp(f"Saving repository topics: {repo['name']}")

    with conn:
        for edge in repo['repositoryTopics']['edges']:
            topic = edge['node']['topic']['name']
            conn.execute('INSERT INTO topics (repository_id, topic) VALUES (?, ?)', (repo['id'], topic))
            conn.commit()


# Saves the contents of the README file to the database.
def save_repository_readme(conn, repo, readme_text):
    logger.print_with_timestamp(f"Saving README for repository: {repo['name']}")

    readme_data = (
        repo['id'],
        readme_text
    )
    sql = '''
        INSERT INTO readme (repository_id, content) VALUES (?, ?)
    '''
    conn.execute(sql, readme_data)
    conn.commit()

# # Saves repository commits to the database.
# def save_repository_commits(conn, repo, commits):
#     logger.print_with_timestamp(f"Saving repository commits: {repo['name']}")

#     with conn:
#         for edge in commits:
#             commit = (
#                 repo['id'],
#                 edge['node']['oid'],
#                 edge['node']['author']['email'],
#                 edge['node']['author']['name'],
#                 edge['node']['author']['date'],
#                 edge['node']['message'],
#                 edge['node']['additions'] + edge['node']['deletions'],
#             )
#             conn.execute('INSERT INTO commits (repository_id, commit_id, author_email, author, commit_date, message, size) VALUES (?, ?, ?, ?, ?, ?, ?)', commit)
#             conn.commit()

def save_repository_commits(conn, repo, commits):
    logger.print_with_timestamp(f"Saving repository commits: {repo['name']}")

    with conn:
        for commit in commits:
            commit_data = (
                repo['id'],
                commit['sha'],
                commit['authorEmail'],
                commit['authorName'],
                commit['date'],
                commit['message'],
                commit['files_changed'],
                commit['insertions'],
                commit['deletions'],
            )
            conn.execute('INSERT INTO commits (repository_id, commit_id, author_email, author, commit_date, message, files_changed, insertions, deletions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', commit_data)
            conn.commit()

# Saves repository pull requests to the database.
def save_repository_pull_requests(conn, repo, pr_edges):
    logger.print_with_timestamp(f"Saving repository pull requests: {repo['name']}")

    for edge in pr_edges:
        pr = edge['node']
        author_id = pr['author']['id'] if pr['author'] is not None else None
        author_login = pr['author']['login'] if pr['author'] is not None else None
        pr_data = (
            pr['number'],
            repo['id'],
            pr['title'],
            pr['body'],
            pr['state'],
            pr['createdAt'],
            pr['updatedAt'],
            pr['closedAt'],
            pr['mergedAt'],
            pr['comments']['totalCount'],
            author_id,
            author_login
        )
        sql = '''
            INSERT INTO pull_requests(
                pr_number, repository_id, pr_title, pr_body, pr_status, created_at, updated_at, closed_at,
                merged_at, comments, AuthorID, AuthorName
            ) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?) 
        '''

        conn.execute(sql, pr_data)
        conn.commit()

# Saves PR comments to the database.
def save_repository_pr_comments(conn, repo, pr_number, comment_edges):
    logger.print_with_timestamp(f"Saving repository PR comments: {repo['name']}")
    
    for edge in comment_edges:
        comment = edge['node']
        author_id = comment['author']['id'] if comment['author'] is not None else None
        author_login = comment['author']['login'] if comment['author'] is not None else None
        comment_data = (
            repo['id'],
            pr_number,
            comment['id'],
            comment['bodyText'],
            author_id,
            author_login,
            comment['createdAt'],
            comment['updatedAt']
        )
        sql = '''
            INSERT INTO pull_request_comments(
                repository_id, pr_number, comment_id, comment_body, commenter_id,
                commenter_login, created_at, updated_at
            ) 
            VALUES(?,?,?,?,?,?,?,?) 
        '''
        conn.execute(sql, comment_data)
        conn.commit()

# Saves the repository issues to the database.
def save_repository_issues(conn, repo, issue_edges):
    logger.print_with_timestamp(f"Saving repository issues: {repo['name']}")

    for edge in issue_edges:
        issue = edge['node']
        author_id = issue['author']['id'] if issue['author'] is not None else None
        author_login = issue['author']['login'] if issue['author'] is not None else None
        issue_data = (
            issue['number'],
            repo['id'],
            issue['title'],
            issue['body'],
            issue['state'],
            issue['createdAt'],
            issue['updatedAt'],
            issue['closedAt'],
            issue['comments']['totalCount'],
            author_id,
            author_login
        )
        sql = '''
            INSERT INTO issues(
                issue_number, repository_id, issue_title, issue_body, issue_status, created_at, updated_at, closed_at,
                comments, AuthorID, AuthorName
            ) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?) 
        '''
        cur = conn.cursor()
        cur.execute(sql, issue_data)
        conn.commit()

# Saves the repository issue comments to the database.
def save_repository_issue_comments(conn, repo, issue_number, comment_edges):
    logger.print_with_timestamp(f"Saving repository issue comments: {repo['name']}")

    for edge in comment_edges:
        comment = edge['node']
        author_id = comment['author']['id'] if comment['author'] is not None else None
        author_login = comment['author']['login'] if comment['author'] is not None else None
        comment_data = (
            repo['id'],
            issue_number,
            comment['id'],
            comment['bodyText'],
            author_id,
            author_login,
            comment['createdAt'],
            comment['updatedAt']
        )
        sql = '''
            INSERT INTO issue_comments(
                repository_id, issue_number, comment_id, comment_body, commenter_id,
                commenter_login, created_at, updated_at
            ) 
            VALUES(?,?,?,?,?,?,?,?) 
        '''
        conn.execute(sql, comment_data)
        conn.commit()

def save_repository_loc_data(conn, repo, loc_data):
    logger.print_with_timestamp(f"Saving repository LoC data: {repo['name']}")

    # Prepare data and SQL statement for each language
    for language, data in loc_data.items():
        # Preparing tuple data
        loc_data_tuple = (
            repo['id'],
            language,
            data['nFiles'],
            data['blank'],
            data['comment'],
            data['code'],
        )

        # Prepare the SQL statement
        sql = '''
            INSERT INTO loc_data (repository_id, language, nFiles, blank, comment, code) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''

        conn.execute(sql, loc_data_tuple)

    conn.commit()

def save_repository_file_names_with_directories_and_content(conn, repo, files):
    logger.print_with_timestamp(f"Saving repository file names with directories: {repo['name']}")

    for file_info in files:
        # file_info should be a dict: {'path': ..., 'content': ..., 'encoding': ..., 'file_type': ...}
        file_data_tuple = (
            repo['id'],
            file_info['path'],
            file_info.get('content'),
            file_info.get('encoding', 'utf-8'),
            file_info.get('file_type')
        )
        sql = '''
            INSERT INTO files (repository_id, file, content, encoding, file_type) 
            VALUES (?, ?, ?, ?, ?)
        '''
        conn.execute(sql, file_data_tuple)

    conn.commit()