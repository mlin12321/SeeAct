from playwright.sync_api import sync_playwright
import time
from random import random 
import os
from dotenv import load_dotenv

def glassdoor_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://glassdoor.com")

        load_dotenv()
        glassdoor_email = str(os.getenv('GLASSDOOR_EMAIL'))
        glassdoor_password = str(os.getenv('GLASSDOOR_PASSWORD'))

        time.sleep(5)
        page.get_by_label("Enter Email").click()
        time.sleep(1)
        page.get_by_label("Enter Email").fill(glassdoor_email)
        time.sleep(1)
        page.get_by_label("Enter Email").press("Enter")
        time.sleep(1)
        page.get_by_test_id("passwordInput").get_by_label("Password").fill(glassdoor_password)
        time.sleep(1)
        page.get_by_test_id("passwordInput").get_by_label("Password").press("Enter")
        time.sleep(5)

        # ---------------------

        # # Wait for navigation or some element indicating successful login
        # page.wait_for_load_state("networkidle")
        
        # Save authentication state to a file
        context.storage_state(path="playwright_login/glassdoor_auth.json")

        browser.close()

def glassdoor_test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="playwright_login/glassdoor_auth.json")

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://glassdoor.com")
        
        browser.close()

if __name__ == "__main__":
    glassdoor_login_and_save_auth()
    time.sleep(5)
    glassdoor_test_auth()
