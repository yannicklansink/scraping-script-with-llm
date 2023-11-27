from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
def scrape_transcript(driver, video_url):
    try:
        # Load the page
        driver.get('https://script.tokaudit.io/')

        # Wait for the input element to be present and set the video URL
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Insert a Tiktok video...']"))
        )
        input_element.clear()
        input_element.send_keys(video_url)

        # Find the START button and click it
        start_button = driver.find_element(By.XPATH, "//button[contains(., 'START')]")
        start_button.click()

        # Wait for the 'Hide Timestamps' checkbox to be clickable and click it
        time.sleep(3)
        wait = WebDriverWait(driver, 10)
        hide_timestamps_checkbox = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(text(), 'Hide Timestamps')]/preceding-sibling::input[@type='checkbox']")))
        hide_timestamps_checkbox.click()


        # Wait for the "Copy" button to be clickable and click it using JavaScript
        copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copy')]")))
        driver.execute_script("arguments[0].click();", copy_button)

        # Wait a moment for the text to be copied and then get it from the clipboard
        time.sleep(1)
        transcript = pyperclip.paste()

        return transcript
    except TimeoutException:
        print(f"Timeout occurred for URL: {video_url}")
    except NoSuchElementException:
        print(f"Element not found for URL: {video_url}")
    except Exception as e:
        print(f"An error occurred for URL: {video_url}: {e}")

    return None

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

# Setup the Selenium ChromeDriver outside of the loop
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

video_urls = [
    "https://www.tiktok.com/@healthytome/video/7256897171285527854",
    "https://www.tiktok.com/@healthytome/video/7257939923163041066"
    # ... add more video URLs here
]

# Iterate over all video URLs and scrape their transcripts
video_data = {}
for video_url in video_urls:
    transcript = scrape_transcript(driver, video_url)
    if transcript:
        video_data[video_url] = transcript
        print(transcript)
    else:
        print(f"No transcript found for URL: {video_url}")

# Close the driver after all URLs are processed
driver.quit()

# Save all video URLs and their transcripts to an Excel file
if video_data:
    save_all_to_excel(list(video_data.keys()), list(video_data.values()))
