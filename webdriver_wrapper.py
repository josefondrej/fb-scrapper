from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import WEBDRIVER_PATH, BINARY_PATH


class WebDriverWrapper(object):
    def __init__(self, webdriver_path: str = WEBDRIVER_PATH, binary_path: str = BINARY_PATH):
        self._webdriver_path = webdriver_path
        self._binary_path = binary_path

        self._binary = FirefoxBinary(self._binary_path)

        self._caps = DesiredCapabilities.FIREFOX.copy()
        self._caps['marionette'] = True

        self._driver: WebDriver = Firefox(firefox_binary=self._binary,
                                          capabilities=self._caps,
                                          executable_path=webdriver_path)

        self._driver.maximize_window()

    def go_to(self, www: str):
        self._driver.get(www)

    def back(self):
        self._driver.back()

    def scrape_text(self, xpath: str) -> str:
        element = self._driver.find_element_by_xpath(xpath)
        return element.text

    def fill_form(self, value: str, xpath: str):
        element = self._driver.find_element_by_xpath(xpath)
        element.send_keys(value)

    def click(self, xpath: str):
        element = self._driver.find_element_by_xpath(xpath)
        element.click()

    def close(self):
        self._driver.close()


if __name__ == "__main__":
    driver_wrapper = WebDriverWrapper()
