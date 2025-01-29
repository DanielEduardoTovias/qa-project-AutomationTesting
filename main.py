import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # Defining the attributes of the class (locators)
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    set_mode = (By.NAME, 'Personal')
    taxi_logo_button = (By.LINK_TEXT, '/static/media/taxi.9a02abc6.svg')
    selectTaxiButton = (By.XPATH, "//button[normalize-space()='Pedir un taxi']")
    comfortButton = (By.XPATH, "//div[@class='tcard-icon']//img[@alt='Comfort']")

    fieldPhoneNumber = (By.CLASS_NAME, "np-text")
    popUpFieldPhoneNumber = (By.CLASS_NAME, "input")
    buttonSiguiente = (By.XPATH, "//button[normalize-space()='Siguiente']")

    fieldSMSCode = (By.ID, 'code')
    buttonConfirmarCode = (By.XPATH, "//button[normalize-space()='Confirmar']")
    buttonSendAgainCode = (By.CSS_SELECTOR, "div[class='buttons'] button[type='button']")

    methodPay = (By.CLASS_NAME, 'pp-text')
    buttonAddCard = (By.CLASS_NAME, 'pp-title')
    fieldCardNumber = (By.ID, 'number')
    fieldCodeNumber = (By.CLASS_NAME, 'card-code')
    separatorForm = (By.CLASS_NAME, 'pp-separator')
    buttonAgregar = (By.NAME, 'Agregar')
    buttonClosePopUp = (By.CLASS_NAME, 'close-button section-close')

    fieldAddComment = (By.ID, 'comment')

    sliderButton = (By.CLASS_NAME, 'r-sw')

    buttonDeliveryTaxi = (By.CLASS_NAME, 'smart-button-secondary')
    messageWaiting = (By.CLASS_NAME, 'order-header-title')
    messageDelivered = (By.CLASS_NAME, 'order-header-title')
    numberCar = (By.CLASS_NAME, "number")
    buttonDetails = (By.XPATH, "//div[@class='order-subbody']//div[2]//button[1]")

    # Constructor of the class
    def __init__(self, driver):
        self.driver = driver

    # ----------    1. Configurar la dirección.   ----------
    # setting the first address
    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    # setting the second address
    def set_to(self, to_address):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    # Obtaining the set values:
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def timming_for_visibility(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.selectTaxiButton))

    # ----------    2. Seleccionar la tarifa Comfort.    ----------
    def selectTaxiOption(self):  #
        WebDriverWait(self.driver, 12).until(expected_conditions.element_to_be_clickable(self.selectTaxiButton))
        self.driver.find_element(*self.selectTaxiButton).click()

    def select_comfort_price(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.comfortButton))
        self.driver.find_element(*self.comfortButton).click()

    # ----------    3. Rellenar el número de teléfono.    ----------
    def add_phone_number(self, phone_number):
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.fieldPhoneNumber))
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.fieldPhoneNumber))
        self.driver.find_element(*self.fieldPhoneNumber).click()
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.popUpFieldPhoneNumber))
        self.driver.find_element(*self.popUpFieldPhoneNumber).send_keys(phone_number)
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.buttonSiguiente))
        self.driver.find_element(*self.buttonSiguiente).click()
        assert WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.fieldSMSCode))
        self.driver.find_element(*self.fieldSMSCode).send_keys(retrieve_phone_code(self.driver))
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.buttonConfirmarCode))
        self.driver.find_element(*self.buttonConfirmarCode).click()

    #   ----------  4. Agregar una tarjeta de crédito.  ----------
    def add_card_number(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.methodPay))
        self.driver.find_element(*self.methodPay).click()
        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.buttonAddCard))
        self.driver.find_element(*self.buttonAddCard).click()

        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.fieldCardNumber))
        self.driver.find_element(*self.fieldCardNumber).send_keys(data.card_number)
        self.driver.find_element(*self.fieldCodeNumber).send_keys(data.card_code)

        self.driver.find_element(*self.separatorForm).click()
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.buttonAgregar))
        self.driver.find_element(*self.buttonAgregar).click()
        WebDriverWait(self.driver, 4).until(expected_conditions.visibility_of_element_located(self.buttonClosePopUp))
        self.driver.find_element(*self.buttonClosePopUp).click()

    #   ----------    5. Escribir un mensaje para el controlador.    ----------
    def message_to_pilot(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.fieldAddComment))
        self.driver.find_element(*self.fieldAddComment).send_keys(data.message_for_driver)

    #   ----------  6. Pedir una manta y pañuelos.  ----------
    def select_manta_pañuelos_ice_cream(self):
        deliver_settings = self.driver.find_element(By.CLASS_NAME, "reqs")
        titleHeladoFresa = self.driver.find_element(By.XPATH, "//div[normalize-space()='Fresa']")
        counterHelado = self.driver.find_element(By.CLASS_NAME, 'counter-plus')
        ActionChains(self.driver) \
            .move_to_element(deliver_settings) \
            .perform()

        self.driver.find_element(*self.sliderButton).click()
        time.sleep(2)

        ActionChains(self.driver) \
            .move_to_element(titleHeladoFresa) \
            .perform()
        assert WebDriverWait(self.driver, 7).until(expected_conditions.element_to_be_clickable(titleHeladoFresa))

        ActionChains(self.driver).double_click(counterHelado).perform()

    #   ----------  7. Pedir 2 helados. ----------
    def deliverTaxi(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.buttonDeliveryTaxi))
        self.driver.find_element(*self.buttonDeliveryTaxi).click()
    #   ----------      Verificar información del automóvil     ----------
    def verify_modal_popUp(self):
        assert WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.messageWaiting))
        assert WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.messageDelivered))
        assert WebDriverWait(self.driver, 40).until(expected_conditions.element_to_be_clickable(self.buttonDetails))
        assert WebDriverWait(self.driver,40).until(expected_conditions.element_to_be_clickable(self.numberCar))
        print("carNumber: " + self.driver.find_element(*self.numberCar).text)



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
        from_address = data.address_from
        to_address = data.address_to
        routes.set_from(from_address)
        routes.set_to(to_address)
        assert routes.get_from() == from_address
        assert routes.get_to() == to_address
        print(from_address)
        print(to_address)
        routes.selectTaxiOption()
        routes.select_comfort_price()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        from_address = data.address_from
        to_address = data.address_to
        phone_number = data.phone_number
        routes.set_from(from_address)
        routes.set_to(to_address)
        assert routes.get_from() == from_address
        assert routes.get_to() == to_address
        print(from_address)
        print(to_address)
        routes.selectTaxiOption()
        routes.select_comfort_price()
        routes.add_phone_number(phone_number)
        time.sleep(5)

    def test_add_credit_card_message(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        from_address = data.address_from
        to_address = data.address_to
        phone_number = data.phone_number
        routes.set_from(from_address)
        routes.set_to(to_address)
        assert routes.get_from() == from_address
        assert routes.get_to() == to_address
        print(from_address)
        print(to_address)
        routes.selectTaxiOption()
        routes.select_comfort_price()
        routes.add_phone_number(phone_number)
        routes.message_to_pilot()
        time.sleep(2)

    def test_ice_cream_deliver_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes = UrbanRoutesPage(self.driver)
        from_address = data.address_from
        to_address = data.address_to
        phone_number = data.phone_number
        routes.set_from(from_address)
        routes.set_to(to_address)
        assert routes.get_from() == from_address
        assert routes.get_to() == to_address
        print(from_address)
        print(to_address)
        routes.selectTaxiOption()
        routes.select_comfort_price()
        routes.add_phone_number(phone_number)
        routes.message_to_pilot()
        routes.select_manta_pañuelos_ice_cream()
        routes.deliverTaxi()
        routes.verify_modal_popUp()
        time.sleep(4)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        print("Test finished!")
