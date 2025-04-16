import requests
import json
import re
import asyncio
from bs4 import BeautifulSoup
import whois
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from typing import Dict, List, Optional

nltk.download('vader_lexicon')

class OSINTAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.sia = SentimentIntensityAnalyzer()
        self.results = {}

    async def search_social_media(self, username: str) -> Dict:
        """Search for username across multiple platforms"""
        results = {}
        try:
            # Twitter API (requires API keys)
            twitter_url = f"https://api.twitter.com/2/users/by/username/{username}"
            # response = requests.get(twitter_url, headers=self.headers)
            # results['twitter'] = response.json()
            
            # Simulated response
            results['twitter'] = {'data': {'id': '123', 'name': 'example_user'}}
        except Exception as e:
            print(f"Social media search error: {e}")
        return results

    async def search_web(self, keyword: str) -> Dict:
        """Search web for mentions of keyword"""
        results = {}
        try:
            google_cse_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': keyword,
                'key': 'YOUR_GOOGLE_API_KEY',
                'cx': 'YOUR_CSE_ID'
            }
            # response = requests.get(google_cse_url, params=params)
            # results['web_results'] = response.json()
            
            # Simulated response
            results['web_results'] = {'items': [{'title': 'Example Result', 'link': '#'}]}
        except Exception as e:
            print(f"Web search error: {e}")
        return results

    async def domain_lookup(self, domain: str) -> Dict:
        """Perform WHOIS lookup and domain analysis"""
        try:
            domain_info = whois.whois(domain)
            return {
                'registrar': domain_info.registrar,
                'creation_date': domain_info.creation_date,
                'expiration_date': domain_info.expiration_date,
                'name_servers': domain_info.name_servers
            }
        except Exception as e:
            print(f"Domain lookup error: {e}")
            return {}

    async def email_analysis(self, email: str) -> Dict:
        """Analyze email address for breaches and validity"""
        try:
            # Check breach status using HaveIBeenPwned API
            hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'hibp-api-key': 'YOUR_HIBP_KEY'}
            # response = requests.get(hibp_url, headers=headers)
            return {
                'breaches': [],  # response.json(),
                'valid_format': re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
            }
        except Exception as e:
            print(f"Email analysis error: {e}")
            return {}

    async def news_analysis(self, keyword: str) -> Dict:
        """Search recent news articles"""
        try:
            news_url = "https://newsapi.org/v2/everything"
            params = {
                'q': keyword,
                'apiKey': 'YOUR_NEWS_API_KEY',
                'pageSize': 5
            }
            # response = requests.get(news_url, params=params)
            # return response.json()
            return {'articles': []}  # Simulated response
        except Exception as e:
            print(f"News analysis error: {e}")
            return {}

    def analyze_sentiment(self, text: str) -> Dict:
        """Perform sentiment analysis on text"""
        return self.sia.polarity_scores(text)

    async def run_investigation(self, target: str):
        """Coordinate all investigation tasks"""
        tasks = {
            'social_media': self.search_social_media(target),
            'web_search': self.search_web(target),
            'domain_info': self.domain_lookup(target),
            'email_info': self.email_analysis(target),
            'news': self.news_analysis(target)
        }
        
        results = {}
        for name, task in tasks.items():
            results[name] = await task
        
        # Add sentiment analysis to news results
        if 'news' in results:
            for article in results['news'].get('articles', []):
                if 'content' in article:
                    article['sentiment'] = self.analyze_sentiment(article['content'])
        
        self.results = results
        return results

    def generate_report(self) -> str:
        """Generate markdown report from results"""
        report = [
            "# OSINT Investigation Report",
            f"Generated: {datetime.now().isoformat()}\n"
        ]
        
        for section, data in self.results.items():
            report.append(f"## {section.replace('_', ' ').title()}")
            report.append(f"```json\n{json.dumps(data, indent=2)}\n```\n")
        
        return '\n'.join(report)

if __name__ == "__main__":
    agent = OSINTAgent()
    
    # Example investigation
    target = "example.com"
    asyncio.run(agent.run_investigation(target))
    
    # Generate and save report
    report = agent.generate_report()
    with open(f"osint_report_{target}.md", "w") as f:
        f.write(report)
    
    print(f"Investigation complete. Report saved for {target}")