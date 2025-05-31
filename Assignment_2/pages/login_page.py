from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage

class LoginPage(BasePage):
    """ログインページのページオブジェクト"""
    
    # ページ要素のロケータ
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def __init__(self, driver):
        """
        ログインページの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        super().__init__(driver)
    
    def login(self, email, password):
        """
        ログイン処理を実行
        
        Args:
            email: ログインメールアドレス
            password: ログインパスワード
            
        Returns:
            TopPage: トップページのインスタンス（ログイン後のページ）
        """
        from pages.top_page import TopPage
        
        self.wait_for_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        time.sleep(1.5)  # ログイン処理完了を待機
        
        return TopPage(self.driver)