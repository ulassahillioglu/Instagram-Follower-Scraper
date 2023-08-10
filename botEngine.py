from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.wait import WebDriverWait
import time, re, os
from urllib.parse import unquote, urlparse, parse_qs
import requests as rq
from sqlClass import sqlClass
from datetime import datetime, timedelta


def initialize():
    global table_name
    db = sqlClass("instaDB.db")
    table_name = input("Enter table name:  (using underscores or camelCase is recommended) ")
    db.createTable(table_name)
    

    
    session = rq.Session()

    firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.binary_location = firefox_binary_path

    user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36"
    firefox_options.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(options=firefox_options)

    # chrome_binary_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36"
    # Get the current working directory
    # current_directory = os.getcwd()

    # # Create the log file path
    # log_file_path = os.path.join(current_directory, "chromedriver.log")
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = chrome_binary_path
    # chrome_options.add_argument(f'user-agent={user_agent}')
    # chrome_options.add_argument("--enable-logging")
    # chrome_options.add_argument(f"--log-path={log_file_path}")
    # chrome_options.add_argument("--verbose")

    # driver = webdriver.Chrome(options=chrome_options)

    # username = ""
    # password = """"""

    # username = ""
    # password = """"""

    # username = ""
    # password = """"""

    username = "hannahdenaudis"
    password = """sifre.09aa"""

    driver.implicitly_wait(10)
    return db, session, driver, username, password


db, session, driver, username, password = initialize()




def login():
    # Open Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")

    # Wait for the login page to load
    login_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )

    print("Page Ready")

    # Enter username and password
    time.sleep(2)
    username_input = login_form.find_element(By.NAME, "username")
    time.sleep(2)
    password_input = login_form.find_element(By.NAME, "password")
    time.sleep(2)
    username_input.send_keys(username)
    time.sleep(2)
    password_input.send_keys(password)
    time.sleep(2)

    print("Logging in ... ")
    # Submit the login form
    # login_button = login_form.find_element(By.XPATH, "Giriş yap")

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )

    time.sleep(5)
    login_button.click()

    # Do something on the home page (e.g., print the page title)
    print("Logged in successfully!")
    print("Page title:", driver.title)

    try:
        save_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_ac8f"))
        )
        time.sleep(5)
        save_button.click()

        print("Continue ...")
    except:
        print("Continue without saving ...")

    try:
        not_now = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Not Now')]")
            )
        )
        not_now.click()
    except:
        pass
    # Wait for the home page to load after login
    time.sleep(3)
    print("Continue ...")





def collect_followers(username):
    profile_link = f"https://www.instagram.com/{username}"
    print(profile_link)

    driver.get(profile_link)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/followers/')]")
            )
        ).click()
    except:
        print("Error")
        driver.quit()

    index = 1
    time.sleep(150) ####Duration on follower list
    if index % 100 == 0:
        time.sleep(60)

    print("Check . . .")
    content = driver.execute_script(
        "return document.getElementsByTagName('html')[0].innerHTML"
    )
    with open("source1.html", "w", encoding="utf-8") as s1:
        s1.write(content)
        s1.close()

    soup = bs(content, features="html.parser")

    hrefs = set()
    for anchor_tag in soup.find_all("a", {"class": "x1i10hfl"}):
        if (
            "reels" not in anchor_tag["href"]
            and "explore" not in anchor_tag["href"]
            and username not in anchor_tag["href"]
            and "inbox" not in anchor_tag["href"]
        ):
            hrefs.add(anchor_tag["href"].strip("/"))

    list_hrefs = list(hrefs)
    print(list_hrefs, len(list_hrefs))
    # Create a list of elements to remove
    elements_to_remove = ["", " ", "#"]

    # Use a loop to remove elements from the list
    for element in elements_to_remove:
        if element in list_hrefs:
            list_hrefs.remove(element)

    return list_hrefs


def filter_followers(usernames):
    # username_input = input("Enter username: ")
    for index, username in enumerate(usernames):
        print(f"Profil no: {index+1} {username}")
        profile_link = f"https://www.instagram.com/{username}"
        hrefs = []
        external_urls = []

        driver.get(profile_link)
        time.sleep(6)

        content = driver.execute_script(
            "return document.getElementsByTagName('html')[0].innerHTML"
        )
        with open("source1.html", "w", encoding="utf-8") as s1:
            s1.write(content)
            s1.close()

        soup = bs(content, features="html.parser")

        #Get followers and followees count
        span_with_title = soup.find("span", class_="_ac2a", title=True)
        last_span = soup.select('li>a>span>span',{'class':'_ac2a'},title=False)

        

        if span_with_title is None:
            print(f"No title attribute found for {username}.")
            exit()

        # Extract the title value
        title_value = span_with_title["title"]
        follower_count = int(title_value.replace(",", "").replace(".", ""))
        followees_count = last_span[1].text
        
        db.insertData(
                            table_name,
                            (
                                username,
                                follower_count,
                                followees_count,
                                
                                
                            ),
                    )
        
                   

        

        print("***************************************************")
        time.sleep(5)
    # Wait for the external URL element to load


def removeDuplicates(table):
    db.removeDuplicatesByUserName(table)


def main(usernames):
    login()
    for username in usernames:
        filter_followers(username)
    driver.quit()
    db.removeDuplicatesByUserName("table_name")



if '__name__' =='__main__':
    print("Main")