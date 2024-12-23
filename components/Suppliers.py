import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vendorlist.SearchEngine import *
# from components.Constructor import Constructor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""Classe para navegar para página de fornecedores e preencher o vendor list"""
class Suppliers():
    def __init__(self, driver, wait, actions):
        self.driver = driver
        self.wait = wait
        self.actions = actions

    def fill_suppliers(self, df):
        # Preenche o vendor list
        todos_cnpjs = supplierSearchEngine(df)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabAba2"]/a'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_pesquisaDataGrid_lkbIncluirFornForaLinhaFornecimento"]'))).click()
        
        for value in todos_cnpjs:
            try:
                cnpj = value.strip()
                zeros_to_insert = 14-len(cnpj)
                for zeros in range(zeros_to_insert):
                    cnpj = '0'+cnpj
            except:
                pass

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPrincipal_txtCnpjCpf"]'))).clear()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPrincipal_txtCnpjCpf"]'))).send_keys(cnpj)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPrincipal_btnPesquisarEmpresa"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ckbTodosEmpresasPesquisa"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentButtom_btnConfirmar"]'))).click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()