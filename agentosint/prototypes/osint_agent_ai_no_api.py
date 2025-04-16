import requests
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
        """Search for username across multiple platforms using web scraping"""
        results = {}
        try:
            # Check Twitter (web scraping)
            twitter_url = f"https://twitter.com/{username}"
            response = requests.get(twitter_url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                name_tag = soup.find('div', {'data-testid': 'UserName'})
                results['twitter'] = {
                    'exists': True,
                    'name': name_tag.text.split('\n')[1] if name_tag else None,
                    'bio': soup.find('div', {'data-testid': 'UserDescription'}).text if soup.find('div', {'data-testid': 'UserDescription'}) else None
                }
            else:
                results['twitter'] = {'exists': False}
        except Exception as e:
            print(f"Social media search error: {e}")
        return results

    async def search_web(self, keyword: str) -> Dict:
        """Search web using DuckDuckGo"""
        results = {}
        try:
            ddg_url = "https://html.duckduckgo.com/html/"
            params = {'q': keyword, 'kl': 'en-us'}
            response = requests.post(ddg_url, data=params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            web_results = []
            for result in soup.find_all('div', class_='result__body'):
                title = result.find('h2').text
                link = result.find('a', class_='result__url')['href']
                snippet = result.find('a', class_='result__snippet').text
                web_results.append({'title': title, 'link': link, 'snippet': snippet})
            
            results['web_results'] = web_results
        except Exception as e:
            print(f"Web search error: {e}")
        return results

    async def domain_lookup(self, domain: str) -> Dict:
        """Perform WHOIS lookup and basic domain analysis"""
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
        """Basic email analysis without external APIs"""
        try:
            return {
                'breaches': 'Unknown (API-less version)',
                'valid_format': re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None,
                'disposable': self._check_disposable_email(email)
            }
        except Exception as e:
            print(f"Email analysis error: {e}")
            return {}

    def _check_disposable_email(self, email: str) -> bool:
        """Check against known disposable email domains"""
        domain = email.split('@')[-1]
        disposable_domains = {
            'mailinator.com', 'tempmail.org', '10minutemail.com',
            'guerrillamail.com', 'throwawaymail.com'
        }
        return domain in disposable_domains

    async def news_analysis(self, keyword: str) -> Dict:
        """Scrape Google News results"""
        try:
            news_url = f"https://news.google.com/search?q={keyword}"
            response = requests.get(news_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            for article in soup.find_all('article')[:5]:
                title = article.find('a', class_='DY5T1d').text
                link = f"https://news.google.com{article.find('a', class_='DY5T1d')['href'][1:]}"
                source = article.find('a', class_='wEwyrc').text
                articles.append({'title': title, 'link': link, 'source': source})
            
            return {'articles': articles}
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
            'domain_info': self.domain_lookup(target) if '.' in target else {},
            'email_info': self.email_analysis(target) if '@' in target else {},
            'news': self.news_analysis(target)
        }
        
        results = {}
        for name, task in tasks.items():
            results[name] = await task
        
        # Add sentiment analysis to news results
        if 'news' in results:
            for article in results['news'].get('articles', []):
                article['sentiment'] = self.analyze_sentiment(article.get('title', ''))
        
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