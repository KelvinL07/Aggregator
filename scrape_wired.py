from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

webdriver_path = 'C:/Users/Kelvi/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Ensure this path is correct

service = Service(webdriver_path)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.wired.com/"

driver.get(url)

wait = WebDriverWait(driver, 20)

try:
    main_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'main')))
except Exception as e:
    print(f"Exception: {e}")
    driver.quit()
    exit()

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait to load page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


articles = []
try:
    article_elements = main_content.find_elements(By.CSS_SELECTOR, 'a.SummaryItemHedLink-civMjp')
    for element in article_elements:
        try:
            title_element = element.find_element(By.CSS_SELECTOR, 'h3')
            title = title_element.text
            link = element.get_attribute('href')
            articles.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Exception extracting article: {e}")
except Exception as e:
    print(f"Exception extracting articles: {e}")


print(f"Collected {len(articles)} articles.")
for article in articles:
    print(f"Title: {article['title']}, Link: {article['link']}")


html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title Aggregator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fff;
            color: #000;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            text-decoration: none;
            color: #000;
        }
    </style>
</head>
<body>
    <h1>Title Aggregator</h1>
    <ul>
'''

for article in articles:
    html_content += f'<li><a href="{article["link"]}">{article["title"]}</a></li>\n'

html_content += '''
    </ul>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML file generated successfully!")


driver.quit()
