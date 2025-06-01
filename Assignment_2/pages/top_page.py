from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage
from pages.login_page import LoginPage

class TopPage(BasePage):
    """トップページのページオブジェクト"""
    
    # ページ要素のロケータ
    LOGIN_LINK = (By.LINK_TEXT, "ログイン")
    RESERVATION_LINK = (By.CSS_SELECTOR, "a.nav-link[href=\"./plans.html\"]")
    
    def __init__(self, driver):
        """
        トップページの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        super().__init__(driver)
    
    def open(self, base_url):
        """
        トップページを開く
        
        Args:
            base_url: サイトのベースURL
            
        Returns:
            TopPage: 自身のインスタンス
        """
        self.driver.get(base_url)
        time.sleep(1)  # ページロード完了を待機
        return self
    
    def go_to_login(self):
        """
        ログインページに移動
        
        Returns:
            LoginPage: ログインページのインスタンス
        """
        self.wait_for_clickable(*self.LOGIN_LINK).click()
        time.sleep(0.5)  # クリックしてログイン画面への遷移を待機
        return LoginPage(self.driver)
    
    def go_to_plans(self):
        """
        宿泊予約（プラン一覧）ページに移動
        
        Returns:
            PlansPage: プランページのインスタンス
        """
        from pages.plans_page import PlansPage
        
        # JavaScriptでクリックするように変更
        self.driver.execute_script("document.querySelector('a.nav-link[href=\"./plans.html\"]').click();")
        time.sleep(1.5)  # 宿泊予約ページへの遷移完了を待機
        return PlansPage(self.driver)
    

    def go_to_mypage(self):
        """
        マイページに移動
        
        Returns:
            TopPage: 自身のインスタンス
        """
        # マイページへのリンクをクリック
        mypage_link = self.wait_for_clickable(By.CSS_SELECTOR, "a.nav-link[href='./mypage.html']")
        mypage_link.click()
        time.sleep(1)  # ページ遷移を待機
        return self

    def logout(self):
        """
        ログアウト処理を実行
        
        Returns:
            TopPage: 自身のインスタンス
        """
        # ログアウトボタンをクリック
        logout_button = self.wait_for_clickable(By.CSS_SELECTOR, "button.btn.btn-outline-success")
        logout_button.click()
        time.sleep(1)  # ログアウト処理の完了を待機
        
        return self
    
    def go_to_signup(self):
        """会員登録ページへ移動
        
        Returns:
            SignupPage: 会員登録ページのオブジェクト
        """
        # 会員登録リンクをクリック
        signup_link = self.wait_for_clickable(By.LINK_TEXT, "会員登録")
        signup_link.click()
        time.sleep(1)  # ページ遷移を待機
        
        from pages.signup_page import SignupPage  # 循環インポートを避けるため、ここでインポート
        return SignupPage(self.driver)