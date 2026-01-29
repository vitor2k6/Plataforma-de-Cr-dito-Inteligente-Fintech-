import requests
import json

# URL da API
url = "http://127.0.0.1:8000/analisar"

# Dados de teste
dados_cliente = {
    "Annual_Income": 50000,
    "Num_Bank_Accounts": 2,
    "Num_Credit_Card": 3,
    "Interest_Rate": 5.5,
    "Num_of_Loan": 1,
    "Delay_from_due_date": 10,
    "Num_of_Delayed_Payment": 0,
    "Changed_Credit_Limit": 1000,
    "Outstanding_Debt": 5000
}

try:
    print("Testando API em:", url)
    print("Enviando dados:", json.dumps(dados_cliente, indent=2))
    
    response = requests.post(url, json=dados_cliente)
    
    print("\nStatus Code:", response.status_code)
    print("Resposta:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    
except Exception as e:
    print("Erro:", str(e))
