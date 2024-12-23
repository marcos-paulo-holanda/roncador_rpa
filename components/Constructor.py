import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

class Constructor:
    """Classe base que define os elementos comuns para todas as páginas."""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=pt-BR")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(service=Service('./chromedriver.exe', log_path=os.devnull))
        self.wait = WebDriverWait(self.driver, 60)
        self.actions = ActionChains(self.driver)