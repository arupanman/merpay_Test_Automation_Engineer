from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .base_page import BasePage

class SignupPage(BasePage):
    """会員登録ページのページオブジェクトクラス"""
    
    # ページ要素のロケータ
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    PASSWORD_CONFIRMATION_INPUT = (By.ID, "password-confirmation")
    USERNAME_INPUT = (By.ID, "username")
    RANK_PREMIUM = (By.ID, "rank-premium")
    RANK_NORMAL = (By.ID, "rank-normal")
    ADDRESS_INPUT = (By.ID, "address")
    TEL_INPUT = (By.ID, "tel")
    BIRTHDAY_INPUT = (By.ID, "birthday")
    GENDER_SELECT = (By.ID, "gender")
    NOTIFICATION_CHECKBOX = (By.ID, "notification")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # エラーメッセージのロケータ
    BIRTHDAY_ERROR = (By.CSS_SELECTOR, "#birthday + .invalid-feedback")
    
    def fill_signup_form(self, user_data):
        """会員登録フォームに情報を入力
        
        Args:
            user_data: 会員情報を含む辞書
        """
        # メールアドレス
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(user_data.get("email", ""))
        
        # パスワード
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(user_data.get("password", ""))
        
        # パスワード確認
        self.driver.find_element(*self.PASSWORD_CONFIRMATION_INPUT).send_keys(user_data.get("password_confirmation", ""))
        
        # 氏名
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(user_data.get("username", ""))
        
        # 会員ランク
        rank = user_data.get("rank", "")
        if rank == "一般会員":
            self.driver.find_element(*self.RANK_NORMAL).click()
        else:
            self.driver.find_element(*self.RANK_PREMIUM).click()
        
        # 住所
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(user_data.get("address", ""))
        
        # 電話番号
        self.driver.find_element(*self.TEL_INPUT).send_keys(user_data.get("tel", ""))
        
        # 生年月日
        birthday = user_data.get("birthday", "")
        if birthday:
            # フォーマット変換（YYYY/MM/DD → YYYY-MM-DD）
            if "/" in birthday:
                parts = birthday.split("/")
                birthday = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
            
            # 直接値をセットする（JavaScriptを使用）
            self.driver.execute_script(
                f"document.getElementById('birthday').value = '{birthday}';"
            )
        
        # 性別
        gender = user_data.get("gender", "")
        select = Select(self.driver.find_element(*self.GENDER_SELECT))
        if gender == "男性":
            select.select_by_value("1")
        elif gender == "女性":
            select.select_by_value("2")
        elif gender == "その他":
            select.select_by_value("9")
        else:
            select.select_by_value("0")  # 回答しない
        
        # お知らせの配信設定
        notification = user_data.get("notification", False)
        notification_checkbox = self.driver.find_element(*self.NOTIFICATION_CHECKBOX)
        if notification and not notification_checkbox.is_selected():
            notification_checkbox.click()
        elif not notification and notification_checkbox.is_selected():
            notification_checkbox.click()
    
    def submit_form(self):
        """フォームを送信し、結果ページを返却
        
        Returns:
            SignupResultPage: 会員登録完了ページのオブジェクト
        """
        submit_button = self.wait_for_clickable(self.SUBMIT_BUTTON[0], self.SUBMIT_BUTTON[1])
        submit_button.click()
        time.sleep(1)  # 画面遷移を待機
        
        from .signup_result_page import SignupResultPage  # 循環インポートを避けるため、ここでインポート
        return SignupResultPage(self.driver)
    
    def submit_form_expecting_error(self):
        """フォーム送信時にエラーが発生することを期待
        
        Returns:
            SignupPage: 自身のインスタンス
        """
        submit_button = self.wait_for_clickable(self.SUBMIT_BUTTON[0], self.SUBMIT_BUTTON[1])
        submit_button.click()
        time.sleep(1)  # エラーメッセージの表示を待機
        return self
    
    def get_birthday_error_message(self):
        """誕生日フィールドのエラーメッセージを取得
        
        Returns:
            str: エラーメッセージのテキスト
        """
        try:
            # 誕生日エラーメッセージは、要素が表示されていて、テキストが空でない場合に取得
            error_element = self.driver.find_element(*self.BIRTHDAY_ERROR)
            if error_element.is_displayed() and error_element.text.strip():
                return error_element.text
            return None
        except:
            return None