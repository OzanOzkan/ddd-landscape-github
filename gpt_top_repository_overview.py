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

OUTPUT_FILENAME = 'ddd_analysis_results_rq3.csv'

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

# Change: Get top repository IDs
def get_repository_ids(conn, min_contributors=2, limit=10):
    print_with_timestamp("get_repository_ids")
    cursor = conn.cursor()
    query = """
    SELECT dal.ID
    FROM ddd_architectural_landscape dal
    JOIN commits c ON dal.ID = c.repository_id
    JOIN repositories r ON dal.ID = r.ID
    GROUP BY dal.ID
    HAVING COUNT(DISTINCT c.author_email) > ?
    ORDER BY COUNT(c.ID) DESC
    LIMIT ?;
    """
    cursor.execute(query, (min_contributors, limit))
    return [row[0] for row in cursor.fetchall()]


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
# Change: Change the system prompt.
def create_system_prompt():
    print_with_timestamp("create_system_prompt")
    return """
You are an expert Software Architect and Researcher assessing collaboratively intensive Domain-Driven Design (DDD) GitHub repositories.

All provided repositories are confirmed DDD projects with a high number of distinct contributors. Your task is to produce a **comprehensive, structured analysis** of each project, describing **how DDD is implemented, the domain it models, and the collaboration practices and patterns it exhibits**.

---

## 1. Business Domain Classification

Classify the project into **exactly ONE** of these domains:

- Traditional Software  
- Unknown/Other  
- Media & Publishing  
- Financial Services  
- Environment  
- Manufacturing  
- Sales  
- Business Services  
- Healthcare  
- Insurance  
- Education  
- Leisure & Recreation  
- Logistics  
- Machine Learning  
- Personal activities  
- Government Services  
- Agriculture  

Base your decision on project description, README, folder structure, and domain-specific terminology. If no clear domain can be inferred, select **Unknown/Other**.

---

## 2. Project Characteristics

Provide a **detailed, structured analysis** covering the following aspects:

- **Bounded Contexts**: Describe the main contexts and how they are separated.  
- **Entities & Aggregates**: Describe key domain entities and aggregates, how rich their behavior is, and how they encapsulate business rules.  
- **Value Objects**: Identify examples and their usage in enforcing domain constraints.  
- **Domain Services**: How the project orchestrates domain logic without violating domain isolation.  
- **Collaboration Features**: How the project structure supports multiple contributors, modularity, or parallel work in different contexts.  
- **Other Notable Practices**: Patterns or structures that make the project distinctive in implementing DDD (e.g., use of events, modularization, domain-driven testing).  
- **Code Quality & Conventions**: Any notable coding practices that make domain logic clear and maintainable.

---

## Analysis Process

1. **Inspect Metadata**: description, README, topics, and naming conventions.  
2. **Inspect Structure**: folder layout, modules, layers, and domain isolation.  
3. **Investigate Code**: request to read a file if needed to confirm richness of entities, aggregates, or services.  
4. **Synthesize Findings**: fill in each structured aspect above with clear evidence.

---

## Output Format (JSON only)

### Type A: Request a File

{
    "action": "read_file",
    "path": "path/to/interesting_file.ext",
    "reason": "Verifying whether this class represents a rich domain concept or just a data container."
}

### Type B: Final Answer

{
    "action": "final_answer",
    "business_domain": "Financial Services",
    "characteristics": {
        "bounded_contexts": "The project models Claims, Policies, and Premiums as separate bounded contexts with minimal coupling.",
        "entities_and_aggregates": "Entities like Policy and Claim aggregate related business logic, with rich behavior encapsulating validation and state transitions.",
        "value_objects": "PremiumAmount and Currency are implemented as value objects to enforce invariants.",
        "domain_services": "ClaimsProcessingService orchestrates multiple aggregates without leaking infrastructure concerns.",
        "collaboration_features": "Clear folder separation allows multiple teams to work on different bounded contexts simultaneously; domain interfaces are stable.",
        "other_notable_practices": "Uses Domain Events for asynchronous workflows; extensive unit tests validate domain rules.",
        "code_quality_and_conventions": "Consistent naming aligned with ubiquitous language; DI used to decouple infrastructure."
    }
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
        
        # Change: Change this to fit the JSON structure.
        # CASE: Final Answer
        elif action == "final_answer":
            characteristics = ai_decision.get("characteristics", {})

            final_result = [
                repo_id,
                name,
                ai_decision.get("business_domain", "Unknown"),
                characteristics.get("bounded_contexts", ""),
                characteristics.get("entities_and_aggregates", ""),
                characteristics.get("value_objects", ""),
                characteristics.get("domain_services", ""),
                characteristics.get("collaboration_features", ""),
                characteristics.get("other_notable_practices", ""),
                characteristics.get("code_quality_and_conventions", "")
            ]

            break

    conn.close()
    
    if final_result:
        print_with_timestamp(
            f"Done {name}: Business Domain={final_result[2]}, "
            f"Bounded Contexts={final_result[3]}, Entities & Aggregates={final_result[4]}, "
            f"Value Objects={final_result[5]}, Domain Services={final_result[6]}, "
            f"Collaboration={final_result[7]}, Other Practices={final_result[8]}, "
            f"Code Quality={final_result[9]}"
        )

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
            # Write Header if new file Change: this to the new structue.
            writer.writerow([
                'ID',
                'Name',
                'Business Domain',
                'Bounded Contexts',
                'Entities & Aggregates',
                'Value Objects',
                'Domain Services',
                'Collaboration Features',
                'Other Notable Practices',
                'Code Quality & Conventions'
            ])

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
