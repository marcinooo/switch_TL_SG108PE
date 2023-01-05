from selenium.webdriver.common.by import By

from switch_TL_SG108PE.control_fields.control_field import ControlField
from switch_TL_SG108PE.utils import Frame


class SwitchingControlField(ControlField):

    MENU_SECTION = 'Switching'

    def ports_settings(self):
        self.open_tab(self.MENU_SECTION, 'Port Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        ports_settings = {}
        ports_rows_details = (By.XPATH, f"//table[@class='BORDER']/tbody/tr/td[@class='TABLE_HEAD_BOTTOM']")
        self.web_controller.wait_until_element_is_present(*ports_rows_details)
        ports_rows = self.web_controller.find_elements(*ports_rows_details)
        for i in range(0, 48, 6):
            ports_settings[f'Port {i // 6 + 1}'] = {
                'Status': ports_rows[i+1].text,
                'Speed/Duplex Config': ports_rows[i+2].text,
                'Speed/Duplex Actual': ports_rows[i+3].text,
                'Flow Control Config': ports_rows[i+4].text,
                'Flow Control Actual': ports_rows[i+5].text,
            }
        return ports_settings
