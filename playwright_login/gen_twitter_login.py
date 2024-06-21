from playwright.sync_api import sync_playwright
import time
from random import random 
from dotenv import load_dotenv
import os

def x_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://x.com/login")

        load_dotenv()
        x_email = str(os.getenv('X_EMAIL'))
        x_username = str(os.getenv('X_USERNAME'))
        x_password = str(os.getenv('X_PASSWORD'))

        time.sleep(5)
        # page.get_by_role("button", name = 'Sign in', exact = True).click()
        page.get_by_label("Phone, email, or username").click()
        time.sleep(1)
        page.get_by_label("Phone, email, or username").press_sequentially(x_email)
        time.sleep(1)
        page.get_by_label("Phone, email, or username").press("Enter")
        time.sleep(1)
        # page.get_by_test_id("ocfEnterTextTextInput").click()
        # page.get_by_test_id("ocfEnterTextTextInput").fill(x_username)
        # page.get_by_test_id("ocfEnterTextTextInput").press("Enter")
        page.get_by_label("Password", exact=True).fill(x_password)
        time.sleep(1)
        page.get_by_label("Password", exact=True).press("Enter")
        time.sleep(5)

        # # Wait for navigation or some element indicating successful login
        # page.wait_for_load_state("networkidle")
        
        # Save authentication state to a file
        context.storage_state(path="playwright_login/x_auth.json")

        browser.close()

def x_test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="playwright_login/twitter_auth.json")

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://twitter.com")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    x_login_and_save_auth()
    time.sleep(5)
    x_test_auth()
