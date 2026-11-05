# Wishlist-Stock-Checker

A hobby project that monitors product availability at a local store. It scrapes product information, compares current stock levels against previously saved data and sends email notifications when wishlist items become available.

The project is split into several Python modules, each handling a specific part of the workflow.

Skills learned:
- Web scraping and regex-based data extraction
- Custom product filtering and comparison logic
- JSON data storage and persistence
- Configuration management using `.env` files
- Jinja2 HTML templating
- Sending email notifications through SMTP
- Structuring Python projects into reusable modules

## 📂 Project Structure

- **main.py** – Entry point that coordinates the stock-checking workflow and connects all modules.
- **config.py** – Loads environment variables from `.env` and manages application settings, such as store URLs and SMTP credentials.
- **utils.py** – Contains helper functions for saving and loading data, including previously scraped product information stored in JSON files.
- **scraper.py** – Scrapes product pages from the local store and extracts product information using HTML parsing and regex.
- **comparer.py** – Compares newly scraped stock information against previously saved JSON data to identify relevant stock changes.
- **composer.py** – Collects the relevant product information and renders an HTML email using the Jinja2 template.
- **mailer.py** – Sends the generated notification emails using SMTP through the configured email provider.
- **wishlist.txt** – Contains the list of products to monitor, with one product per line.
- **notification_template.html** – Jinja2 HTML template used to format stock notification emails.
