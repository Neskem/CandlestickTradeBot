import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait


class CandlestickBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-features=RendererCodeIntegrity")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(chrome_options)

    def click(self, url: str):
        self.driver.get(url)

    def wait_and_click(self, wait_seconds: int, elements_path: str):
        wait = WebDriverWait(self.driver, wait_seconds)
        element_to_click = wait.until(
            EC.element_to_be_clickable((By.XPATH, elements_path)))
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_click).perform()
        element_to_click.click()

    def parse_alerts(self, wait_seconds: int, elements_path: str):
        wait = WebDriverWait(self.driver, wait_seconds)
        while True:
            # Determine if the minute is a multiple of 6.
            current_minute = datetime.now().minute
            if current_minute % 10 != 6:
                continue
            print("Start to parse elements")
            # Wait for alerts element
            message_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, elements_path)))

            for i, message_element in enumerate(message_elements):
                message_content = message_element.text
                print("Message：", message_content)

                # Parse time
                time_line = message_content.split("\n")[-1]
                try:
                    message_time = datetime.strptime(time_line, "%H:%M")
                    today_date = datetime.now().date()
                    full_date_time = datetime.combine(today_date, message_time.time())
                    time_difference = datetime.now() - full_date_time
                    if time_difference.total_seconds() <= 300:
                        print("Current time: ", full_date_time)
                except ValueError:
                    print("Can not parse time.")

            # Check for updates again after waiting for a while.
            time.sleep(60)

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    bot = CandlestickBot()
    bot.click('https://web.telegram.org/k/')

    bot.wait_and_click(20, '//*[@id="folders-container"]/div/div[1]/ul/a[1]/div[1]')

    bot.parse_alerts(20, '//*[@id="column-center"]/div/div/div[3]/div/div/section')
