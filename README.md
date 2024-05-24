
 # Web Scraping and MongoDB Insertion

This Python script is designed to scrape data from multiple websites and insert it into a MongoDB database. It utilizes the requests library to make HTTP requests, BeautifulSoup for parsing HTML, and pymongo to interact with the MongoDB database.

## Requirements

- Python 3.x
- BeautifulSoup4 (`pip install beautifulsoup4`)
- pymongo (`pip install pymongo`)

## Usage

1. Make sure you have MongoDB installed and running on your system.
2. Install the required Python packages using pip.
3. Configure the MongoDB connection details in the script (`MONGO_HOST`, `MONGO_PORT`, `MONGO_DB`, `MONGO_COLLECTION`).
4. Run the script using Python.

## Functionality

- The script contains functions to scrape data from three different URLs.
- Each scraping function extracts specific information from the HTML content of the webpage.
- Scraped data is then inserted into a MongoDB database.
- Error handling is implemented to log any issues encountered during scraping or database insertion.

## Files

- `scraping_errors.log`: Log file to store any errors encountered during scraping.
- `README.md`: This file containing instructions and information about the script.

## Additional Notes

- Ensure that you have the necessary permissions to write to the MongoDB database.
- Check the URLs being scraped and adjust the scraping functions accordingly if the HTML structure changes.
- Monitor the log file (`scraping_errors.log`) for any errors or issues during scraping.

