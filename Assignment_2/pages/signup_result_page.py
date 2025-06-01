from selenium.webdriver.common.by import By
from .base_page import BasePage

    
class SignupResultPage(BasePage):
    """会員登録完了ページのページオブジェクトクラス"""
    
    # ログアウトボタンのロケータ
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "form#logout-form button[type='submit']")
    
    # マイページに遷移した場合は成功とみなす
    def is_signup_successful(self):
        """会員登録が成功したかを確認
        
        Returns:
            bool: 登録成功時はTrue、失敗時はFalse
        """
        try:
            # URLにmypage.htmlが含まれていれば成功と判断
            current_url = self.driver.current_url
            return "mypage.html" in current_url
        except:
            return False
    