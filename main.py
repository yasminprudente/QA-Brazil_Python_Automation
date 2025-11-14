import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages import UrbanRoutesPage

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Verifica se o servidor Urban Routes está ativo
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(5)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.ADDRESS_FROM
        address_to = data.ADDRESS_TO
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_plan(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Comfort'


    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = data.PHONE_NUMBER
        routes_page.set_phone(phone_number)
        assert routes_page.get_phone() == phone_number

    def test_fill_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_card(data.CARD_NUMBER, data.CARD_CODE)
        assert routes_page.get_current_payment_method() == 'Cartão'

    def test_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        message = data.MESSAGE_FOR_DRIVER
        routes_page.set_message_for_driver(message)
        assert routes_page.get_message_for_driver() == message

    def test_order_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_and_handkerchiefs_option()
        assert routes_page.get_blanket_and_handkerchiefs_option_checked()

    def test_order_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream(2)
        assert routes_page.get_amount_of_ice_cream() == 2


    def test_car_search_model_appears(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi_buton()
        routes_page.wait_order_taxi_popup()

    def test_driver_info_appears(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_driver_info()
        name, rating, image = routes_page.get_driver_info()
        assert name
        assert rating
        assert image

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()