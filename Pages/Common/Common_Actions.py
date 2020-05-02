from GoBearCore.keywords import GoBearCore
from .Common_Variables import *


class CommonActions():
    def __init__(self, browser):
        self.actions = GoBearCore(browser)

    def insurance_should_be_visible(self):
        self.actions.wait_until_element_is_visible(INSURANCE)

    def navigate_to_insurance(self):
        self.actions.select_element(INSURANCE)

