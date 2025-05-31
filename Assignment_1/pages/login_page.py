import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """ログインページのページオブジェクト"""
    
    # ロケーター
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def login(self, email, password):
        """ログイン処理を実行"""
        self.wait_for_element(self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        time.sleep(1.5)  # ログイン処理完了を待機
        
        from pages.plans_page import PlansPage
        return PlansPage(self.driver)