import requests
import json

def scrape_entity_data(query: str, api_key: str) -> list:
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google", 
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        
        if "organic_results" in data:
            results = [{"title": result["title"], "url": result["link"], "snippet": result["snippet"]} for result in data["organic_results"]]
            return results
        else:
            return []

    except Exception as e:
        print(f"Error during web scraping: {e}")
        return []


