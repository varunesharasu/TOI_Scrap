from scraper.toi_scraper import parse_headlines


def test_parse_headlines_basic():
    html = """
    <html><body>
      <h1><a href="/news/india/article1">Headline One</a></h1>
      <div class="story"><a href="https://timesofindia.indiatimes.com/news/article2">Headline Two</a></div>
      <h2 class="title"><a href="//timesofindia.indiatimes.com/news/article3">Headline Three</a></h2>
      <!-- navigation like language links that should be ignored -->
      <a href="/">IN</a>
      <a href="/us">US</a>
    </body></html>
    """
    res = parse_headlines(html, max_items=10)
    titles = [r["title"] for r in res]
    assert "Headline One" in titles
    assert "Headline Two" in titles
    assert "Headline Three" in titles
    assert "IN" not in titles
    assert "US" not in titles

