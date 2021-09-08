from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as SE
import time
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("--start_maximized")
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://mail.ru/")

login = driver.find_element_by_class_name("email-input")
login.send_keys("study.ai_172@mail.ru")
login.send_keys(Keys.ENTER)

time.sleep(0.5)

passw = driver.find_element_by_class_name("password-input")
passw.send_keys("NextPassword172???")
passw.send_keys(Keys.ENTER)

# page = driver.find_element_by_tag_name('body')
# page.send_keys(Keys.DOWN)
urls_list = set()
time.sleep(5)
while True:
    time.sleep(1)
    url_amount = len(urls_list)
    urls = driver.find_elements_by_xpath('//a[contains(@class,"llc")]')
    for url in urls:
        urls_list.add(url.get_property('href'))
    ActionChains(driver).move_to_element(urls[-1]).perform()
    try:
        urls[-1].send_keys(Keys.PAGE_DOWN)
    except SE.ElementNotInteractableException:
        break

letter_list = []
for url in urls_list:
    letter = {}
    driver.get(url)
    time.sleep(1.5)
    author = driver.find_element_by_xpath('//div[contains(@class, "letter__author")]/span[contains(@class, "letter-contact")]').text
    author_email = driver.find_element_by_xpath('//div[contains(@class, "letter__author")]/span[contains(@class, "letter-contact")]').get_attribute('title')
    data = driver.find_element_by_xpath('//div[contains(@class, "letter__author")]/div[contains(@class, "letter__date")]').text
    header = driver.find_element_by_xpath('//div/h2').text
    text = driver.find_element_by_xpath('//div[contains(@class, "letter-body")]').text

    letter['author'] = author
    letter['author_email'] = author_email
    letter['data'] = data
    letter['header'] = header
    letter['text'] = text

    letter_list.append(letter)

client = MongoClient('127.0.0.1', 27017)
db = client['letters']
mailru = db.mailru
mailru.insert_many(letter_list)

print(mailru)


