from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.wait import WebDriverWait
from botEngine import login,collect_followers,filter_followers,removeDuplicates
from sqlClass import sqlClass

# initialize()
account_to_check = input("Enter the account to check: ")
login()
usernames = collect_followers(account_to_check)
filter_followers(usernames)
removeDuplicates("shopier")

print("Done")