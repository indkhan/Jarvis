
from newspaper import Article
import feedparser
from groq import Groq

groq_client = Groq(api_key="your-groq-api-key")

def fetch_news(sources):
    """Fetch news from configured sources"""
    news_items = []
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:5]:
            article = Article(entry.link)
            try:
                article.download()
                article.parse()
                news_items.append({
                    'title': entry.title,
                    'text': article.text,
                    'source': source['name'],
                    'url': entry.link,
                    'published': entry.published
                })
            except:
                continue
    
    return news_items

def summarize_news(news_items):
    """Summarize news articles using Groq"""
    summaries = []
    for item in news_items:
        prompt = f"Summarize this news article in 2-3 sentences: {item['text']}"
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        summaries.append({
            **item,
            'summary': response.choices[0].message.content
        })
    return summaries
