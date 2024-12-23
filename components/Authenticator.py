
import json
# from components.Constructor import Constructor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

with open('arqs/vars.json') as json_vars:
    vars_ambiente = json.load(json_vars)

"""Classe para autenticar usuário no sistema Paradigma"""
class Authenticator():
    def __init__(self, driver, wait, actions):
        self.driver = driver
        self.wait = wait
        self.actions = actions
    
    def login(self):
        self.driver.get(vars_ambiente['url_inicial_paradigma'])
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-modal-body")))
        self.actions.send_keys(Keys.ESCAPE).perform()
