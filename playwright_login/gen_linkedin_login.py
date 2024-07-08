from playwright.sync_api import sync_playwright
import time
from random import random 
from dotenv import load_dotenv
import os

def linkedin_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://linkedin.com/")

        load_dotenv()
        linkedin_email = str(os.getenv('LINKEDIN_EMAIL'))
        linkedin_password = str(os.getenv('LINKEDIN_PASSWORD'))

        time.sleep(5)
        page.locator("[data-test-id=\"home-hero-sign-in-cta\"]").click()
        time.sleep(1)
        page.get_by_label("Email or Phone").click()
        time.sleep(1)
        page.get_by_label("Email or Phone").press_sequentially(linkedin_email)
        time.sleep(1)
        page.get_by_label("Password").click()
        time.sleep(1)
        page.get_by_label("Password").press_sequentially(linkedin_password)
        time.sleep(1)
        page.get_by_label("Sign in", exact=True).click()
        time.sleep(5)

        # Save authentication state to a file
        context.storage_state(path="playwright_login/linkedin_auth.json")
        context.storage_state(path="playwright_login/linkedin_jobs_auth.json")

        browser.close()

def linkedin_test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="playwright_login/linkedin_auth.json")

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://linkedin.com/")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    # linkedin_login_and_save_auth()
    # time.sleep(5)
    linkedin_test_auth()
