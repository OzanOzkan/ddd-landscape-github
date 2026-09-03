import os
import nltk
import re
import sqlite3
import requests
import json
import csv
from sqlite3 import Error
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from requests.exceptions import Timeout
from multiprocessing import Pool, Manager
import socket
import time
from datetime import datetime
import multiprocessing

OUTPUT_FILENAME = 'results.csv'

# Prints message with the current time and process.
def print_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    process_name = multiprocessing.current_process().name
    print(f"[{timestamp}] [{process_name}] {message}")

# Set a default timeout for all socket operations
socket.setdefaulttimeout(30)

DATABASE_FILE = ".db"
RUN_DATETIME = datetime.now().strftime("%Y%m%d_%H%M%S")

# Your API Keys
API_KEYS = [
]

# NLTK Setup
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

####### DATABASE OPERATIONS #######

def create_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print_with_timestamp(e)
    return None

def get_repository_ids(conn):
    print_with_timestamp(f"get_repository_ids")
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM included_repositories")
    return [item[0] for item in cursor.fetchall()]

def get_repository_details(conn, repository_id):
    print_with_timestamp(f"get_repository_details")
    cursor = conn.cursor()
    # Fetch basic details
    cursor.execute("SELECT Name, Description FROM included_repositories WHERE ID=?", (repository_id,))
    res = cursor.fetchone()
    name = res[0] if res else "Unknown"
    desc = res[1] if res else ""
    
    # Fetch Topics
    cursor.execute("SELECT topic FROM topics WHERE repository_id=?", (repository_id,))
    topics = [t[0] for t in cursor.fetchall()]
    
    # Fetch Readme
    cursor.execute("SELECT content FROM readme WHERE repository_id=?", (repository_id,))
    readme_res = cursor.fetchone()
    readme = readme_res[0] if readme_res else ""

    return name, desc, topics, readme

def get_all_file_paths(conn, repository_id):
    print_with_timestamp(f"get_all_file_paths")
    """Returns a list of all file paths in the repo to help GPT choose."""
    cursor = conn.cursor()
    cursor.execute("SELECT file FROM files WHERE repository_id=?", (repository_id,))
    res = cursor.fetchall()
    return [item[0] for item in res] if res else []

def get_file_content_from_db(conn, repository_id, file_path_query):
    print_with_timestamp(f"get_file_content_from_db")
    """
    Fetches content for a specific file. 
    It attempts to match the path provided by GPT to the DB path.
    """
    cursor = conn.cursor()
    
    # exact match try
    cursor.execute("SELECT content FROM files WHERE repository_id=? AND file=?", (repository_id, file_path_query))
    res = cursor.fetchone()
    
    if res:
        return res[0]
    
    # If exact match fails, try partial match (e.g., GPT asks for "Order.java" but DB has "src/Domain/Order.java")
    # We pick the shortest match assuming it's the most direct hit
    like_query = f"%{file_path_query}"
    cursor.execute("SELECT file, content FROM files WHERE repository_id=? AND file LIKE ?", (repository_id, like_query))
    results = cursor.fetchall()
    
    if results:
        # Sort by length of path to get the most likely candidate (heuristic)
        results.sort(key=lambda x: len(x[0]))
        return results[0][1] # return content of best match

    return "File not found in database."

####### CLEANING #######

def clean_html(raw_html):
    print_with_timestamp(f"clean_html")
    if raw_html is None: return ""
    return BeautifulSoup(raw_html, "html.parser").get_text()

def preprocess_text(text):
    print_with_timestamp(f"preprocess_text")
    text = text.lower()
    text = re.sub('&lt;/?.*?&gt;', ' &lt;&gt; ', text)
    text = re.sub('(\\d|\\W)+', ' ', text)
    text = text.split()
    text = [word for word in text if word not in stop_words]
    return ' '.join(text)

####### GPT INTERACTION #######

