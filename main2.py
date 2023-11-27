from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
# Configureer ChromeOptions om SSL-fouten te negeren (indien nodig)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')

# Start de WebDriver met de geconfigureerde opties
# service = Service('D:\\chromedriver.exe')  # Voeg het pad naar je chromedriver toe
# driver = webdriver.Chrome(service=service, options=chrome_options)

driver = webdriver.Chrome('D:\\chromedriver.exe')  # Optional argument, if not specified will search path.



# Verzamel de URLs van de TikTok-video's
video_urls = ['https://www.tiktok.com/@healthytome/video/7256897171285527854?q=%23health&t=1701082211538']

# DataFrame voor opslaan van data
data = {"URL": [], "Transcript": []}

for url in video_urls:
    # Navigeer naar de transcript tool
    driver.get("https://script.tokaudit.io/")

    # Voer de URL in en start het proces
    input_element = driver.find_element(By.CSS_SELECTOR, "input.block.w-full.px-10.py-4.text-base.font-light.text-gray-900.shadow.bg-white.bg-clip-padding.rounded-3xl.transition.ease-in-out.m-0")
    input_element.send_keys(url)

    # Zoek de START knop op basis van zijn tekst
    start_button = driver.find_element_by_xpath("//button[contains(text(), 'START')]")
    start_button.click()

    # Wacht tot het transcript verschijnt
    time.sleep(5)  # Aanpassen op basis van de laadtijd

    # Klik op de input checkbox element "Hide Timestamps"
    checkbox_element = driver.find_element_by_xpath("//input[@name='Hide Timestamps']")
    checkbox_element.click()

    # Selecteer het transcriptelement
    transcript_element = driver.find_element_by_css_selector(".bg-pink-600.text-white")
    transcript = transcript_element.text

    # Voeg data toe aan DataFrame
    data["URL"].append(url)
    data["Transcript"].append(transcript)

# Sluit de WebDriver
driver.quit()

# Maak een DataFrame en sla het op als Excel
df = pd.DataFrame(data)
df.to_excel("tiktok_transcripts.xlsx", index=False)
