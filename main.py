from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome('/chromedriver')

url = 'https://finance.yahoo.com/quote/NQ%3DF/history?period1=969235200&period2=1685232000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
driver.get(url)

# Define the number of times to scroll
scroll_times = 3


import time
# Scroll down multiple times to load more data
for _ in range(scroll_times):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    # Wait for a short interval after each scroll
    time.sleep(0.25)

# Find the table containing historical prices
table = driver.find_element(By.CSS_SELECTOR, 'table[data-test="historical-prices"]')


# Open a CSV file for writing
with open('historical_prices.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the title/header to the CSV file
    title = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    writer.writerow(title)
    
    # Extract data from the table
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 7:
            date = cells[0].text
            open_price = cells[1].text
            high_price = cells[2].text
            low_price = cells[3].text
            close_price = cells[4].text
            adj_close = cells[5].text
            vol = cells[6].text
            # Process or store the extracted data as needed
            print(date, open_price, high_price, low_price, close_price, adj_close, vol)
           # Write the extracted data to the CSV file
            writer.writerow([date, open_price, high_price, low_price, close_price, adj_close, vol])

# Quit the WebDriver
driver.quit()
