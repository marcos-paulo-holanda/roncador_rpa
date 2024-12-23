import pickle, sys, os, warnings
import pandas as pd
import sklearn, sklearn.feature_extraction.text, numpy.core.multiarray
warnings.filterwarnings('ignore')

# Define the function to load the trained model
def load_model():
    if getattr(sys, 'frozen', False):
        # Se o aplicativo está sendo executado como um executável gerado (ex: PyInstaller)
        dir_path = os.path.dirname(sys.executable)
    else:
        # Se o aplicativo está sendo executado em um ambiente de desenvolvimento (ex: Python)
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # Caminho completo para o arquivo .pkl
    model_path = os.path.join(dir_path, 'arqs', 'aprendizado.pkl')

    # Carrega o modelo do arquivo .pkl
    with open(model_path, 'rb') as file:
        clf, cvt, tfi = pickle.load(file)
    
    return clf, cvt, tfi

def classify_item(descricao):
    # Load the trained model
    clf, cvt, tfi = load_model()

    # Perform classification using the loaded model
    novo_cvt = cvt.transform(pd.Series(descricao))
    novo_tfi = tfi.transform(novo_cvt)

    familia = clf.predict(novo_tfi)[0]
    return familia
