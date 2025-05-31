import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PlansPage(BasePage):
    """宿泊プラン一覧ページのページオブジェクト"""
    
    # ロケーター
    BOOKING_NAV_LINK = (By.CSS_SELECTOR, "a.nav-link[href=\"./plans.html\"]")
    THEME_PARK_PLAN_HEADING = (By.XPATH, "//*[text()='テーマパーク優待プラン']")
    
    def navigate_from_top(self):
        """トップメニューから宿泊予約ページへ移動"""
        self.driver.execute_script("document.querySelector('a.nav-link[href=\"./plans.html\"]').click();")
        time.sleep(1.5)  # 宿泊予約ページへの遷移を待機
        return self
    
    def select_theme_park_plan(self):
        """テーマパーク優待プランを選択"""
        theme_park_heading = self.wait_for_element(self.THEME_PARK_PLAN_HEADING)
        parent_card = theme_park_heading.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card') or contains(@class, 'col')]")
        reserve_button = parent_card.find_element(By.XPATH, ".//a[contains(text(), 'このプランで予約')]")

        self.scroll_to_element(reserve_button)
        time.sleep(0.5)  # スクロール完了を待機
        self.driver.execute_script("arguments[0].click();", reserve_button)
        time.sleep(1.5)  # 予約ページへの遷移を待機
        
        # 新しいウィンドウ（タブ）に切り替え
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)
        
        from pages.reservation_page import ReservationPage
        return ReservationPage(self.driver)