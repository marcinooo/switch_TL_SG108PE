"""Contains main class to control web page."""

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from switch_TL_SG108PE.errors import LoginError, LogoutError, TpLinkSwitchError, SwitchManagerNotConnectedError
from switch_TL_SG108PE.utils import Frame


class WebController:
    """Creates object to control admin web page of switch."""
    def __init__(self, ip, username, password, webdriver):
        self.ip = ip
        self.username = username
        self.password = password
        self.webdriver = webdriver
        self._active_frame = ''

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

    def login(self) -> None:
        """
        Login user in admin web page of switch.
        :return: None
        """
        self.webdriver.get(f'http://{self.ip}')
        try:
            self.wait_until_element_is_present(By.ID, 'logon', close_browser=False)
        except TpLinkSwitchError:
            self.logout()
        self.wait_until_element_is_present(By.ID, 'logon', exception=LoginError)
        self.webdriver.find_element(By.ID, 'username').send_keys(self.username)
        self.webdriver.find_element(By.ID, 'password').send_keys(self.password)
        self.webdriver.find_element(By.ID, 'logon').click()
        self.wait_until_element_is_present(By.XPATH, f"//frame[@name='{Frame.TOP.value}']", exception=LoginError)

    def logout(self) -> None:
        """
        Logout user from admin web page of switch.
        :return: None
        """
        self.switch_to_frame(Frame.MENU)
        logout_link_details = (By.XPATH, "//div[@id='logout']//a[@class='menulink']")
        self.wait_until_element_is_present(*logout_link_details, exception=LogoutError)
        logout_link = self.webdriver.find_element(*logout_link_details)
        logout_link.click()
        self.wait_until_alert_is_present()
        alert = self.webdriver.switch_to.alert
        alert.accept()

    def switch_to_frame(self, frame_name: Frame) -> None:
        """
        Changes current frame. Switch admin page consists of many frames like menu frame, main page frame...
        To manipulate content of frame we need to activate it.
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

    def find_element(self, method: str, query: str):  # TODO: add return type
        """
        Finds first element with matching query and returns it.
        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :return: found element
        """
        return self.webdriver.find_element(method, query)

    def find_elements(self, method: str, query: str):  # TODO: add return type
        """
        Finds multiple elements with matching query and returns them.
        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :return: found elements
        """
        return self.webdriver.find_elements(method, query)

    def click_element_with_control_key_pressed(self, element) -> None:  # TODO: add type of element
        """
        Clicks given element with Ctrl key pressed.
        :param element: element to click
        :return: None
        """
        ActionChains(self.webdriver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

    def wait_until_element_is_present(self, method: str, query: str, timeout: int = 4, close_browser: bool = True,
                                      exception=TpLinkSwitchError) -> None:  # TODO: Add typing
        """
        Waits until given element is present on web page.
        If element wasn't be found on web page an error will be raised.
        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param timeout: maximum time of waiting
        :param close_browser: flag to control if web browser should be closed in error case  # TODO: consider new name
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.presence_of_element_located((method, query)))
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Element identified as "({method}, {query})" not present after {timeout} seconds')

    def wait_until_element_is_visible(self, method: str, query: str, timeout: int = 4, close_browser: bool = True,
                                      exception=TpLinkSwitchError) -> None:
        """
        Waits until given element is visible on web page.
        If element wasn't be found on web page an error will be raised.
        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param timeout: maximum time of waiting
        :param close_browser: flag to control if web browser should be closed in error case
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.visibility_of_element_located((method, query)))
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Element identified as "({method}, {query})" not visible after {timeout} seconds')

    def wait_until_alert_is_present(self, timeout: int = 4, close_browser: bool = True,
                                    exception=TpLinkSwitchError) -> None:
        """
        Waits until given alert is present on web page.
        If alert wasn't be found on web page an error will be raised.
        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param timeout: maximum time of waiting
        :param close_browser: flag to control if web browser should be closed in error case
        :param exception: exception object raised in case of error
        :return: None
        """
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.alert_is_present())
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Alert not present after {timeout} seconds')  # Change error
