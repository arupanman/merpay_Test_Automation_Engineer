import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TopPage(BasePage):
    """トップページのページオブジェクト"""
    
    # ロケーター
    LOGIN_LINK = (By.LINK_TEXT, "ログイン")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'https://hotel-example-site.takeyaqa.dev/ja/index.html'
    
    def navigate(self):
        """トップページに移動"""
        self.driver.get(self.url)
        time.sleep(1)  # ページロード完了を待機
        return self
        
    def go_to_login(self):
        """ログインページに移動"""
        self.wait_for_clickable(self.LOGIN_LINK).click()
        time.sleep(0.5)  # 画面遷移を待機
        from pages.login_page import LoginPage
        return LoginPage(self.driver)