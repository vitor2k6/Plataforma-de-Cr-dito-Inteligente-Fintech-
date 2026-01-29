# Fintech Credit Scoring API

API de análise de risco de crédito usando XGBoost e LangChain.

## Visão Geral

Este projeto treina um modelo XGBoost para prever o comportamento de pagamento de clientes com base em dados financeiros. A API FastAPI expõe um endpoint para fazer predições em tempo real.

## Estrutura do Projeto

```
fintech-credit-scoring/
├── data/
│   └── bronze/
│       └── train.csv           # Dados de treinamento
├── models/                      # Modelos treinados (criados ao executar train_model.py)
│   ├── credit_model.pkl
│   └── label_encoder.pkl
├── src/
│   ├── agents/
│   │   └── brain.py            # Agente com ferramenta de predição
│   ├── engine/
│   │   └── train_model.py      # Script de treinamento do modelo
│   └── main.py                 # API FastAPI
├── start_server.bat            # Inicia servidor (Windows)
├── call_api.bat                # Testa API (Windows)
└── test_api.py                 # Cliente Python para testar API
```

## Instalação

### 1. Dependências

Instale as dependências com o Python 3.13:

```powershell
C:\Users\Vitor\AppData\Local\Microsoft\WindowsApps\python3.13.exe -m pip install langchain_openai langchain pandas xgboost joblib scikit-learn python-dotenv fastapi uvicorn requests
```

### 2. Treinar o Modelo

Se ainda não treinou o modelo:

```powershell
C:\Users\Vitor\AppData\Local\Microsoft\WindowsApps\python3.13.exe "src/engine/train_model.py"
```

Isso criará os arquivos `models/credit_model.pkl` e `models/label_encoder.pkl`.

## Como Usar

### Opção 1: Windows (Scripts .bat)

#### Iniciar Servidor
```powershell
.\start_server.bat
```
Abrirá uma nova janela com o servidor rodando em `http://127.0.0.1:8000`.

#### Testar API
```powershell
.\call_api.bat
```
Executará `test_api.py` e mostrará a resposta da predição.

### Opção 2: Terminal (Manual)

#### Iniciar Servidor
```powershell
C:\Users\Vitor\AppData\Local\Microsoft\WindowsApps\python3.13.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

#### Testar API

**Swagger (Navegador):**
```
http://127.0.0.1:8000/docs
```

**Python:**
```powershell
C:\Users\Vitor\AppData\Local\Microsoft\WindowsApps\python3.13.exe test_api.py
```

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/analisar \
  -H "Content-Type: application/json" \
  -d '{
    "Annual_Income": 50000,
    "Num_Bank_Accounts": 2,
    "Num_Credit_Card": 3,
    "Interest_Rate": 5.5,
    "Num_of_Loan": 1,
    "Delay_from_due_date": 10,
    "Num_of_Delayed_Payment": 0,
    "Changed_Credit_Limit": 1000,
    "Outstanding_Debt": 5000
  }'
```

## Endpoints da API

### `POST /analisar`
Analisa dados de um cliente e retorna a predição de comportamento de pagamento.

**Entrada:**
```json
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
```

**Saída:**
```json
{
  "resposta": "O comportamento de pagamento previsto é: Low_spent_Small_value_payments"
}
```

### `GET /health`
Verifica se a API está funcionando.

**Saída:**
```json
{
  "status": "API Fintech funcionando corretamente"
}
```

### `GET /`
Retorna informações gerais sobre a API.

## Variáveis de Ambiente

O arquivo `.env` deve conter sua chave de API OpenAI (se usar integração com LLM):

```
OPENAI_API_KEY=sua_chave_aqui
```

## Modelo XGBoost

- **Features:** Annual_Income, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate, Num_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment, Changed_Credit_Limit, Outstanding_Debt
- **Target:** Payment_Behaviour (classificação multiclasse)
- **Validação:** 80% treino, 20% teste

## Dúvidas Frequentes

**P: A API não conecta?**  
R: Certifique-se de que o servidor está rodando (verá "Uvicorn running on http://127.0.0.1:8000" no terminal).

**P: Erro de módulos não encontrados?**  
R: Instale as dependências listadas na seção "Instalação".

**P: Como parar o servidor?**  
R: Pressione `Ctrl+C` no terminal onde ele está rodando.

## Contato & Suporte

Para problemas, verifique os logs do servidor e valide os dados de entrada.
