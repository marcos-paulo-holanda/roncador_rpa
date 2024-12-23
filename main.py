
import  os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from components.Quotation import Quotation
from components.ItemService import ItemService
from components.Suppliers import Suppliers
from components.Files import Files
from components.Authenticator import Authenticator
    
def main():
  
    #driver = webdriver.Chrome(service=Service('./chromedriver.exe', log_path=os.devnull))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), log_path = os.devnull))
    wait = WebDriverWait(driver, 240)
    actions = ActionChains(driver)
    
    carteira_ocs = pd.read_excel('rodagem.xlsx')
    carteira_ocs['requisicoes_ocs'] = carteira_ocs.apply(lambda row: f"{row['nr_requisicao']}-{row['numero_ordem']}", axis=1)
    carteira_ocs = carteira_ocs[['requisicoes_ocs', 'it_codigo', 'Desc Resumida', 'narrativa', 'Familia_robo']]

    auth = Authenticator(driver, wait, actions)
    auth.login()

    for familia in carteira_ocs['Familia_robo'].unique():
        # Cria uma DataFrame temporária contendo apenas as linhas correspondentes ao valor atual de 'Familia_robo'
        dataframe_temporaria = carteira_ocs[carteira_ocs['Familia_robo'] == familia]
        dataframe_temporaria = dataframe_temporaria.reset_index(drop=True)
        nome_familia = list(dataframe_temporaria['Familia_robo'].values)[0]

        requisicoes = dataframe_temporaria.requisicoes_ocs
        quotation = Quotation(driver, wait, actions)
        quotation.fill_data(nome_familia)
        item_service = ItemService(driver, wait, actions)
        item_service.fill_data(requisicoes)
        suppliers = Suppliers(driver, wait, actions)
        suppliers.fill_suppliers(dataframe_temporaria)
        attach = Files(driver, wait, actions)
        attach.insert_attachments()
        item_service.payment_condition()

    driver.quit()
    print('--- As cotações foram geradas com sucesso ---')
    input('Pressione qualquer tecla para finalizar: ')

if __name__ == '__main__':
    main()