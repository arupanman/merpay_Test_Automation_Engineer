import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TestPremiumThemeParkReservation(unittest.TestCase):
    """テーマパーク優待プランの予約フローをテストするクラス"""
    
    @classmethod
    def setUpClass(cls):
        """テスト開始前にWebDriverを初期化"""
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(4)  # 暗黙的待機
        cls.wait = WebDriverWait(cls.driver, 12)  # 明示的待機の最大時間

    def test_premium_member_theme_park_reservation(self):
        """プレミアム会員としてテーマパーク優待プランを予約する一連のフローをテスト"""
        driver = self.driver
        wait = self.wait

        # 1. プレミアム会員でログイン
        driver.get('https://hotel-example-site.takeyaqa.dev/ja/index.html')
        time.sleep(1)  # ページロード完了を待機
        
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))).click()
        time.sleep(0.5)  # ログイン画面への遷移を待機
        
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("ichiro@example.com")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)  # ログイン処理完了を待機

        # 2. 「宿泊予約」ボタンをクリック
        driver.execute_script("document.querySelector('a.nav-link[href=\"./plans.html\"]').click();")
        time.sleep(1.5)  # 宿泊予約ページへの遷移を待機

        # 3. テーマパーク優待プランの「このプランで予約」ボタンをクリック
        theme_park_heading = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[text()='テーマパーク優待プラン']")))
        parent_card = theme_park_heading.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card') or contains(@class, 'col')]")
        reserve_button = parent_card.find_element(By.XPATH, ".//a[contains(text(), 'このプランで予約')]")

        driver.execute_script("arguments[0].scrollIntoView(true);", reserve_button)
        time.sleep(0.5)  # スクロール完了を待機
        driver.execute_script("arguments[0].click();", reserve_button)
        time.sleep(1.5)  # 予約ページへの遷移を待機

        # 新しいウィンドウ（タブ）に切り替え
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        # 4. 予約フォームに値を入力
        wait.until(EC.visibility_of_element_located((By.ID, "date")))
        driver.find_element(By.ID, "date").clear()
        driver.find_element(By.ID, "date").send_keys("2025/07/15")
        time.sleep(0.3)
        
        driver.find_element(By.ID, "term").clear()
        driver.find_element(By.ID, "term").send_keys("3")
        time.sleep(0.3)
        
        driver.find_element(By.ID, "head-count").clear()
        driver.find_element(By.ID, "head-count").send_keys("2", Keys.ENTER)
        time.sleep(0.3)
        
        # 朝食バイキングオプションを選択
        driver.execute_script("document.getElementById('breakfast').click();")
        time.sleep(0.5)
        
        # 連絡方法を電話に設定
        contact_select = Select(driver.find_element(By.ID, "contact"))
        contact_select.select_by_visible_text("電話でのご連絡")
        time.sleep(0.5)
        
        # 電話番号を入力
        tel_input = wait.until(EC.visibility_of_element_located((By.ID, "tel")))
        tel_input.clear()
        tel_input.send_keys("00011112222")
        time.sleep(0.8)

        # 5. 合計金額が表示されていることを確認
        total_text = wait.until(EC.visibility_of_element_located((By.ID, "total-bill"))).text
        self.assertIn("円", total_text)
        time.sleep(0.5)

        # 6. 「予約内容を確認する」ボタンをクリック
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(2)

        # 7. 「宿泊予約確認」画面に遷移したことを確認
        confirm_header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#confirm h2.my-3")))
        self.assertEqual(confirm_header.text.strip(), "宿泊予約確認")
        time.sleep(0.5)

        # 8. 「この内容で予約する」ボタンをクリック
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "#confirm button[data-target='#success-modal']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", confirm_btn)
        driver.execute_script("arguments[0].click();", confirm_btn)

        # 9. 予約完了モーダルが表示されることを確認
        modal = wait.until(EC.visibility_of_element_located((By.ID, "success-modal")))
        modal_content = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
        self.assertIn("予約を完了しました", modal_content.text)
        time.sleep(1)

        # 10. 「閉じる」ボタンをクリック
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '閉じる')]")))
        close_button.click()
        time.sleep(1)

        # 11. 「宿泊プラン一覧」画面に戻ったことを確認
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '宿泊プラン一覧')]")))
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """テスト終了時にブラウザを閉じる"""
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)