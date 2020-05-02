from GoBearCore import *
from Utilities.utils import *


class BaseTest():
    def __init__(self):
        self.settings = read_yaml('settings.yaml')
        self.browser = BrowserDriver(self.settings)
        self.driver = self.browser.browser_driver
        # self.clean_old_output()

    def navigate_to_web(self):
        self.driver.get(self.settings.get('WEB_URL'))

    def prepare_test_environment(self):
        self.navigate_to_web()

    def cleanup_test_environment(self):
        self.take_screenshot()
        self.browser.browser_driver.close()
        # self.driver.quit()

    def take_screenshot(self):
        filename = gen_file_name(self.settings.get('RESULT'))
        return self.driver.save_screenshot(filename)

    def clean_old_output(self):
        remove_directory(self.settings.get('RESULT'))

    def __del__(self):
        self.driver.quit()
