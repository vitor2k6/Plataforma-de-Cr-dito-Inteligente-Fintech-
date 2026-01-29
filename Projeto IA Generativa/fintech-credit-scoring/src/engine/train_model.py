import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_credit_model():
    # 1. Carregar os dados
    df = pd.read_csv(r'C:\Users\Vitor\OneDrive\Área de Trabalho\Projeto IA Generativa\fintech-credit-scoring\data\bronze\train.csv')

    # 2. Pré-processamento Simples (O essencial para o modelo rodar)
    # Vamos focar em colunas numéricas para este exemplo
    features = ['Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Outstanding_Debt']
    
    x = df[features].copy()
    y = df['Payment_Behaviour'] # O que queremos prever

    # Limpar dados: remover underscores e converter para numérico
    for col in features:
        x[col] = x[col].astype(str).str.replace('_', '', regex=False)
        x[col] = pd.to_numeric(x[col], errors='coerce')
    
    # Remover linhas com valores faltantes
    x = x.dropna()
    y = y[x.index]

    # Transformar o alvo (texto) em Números (0, 1, 2)
    le = LabelEncoder()
    y = le.fit_transform(y)

    # 3. Dividir os dados em Treino e Teste 
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # 4. Treinar o XGBoost
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        objective='multi:softmax'
    )

    print("Iniciando treinamento do modelo...")
    model.fit(x_train, y_train)

    # 5. Salvar o modelo e encoder na pasta models/
    # Usar caminho relativo ao projeto
    models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(model, os.path.join(models_dir, 'credit_model.pkl'))
    joblib.dump(le, os.path.join(models_dir, 'label_encoder.pkl'))
    print("Modelo salvo com sucesso em models/credit_model.pkl")

if __name__ == "__main__":
    train_credit_model()