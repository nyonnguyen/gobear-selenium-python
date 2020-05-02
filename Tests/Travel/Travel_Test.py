# Python code to demonstrate working of unittest
import unittest
from Tests.base_test import BaseTest
from Pages.Common.Common_Actions import CommonActions
from Pages.Travel.Travel_Page import TravelPage
from Pages.TravelResult.TravelResult_Page import TravelResultPage
from Utilities.utils import *


class TravelTest(unittest.TestCase):

    def setUp(self):
        self.test = BaseTest()
        self.test.prepare_test_environment()
        CommonPage = CommonActions(self.test.browser)
        CommonPage.insurance_should_be_visible()
        CommonPage.navigate_to_insurance()
        data = read_yaml("Tests/Travel/travel_data.yaml")
        self.data1 = data.get('TEST1')
        self.data2 = data.get('TEST2')
        self.data3 = data.get('TEST3')
        self.TravelPage = TravelPage(self.test.browser)
        self.TravelResultPage = TravelResultPage(self.test.browser)

    def test_user_can_search_for_travel_insurance(self):
        self.TravelPage.user_navigate_to_travel_tab()
        self.TravelPage.set_trip_type(self.data1.get('TRIP_TYPE'))
        self.TravelPage.set_traveller(self.data1.get('TRAVELER'))
        self.TravelPage.set_travel_place(self.data1.get('TRAVEL_PLACE'))
        self.TravelPage.set_travel_start_date(self.data1.get('TRAVEL_DATE'))
        self.TravelPage.user_click_show_travel_result_button()
        self.TravelResultPage.user_should_see_travel_result_page()
        self.TravelResultPage.number_found_travel_cards_should_at_least(self.data1.get('TRAVEL_RESULT'))

    def test_user_can_filter_travel_insurance(self):
        self.user_is_in_search_travel_result_page()
        self.TravelResultPage.user_expand_filter_options()
        self.TravelResultPage.user_select_filter_option(self.data2.get('FILTER_OPTION'))
        self.TravelResultPage.user_set_min_slider_personal_accident_on_filter(self.data2.get('FILTER_ACCIDENT'))
        self.TravelResultPage.user_set_max_slider_trip_cancellation(self.data2.get('FILTER_CANCELLATION'))
        self.TravelResultPage.number_found_travel_cards_should_at_least(self.data2.get('TRAVEL_RESULT'))

    def test_user_can_set_detail_travel_insurance_at_travel_result_page(self):
        self.user_is_in_search_travel_result_page()
        self.TravelResultPage.user_select_filter_sort_option(self.data3.get('FILTER_SORT'))
        self.TravelResultPage.user_filter_travel_by_policy_type(self.data3.get('DETAIL_POLICY'))
        self.TravelResultPage.user_filter_travel_by_detail_traveller(self.data3.get('DETAIL_TRAVELER'))
        self.TravelResultPage.user_select_filter_destination(self.data3.get('FILTER_DESTINATION'))
        self.TravelResultPage.user_set_filter_start_date(self.data3.get('FILTER_START_DATE'))
        self.TravelResultPage.user_set_filter_end_date(self.data3.get('FILTER_END_DATE'))
        self.TravelResultPage.number_found_travel_cards_should_at_least(self.data3.get('TRAVEL_RESULT'))

    def user_is_in_search_travel_result_page(self):
        self.TravelPage.user_navigate_to_travel_tab()
        self.TravelPage.user_click_show_travel_result_button()
        self.TravelResultPage.user_should_see_travel_result_page()

    def tearDown(self):
        self.test.cleanup_test_environment()


if __name__ == '__main__':
    unittest.main()
