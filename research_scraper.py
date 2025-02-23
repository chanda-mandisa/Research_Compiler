import asyncio
import aiohttp
import csv
import json
import os
from datetime import datetime

# Retrieve API Key from Environment Variable
# The API key is required for using SerpAPI to fetch Google Scholar results.
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Ensure API Key is Set
# If the key is missing, the script will raise an error and stop execution.
if not SERPAPI_KEY:
    raise ValueError("SerpAPI key is missing. Set it via the SERPAPI_KEY environment variable.")

# Define a generic directory name for saving results
SAVE_DIRECTORY = os.path.join(os.getcwd(), "research_results")

# Ensure the directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

async def fetch(session, url, params=None):
    """
    Asynchronously fetch data from an API with error handling.
    
    Parameters:
    session (aiohttp.ClientSession): The active session for making HTTP requests.
    url (str): The API endpoint URL.
    params (dict, optional): Query parameters for the API request.
    
    Returns:
    dict: The JSON response from the API or an empty dictionary if an error occurs.
    """
    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()  # Convert response to JSON format
            else:
                print(f"Error: Received status code {response.status} from {url}")
                return {}
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return {}

async def get_google_scholar_results(query, num_results=50):
    """
    Retrieve research papers from Google Scholar using SerpAPI asynchronously.
    
    Parameters:
    query (str): The search keyword to query Google Scholar.
    num_results (int): The number of research papers to retrieve.
    
    Returns:
    list: A list of research results extracted from Google Scholar.
    """
    all_results = []
    async with aiohttp.ClientSession() as session:
        for start in range(0, num_results, 10):  # Fetch in batches of 10
            params = {
                "engine": "google_scholar",  # Define the API search engine
                "q": query,  # Search query provided by the user
                "api_key": SERPAPI_KEY,  # API key required for authentication
                "num": 10,  # Number of results per request
                "start": start,  # Pagination offset
            }
            data = await fetch(session, "https://serpapi.com/search", params)
            all_results.extend(data.get("organic_results", []))  # Extract relevant results
            
            if len(data.get("organic_results", [])) < 10:
                break  # Stop if there are no more results to fetch
    return all_results

def save_results(results, query):
    """
    Save research results to a CSV file in the specified directory.
    
    Parameters:
    results (list): A list of research results to be saved.
    query (str): The search keyword used, included in the filename.
    """
    if not results:
        print("No results found. Skipping file save.")
        return
    
    # Generate the filename dynamically based on current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(SAVE_DIRECTORY, f"research_results_{query}_{timestamp}.csv")
    
    seen_titles = set()  # Store titles to avoid duplicate entries
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Type", "Title", "Authors/Inventors", "Link/Patent Number"])  # CSV headers
        
        for idx, item in enumerate(results, start=1):  # Start ID numbering from 1
            title = item.get("Title", "N/A")
            if title not in seen_titles:
                seen_titles.add(title)
                writer.writerow([
                    idx,
                    item.get("Type", "N/A"),
                    title,
                    item.get("Authors/Inventors", "N/A"),
                    item.get("Link/Patent Number", "N/A")
                ])
    
    print(f"Results saved to {output_file}")

def format_google_scholar_results(results):
    """
    Format Google Scholar results into a structured output for CSV saving.
    
    Parameters:
    results (list): The raw results retrieved from Google Scholar.
    
    Returns:
    list: A formatted list of research paper details including title, authors, and link.
    """
    formatted_results = []
    for result in results:
        # Extract authors from the publication_info field if available
        publication_info = result.get("publication_info", {})
        authors = publication_info.get("authors", [])
        author_names = [author.get("name", "N/A") for author in authors] if authors else ["N/A"]

        formatted_results.append({
            "Type": "Research Paper",
            "Title": result.get("title", "N/A"),
            "Authors/Inventors": ", ".join(author_names),
            "Link/Patent Number": result.get("link", "N/A")
        })
    return formatted_results

async def main():
    """
    Main function that handles user input, fetches research data, and saves it.
    Loops continuously until the user decides to exit.
    """
    while True:
        query = input("Enter search keyword (or type 'exit' to quit): ")
        if query.lower() == "exit":
            print("Exiting script.")
            break  # Exit the loop if the user types 'exit'
        
        if not query.strip():  # Prevent empty queries
            print("Query is empty. Please enter a valid search keyword.")
            continue
        
        print("Fetching Google Scholar results...")
        scholar_results = await get_google_scholar_results(query, num_results=50)  # Fetch 50 results
        print(f"Fetched {len(scholar_results)} Google Scholar results.")
        formatted_scholar_results = format_google_scholar_results(scholar_results)
        
        save_results(formatted_scholar_results, query)  # Save results to CSV file

if __name__ == "__main__":
    asyncio.run(main())  # Run the script using asyncio

