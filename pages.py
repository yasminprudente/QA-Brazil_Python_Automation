from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import retrieve_phone_code

import time

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Chamar um táxi")]')
    tariff_cards = (By.CLASS_NAME, 'tariff-cards')
    supportive_plan_card = (By.XPATH, '//div[contains(@class, "tcard")]//div[contains(text(), "Comfort")]')
    active_plan_card = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')
    phone_number_control = (By.XPATH,
                            '//div[@class="np-button" or contains(@class, "np-button")][.//div[contains(text(), "Número de telefone")]]')
    phone_number_input = (By.ID, 'phone')
    phone_number_code_input = (By.ID, 'code')
    phone_number_next_button = (By.CSS_SELECTOR, '.full')
    phone_number_confirm_button = (By.XPATH, '//button[contains(text(), "Confirm")]')
    phone_number = (By.CLASS_NAME, 'np-text')
    payment_method_select = (By.XPATH,
                             '//div[contains(@class, "pp-button")]//div[contains(text(), "Método de pagamento")]')
    add_card_control = (By.XPATH, '//div[contains(@class, "pp-title") and contains(text(), "Adicionar cartão")]')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.ID, 'code')
    card_plc_image = (By.CLASS_NAME, 'plc')
    card_credentials_confirm_button = (By.XPATH, '//button[contains(text(), "Adicionar")]')
    close_button_payment_method = (By.XPATH,
                                   '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    current_payment_method = (By.CLASS_NAME, 'pp-value-text')
    message_for_driver = (By.ID, 'comment')
    option_switches = (By.CLASS_NAME, 'switch')
    option_switches_inputs = (By.CLASS_NAME, 'switch-input')
    add_enumerable_option = (By.CLASS_NAME, 'counter-plus')
    amount_of_enumerable_option = (By.CLASS_NAME, 'counter-value')
    order_car_button = (By.CLASS_NAME, 'smart-button-wrapper')
    order_popup = (By.CLASS_NAME, 'order-body')
    progress_bar = (By.CLASS_NAME, 'order-progress visible')
    driver_wait_time = (By.CLASS_NAME, 'order-header-time')
    order_driver_rating = (By.CLASS_NAME, 'order-btn-rating')
    order_driver_image = (By.XPATH, '//div[@class="order-button"]//img')
    order_driver_name = (By.XPATH, '//div[@class="order-btn-group"][1]/div[2]')

    def __init__(self, driver):
        self.driver = driver

    def _wait_for(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )

    def _wait_for_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def set_from(self, from_address):
        self._wait_for_visible(self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self._wait_for_visible(self.to_field).send_keys(to_address)

    def get_from(self):
        return self._wait_for(self.from_field).get_property('value')

    def get_to(self):
        return self._wait_for(self.to_field).get_property('value')

    def click_call_taxi_button(self):
        self._wait_for_visible(self.call_taxi_button).click()

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_call_taxi_button()

    def select_supportive_plan(self):
        card = self._wait_for_visible(self.supportive_plan_card)
        self.driver.execute_script("arguments[0].scrollIntoView();", card)
        card.click()

    def get_current_selected_plan(self):
        return self._wait_for(self.active_plan_card).text

    def set_phone(self, number):
        self._wait_for(self.phone_number_control).click()
        self._wait_for(self.phone_number_input).send_keys(number)
        self._wait_for(self.phone_number_next_button).click()
        code = retrieve_phone_code(self.driver)
        self._wait_for(self.phone_number_code_input).send_keys(code)
        self._wait_for(self.phone_number_confirm_button).click()

    def get_phone(self):
        return self._wait_for(self.phone_number).text

    def set_card(self, card_number, code):
        self.driver.find_element(*self.payment_method_select).click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(*self.add_card_control).click()
        self.driver.find_element(*self.add_card_control)
        self.driver.find_element(*self.card_number_input).send_keys(card_number + Keys.TAB + code)
        self.driver.find_element(*self.card_plc_image).click()
        self.driver.find_element(*self.card_credentials_confirm_button).click()
        self.driver.find_element(*self.close_button_payment_method).click()

    def get_current_payment_method(self):
        return self._wait_for(self.current_payment_method).text

    def set_message_for_driver(self, message):
        self._wait_for(self.message_for_driver).send_keys(message)

    def get_message_for_driver(self):
        return self._wait_for(self.message_for_driver).get_property('value')

    def click_blanket_and_handkerchiefs_option(self):
        switches = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_all_elements_located(self.option_switches)
        )
        switches[0].click()
        self.get_blanket_and_handkerchiefs_option_checked()

    def get_blanket_and_handkerchiefs_option_checked(self):
        switches = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_all_elements_located(self.option_switches_inputs)
        )
        return switches[0].get_property('checked')

    def add_ice_cream(self, amount: int):
        option_add_controls = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_all_elements_located(self.add_enumerable_option)
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", option_add_controls[0])
        for _ in range(amount):
            option_add_controls[0].click()

    def get_amount_of_ice_cream(self):
        return int(WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_all_elements_located(self.amount_of_enumerable_option)
        )[0].text)

    def click_order_taxi_buton(self):
        self._wait_for(self.order_car_button).click()

    def wait_order_taxi_popup(self):
        self._wait_for_visible(self.order_popup)

    def wait_driver_info(self):
        WebDriverWait(self.driver, 60).until(
            expected_conditions.invisibility_of_element_located(self.driver_wait_time)
        )
        self._wait_for(self.order_driver_rating)
        self._wait_for(self.order_driver_image)
        self._wait_for(self.order_driver_name)

    def get_driver_info(self):
        rating = self._wait_for(self.order_driver_rating).text
        image = self._wait_for(self.order_driver_image).get_property('src')
        name = self._wait_for(self.order_driver_name).text
        return name, rating, image
