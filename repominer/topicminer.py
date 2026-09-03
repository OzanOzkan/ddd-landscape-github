import os
import traceback
import argparse
import time
import utils.repoprocessor as repoprocessor
import utils.logger as logger
import utils.filemanager as filemanager
import utils.requestmanager as requestmanager
import utils.databasemanager as databasemanager
from multiprocessing import Process, Queue, Manager
from datetime import datetime

# List of repos according to their processing state for the summary
REPOS_PROCESSED = None
REPOS_FAILED = None
REPOS_SKIPPED = None

# Process worker
def worker(token, output_location, queue, REPOS_PROCESSED, REPOS_FAILED, REPOS_SKIPPED):
    while not queue.empty():
        retries = 0
        max_retries = 3
        clone_path = ""
        while retries < max_retries:
            try:
                # Get repository metadata
                repo, topic = queue.get()
                repo = repoprocessor.get_repository_metadata_by_name(repo, token)

                # Unpack the data
                year = datetime.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ").year
                repo_name = repo["name"]
                repo_id = repo["id"]
                repo_id_safe = repo_id.replace('/', '_').replace('=', '_')
                db_path = f'{output_location}/github_data_{repo_name}_{repo_id_safe}.db'

                if os.path.exists(db_path):
                    logger.print_with_timestamp(f"Repository processed before. Skipping. - Name: {repo_name}")
                    REPOS_SKIPPED.append(repo_name)
                    break
                
                logger.print_with_timestamp(f"Processing repository: ID: {repo_id}, Name: {repo_name}, Year: {year}")
            
                # Create a new database and connection
                conn = databasemanager.create_connection(db_path)

                # Create database tables
                databasemanager.create_database_tables(conn)

                # Call all the data gathering and insertion functions
                clone_path = repoprocessor.clone_repository(repo, output_location)
                repoprocessor.process_repository_metadata_and_topics(repo, year, conn, topic)
                repoprocessor.process_repository_readme(repo, clone_path, conn)
                repoprocessor.calculate_loc(repo, clone_path, conn)
                repoprocessor.process_file_names_with_directories_and_content(repo, clone_path, conn)
                repoprocessor.process_repository_commits(repo, clone_path, conn)
                repoprocessor.process_repository_pull_requests_and_comments(repo, token, conn)
                repoprocessor.process_repository_issues_and_comments(repo, token, conn)
                filemanager.delete_directory(clone_path)

                conn.close()

                logger.print_with_timestamp(f"Processing DONE for repository: ID: {repo_id}, Name: {repo_name}, Year: {year}")
                REPOS_PROCESSED.append(repo_name)
                break
            except Exception as e:
                logger.print_with_timestamp(f"Error occurred while processing {repo_name}. Error: {e}")
                traceback.print_exc()  # Print the full traceback
                retries += 1
                # Remove the db file if it exists
                if os.path.exists(db_path):
                        os.remove(db_path)
                if retries >= max_retries:
                    logger.print_with_timestamp(f"Max retries reached. Giving up on {repo_name}.")
                    REPOS_FAILED.append(repo_name)
                    filemanager.delete_directory(clone_path)
                    break
                else:
                    logger.print_with_timestamp(f"Retrying after 60 seconds...")
                    time.sleep(60)

def process_repositories_from_topic_list(tokens, output_location, start_year, end_year, min_stars, topics):
    logger.print_with_timestamp("Starting topic processing.")

    search_repos_query = """
        query($query: String!, $cursor: String){
        search(query: $query, type: REPOSITORY, first: 100, after: $cursor) {
            edges {
            node {
                ... on Repository {
                nameWithOwner
                }
            }
            }
            pageInfo {
            hasNextPage
            endCursor
            }
        }
        }
        """

    queue = Queue()
    for topic in topics:
        logger.print_with_timestamp(f"Processing the topic: {topic}")
        for year in range(start_year, end_year):
            logger.print_with_timestamp(f"Querying the year: {year}")

            hasNextPage = True
            endCursor = None
            totalRepos = 0

            while hasNextPage:
                # Modify your query here
                variables = {
                    "query": f"topic:{topic} created:{year}-01-01..{year}-12-31 stars:>{min_stars}",
                    "cursor": endCursor
                }

                result = requestmanager.graphql_request(tokens[0], search_repos_query, variables)

                repos = [edge['node'] for edge in result['data']['search']['edges']]
                for repo in repos:
                    queue.put((repo['nameWithOwner'], topic))

                hasNextPage = result['data']['search']['pageInfo']['hasNextPage']
                endCursor = result['data']['search']['pageInfo']['endCursor']
                totalRepos += len(repos)
            
            logger.print_with_timestamp(f"{totalRepos} repositories found in {year}")


    processes = [Process(target=worker, args=(token, output_location, queue, REPOS_PROCESSED, REPOS_FAILED, REPOS_SKIPPED)) for token in tokens]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    logger.print_with_timestamp("Topic processing completed!")

def print_processing_summary():
    logger.print_with_timestamp("======== Processing Summary ========")
    logger.print_with_timestamp(f"{len(REPOS_PROCESSED)} repositories processed: {','.join(REPOS_PROCESSED)}")
    logger.print_with_timestamp(f"{len(REPOS_FAILED)} repositories failed: {','.join(REPOS_FAILED)}")
    logger.print_with_timestamp(f"{len(REPOS_SKIPPED)} repositories skipped: {','.join(REPOS_SKIPPED)}")
    logger.print_with_timestamp("======== Processing Summary ========")

def main(config_path):
    global REPOS_PROCESSED, REPOS_FAILED, REPOS_SKIPPED
    manager = Manager()
    REPOS_PROCESSED = manager.list()
    REPOS_FAILED = manager.list()
    REPOS_SKIPPED = manager.list()

    # Load the config file
    config = filemanager.load_config(config_path)

    # Get tokens
    tokens = config['tokens']

    # Get the output location and create the directory
    output_location = config['output_location']
    filemanager.create_directory(output_location)

    # Check if topic mining is enabled and process accordingly
    if config.get('topic_mining', {}).get('enabled', False):
        start_year = config['topic_mining']['start_year']
        end_year = config['topic_mining']['end_year']
        topics = config['topic_mining']['topics']
        min_stars = config['topic_mining']['min_stars']
        process_repositories_from_topic_list(tokens, output_location, start_year, end_year, min_stars, topics)

    # Print the summary
    print_processing_summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process GitHub topics.')
    parser.add_argument('-job', type=str, required=True, help='Path to the job configuration YAML file')
    args = parser.parse_args()

    main(args.job)