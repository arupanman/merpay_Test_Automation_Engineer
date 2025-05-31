import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
    """予約確認ページのページオブジェクト"""
    
    # ロケーター
    CONFIRM_HEADER = (By.CSS_SELECTOR, "#confirm h2.my-3")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "#confirm button[data-target='#success-modal']")
    SUCCESS_MODAL = (By.ID, "success-modal")
    MODAL_CONTENT = (By.CLASS_NAME, "modal-content")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(., '閉じる')]")
    PLAN_LIST_HEADER = (By.XPATH, "//*[contains(text(), '宿泊プラン一覧')]")
    
    def verify_confirmation_page(self):
        """確認ページであることを検証"""
        confirm_header = self.wait_for_element(self.CONFIRM_HEADER)
        return confirm_header.text.strip()
    
    def complete_reservation(self):
        """予約を確定する"""
        confirm_btn = self.wait_for_clickable(self.CONFIRM_BUTTON)
        self.scroll_to_element(confirm_btn)
        self.driver.execute_script("arguments[0].click();", confirm_btn)
        return self
    
    def verify_reservation_complete(self):
        """予約完了を確認"""
        modal = self.wait_for_element(self.SUCCESS_MODAL)
        modal_content = self.wait_for_element(self.MODAL_CONTENT)
        return modal_content.text
    
    def close_success_modal(self):
        """完了モーダルを閉じる"""
        close_button = self.wait_for_clickable(self.CLOSE_BUTTON)
        close_button.click()
        time.sleep(1)
        
        from pages.plans_page import PlansPage
        return PlansPage(self.driver)
    
    def verify_return_to_plan_list(self):
        """プラン一覧に戻ったことを確認"""
        return self.wait_for_element(self.PLAN_LIST_HEADER) is not None