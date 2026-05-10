from ddgs import DDGS

# using duckduckgo for web search
def search_web(query, max_results=5):

    """
    Search the web using DuckDuckGo and return a formatted string
    containing titles, snippets, and URLs.
    """

    search_results = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        # formatting search result 
        for result in results:
            title = result.get("title", "No Title")
            snippet = result.get("body", "No Description")
            url = result.get("href", "No URL")

            formatted_result = (
                f"Title: {title}\n"
                f"Snippet: {snippet}\n"
                f"URL: {url}\n"
            )

            search_results.append(formatted_result)

    return "\n\n".join(search_results)