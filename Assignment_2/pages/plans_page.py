from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage

class PlansPage(BasePage):
    """宿泊プラン一覧ページのページオブジェクト"""
    
    # テーマパーク優待プランのロケータ
    THEME_PARK_HEADING = (By.XPATH, "//*[text()='テーマパーク優待プラン']")
    
    def __init__(self, driver):
        """
        プランページの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        super().__init__(driver)
    
    def select_theme_park_plan(self):
        """
        テーマパーク優待プランの「このプランで予約」ボタンをクリック
        
        Returns:
            ReservationPage: 予約ページのインスタンス
        """
        from pages.reservation_page import ReservationPage
        
        # テーマパーク優待プランの見出しを探す
        theme_park_heading = self.wait.until(EC.presence_of_element_located(self.THEME_PARK_HEADING))
            
        # その見出しの親要素（カード）を見つけ、その中の予約ボタンをクリック
        parent_card = theme_park_heading.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card') or contains(@class, 'col')]")
        reserve_button = parent_card.find_element(By.XPATH, ".//a[contains(text(), 'このプランで予約')]")

        # ボタンを確実にクリックするためにJavaScriptを使用
        self.safe_click(reserve_button)
        time.sleep(1.5)  # 予約ページへの遷移を待つ

        # 新しいウィンドウ（タブ）に切り替え
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        return ReservationPage(self.driver)