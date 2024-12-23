import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.Connectors import *
from vendorlist.VendorList import *
from vendorlist.Classifier import *
import traceback

def supplierSearchEngine(df):
    pg_connector = PostgreConnector()
    pg_connector.connect()
    sql_server_connector = SqlServerConnector()
    sql_server_connector.connect()
    
    # Busca fornecedores conforme GCAT
    try:
        itens = df['it_codigo']
        itens_str = ','.join(["'{}'".format(item) for item in itens.tolist()])
        query = f"SELECT DISTINCT fc.cnpj FROM vendorlist.vw_fornecedores_classificados fc JOIN vendorlist.vw_itens_classificados ic ON ic.categoria = fc.categoria WHERE ic.cod_item IN ({itens_str});"
        vendor_list = VendorList(pg_connector).define_vendorlist(query)
        fornecedores_cnpj = list(vendor_list.cnpj)
    except Exception as e:
        tb = traceback.format_exc()
        print('Erro ao buscar fornecedor para o item:', e)
        print('O erro ocorreu na seguinte linha:', tb)

    # Busca fornecedores conforme histórico de compra
    try:
        itens = df['it_codigo']
        itens_str = ','.join(["'{}'".format(item) for item in itens.tolist()])
        query = f"SELECT cnpj FROM vendorlist.vw_historico_compra WHERE cod_item IN ({itens_str});"
        vendor_list = VendorList(pg_connector).define_vendorlist(query)
        fornecedores_cnpj.extend(list(vendor_list.cnpj))
    except Exception as e:
        tb = traceback.format_exc()
        print('Erro ao buscar fornecedor para o item: ', e)
        print('O erro ocorreu na seguinte linha:', tb)

    # Busca fornecedores conforme última compra
    try:
        itens = df['it_codigo']
        itens_str = ','.join(["'{}'".format(item) for item in itens.tolist()])
        query = f"SELECT e.cgc FROM vw_tbl_emitente e JOIN vw_ultima_compra c ON e.cod_emitente = c.cod_emitente WHERE c.it_codigo IN ({itens_str});"
        vendor_list = VendorList(sql_server_connector).define_vendorlist(query)
        fornecedores_cnpj.extend(list(vendor_list.cgc))
    except Exception as e:
        tb = traceback.format_exc()
        print('Erro ao buscar fornecedor para o item: ', e)
        print('O erro ocorreu na seguinte linha:', tb)
    
    # Classifica o item conforme o aprendizado de máquina e busca fornecedor através da categoria do item
    try:
        narrativa_exemplar = df['narrativa'][0]
        categoria = classify_item(narrativa_exemplar)
        query = f"SELECT cnpj FROM vendorlist.vw_fornecedores_classificados WHERE categoria = '{categoria}';"
        vendor_list = VendorList(pg_connector).define_vendorlist(query)
        fornecedores_cnpj.extend(list(vendor_list.cnpj)[:3])
    except Exception as e:
        tb = traceback.format_exc()
        print('Erro ao buscar fornecedor para o item: ', e)
        print('O erro ocorreu na seguinte linha:', tb)

    pg_connector.disconnect()
    sql_server_connector.disconnect()
    return fornecedores_cnpj