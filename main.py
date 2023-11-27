import requests
from bs4 import BeautifulSoup
import openpyxl
import win32clipboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Function to scrape the transcript using Selenium
def scrape_transcript(video_url):
    # Setup the Selenium ChromeDriver with suppressed error logging
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppresses the USB errors

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open the TikTok transcript tool website
    driver.get('https://script.tokaudit.io/')

    time.sleep(5)  # Adjust the sleep time if necessary

    # Find the input element and set the video URL
    input_element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Insert a Tiktok video...']")
    input_element.send_keys(video_url)

    # Find the START button and click it
    start_button = driver.find_element(By.XPATH, "//button[contains(., 'START')]")
    start_button.click()

    time.sleep(5) 
    wait = WebDriverWait(driver, 2)  # Adjust the timeout as necessary

    # hide_timestamps_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Hide Timestamps')]/preceding-sibling::input[@type='checkbox']")))
    # hide_timestamps_checkbox.click()

    # Attempt to find the checkbox and handle potential timeout
    try:
        hide_timestamps_checkbox = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Hide Timestamps')]/preceding-sibling::input[@type='checkbox']")))
        hide_timestamps_checkbox.click()
    except TimeoutException:
        print(f"Failed to find the 'Hide Timestamps' checkbox for URL: {video_url}")
        return None  # Or use an empty string '' if that's more appropriate for your data handling


    # Wait for the "Copy" button to be clickable and click it using JavaScript
    copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copy')]")))
    driver.execute_script("arguments[0].click();", copy_button)

    # Use pyperclip to get the copied text from the clipboard
    time.sleep(1)  # Give it a moment for the text to be copied
    transcript = pyperclip.paste()

    driver.quit()

    return transcript


# Function to save all video URLs and their transcripts to an Excel file
def save_all_to_excel(video_urls, transcripts):
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set the column headers
    sheet['A1'] = 'Video URL'
    sheet['B1'] = 'Transcript'

    # Add all video URLs and their transcripts to the worksheet
    for video_url, transcript in zip(video_urls, transcripts):
        sheet.append([video_url, transcript])

    # Save the workbook
    workbook.save('transcripts.xlsx')

# Example usage
# video_url = "https://www.tiktok.com/@healthytome/video/7256897171285527854"
video_urls = [
    "https://www.tiktok.com/@healthytome/video/7256897171285527854",
    "https://www.tiktok.com/@healthytome/video/7257939923163041066"
    # ... add more video URLs here
]

# Dictionary to store video URLs and their transcripts
video_data = {}

# Iterate over all video URLs and scrape their transcripts
for video_url in video_urls:
    try:
        transcript = scrape_transcript(video_url)
        if transcript:  # If a transcript was successfully scraped
            video_data[video_url] = transcript
            print(transcript)
        else:
            print(f"No transcript found for URL: {video_url}")
    except Exception as e:
        print(f"An error occurred for URL: {video_url}: {e}")


# Save all video URLs and their transcripts to an Excel file
if video_data:
    save_all_to_excel(list(video_data.keys()), list(video_data.values()))


