from playwright.sync_api import sync_playwright
import time
from random import random 
from dotenv import load_dotenv
import os

def facebook_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://www.facebook.com/")

        load_dotenv()
        facebook_email = str(os.getenv('FACEBOOK_EMAIL'))
        facebook_password = str(os.getenv('FACEBOOK_PASSWORD'))

        time.sleep(5)
        page.get_by_test_id("royal_email").click()
        time.sleep(1)
        page.get_by_test_id("royal_email").press_sequentially(facebook_email)
        time.sleep(1)
        page.get_by_test_id("royal_pass").click()
        time.sleep(1)
        page.get_by_test_id("royal_pass").press_sequentially(facebook_password)
        time.sleep(1)
        page.get_by_test_id("royal_login_button").click()
        time.sleep(5)
        #page.get_by_label("Close").click()
        
        # Save authentication state to a file
        context.storage_state(path="playwright_login/facebook_auth.json")
        browser.close()

def facebook_test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="playwright_login/facebook_auth.json")

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://facebook.com")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    facebook_login_and_save_auth()
    time.sleep(5)
    facebook_test_auth()
