import unittest
import time
import os
from selenium import webdriver
from pages.top_page import TopPage

class TestPremiumThemeParkReservation(unittest.TestCase):
    """テーマパーク優待プラン予約のテストクラス
    
    プレミアム会員のテーマパーク優待プラン予約フローを検証します。
    """
    
    # 定数定義
    BASE_URL = 'https://hotel-example-site.takeyaqa.dev/ja/index.html'
    RESERVATION_DATE = "2025/07/15"  # 入力用日付フォーマット
    STAY_NIGHTS = "3"
    GUEST_COUNT = "2"
    PHONE_NUMBER = "00011112222"
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化メソッド - WebDriverの設定を行います"""
        # 環境変数から認証情報を取得するか、デフォルト値を使用
        cls.test_email = os.environ.get('TEST_EMAIL', "ichiro@example.com")
        cls.test_password = os.environ.get('TEST_PASSWORD', "password")
        
        # WebDriverの設定
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(4)  # 暗黙的待機

    def test_premium_member_theme_park_reservation(self):
        """テーマパーク優待プラン予約のテストケース
        
        プレミアム会員としてログインし、テーマパーク優待プランを予約する一連のフローをテストします。
        """
        # トップページを開き、ログインする
        top_page = TopPage(self.driver).open(self.BASE_URL)
        login_page = top_page.go_to_login()
        top_page = login_page.login(self.test_email, self.test_password)
        
        # 宿泊プラン一覧ページに移動し、テーマパーク優待プランを選択
        plans_page = top_page.go_to_plans()
        reservation_page = plans_page.select_theme_park_plan()
        
        # 予約フォームに情報を入力
        reservation_page.fill_reservation_form(
            date=self.RESERVATION_DATE,
            nights=self.STAY_NIGHTS,
            guest_count=self.GUEST_COUNT,
            phone_number=self.PHONE_NUMBER
        )
        
        # 合計金額が表示されていることを確認
        total_text = reservation_page.get_total_price()
        self.assertIn("円", total_text, "合計金額に「円」が含まれていません")
        
        # 予約内容確認ページへ進む
        confirmation_page = reservation_page.confirm_reservation()
        
        # 確認ページが表示されているか確認
        self.assertTrue(
            confirmation_page.is_confirmation_page_displayed(),
            "宿泊予約確認画面が表示されていません"
        )
        print("宿泊予約確認画面に遷移しました。入力内容の検証はスキップします。")
        
        # 予約を完了する
        confirmation_page.complete_reservation()
        
        # 予約完了のモーダルが表示されているか確認
        modal_text = confirmation_page.get_modal_text()
        self.assertIn("予約を完了しました", modal_text, "予約完了メッセージが表示されていません")
        
        # モーダルを閉じる
        plans_page = confirmation_page.close_modal()
        
        # 宿泊プラン一覧に戻ったことを確認
        self.assertTrue(
            plans_page.is_returned_to_plans_page(),
            "宿泊プラン一覧画面に戻っていません"
        )

    @classmethod
    def tearDownClass(cls):
        """テストクラスの終了処理 - WebDriverを閉じます"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)