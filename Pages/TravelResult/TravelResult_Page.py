from GoBearCore import *
from .TravelResult_Variables import *


class TravelResultPage():
    def __init__(self, browser):
        self.actions = GoBearCore(browser)

    def user_should_see_travel_result_page(self):
        self.travel_results_page_should_be_visible()

    def user_set_min_slider_personal_accident_on_filter(self, value):
        self.set_min_slider_personal_accident(value)

    def user_set_max_slider_trip_cancellation(self, value):
        self.set_max_slider_trip_cancellation(value)

    def user_expand_filter_options(self):
        self.expand_more_filter_options()

    def user_select_filter_option(self, option):
        self.click_on_filter_option(option)

    def user_select_filter_sort_option(self, option):
        self.click_on_sort_option(option)

    def user_filter_travel_by_policy_type(self, value):
        self.set_detail_policy_type(value)

    def user_filter_travel_by_detail_traveller(self, value):
        self.set_detail_traveller(value)

    def user_select_filter_destination(self, value):
        self.select_detail_destination(value)

    def user_set_filter_start_date(self, value):
        self.set_detail_start_date(value)

    def user_set_filter_end_date(self, value):
        self.set_detail_end_date(value)

    def user_see_result_information(self, count_result, trip_type, traveller, place, date):
        self.top_nav_should_match(count_result, trip_type, traveller, place, date)

    def user_see_result_information_with_end_date(self, count_result, trip_type, traveller, place, start_date, end_date):
        self.top_nav_with_end_date_should_match(count_result, trip_type, traveller, place, start_date, end_date)

    def travel_cards_should_be_found(self, value):
        self.number_found_travel_cards_should_be_matched(value)

    def travel_cards_should_be_at_least(self, value):
        self.number_found_travel_cards_should_at_least(value)

    def travel_results_page_should_be_visible(self):
        self.travel_result_top_result_bar_should_be_visible()
        self.wait_until_page_loaded()
        self.travel_result_filter_should_be_visible()
        self.travel_result_list_should_be_visible()
        self.travel_result_filter_should_be_visible()

    def wait_until_page_loaded(self):
        self.actions.wait_until_loaded()

    def travel_result_top_result_bar_should_be_visible(self):
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_NAV_DATA)

    def travel_result_list_should_be_visible(self):
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_LIST)

    def travel_result_filter_should_be_visible(self):
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_SB_FILTER)
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_SB_FILTER_OPTIONS)

    def travel_result_filter_detail_should_be_visible(self):
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_DETAIL_COLLAPSE)

    def click_on_filter_option(self, option):
        self.actions.select_filter_option(TRAVEL_RESULT_SB_FILTER_COLLAPSE, option)
        self.wait_until_page_loaded()

    def click_on_sort_option(self, option):
        self.actions.select_sort_option(TRAVEL_RESULT_SB_SORT_BAR, option)
        self.wait_until_page_loaded()

    def expand_more_filter_options(self):
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_SB_FILTER_COLLAPSE_BUTTON)
        self.actions.select_element(TRAVEL_RESULT_SB_FILTER_COLLAPSE_BUTTON)
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_SB_FILTER_COLLAPSE)
        self.actions.wait_until_element_is_visible(TRAVEL_RESULT_SB_FILTER_COLLAPSE_MORE)

    def set_min_slider_personal_accident(self, value):
        self.actions.set_min_slider(TRAVEL_RESULT_SB_FILTER_COLLAPSE_MORE, PERSONAL_ACCIDENT, value)
        self.wait_until_page_loaded()

    def set_max_slider_trip_cancellation(self, value):
        self.actions.set_max_slider(TRAVEL_RESULT_SB_FILTER_COLLAPSE_MORE, TRIP_CANCELLATION, value)

    def set_detail_policy_type(self, value):
        self.actions.select_detail_option(TRAVEL_RESULT_DETAIL_COLLAPSE, value)
        self.wait_until_page_loaded()

    def set_detail_traveller(self, value):
        self.actions.select_detail_option(TRAVEL_RESULT_DETAIL_COLLAPSE, value)
        self.wait_until_page_loaded()

    def select_detail_destination(self, value):
        self.actions.select_button_dropdown(TRAVEL_RESULT_FILTER_DESTINATION, value)
        self.wait_until_page_loaded()

    def set_detail_start_date(self, value):
        self.actions.set_date(TRAVEL_RESULT_FILTER_START_DATE, value)
        self.wait_until_page_loaded()

    def set_detail_end_date(self, value):
        self.actions.set_date(TRAVEL_RESULT_FILTER_END_DATE, value)
        self.wait_until_page_loaded()

    def top_nav_should_match(self, count_result, trip_type, traveller, place, date):
        expected_string = TRAVEL_RESULT_VALIDATE_FORMAT.format(count_result, trip_type, traveller, place
                                                               , date)
        self.actions.text_should_be_equal(TRAVEL_RESULT_NAV_DATA, expected_string)

    def top_nav_with_end_date_should_match(self, count_result, trip_type, traveller, place, start_date, end_date):
        expected_string = TRAVEL_RESULT_VALIDATE_WITH_DATE_FORMAT.format(count_result, trip_type, traveller, place
                                                                         , start_date, end_date)
        self.actions.text_should_be_equal(TRAVEL_RESULT_NAV_DATA, expected_string)

    def number_found_travel_cards_should_be_matched(self, value):
        self.actions.number_of_found_elements_should_be(TRAVEL_RESULT_PLAN, value,
                                                        "Number found travel cards is NOT {}".format(value))

    def number_found_travel_cards_should_at_least(self, value):
        self.actions.number_of_found_elements_should_at_least(TRAVEL_RESULT_PLAN, value,
                                                              "Number found travel cards LESS THAN {}".format(value))
