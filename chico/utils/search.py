"""
Internet search for coding solutions using DuckDuckGo
"""

from typing import List, Dict, Optional

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


class CodeSearcher:
    """Search for coding solutions on the internet"""
    
    def __init__(self):
        self.available = DDGS_AVAILABLE
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for coding solutions
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of search results with title, url, and snippet
        """
        if not self.available:
            return [{
                'title': 'Search unavailable',
                'url': '',
                'snippet': 'Install duckduckgo-search to enable web search'
            }]
        
        try:
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                for r in search_results:
                    results.append({
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'snippet': r.get('body', '')
                    })
            return results
        except Exception as e:
            return [{
                'title': 'Search error',
                'url': '',
                'snippet': f'Error performing search: {str(e)}'
            }]
    
    def search_stackoverflow(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search specifically on Stack Overflow
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of Stack Overflow results
        """
        stackoverflow_query = f"site:stackoverflow.com {query}"
        return self.search(stackoverflow_query, max_results)
    
    def search_github(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search GitHub for code examples
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of GitHub results
        """
        github_query = f"site:github.com {query}"
        return self.search(github_query, max_results)
    
    def format_results(self, results: List[Dict]) -> str:
        """
        Format search results for display
        
        Args:
            results: List of search results
        
        Returns:
            Formatted string
        """
        if not results:
            return "No results found."
        
        formatted = "\n🔍 Search Results:\n" + "="*60 + "\n"
        for i, result in enumerate(results, 1):
            formatted += f"\n{i}. {result['title']}\n"
            formatted += f"   {result['url']}\n"
            snippet = result['snippet'][:200] if len(result['snippet']) > 200 else result['snippet']
            formatted += f"   {snippet}{'...' if len(result['snippet']) > 200 else ''}\n"
        
        return formatted
