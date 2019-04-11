import time
from urllib import request
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config import WEBDRIVER_PATH, BINARY_PATH, MAX_TIMEOUT, REFRESH_RATE


class WebDriverWrapper(object):
    def __init__(self, webdriver_path: str = WEBDRIVER_PATH, binary_path: str = BINARY_PATH,
                 max_timeout: float = MAX_TIMEOUT, refresh_rate: float = REFRESH_RATE):
        self._webdriver_path = webdriver_path
        self._binary_path = binary_path
        self._max_timeout = max_timeout
        self._refresh_rate = refresh_rate

        self._binary = FirefoxBinary(self._binary_path)

        self._caps = DesiredCapabilities.FIREFOX.copy()
        self._caps['marionette'] = True

        self._driver: WebDriver = Firefox(firefox_binary=self._binary,
                                          capabilities=self._caps,
                                          executable_path=webdriver_path)

        self._driver.maximize_window()

    def go_to(self, www: str):
        self._driver.get(www)

    def back(self, repeat: int = 1):
        for i in range(repeat):
            self._driver.back()

    def scrape_text(self, xpath: str) -> str:
        element = self._driver.find_element_by_xpath(xpath)
        return element.text

    def download_image(self, target_file: str, xpath: str = "//img") -> bool:
        start = time.time()
        while True:
            time.sleep(self._refresh_rate)
            try:
                element = self._driver.find_element_by_xpath(xpath)
                src = element.get_attribute("src")
                request.urlretrieve(url=src, filename=target_file)
                return True
            except:
                pass
            if time.time() - start > self._max_timeout:
                return False

    def fill_form(self, value: str, xpath: str):
        element = self._driver.find_element_by_xpath(xpath)
        element.send_keys(value)

    def click(self, xpath: str):
        element = self._driver.find_element_by_xpath(xpath)
        element.click()

    def close_tab(self):
        self._driver.close()

    def focus_on_window(self, window_index: int) -> bool:
        handles = []
        start = time.time()
        while len(handles) < window_index + 1:
            time.sleep(self._refresh_rate)
            end = time.time()
            if (end - start) > self._max_timeout:
                return False
            handles = self._driver.window_handles

        new_window = handles[window_index]
        self._driver.switch_to.window(new_window)
        return True

    def close(self):
        self._driver.quit()


if __name__ == "__main__":
    driver_wrapper = WebDriverWrapper()
