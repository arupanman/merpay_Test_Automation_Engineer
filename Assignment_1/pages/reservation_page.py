import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class ReservationPage(BasePage):
    """予約フォームページのページオブジェクト"""
    
    # ロケーター
    DATE_FIELD = (By.ID, "date")
    TERM_FIELD = (By.ID, "term")
    HEAD_COUNT_FIELD = (By.ID, "head-count")
    BREAKFAST_OPTION = (By.ID, "breakfast")
    CONTACT_SELECT = (By.ID, "contact")
    TEL_FIELD = (By.ID, "tel")
    TOTAL_BILL_ELEMENT = (By.ID, "total-bill")
    SUBMIT_BUTTON = (By.ID, "submit-button")
    
    def fill_reservation_form(self, date="2025/07/15", term="3", head_count="2", 
                             breakfast=True, contact_method="電話でのご連絡", tel="00011112222"):
        """予約フォームに入力"""
        # 日付入力
        date_field = self.wait_for_element(self.DATE_FIELD)
        date_field.clear()
        date_field.send_keys(date)
        time.sleep(0.3)
        
        # 泊数入力
        term_field = self.driver.find_element(*self.TERM_FIELD)
        term_field.clear()
        term_field.send_keys(term)
        time.sleep(0.3)
        
        # 人数入力
        head_count_field = self.driver.find_element(*self.HEAD_COUNT_FIELD)
        head_count_field.clear()
        head_count_field.send_keys(head_count, Keys.ENTER)
        time.sleep(0.3)
        
        # 朝食オプション選択
        if breakfast:
            self.driver.execute_script("document.getElementById('breakfast').click();")
            time.sleep(0.5)
        
        # 連絡方法選択
        contact_select = Select(self.driver.find_element(*self.CONTACT_SELECT))
        contact_select.select_by_visible_text(contact_method)
        time.sleep(0.5)
        
        # 電話番号入力
        tel_input = self.wait_for_element(self.TEL_FIELD)
        tel_input.clear()
        tel_input.send_keys(tel)
        time.sleep(0.8)
        
        return self
    
    def get_total_price(self):
        """合計金額を取得"""
        return self.wait_for_element(self.TOTAL_BILL_ELEMENT).text
    
    def submit_reservation(self):
        """予約内容確認ボタンをクリック"""
        submit_button = self.wait_for_clickable(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(2)
        
        from pages.confirmation_page import ConfirmationPage
        return ConfirmationPage(self.driver)