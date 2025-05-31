from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from pages.base_page import BasePage

class ReservationPage(BasePage):
    """宿泊予約ページのページオブジェクト"""
    
    # フォーム要素のロケータ
    DATE_FIELD = (By.ID, "date")
    TERM_FIELD = (By.ID, "term")
    HEAD_COUNT_FIELD = (By.ID, "head-count")
    BREAKFAST_CHECKBOX = (By.ID, "breakfast")
    CONTACT_SELECT = (By.ID, "contact")
    TEL_FIELD = (By.ID, "tel")
    TOTAL_BILL = (By.ID, "total-bill")
    SUBMIT_BUTTON = (By.ID, "submit-button")
    
    def __init__(self, driver):
        """
        予約ページの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        super().__init__(driver)
    
    def fill_reservation_form(self, date, nights, guest_count, phone_number):
        """
        予約フォームに情報を入力
        
        Args:
            date: 宿泊日
            nights: 宿泊数
            guest_count: 宿泊人数
            phone_number: 電話番号
            
        Returns:
            ReservationPage: 自身のインスタンス
        """
        # 日付入力
        date_field = self.wait_for_element(*self.DATE_FIELD)
        date_field.clear()
        date_field.send_keys(date)
        time.sleep(0.3)  # 入力反映を待機
        
        # 宿泊数入力
        term_field = self.driver.find_element(*self.TERM_FIELD)
        term_field.clear()
        term_field.send_keys(nights)
        time.sleep(0.3)  # 入力反映を待機
        
        # 宿泊人数入力
        head_count_field = self.driver.find_element(*self.HEAD_COUNT_FIELD)
        head_count_field.clear()
        head_count_field.send_keys(guest_count, Keys.ENTER)
        time.sleep(0.3)  # 入力反映を待機
        
        # 朝食チェックボックスをオン
        self.driver.execute_script("document.getElementById('breakfast').click();")
        time.sleep(0.5)  # 状態変更と計算のために少し待機
        
        # 連絡方法を「電話」に設定
        contact_select = Select(self.driver.find_element(*self.CONTACT_SELECT))
        contact_select.select_by_visible_text("電話でのご連絡")
        time.sleep(0.5)  # セレクト変更とTEL入力フィールド表示を待機
        
        # 電話番号入力
        tel_input = self.wait_for_element(*self.TEL_FIELD)
        tel_input.clear()
        tel_input.send_keys(phone_number)
        time.sleep(0.8)  # 入力反映と金額計算完了を待機
        
        return self
    
    def get_total_price(self):
        """
        合計金額のテキストを取得
        
        Returns:
            str: 合計金額のテキスト
        """
        total_element = self.wait_for_element(*self.TOTAL_BILL)
        return total_element.text
    
    def confirm_reservation(self):
        """
        「予約内容を確認する」ボタンをクリック
        
        Returns:
            ConfirmationPage: 予約確認ページのインスタンス
        """
        from pages.confirmation_page import ConfirmationPage
        
        submit_button = self.wait_for_clickable(*self.SUBMIT_BUTTON)
        self.safe_click(submit_button)
        time.sleep(2)  # 遷移を待機
        
        return ConfirmationPage(self.driver)