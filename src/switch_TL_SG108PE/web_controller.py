"""Contains class to control web browser."""

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from .exceptions import LoginException, LogoutException, TpLinkSwitchException
from .utils import Frame


class WebController:
    """Creates object to control admin web page of switch via selenium library."""

    # pylint: disable=invalid-name
    def __init__(self, host, username: str, password: str, webdriver: WebDriver) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.webdriver = webdriver
        self._active_frame = ''

    def login(self) -> None:
        """
        Login user in admin web page of switch.

        :return: None
        """
        try:
            self.webdriver.get(f'http://{self.host}')
            self.wait_until_element_is_present(By.ID, 'logon')
        except WebDriverException:
            raise LoginException(f'Couldn\'t connect to {self.host}.') from None
        except TpLinkSwitchException:
            self.logout()
        self.wait_until_element_is_present(By.ID, 'username', exception=LoginException)
        self.webdriver.find_element(By.ID, 'username').send_keys(self.username)
        self.wait_until_element_is_present(By.ID, 'password', exception=LoginException)
        self.webdriver.find_element(By.ID, 'password').send_keys(self.password)
        self.wait_until_element_is_present(By.ID, 'logon', exception=LoginException)
        self.webdriver.find_element(By.ID, 'logon').click()
        self.wait_until_element_is_present(By.XPATH, f"//frame[@name='{Frame.TOP.value}']", exception=LoginException)

    def logout(self) -> None:
        """
        Logout user from admin web page of switch.

        :return: None
        """
        self.switch_to_frame(Frame.MENU)
        logout_link_details = (By.XPATH, "//div[@id='logout']//a[@class='menulink']")
        self.wait_until_element_is_present(*logout_link_details, exception=LogoutException)
        logout_link = self.webdriver.find_element(*logout_link_details)
        logout_link.click()
        self.wait_until_alert_is_present(exception=LogoutException)
        alert = self.webdriver.switch_to.alert
        alert.accept()

    def is_logged_in(self) -> bool:
        """
        Checks if client is authenticated.

        :return: True if it is, otherwise False
        """
        self.switch_to_default_content()
        top_frame_details = (By.XPATH, f"//frame[@name='{Frame.TOP.value}']")
        try:
            self.webdriver.find_element(*top_frame_details)
        except NoSuchElementException:
            return False
        return True

    def quit(self) -> None:
        """
        Quits web browser.

        :return: None
        """
        self.webdriver.quit()

    def switch_to_frame(self, frame_name: Frame) -> None:
        """
        Changes current frame. Switch admin page consists of many frames like sidebar navigation frame,
        main content frame... To manipulate content of frame we need to activate it before.

        :param frame_name: name of frame
        :return: None
        """
        self.switch_to_default_content()
        frame_details = (By.XPATH, f"//frame[@name='{frame_name.value}']")
        self.wait_until_element_is_present(*frame_details)
        frame = self.webdriver.find_element(*frame_details)
        self.webdriver.switch_to.frame(frame)
        self._active_frame = frame_name

    def switch_to_default_content(self) -> None:
        """
        Switches to default content of page. It disables active frame.

        :return: None
        """
        self.webdriver.switch_to.default_content()
        self._active_frame = None

    def find_element(self, method: By, query: str) -> WebElement:
        """
        Finds first element with matching query and returns it.

        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :return: found element
        """
        return self.webdriver.find_element(method, query)

    def find_elements(self, method: By, query: str) -> List[WebElement]:
        """
        Finds multiple elements with matching query and returns them.

        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :return: found elements
        """
        return self.webdriver.find_elements(method, query)

    def click_element_with_control_key_pressed(self, element: WebElement) -> None:
        """
        Clicks given element with Ctrl key pressed.

        :param element: element to click
        :return: None
        """
        ActionChains(self.webdriver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

    def wait_until_element_is_present(self, method: By, query: str, timeout: int = 4,
                                      exception=TpLinkSwitchException) -> None:
        """
        Waits until given element is present on web page.
        If element wasn't be found on web page an error will be raised.

        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param timeout: maximum time of waiting
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.presence_of_element_located((method, query)))
        except TimeoutException:
            raise exception(f'Element identified as "({method}, {query})" not present after {timeout} seconds') \
                from None

    def wait_until_element_is_visible(self, method: By, query: str, timeout: int = 6,
                                      exception=TpLinkSwitchException) -> None:
        """
        Waits until given element is visible on web page.
        If element wasn't be found on web page an error will be raised.

        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param timeout: maximum time of waiting
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.visibility_of_element_located((method, query)))
        except TimeoutException:
            raise exception(f'Element identified as "({method}, {query})" not visible after {timeout} seconds') \
                from None

    def wait_until_alert_is_present(self, timeout: int = 4, exception=TpLinkSwitchException) -> None:
        """
        Waits until given alert is present on web page.
        If alert wasn't be found on web page an error will be raised.

        :param timeout: maximum time of waiting
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.alert_is_present())
        except TimeoutException:
            raise exception(f'Alert not present after {timeout} seconds') from None
