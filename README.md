TOI_Scrap
=========

Minimal Times of India homepage scraper.

Setup
-----

1. Create and activate a Python virtual environment (Python 3.8+ recommended).
2. Install dependencies:

   pip install -r requirements.txt

Usage
-----

Run the simple CLI:

   python run_scraper.py

Or import `scraper.toi_scraper.get_top_headlines` in your code.

Notes
-----

- This scraper only fetches the homepage and extracts anchor text/links. It
  won't run heavy JavaScript. For richer scraping use Playwright or Selenium.
-- Respect terms of service and robots.txt. This is for educational/testing only.


Developer
---------

If you see "No module named pytest" when running tests, make sure you install
the test dependencies using the exact Python interpreter you use to run
commands. From Windows cmd.exe, run:

```cmd
python -m pip install -r d:\Projects\TOI_Scrap\dev-requirements.txt
```

Then run tests with the same interpreter:

```cmd
python -m pytest -q d:\Projects\TOI_Scrap\tests
```

If you have multiple Python versions installed, replace `python` with the
full path to the interpreter you intend to use. Example:

```cmd
C:\Users\Varunesh.T\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r d:\Projects\TOI_Scrap\dev-requirements.txt
C:\Users\Varunesh.T\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q d:\Projects\TOI_Scrap\tests
```
