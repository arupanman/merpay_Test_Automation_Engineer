from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time

class BasePage:
    """全てのページオブジェクトの基底クラス"""
    
    def __init__(self, driver):
        """
        ページオブジェクトの初期化
        
        Args:
            driver: WebDriverインスタンス
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)
    
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
            raise Exception(f"要素のクリックに失敗しました: {e}")
    
    def wait_for_element(self, by, value):
        """要素が表示されるまで待機して、要素を返す
        
        Args:
            by: locator type
            value: locator value
            
        Returns:
            WebElement: 見つかった要素
        """
        return self.wait.until(EC.visibility_of_element_located((by, value)))
    
    def wait_for_clickable(self, by, value):
        """要素がクリック可能になるまで待機して、要素を返す
        
        Args:
            by: locator type
            value: locator value
            
        Returns:
            WebElement: 見つかった要素
        """
        return self.wait.until(EC.element_to_be_clickable((by, value)))