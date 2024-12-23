
import os, json
# from components.Constructor import Constructor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

with open('arqs/vars.json') as json_vars:
    vars_ambiente = json.load(json_vars)

"""Navega para página de anexos e insere arquivos de anexo"""
class Files():
    def __init__(self, driver, wait, actions):
        self.driver = driver
        self.wait = wait
        self.actions = actions

    def insert_attachments(self):
        # Insere arquivos de anexo
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"tabAba3\"]/a"))).click()
        anexo_path = os.getcwd().replace('\\', '/')
        file_path1 = anexo_path + "/arqs/INFORME FORNECEDOR MRN.pdf"
        file_path2 = anexo_path + "/arqs/Manual de Regras de Fornecimento e Embalagem de Materiais.pdf"
        file_path3 = anexo_path + "/arqs/Restrição de coleta Transportadora Della Volpe.pdf"
        self.driver.find_element(By.ID, "files").send_keys(f"{file_path1}\n{file_path2}\n{file_path3}")
        self.driver.find_element(By.XPATH, "//*[@id=\"upload\"]/div/div[2]/button[2]").click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"idBtPrimeiro_AnexoCotacao_mbxAnexo\"]"))).click()
        