import re
import json
import urllib.parse
import urllib.request
from typing import List, Dict

def search_duckduckgo_api(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Primary search using the official ddgs package."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))
            results = []
            for r in raw_results:
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", "")[:350],
                    "url": r.get("href", "")
                })
            return results
    except Exception:
        return []

def search_duckduckgo_fallback(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Fallback search using DuckDuckGo Instant Answer / HTML without third-party dependencies."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Extract title and snippet snippets via regex
        titles = re.findall(r'<a class="result__snippet[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html)
        results = []
        for href, snippet in titles[:max_results]:
            clean_snippet = re.sub(r"<[^>]+>", "", snippet).strip()
            results.append({
                "title": query,
                "snippet": clean_snippet[:350],
                "url": href
            })
        return results
    except Exception as e:
        return [{"title": "Search Error", "snippet": f"Could not complete web search: {e}", "url": ""}]

def search_web_knowledge(query: str, max_results: int = 3) -> str:
    """
    Public entrypoint for the LangGraph agent.
    Returns formatted Markdown search context for injection into LLM prompts.
    """
    results = search_duckduckgo_api(query, max_results=max_results)
    if not results:
        results = search_duckduckgo_fallback(query, max_results=max_results)

    if not results:
        return "No web knowledge retrieved for this query."

    formatted = []
    for i, r in enumerate(results, 1):
        formatted.append(f"[{i}] {r['title']}\n    URL: {r['url']}\n    Snippet: {r['snippet']}")
    return "\n\n".join(formatted)

if __name__ == "__main__":
    print(search_web_knowledge("sklearn ValueError Input X contains NaN LinearRegression"))