def create_system_prompt():
    print_with_timestamp(f"create_system_prompt")
    return """
You are an expert Software Architect and Researcher acting as an assessor for a Systematic Literature Review on Domain-Driven Design (DDD).

Your goal is to analyze the provided GitHub repository metadata and source code to determine:
1. **isDDD**: Does this project demonstrate the use of Domain-Driven Design?
2. **Architecture**: What is the specific software architecture style used?

### 1. Assessment Criteria for 'isDDD' (YES/NO)
**Threshold:** You must label the project as **YES** if there is **clear evidence of DDD intent** and **structural patterns**, even if the implementation is not 100% theoretically perfect or complete. 
Do not disqualify a project strictly because some entities are slightly anemic. Look for the *attempt* to isolate the domain.

**Indicators for YES:**
* **Strategic Design:** Evidence of Bounded Contexts (e.g., modules named by business area rather than technical layer).
* **Structural Isolation:** A clear separation between the 'Domain' logic and 'Infrastructure'/'Technology'.
* **Tactical Patterns:** Presence of DDD building blocks (Entities, Value Objects, Aggregates, Repositories).
* **Ubiquitous Language:** Class and folder names reflect business concepts (e.g., `SubmitOrder`, `PaySalary`) rather than generic CRUD (e.g., `OrderController`, `UserTable`).

### 2. Classification for 'Architecture'
Classify the architecture into ONE of the following categories common in DDD literature (Özkan et al.):
* **Layered Architecture** (Traditional DDD with strict layering: Presentation -> App -> Domain -> Infra)
* **Hexagonal Architecture** (Ports and Adapters)
* **Onion Architecture** (Explicit concentric circles of dependency)
* **Clean Architecture** (Robert C. Martin's variation, similar to Onion)
* **CQRS** (Command Query Responsibility Segregation - distinct read/write models)
* **Event-Driven Architecture** (Focus on Domain Events and async communication)
* **MVC / Monolithic** (Standard web frameworks without distinct DDD domain isolation - likely 'isDDD: NO')
* **Microservices** (If the repo represents a single service within a larger distributed system)

### Process
1.  **Analyze Metadata:** Look at the Description, Topics, and Folder Structure.
2.  **Investigate Code:** If the structure looks promising (e.g., a `Domain` folder exists), **you must request to read a file** to confirm it contains business logic and is not just a standard MVC model.
3.  **Make a Decision:**
    * If you see a `Domain` folder but it only contains database POJOs (Hibernate/JPA entities with no logic), check one more file (e.g., a Service). If still no logic, mark NO.
    * If you see distinct Artifacts (Value Objects, Aggregates) or clear Dependency Inversion (Domain definitions independent of Infra), mark YES.

### Output Format (JSON only)

**Type A: Request a File** (Use this to verify if a class is a rich Entity or just a data container)
{
    "action": "read_file",
    "path": "path/to/interesting_file.ext",
    "reason": "Checking if the 'Order' class contains business methods or just getters/setters."
}

**Type B: Final Answer**
{
    "action": "final_answer",
    "isDDD": "YES", 
    "ddd_reason": "Project uses Onion Architecture with a clear 'Core' domain layer. Although some entities are simple, the repository interfaces are defined in the Domain and implemented in Infrastructure, demonstrating clear DDD intent.",
    "architecture": "Onion Architecture"
}
"""

def send_chat_request(messages, api_keys, api_key_index):
    print_with_timestamp(f"send_chat_request")
    """
    Sends the entire message history to the Chat Completion endpoint.
    """
    url = ''

    data = {
        "temperature": 0.0, # Low temp for deterministic analysis
        "seed": 42, # Fixed seed ensures consistent sampling across runs
        "messages": messages,
        "response_format": { "type": "json_object" } # Force JSON mode if supported by your model version, otherwise remove
    }

    max_retries = 5
    for attempt in range(max_retries):
        headers = {
            "api-key": api_keys[api_key_index],
            "Content-Type": "application/json"
        }
        
        try:
            time.sleep(10)
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=20)
            
            # Handle Quota/Rate Limits
            if response.status_code == 403:
                print_with_timestamp(f"Key {api_key_index} quota exceeded.")
                return None, (api_key_index + 1) % len(api_keys)
            
            if response.status_code == 429:
                print_with_timestamp("Rate limit. Sleeping...")
                time.sleep(5)
                continue

            if response.status_code == 200:
                return response.json(), api_key_index
            
            print_with_timestamp(f"API Error {response.status_code}: {response.text}")

        except Exception as e:
            print_with_timestamp(f"Request failed: {e}")
        
        time.sleep(2)

    return None, api_key_index # Failed after retries

def extract_json_content(response_dict):
    print_with_timestamp(f"extract_json_content")
    try:
        content = response_dict['choices'][0]['message']['content']
        # Clean markdown wrappers if present
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content.strip("```")
        return json.loads(content)
    except Exception as e:
        print_with_timestamp(f"JSON Parse Error: {e}")
        return None

####### MAIN LOGIC #######

def get_processed_ids(filename):
    """
    Reads the existing CSV and returns a set of repository IDs 
    that have already been successfully processed.
    """
    processed = set()
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Attempt to skip header
                try:
                    header = next(reader)
                except StopIteration:
                    return processed # File exists but is empty
                
                for row in reader:
                    if row and len(row) > 0:
                        processed.add(row[0]) # Assuming ID is the first column
        except Exception as e:
            print_with_timestamp(f"Warning: Could not read existing CSV to resume progress. Reason: {e}")
            
    return processed

