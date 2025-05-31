from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    """全てのページオブジェクトの基底クラス"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)
    
    def wait_for_element(self, locator):
        """要素が表示されるまで待機"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_clickable(self, locator):
        """要素がクリック可能になるまで待機"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator):
        """要素をクリック（JavaScriptを使用）"""
        element = self.wait_for_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)
        
    def scroll_to_element(self, element):
        """指定された要素までスクロール"""
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)