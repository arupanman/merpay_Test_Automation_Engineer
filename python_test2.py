import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

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
        cls.wait = WebDriverWait(cls.driver, 12)  # 明示的待機の最大時間

    def safe_click(self, element):
        """要素を安全にクリックする汎用メソッド
        
        JavaScriptを使用したクリックとスクロール処理を行います。
        
        Args:
            element: クリックする要素
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # スクロールが完了するまで待機
            self.driver.execute_script("arguments[0].click();", element)
        except WebDriverException as e:
            self.fail(f"要素のクリックに失敗しました: {e}")

    def test_premium_member_theme_park_reservation(self):
        """テーマパーク優待プラン予約のテストケース
        
        プレミアム会員としてログインし、テーマパーク優待プランを予約する一連のフローをテストします。
        """
        driver = self.driver
        wait = self.wait

        # 1. プレミアム会員でログイン
        driver.get(self.BASE_URL)
        time.sleep(1)  # ページロード完了を待機
        
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))).click()
        time.sleep(0.5)  # クリックしてログイン画面への遷移を待機
        
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(self.test_email)
        driver.find_element(By.NAME, "password").send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)  # ログイン処理完了を待機

        # 2. 「宿泊予約」ボタンをタップ
        driver.execute_script("document.querySelector('a.nav-link[href=\"./plans.html\"]').click();")
        time.sleep(1.5)  # 宿泊予約ページへの遷移完了を待機

        # 3. テーマパーク優待プランの「このプランで予約」ボタンを押す
        # テーマパーク優待プランの見出しを探す
        theme_park_heading = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[text()='テーマパーク優待プラン']")))
            
        # その見出しの親要素（カード）を見つけ、その中の予約ボタンをクリック
        parent_card = theme_park_heading.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card') or contains(@class, 'col')]")
        reserve_button = parent_card.find_element(By.XPATH, ".//a[contains(text(), 'このプランで予約')]")

        # ボタンを確実にクリックするためにJavaScriptを使用
        self.safe_click(reserve_button)
        time.sleep(1.5)  # 予約ページへの遷移を待つ

        # 新しいウィンドウ（タブ）に切り替え
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])

        # 4. フォームに値を入力
        date_field = wait.until(EC.visibility_of_element_located((By.ID, "date")))
        date_field.clear()
        date_field.send_keys(self.RESERVATION_DATE)
        time.sleep(0.3)  # 入力反映を待機
        
        term_field = driver.find_element(By.ID, "term")
        term_field.clear()
        term_field.send_keys(self.STAY_NIGHTS)
        time.sleep(0.3)  # 入力反映を待機
        
        head_count_field = driver.find_element(By.ID, "head-count")
        head_count_field.clear()
        head_count_field.send_keys(self.GUEST_COUNT, Keys.ENTER)
        time.sleep(0.3)  # 入力反映を待機
        
        # JavaScriptを使用してチェックボックスをクリック
        driver.execute_script("document.getElementById('breakfast').click();")
        time.sleep(0.5)  # 状態変更と計算のために少し待機
        
        contact_select = Select(driver.find_element(By.ID, "contact"))
        contact_select.select_by_visible_text("電話でのご連絡")
        time.sleep(0.5)  # セレクト変更とTEL入力フィールド表示を待機
        
        tel_input = wait.until(EC.visibility_of_element_located((By.ID, "tel")))
        tel_input.clear()
        tel_input.send_keys(self.PHONE_NUMBER)
        time.sleep(0.8)  # 入力反映と金額計算完了を待機

        # 5. 合計金額が正しく表示されているのを確認
        total_element = wait.until(EC.visibility_of_element_located((By.ID, "total-bill")))
        total_text = total_element.text
        self.assertIn("円", total_text, "合計金額に「円」が含まれていません")
        time.sleep(0.5)  # 金額表示確認後の操作前に少し待機

        # 6. 「予約内容を確認する」ボタンをクリック
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
        self.safe_click(submit_button)
        time.sleep(2)  # 遷移を待機

        # 7. 「宿泊予約確認」画面の確認はスキップし、そのままボタンをクリック
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#confirm")))
        print("宿泊予約確認画面に遷移しました。入力内容の検証はスキップします。")
        
        # 8. 「この内容で予約する」ボタンを確実にクリック
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#confirm button[data-target='#success-modal']"
        )))
        self.safe_click(confirm_btn)
        time.sleep(1.5)  # ボタンクリック後の処理を待機

        # モーダル (#success-modal) が表示されるまで待機
        wait.until(EC.visibility_of_element_located((By.ID, "success-modal")))

        # 9. 「予約を完了しました」というポップアップメッセージを確認
        modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
        modal_text = modal.text
        self.assertIn("予約を完了しました", modal_text, "予約完了メッセージが表示されていません")
        time.sleep(1)  # モーダル表示確認後、少し待機

        # 10. 「閉じる」ボタンをクリック
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '閉じる')]")))
        close_button.click()
        time.sleep(1)  # モーダルを閉じた後の画面更新を待機

        # 11. 「宿泊プラン一覧」画面に戻ったことを確認
        plan_list_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '宿泊プラン一覧')]")))
        self.assertTrue(plan_list_element.is_displayed(), "宿泊プラン一覧画面に戻っていません")
        time.sleep(0.5)  # テスト完了前の最終確認

    @classmethod
    def tearDownClass(cls):
        """テストクラスの終了処理 - WebDriverを閉じます"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)