from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
import time
from ..utilities import Utilities


class ExtDriverWait(WebDriverWait):
    def __init__(self, driver, timeout=30):
        WebDriverWait.__init__(self, driver, timeout)
        self.timeout = timeout

    def _until(self, condition, error, timeout, custom_error=None):
        timeout = timeout if timeout else self.timeout
        if custom_error is None or isinstance(custom_error, str) and custom_error.upper() == 'NONE':
            error = error.replace('<TIMEOUT>', str(timeout) + ' seconds')
        else:
            error = custom_error
        self._until_worker(condition, timeout, error)

    def _until_worker(self, condition, timeout, error):
        max_time = time.time() + timeout
        not_found = None
        while time.time() < max_time:
            try:
                if condition():
                    return
            except StaleElementReferenceException as err:
                not_found = err
            else:
                not_found = None
            time.sleep(0.2)
        raise AssertionError(not_found or error)
