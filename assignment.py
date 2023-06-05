from selenium import webdriver
from scrapy import Selector
import time,csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--page-load-strategy=normal")  # Set page load strategy
driver = webdriver.Chrome(options=chrome_options)
url = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"
result = []
for i in range(5):
    driver.get(url=url)
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 350);")
    time.sleep(1)
    x_path = "//tr[@role='row']/td[2]/a"
    nav = driver.find_elements(By.XPATH, x_path)
    nav[i].click()
    time.sleep(5)
    navigation_html = driver.page_source
    sel_new = Selector(text=navigation_html)
    est_value = sel_new.xpath("//td[contains(text(), 'Value Notes')]/parent::*/td[2]/text()").get()
    description = sel_new.xpath("//td[contains(text(), 'Description')]/parent::*/td[2]/text()").extract()
    closing_date = sel_new.xpath("//td[contains(text(), 'Closing Date')]/parent::*/td[2]/text()").get()
    result.append({"Est. Value Notes":est_value, "Description":description[0], "Additional Description":description[-1], "Closing Date":closing_date})
    print(result[-1])
    print(" ")
    time.sleep(1)

field_names = ["Est. Value Notes", "Description", "Additional Description", "Closing Date"]
filename = "assignment1.csv"

# Open the CSV file in write mode and write the data
with open(filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    # Write the header
    writer.writeheader()

    # Write the data rows
    for row in result:
        writer.writerow(row)

print("CSV file created successfully.")
