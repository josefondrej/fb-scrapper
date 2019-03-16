from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebDriverWrapper(object):
    def __init__(self, webdriver_path: str = "/home/josef/Downloads/geckodriver-v0.24.0-linux64/geckodriver",
                 binary_path: str = "/usr/bin/firefox"):
        self._webdriver_path = webdriver_path
        self._binary_path = binary_path

        self._binary = FirefoxBinary(r'/usr/bin/firefox')

        self._caps = DesiredCapabilities.FIREFOX.copy()
        self._caps['marionette'] = False

        self._driver: WebDriver = Firefox(firefox_binary=self._binary,
                                          capabilities=self._caps,
                                          executable_path=webdriver_path)

    def go_to(self, www: str):
        self._driver.navigate.to(www)

    def back(self):
        self._driver.navigate.back()

    def scrape_text(self, xpath: str) -> str:
        element = self._driver.find_element_by_xpath(xpath)
        return element.text

    def close(self):
        self._driver.close()

if __name__ == "__main__":
    driver_wrapper = WebDriverWrapper()
