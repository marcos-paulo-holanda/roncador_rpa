import json, time
# from components.Constructor import Constructor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

with open('arqs/vars.json') as json_vars:
    vars_ambiente = json.load(json_vars)

"""Classe para navegar para página de itens e preencher campos de requisição"""
class ItemService():
    def __init__(self, driver, wait, actions):
        self.driver = driver
        self.wait = wait
        self.actions = actions

    def fill_data(self, requisicoes):
        # Navega para página de itens e insere requisições
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['aba1']))).click()
        janelas_anteriores = self.driver.window_handles
        janela_atual = self.driver.current_window_handle
    
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['incluir_requisicao']))).click()
        self.wait.until(EC.number_of_windows_to_be(len(janelas_anteriores) + 1))

        janelas_atuais = self.driver.window_handles
        nova_janela_id = None
        for janela in janelas_atuais:
            if janela not in janelas_anteriores:
                nova_janela_id = janela
                break

        nova_janela_index = janelas_atuais.index(nova_janela_id)
        self.driver.switch_to.window(janelas_atuais[nova_janela_index])

        for i in range(len(requisicoes)):
            requisicao = requisicoes[i]

            self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['campo_req_empresa']))).clear()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['campo_req_empresa']))).send_keys(requisicao)

            self.actions.send_keys(Keys.TAB).perform()
            self.actions.send_keys(Keys.UP).perform()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['btn_pesquisar']))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ckbTodos"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['btn_agrupar']))).click()
        self.wait.until(EC.alert_is_present()).accept()
        self.wait.until(EC.alert_is_present()).accept()
        self.driver.switch_to.window(janela_atual)

    def payment_condition(self):
        # Navega para página de condições de pagamento e preenche campo
        self.driver.find_element(By.XPATH, '//*[@id=\"tabAba1\"]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="ckbTodos"]').click()

        janelas_anteriores = self.driver.window_handles
        janela_atual = self.driver.current_window_handle
        self.driver.find_element(By.XPATH, vars_ambiente['cond_pagamento']).click()

        self.wait.until(EC.number_of_windows_to_be(len(janelas_anteriores) + 1)) #isso é para esperar abrir a nova janela
        #time.sleep(3) #isso é para esperar abrir a nova janela

        janelas_atuais = self.driver.window_handles
        nova_janela_id = None
        for janela in janelas_atuais:
            if janela not in janelas_anteriores:
                nova_janela_id = janela
                break

        nova_janela_index = janelas_atuais.index(nova_janela_id)
        self.driver.switch_to.window(janelas_atuais[nova_janela_index])

        self.actions.send_keys(Keys.TAB).perform()
        for _ in range(3):
            self.actions.send_keys('6').perform()
        self.actions.send_keys(Keys.TAB).perform()
        self.actions.send_keys(Keys.SPACE).perform()
        time.sleep(3)
        self.driver.switch_to.window(janela_atual)
        self.wait.until(EC.alert_is_present()).accept()
