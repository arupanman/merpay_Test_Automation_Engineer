import unittest
import time
from selenium import webdriver
from pages.top_page import TopPage

class TestPremiumThemeParkReservation(unittest.TestCase):
    """テーマパーク優待プランの予約フローをテストするクラス"""
    
    @classmethod
    def setUpClass(cls):
        """テスト開始前にWebDriverを初期化"""
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(4)  # 暗黙的待機
    
    def test_premium_member_theme_park_reservation(self):
        """プレミアム会員としてテーマパーク優待プランを予約する一連のフローをテスト"""
        # トップページに移動してログイン
        top_page = TopPage(self.driver).navigate()
        login_page = top_page.go_to_login()
        plans_page = login_page.login("ichiro@example.com", "password")
        
        # 宿泊プランページに移動
        plans_page = plans_page.navigate_from_top()
        
        # テーマパーク優待プランを選択
        reservation_page = plans_page.select_theme_park_plan()
        
        # 予約フォーム入力
        reservation_page = reservation_page.fill_reservation_form(
            date="2025/07/15",
            term="3",
            head_count="2",
            breakfast=True,
            contact_method="電話でのご連絡",
            tel="00011112222"
        )
        
        # 合計金額が表示されていることを確認
        total_text = reservation_page.get_total_price()
        self.assertIn("円", total_text)
        
        # 予約内容を確認するボタンをクリック
        confirmation_page = reservation_page.submit_reservation()
        
        # 確認ページの確認
        page_title = confirmation_page.verify_confirmation_page()
        self.assertEqual(page_title, "宿泊予約確認")
        
        # 予約を確定
        confirmation_page = confirmation_page.complete_reservation()
        
        # 予約完了モーダルを確認
        modal_text = confirmation_page.verify_reservation_complete()
        self.assertIn("予約を完了しました", modal_text)
        
        # モーダルを閉じる
        plans_page = confirmation_page.close_success_modal()
        
        # プラン一覧に戻ったことを確認
        self.assertTrue(confirmation_page.verify_return_to_plan_list())

    @classmethod
    def tearDownClass(cls):
        """テスト終了時にブラウザを閉じる"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)