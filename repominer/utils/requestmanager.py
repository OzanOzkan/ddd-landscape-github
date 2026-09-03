import requests
import time
import re
import utils.logger as logger

# Handles the GitHub GraphQL requests.
def graphql_request(token, query, variables, retries=5, backoff=5):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.github.com/graphql"

    for _ in range(retries):
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                if any(error.get('type') == 'RATE_LIMITED' for error in data['errors']):
                    logger.print_with_timestamp("Rate limit exceeded. Waiting for rate limit to reset.")
                    time.sleep(900)  # Wait for 15 mins to reset
                    continue
                elif any(error.get('type') == 'SERVICE_UNAVAILABLE' and 'additions' in error.get('message', '') for error in data['errors']):
                    logger.print_with_timestamp("The additions count for a commit is unavailable. Skipping this commit.")
                    continue
                else:
                    raise Exception(f"GraphQL request failed: {response.content}")
            else:
                return data
        else: # This is for tackling GitHub's strange "something went wrong" error.
            logger.print_with_timestamp(f"Error during request. Will retry in {backoff} seconds with querying deduced number of results.")
            query = re.sub(r'first: \d+', f'first: 1', query)
            time.sleep(backoff)  # wait before retrying the request

    raise Exception(f"GraphQL request failed after {retries} retries: {response.content}. The query was: {query} with variables: {variables}")