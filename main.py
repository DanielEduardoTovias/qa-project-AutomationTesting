import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import data
from selenium import webdriver
from Pages import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        '''from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)'''
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        # Crear el controlador
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.driver.maximize_window()

        #       ----------      TESTS      ----------

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        from_address = data.address_from
        to_address = data.address_to
        routes.set_from(from_address)
        routes.set_to(to_address)
        assert routes.get_from() == from_address
        assert routes.get_to() == to_address
        routes.timming_for_visibility()  # waiting a time by visualize completely the previous steps

    def test_select_price(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        self.test_set_route()
        routes.selectTaxiOption()
        routes.select_comfort_price()

    def test_fill_phone_number(self):

        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        self.test_select_price()
        phone_number = data.phone_number
        routes.add_phone_number(phone_number)
        time.sleep(5)

    def test_add_credit_card_message(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        self.test_fill_phone_number()
        routes.add_card_number()
        routes.message_to_pilot()


    def test_ice_cream_deliver_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        self.test_add_credit_card_message()
        routes.select_manta_pañuelos_ice_cream()
        routes.deliverTaxi()
        routes.verify_modal_popUp()
        time.sleep(4)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        print("Test finished!")
