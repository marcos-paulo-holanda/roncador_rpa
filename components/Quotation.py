import json, time
# from components.Constructor import Constructor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

with open('arqs/vars.json') as json_vars:
    vars_ambiente = json.load(json_vars)

class Quotation():
    def __init__(self, driver, wait, actions):
        self.driver = driver
        self.wait = wait
        self.actions = actions

    def fill_data(self, item_family_name):
        
        self.driver.get(vars_ambiente['url_cotacao_manutencao'])
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['id_cotacao'])))
        cotacao_numero = str(self.driver.find_element(By.XPATH, vars_ambiente['id_cotacao']).get_attribute("value"))

        self.driver.find_element(By.XPATH, vars_ambiente['desc_cotacao']).send_keys(
                f"""TRM{cotacao_numero} - {item_family_name} """ 
            )
        time.sleep(3)      
        cotacao_obs_element = self.wait.until(EC.presence_of_element_located((By.XPATH, vars_ambiente['cotacao_obs'])))

        cotacao_obs_element.send_keys("""
            Prezado fornecedor,

            Favor nos apesentar suas condições comerciais, seguindo as premissas abaixo:

            A T E N Ç Ã O
            Favor anexar proposta técnica, datasheet ou catálogo do item;
            Orçar de acordo com a especificação técnica solicitada, sempre respeitar o modelo e marca solicitada.

            NÃO ACEITAMOS ITENS SIMILARES
        """)

        select_frete = self.wait.until(EC.presence_of_element_located((By.ID, "_cCOTACAO_x_nCdFrete")))
        script = """
        var select = arguments[0];
        select.value = '2';
        var event = new Event('change', { bubbles: true });
        select.dispatchEvent(event);
        """
        self.driver.execute_script(script, select_frete)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['frete']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['pagamento']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['permissao_empresa']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, vars_ambiente['visivel']))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'btnSalvar'))).click()

        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
        time.sleep(2)
