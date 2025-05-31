from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
    """予約確認ページのページオブジェクト"""
    
    # ページ要素のロケータ
    CONFIRM_CONTAINER = (By.CSS_SELECTOR, "#confirm")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "#confirm button[data-target='#success-modal']")
    SUCCESS_MODAL = (By.ID, "success-modal")
    MODAL_CONTENT = (By.CLASS_NAME, "modal-content")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(., '閉じる')]")
    PLAN_LIST_ELEMENT = (By.XPATH, "//*[contains(text(), '宿泊プラン一覧')]")
    
    def __init__(self, driver):
        """
        確認ページの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        super().__init__(driver)
    
    def is_confirmation_page_displayed(self):
        """
        確認ページが表示されているか確認
        
        Returns:
            bool: 確認ページが表示されていればTrue
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.CONFIRM_CONTAINER))
            return True
        except:
            return False
    
    def complete_reservation(self):
        """
        「この内容で予約する」ボタンをクリックして予約を完了
        
        Returns:
            ConfirmationPage: 自身のインスタンス（モーダルが表示された状態）
        """
        confirm_btn = self.wait_for_clickable(self.CONFIRM_BUTTON)
        self.safe_click(confirm_btn)
        time.sleep(1.5)  # ボタンクリック後の処理を待機
        
        # モーダルが表示されるまで待機
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MODAL))
        
        return self
    
    def get_modal_text(self):
        """
        モーダルのテキストを取得
        
        Returns:
            str: モーダルのテキスト
        """
        modal = self.wait_for_element(*self.MODAL_CONTENT)
        return modal.text
    
    def close_modal(self):
        """
        「閉じる」ボタンをクリックしてモーダルを閉じる
        
        Returns:
            PlansPage: プランページのインスタンス
        """
        from pages.plans_page import PlansPage
        
        close_button = self.wait_for_clickable(*self.CLOSE_BUTTON)
        close_button.click()
        time.sleep(1)  # モーダルを閉じた後の画面更新を待機
        
        return PlansPage(self.driver)
    
    def is_returned_to_plans_page(self):
        """
        宿泊プラン一覧画面に戻ったか確認
        
        Returns:
            bool: 宿泊プラン一覧画面に戻っていればTrue
        """
        plan_list_element = self.wait_for_element(*self.PLAN_LIST_ELEMENT)
        return plan_list_element.is_displayed()