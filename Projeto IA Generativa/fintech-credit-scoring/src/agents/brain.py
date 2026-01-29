# Código do "Cérebro"
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.tools import tool
import joblib
import pandas as pd
import os
import json

# Carrega o motor treinado
models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
model = joblib.load(os.path.join(models_dir, 'credit_model.pkl'))
le = joblib.load(os.path.join(models_dir, 'label_encoder.pkl'))

# ORDEM EXATA das features usadas no treinamento
FEATURE_ORDER = ['Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 
                 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 
                 'Changed_Credit_Limit', 'Outstanding_Debt']

@tool
def motor_predicao_credito(dados_cliente_json: str) -> str:
    """
    Analisa dados do cliente e retorna o comportamento de pagamento previsto.
    
    Args:
        dados_cliente_json: String JSON com os dados do cliente contendo:
            - Annual_Income, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate,
            - Num_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment,
            - Changed_Credit_Limit, Outstanding_Debt
    
    IMPORTANTE: As colunas devem estar na ordem exata para garantir predições corretas!
    """
    try:
        dados_cliente = json.loads(dados_cliente_json)
        
        # Garantir que o DataFrame tem as colunas na ORDEM EXATA do treinamento
        df_input = pd.DataFrame([dados_cliente])
        
        # Reordenar as colunas para a ordem correta
        df_input = df_input[FEATURE_ORDER]
        
        # Fazer a predição
        pred = model.predict(df_input)
        resultado = le.inverse_transform(pred)[0]
        return f"O comportamento de pagamento previsto é: {resultado}"
    except KeyError as e:
        return f"Erro: Coluna faltando - {str(e)}. Colunas necessárias: {FEATURE_ORDER}"
    except Exception as e:
        return f"Erro na predição: {str(e)}"

def get_fintech_agent():
    """Retorna um agente com acesso às ferramentas financeiras"""
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Retornar o LLM configurado com acesso às ferramentas
    # O LLM agora tem acesso ao motor_predicao_credito como ferramenta
    return {
        'llm': llm,
        'tools': [motor_predicao_credito],
        'predictor': motor_predicao_credito.func  # Função bruta para chamadas diretas
    }

if __name__ == "__main__":
    print("✓ Modelos carregados com sucesso!")
    print("✓ Ferramenta motor_predicao_credito disponível para o agente")
    print("✓ Agente financeiro pronto para usar\n")
    
    # Exemplo de uso
    exemplo_cliente = {
        'Annual_Income': 50000,
        'Num_Bank_Accounts': 2,
        'Num_Credit_Card': 3,
        'Interest_Rate': 5.5,
        'Num_of_Loan': 1,
        'Delay_from_due_date': 10,
        'Num_of_Delayed_Payment': 0,
        'Changed_Credit_Limit': 1000,
        'Outstanding_Debt': 5000
    }
    
    # Chamar a ferramenta com JSON
    resultado = motor_predicao_credito.invoke(json.dumps(exemplo_cliente))
    print(f"Exemplo de predição:\n{resultado}")