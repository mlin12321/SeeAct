from playwright.sync_api import sync_playwright
import time
from random import random 
from dotenv import load_dotenv
import os

def spotify_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://www.spotify.com/")

        load_dotenv()
        spotify_email = str(os.getenv('SPOTIFY_EMAIL'))
        spotify_password = str(os.getenv('SPOTIFY_PASSWORD'))

        time.sleep(5)
        page.get_by_test_id("login-button").click()
        time.sleep(1)
        page.get_by_test_id("login-username").click()
        time.sleep(1)
        page.get_by_test_id("login-username").press_sequentially(spotify_email)
        time.sleep(1)
        page.get_by_test_id("login-password").click()
        time.sleep(1)
        page.get_by_test_id("login-password").press_sequentially(spotify_password)
        time.sleep(1)
        page.get_by_test_id("login-button").click()
        time.sleep(5)
        
        # Save authentication state to a file
        context.storage_state(path="playwright_login/spotify_auth.json")
        browser.close()

def spotify_test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="playwright_login/spotify_auth.json")

        # Replace with your login page URL
        page = context.new_page()
        page.goto("https://spotify.com")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    spotify_login_and_save_auth()
    time.sleep(5)
    spotify_test_auth()
