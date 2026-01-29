from fastapi import FastAPI
from agents.brain import get_fintech_agent, motor_predicao_credito
from pydantic import BaseModel
import json
import uvicorn

# Definir o modelo de entrada
class DadosCliente(BaseModel):
    Annual_Income: float
    Num_Bank_Accounts: int
    Num_Credit_Card: int
    Interest_Rate: float
    Num_of_Loan: int
    Delay_from_due_date: int
    Num_of_Delayed_Payment: int
    Changed_Credit_Limit: float
    Outstanding_Debt: float

app = FastAPI(title="Fintech Credit Agent API")
agent_config = get_fintech_agent()

@app.get("/")
async def root():
    """Rota raiz com instruções de uso"""
    return {
        "title": "Fintech Credit Agent API",
        "descricao": "API para análise de risco de crédito usando XGBoost",
        "endpoints": {
            "POST /analisar": "Analisar dados de um cliente",
            "GET /health": "Verificar status da API",
            "GET /docs": "Documentação interativa (Swagger)"
        },
        "exemplo_uso": "POST /analisar com os dados do cliente em JSON"
    }

@app.post("/analisar")
async def analisar_pergunta(dados_cliente: DadosCliente):
    """
    Analisa dados de um cliente para prever comportamento de pagamento.
    
    Exemplo de entrada:
    {
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
    """
    try:
        resultado = motor_predicao_credito.invoke(json.dumps(dados_cliente.dict()))
        return {"resposta": resultado}
    except Exception as e:
        return {"erro": str(e)}

@app.get("/health")
async def health_check():
    """Verificar se a API está funcionando"""
    return {"status": "API Fintech funcionando corretamente"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)