def process_single_repo_agentic(shared_queue, api_keys, current_key_index):
    print_with_timestamp(f"process_single_repo_agentic")
    if shared_queue.empty():
        return None, current_key_index

    repo_id = shared_queue.get()
    
    conn = create_connection()
    if not conn:
        return None, current_key_index

    name, desc, topics, readme = get_repository_details(conn, repo_id)
    all_files = get_all_file_paths(conn, repo_id)
    
    # Filter files for the prompt (send top 300 files max to avoid context explosion)
    # We prioritize source code files
    interesting_extensions = ['.java', '.cs', '.ts', '.js', '.py', '.php', '.go']
    filtered_files = [f for f in all_files if any(f.endswith(ext) for ext in interesting_extensions)]
    files_str = "\n".join(filtered_files[:300]) 

    print_with_timestamp(f"Analyzing: {name} ({len(filtered_files)} src files)")

    # 1. Initialize Conversation
    messages = [
        {"role": "system", "content": create_system_prompt()},
        {"role": "user", "content": f"""
        Repository: {name}
        Description: {desc}
        Topics: {topics}
        Readme Snippet: {preprocess_text(clean_html(readme))[:1000]}
        
        File List:
        {files_str}
        """}
    ]

    max_turns = 8 # Prevent infinite loops. 1 initial + 2 tool uses + 1 final
    final_result = None
    
    for turn in range(max_turns):
        response_dict, current_key_index = send_chat_request(messages, api_keys, current_key_index)
        
        if not response_dict:
            break # API failure
        
        ai_response_content = response_dict['choices'][0]['message']['content']
        ai_decision = extract_json_content(response_dict)
        
        # Append AI's thought to history
        messages.append({"role": "assistant", "content": ai_response_content})

        if not ai_decision:
            print_with_timestamp("Failed to parse JSON from AI.")
            break

        action = ai_decision.get("action", "final_answer")

        # CASE: AI wants to read a file
        if action == "read_file":
            requested_file = ai_decision.get("path")
            print_with_timestamp(f" > AI requesting file: {requested_file}")
            
            file_content = get_file_content_from_db(conn, repo_id, requested_file)
            
            # Truncate content if too massive (e.g., > 10k chars)
            if len(file_content) > 10000:
                file_content = file_content[:10000] + "\n...[TRUNCATED]"

            messages.append({
                "role": "user", 
                "content": f"Here is the content of {requested_file}:\n{file_content}"
            })
            continue # Go to next turn
        
        # CASE: Final Answer
        elif action == "final_answer":
            final_result = [
                repo_id,
                name,
                ai_decision.get("isDDD", "Unknown"),
                ai_decision.get("ddd_reason", "No reason provided"),
                ai_decision.get("architecture", "Unknown")
            ]
            break

    conn.close()
    
    if final_result:
        print_with_timestamp(f"Done {name}: DDD={final_result[2]}, Arch={final_result[4]}")
        return final_result, current_key_index
    else:
        print_with_timestamp(f"Failed to get result for {name}, putting back in queue.")
        shared_queue.put(repo_id) # Retry logic
        return None, current_key_index

def write_to_csv(data):
    print_with_timestamp(f"write_to_csv")
    file_exists = os.path.isfile(OUTPUT_FILENAME)
    
    with open(OUTPUT_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            # Write Header if new file
            writer.writerow(['ID', 'Name', 'isDDD', 'Reason', 'Architecture'])
        for row in data:
            writer.writerow(row)

def main():
    print_with_timestamp("--- STARTING SCRIPT ---")
    
    # 1. Setup Database
    if not os.path.exists(DATABASE_FILE):
        print_with_timestamp(f"ERROR: Database file '{DATABASE_FILE}' not found.")
        return

    conn = create_connection()
    if not conn:
        return

    # 2. Get All IDs from DB
    all_ids = get_repository_ids(conn)
    conn.close() # Close immediately, we open new connections in the workers
    
    # 3. Get Processed IDs from CSV (RESUME LOGIC)
    processed_ids = get_processed_ids(OUTPUT_FILENAME)
    
    # 4. Filter: Only keep IDs that are NOT in the processed set
    ids_to_process = [repo_id for repo_id in all_ids if repo_id not in processed_ids]

    print_with_timestamp(f"Total Repositories in DB: {len(all_ids)}")
    print_with_timestamp(f"Already Processed in CSV: {len(processed_ids)}")
    print_with_timestamp(f"Remaining to Process:     {len(ids_to_process)}")

    if len(ids_to_process) == 0:
        print_with_timestamp("All repositories have been processed! Exiting.")
        return

    # 5. Fill the Queue
    manager = Manager()
    shared_repository_ids = manager.Queue()
    
    for i in ids_to_process: 
        shared_repository_ids.put(i)

    # 6. Start Processing Loop
    api_key_index = 0
    buffer_data = []

    while not shared_repository_ids.empty():
        # Pass the queue to the worker
        result, api_key_index = process_single_repo_agentic(shared_repository_ids, API_KEYS, api_key_index)
        
        if result:
            buffer_data.append(result)

        # Write to CSV every 1 record
        if len(buffer_data) >= 1:
            write_to_csv(buffer_data)
            print_with_timestamp(f"Saved {len(buffer_data)} records to CSV.")
            buffer_data = []

    # Write remaining records after loop finishes
    if buffer_data:
        write_to_csv(buffer_data)
        print_with_timestamp(f"Saved final {len(buffer_data)} records to CSV.")

    print_with_timestamp("--- JOB COMPLETE ---")

if __name__ == '__main__':
    main()
