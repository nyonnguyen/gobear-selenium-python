from GoBearCore import *
from .Travel_Variables import *


class TravelPage():
    def __init__(self, browser):
        self.actions = GoBearCore(browser)

    def user_should_see_travel_tab(self):
        self.travel_tab_should_be_appeared()

    def user_navigate_to_travel_tab(self):
        self.navigate_to_travel_tab()
        self.travel_tab_should_be_appeared()

    def user_click_show_travel_result_button(self):
        self.click_travel_show_result_button()

    def navigate_to_travel_tab(self):
        self.actions.select_element(TRAVEL_LINK)

    def travel_tab_should_be_appeared(self):
        self.actions.tab_should_be_active(TRAVEL_PANEL)

    def set_trip_type(self, value):
        self.actions.select_button_dropdown(TRAVEL_TRIP_TYPE, value)

    def set_traveller(self, value):
        self.actions.select_button_dropdown(TRAVEL_TRAVELLER, value)

    def set_travel_place(self, value):
        self.actions.select_button_dropdown(TRAVEL_FROM_PLACE, value)

    def set_travel_start_date(self, value):
        self.actions.set_date(TRAVEL_STARTDATE, value)

    def set_travel_end_date(self, value):
        self.actions.set_date(TRAVEL_ENDDATE, value)

    def click_travel_show_result_button(self):
        self.actions.wait_until_element_is_enable(TRAVEL_SHOW_RESULT_BUTTON)
        self.actions.select_element(TRAVEL_SHOW_RESULT_BUTTON)

    def click_travel_reset_button(self):
        self.actions.wait_until_element_is_enable(TRAVEL_RESET_FORM_BUTTON)
        self.actions.select_element(TRAVEL_RESET_FORM_BUTTON)