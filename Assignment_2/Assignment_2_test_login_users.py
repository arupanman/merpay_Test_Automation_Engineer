import unittest
import time
from selenium import webdriver
from pages.top_page import TopPage

class TestMultipleUsersLogin(unittest.TestCase):
    """複数ユーザーのログインテストクラス
    
    複数のユーザーアカウントでのログインとログアウトを検証します。
    """
    
    # テスト対象のURL
    BASE_URL = 'https://hotel-example-site.takeyaqa.dev/ja/index.html'
    
    # テスト用ユーザーデータ
    TEST_USERS = [
        {"email": "ichiro@example.com", "password": "password"},
        {"email": "sakura@example.com", "password": "pass1234"},
        {"email": "jun@example.com", "password": "pa55w0rd!"},
        {"email": "yoshiki@example.com", "password": "pass-pass"}
    ]
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化メソッド - WebDriverの設定を行います"""
        # WebDriverの設定
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(3)  # 暗黙的待機

    def setUp(self):
        """各テストケース実行前の処理"""
        # トップページを開く
        self.top_page = TopPage(self.driver).open(self.BASE_URL)
        
    def test_multiple_users_login_logout(self):
        """複数ユーザーのログイン・ログアウトテスト
        
        複数のユーザーアカウントで順にログイン・ログアウトを行い、
        正常に処理できることを検証します。
        """
        for i, user in enumerate(self.TEST_USERS, 1):
            email = user["email"]
            password = user["password"]
            
            with self.subTest(f"ユーザー{i}: {email}"):
                print(f"\nテストケース {i}: {email} でログインを試行")
                
                # ログインページに移動
                login_page = self.top_page.go_to_login()
                
                # ログイン実行
                self.top_page = login_page.login(email, password)
                
                # マイページへ移動できることを確認
                self.top_page.go_to_mypage()
                
                # 現在のURLがマイページであることを確認
                current_url = self.driver.current_url
                self.assertIn("mypage.html", current_url, f"ユーザー {email} はマイページにアクセスできません")
                
                print(f"ユーザー {email} のログイン成功を確認")
                
                # ログアウト処理
                self.top_page = self.top_page.logout()
                time.sleep(1)  # ログアウト後の画面遷移を待つ
                
                # ログアウト後、トップページに戻っていることを確認
                current_url = self.driver.current_url
                self.assertIn("index.html", current_url, "ログアウト後にトップページに戻っていません")
                
                print(f"ユーザー {email} のログアウト成功を確認")
                
                # 次のテスト用に状態をリセット
                self.top_page = TopPage(self.driver)

    @classmethod
    def tearDownClass(cls):
        """テストクラスの終了処理 - WebDriverを閉じます"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)