# import libraries and methods and attributes
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import data
from helpers import retrieve_phone_code


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
    buttonAddCard = (By.CLASS_NAME, 'pp-plus-container')
    fieldCardNumber = (By.ID, 'number')
    fieldCodeNumber = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    separatorForm = (By.XPATH, "(//div[@class='pp-separator'])[2]")
    buttonAgregar = (By.XPATH, "//button[normalize-space()='Agregar']")
    buttonClosePopUp = (By.XPATH, "(//button[@class='close-button section-close'])[3]")

    fieldAddComment = (By.ID, 'comment')
    errorMessage = (By.CLASS_NAME, "error")
    sliderButton = (By.CLASS_NAME, 'r-sw')
    counter_value = (By.CLASS_NAME, "counter-value")
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
        try:
            assert WebDriverWait(self.driver, 7).until(
                expected_conditions.element_to_be_clickable(self.comfortButton))
        finally:
            self.driver.find_element(*self.comfortButton).click()
            print("\nclick hecho en la tarifa Comfort")

    # ----------    3. Rellenar el número de teléfono.    ----------

    def add_phone_number(self, phone_number):
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.fieldPhoneNumber))
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.fieldPhoneNumber))
        self.driver.find_element(*self.fieldPhoneNumber).click()
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.popUpFieldPhoneNumber))
        self.driver.find_element(*self.popUpFieldPhoneNumber).send_keys(phone_number)

        input_element = self.driver.find_element(*self.popUpFieldPhoneNumber)
        input_value = input_element.get_attribute("value")
        # Comparar con el valor esperado
        assert input_value == phone_number, f"Valor: '{input_value}', esperado: '{phone_number}'"

        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.buttonSiguiente))
        self.driver.find_element(*self.buttonSiguiente).click()
        assert WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.fieldSMSCode))
        self.driver.find_element(*self.fieldSMSCode).send_keys(retrieve_phone_code(self.driver))
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.buttonConfirmarCode))
        self.driver.find_element(*self.buttonConfirmarCode).click()



    #   ----------  4. Agregar una tarjeta de crédito.  ----------
    def add_card_number(self):
        assert WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.methodPay))
        self.driver.find_element(*self.methodPay).click()
        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.buttonAddCard))

        self.driver.find_element(*self.buttonAddCard).click()
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.fieldCardNumber))
        self.driver.find_element(*self.fieldCardNumber).send_keys(data.card_number)
        self.driver.find_element(*self.fieldCodeNumber).send_keys(data.card_code)
        time.sleep(3)

        card_numb = self.driver.find_element(*self.fieldCardNumber)
        card_value = card_numb.get_attribute('value')
        try:
            assert card_value == data.card_number, f"Número: '{card_value}', esperado: '{data.card_number}'"
        finally:
            print("Número extraído: " + card_value + ", es correcto")

        self.driver.find_element(*self.separatorForm).click()
        assert WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.buttonAgregar))
        self.driver.find_element(*self.buttonAgregar).click()
        time.sleep(5)
        WebDriverWait(self.driver, 4).until(expected_conditions.visibility_of_element_located(self.buttonClosePopUp))
        self.driver.find_element(*self.buttonClosePopUp).click()



    #   ----------    5. Escribir un mensaje para el controlador.    ----------
    def message_to_pilot(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.presence_of_element_located(self.fieldAddComment))
        self.driver.find_element(*self.fieldAddComment).send_keys(data.message_for_driver)

        try:
            assert WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.errorMessage))
        finally:
            print("Mensaje de error presente al exceder el límite de caracteres")

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
        assert WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.messageWaiting))
        assert WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.messageDelivered))
        assert WebDriverWait(self.driver, 40).until(expected_conditions.element_to_be_clickable(self.buttonDetails))
        assert WebDriverWait(self.driver, 40).until(expected_conditions.element_to_be_clickable(self.numberCar))
        print("carNumber: " + self.driver.find_element(*self.numberCar).text)
