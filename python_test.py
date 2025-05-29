import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TestPremiumThemeParkReservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(4)  # 暗黙的待機
        cls.wait = WebDriverWait(cls.driver, 12)  # 明示的待機の最大時間

    def test_premium_member_theme_park_reservation(self):
        driver = self.driver
        wait = self.wait

        # 1. プレミアム会員でログイン
        driver.get('https://hotel-example-site.takeyaqa.dev/ja/index.html')
        time.sleep(1)  # ページロード完了を待機
        
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))).click()
        time.sleep(0.5)  # クリックしてログイン画面への遷移を待機
        
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("ichiro@example.com")
        driver.find_element(By.NAME, "password").send_keys("password")
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
        driver.execute_script("arguments[0].scrollIntoView(true);", reserve_button)
        time.sleep(0.5)  # スクロールが完了するのを待つ
        driver.execute_script("arguments[0].click();", reserve_button)
        time.sleep(1.5)  # 予約ページへの遷移を待つ

        # 新しいウィンドウ（タブ）に切り替え
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])

        # 4. フォームに値を入力
        wait.until(EC.visibility_of_element_located((By.ID, "date")))
        driver.find_element(By.ID, "date").clear()
        driver.find_element(By.ID, "date").send_keys("2025/07/15")
        time.sleep(0.3)  # 入力反映を待機
        
        driver.find_element(By.ID, "term").clear()
        driver.find_element(By.ID, "term").send_keys("3")
        time.sleep(0.3)  # 入力反映を待機
        
        driver.find_element(By.ID, "head-count").clear()
        driver.find_element(By.ID, "head-count").send_keys("2", Keys.ENTER)
        time.sleep(0.3)  # 入力反映を待機
        
        # JavaScriptを使用してチェックボックスをクリック
        driver.execute_script("document.getElementById('breakfast').click();")
        time.sleep(0.5)  # 状態変更と計算のために少し待機
        
        contact_select = Select(driver.find_element(By.ID, "contact"))
        contact_select.select_by_visible_text("電話でのご連絡")
        time.sleep(0.5)  # セレクト変更とTEL入力フィールド表示を待機
        
        tel_input = wait.until(EC.visibility_of_element_located((By.ID, "tel")))
        tel_input.clear()
        tel_input.send_keys("00011112222")
        time.sleep(0.8)  # 入力反映と金額計算完了を待機

        # 5. 合計金額が正しく表示されているのを確認
        wait.until(EC.visibility_of_element_located((By.ID, "total-bill")))
        total_text = driver.find_element(By.ID, "total-bill").text
        self.assertIn("円", total_text)
        time.sleep(0.5)  # 金額表示確認後の操作前に少し待機

        # 6. 「予約内容を確認する」ボタンをクリック
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
        submit_button.click()
        time.sleep(1.2)  # 確認ページへの遷移を待機

        # 7. 「宿泊予約確認」画面で入力内容が正しいか確認
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '宿泊予約確認')]")))
        time.sleep(1)  # 確認画面の表示を待機
        
        self.assertIn("テーマパーク優待プラン", driver.page_source)
        self.assertIn("2025年7月15日", driver.page_source)
        self.assertIn("3泊", driver.page_source)
        self.assertIn("2名様", driver.page_source)
        self.assertIn("朝食バイキング", driver.page_source)
        self.assertIn("00011112222", driver.page_source)
        time.sleep(0.5)  # 確認後、次の操作前に少し待機

        # 8. 「この内容で予約する」ボタンをクリック
        driver.find_element(By.XPATH, "//button[contains(., 'この内容で予約する')]").click()
        time.sleep(1.5)  # モーダル表示を待機

        # 9. 「予約を完了しました」というポップアップメッセージを確認
        modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
        self.assertIn("予約を完了しました", modal.text)
        time.sleep(0.8)  # モーダル表示確認後、少し待機

        # 10. 「閉じる」ボタンをクリック
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '閉じる')]")))
        close_button.click()
        time.sleep(1)  # モーダルを閉じた後の画面更新を待機

        # 11. 「宿泊プラン一覧」画面に戻ったことを確認
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '宿泊プラン一覧')]")))
        time.sleep(0.5)  # テスト完了前の最終確認

    def tearDown(self):
        if hasattr(self, '_outcome') and self._outcome.errors:
            self.driver.save_screenshot(f"error-screenshot-{time.time()}.png")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)