import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

def perform_web_search(query: str, num_results: int = 3):
    API_KEY = os.getenv("SERPAPI_API_KEY")

    search = GoogleSearch({
        "q": query,
        "api_key": API_KEY,
        "num": num_results
    })
    results = search.get_dict()

    output = ""
    for result in results.get("organic_results", [])[:num_results]:
        title = result.get("title")
        snippet = result.get("snippet", "")
        link = result.get("link")
        output += f"{title}:\n{snippet}\n{link}\n\n"

    return output.strip()

if __name__ == '__main__':
    summary = "search for new llm architectures"
    print(perform_web_search(summary))