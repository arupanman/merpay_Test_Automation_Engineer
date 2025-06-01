import unittest
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.top_page import TopPage
from pages.signup_page import SignupPage

class TestBirthdayValidation(unittest.TestCase):
    """会員登録時の誕生日バリデーションテストクラス"""
    
    # テスト対象のURL
    BASE_URL = 'https://hotel-example-site.takeyaqa.dev/ja/index.html'
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化メソッド - WebDriverの設定を行います"""
        # WebDriverの設定
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(3)  # 暗黙的待機
        
        # テスト実行時の一意のIDを生成
        cls.unique_id = int(time.time())

    def setUp(self):
        """各テストケース実行前の処理"""
        # トップページを開く
        self.top_page = TopPage(self.driver).open(self.BASE_URL)
        
        # 会員登録ページへ移動
        self.signup_page = self.top_page.go_to_signup()
        
        # テスト用のユーザーデータ基本設定
        self.user_data = {
            "email": f"test{self.unique_id}@example.com",
            "password": "password123",
            "password_confirmation": "password123",
            "username": "テストユーザー",
            "rank": "一般会員",
            "address": "東京都渋谷区",
            "tel": "01234567890",
            "gender": "男性",
            "notification": True
        }

    def test_future_birthday_is_invalid(self):
        """未来の日付での誕生日登録が拒否されることを検証"""
        # 明日の日付を生成
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # ユーザーデータを設定
        user_data = self.user_data.copy()
        user_data["email"] = f"future{self.unique_id}@example.com"
        user_data["birthday"] = tomorrow
        
        # フォーム入力と送信
        self.signup_page.fill_signup_form(user_data)
        self.signup_page.submit_form_expecting_error()
        
        # エラーメッセージが表示されることを検証
        error_message = self.signup_page.get_birthday_error_message()
        self.assertIsNotNone(error_message, f"未来の日付 {tomorrow} でエラーメッセージが表示されませんでした")
        print(f"未来の日付 {tomorrow} で適切にエラーメッセージが表示されました: {error_message}")



    @classmethod
    def tearDownClass(cls):
        """テストクラスの終了処理 - WebDriverを閉じます"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)