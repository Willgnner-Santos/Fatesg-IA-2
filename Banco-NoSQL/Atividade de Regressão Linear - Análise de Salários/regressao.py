import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

CARGO_ABREV = {
    "Diretor TI": "DIR",
    "Gerente Projetos": "GP",
    "Coordenador TI": "COORD",
    "Analista Senior": "AS",
    "Analista Pleno": "AP",
    "Analista Junior": "AJ",
    "Dev Front-End": "FE",
    "Dev Back-End": "BE",
    "Dev FullStack": "FS",
    "Dev Mobile": "MOB",
    "Dev Python": "PY",
    "Dev Java": "JAVA",
    "Dev C#": "C#",
    "Dev PHP": "PHP",
    "DBA": "DBA",
    "Especialista Cloud": "CLOUD",
    "Cybersecurity": "CYBER",
    "Estagiário TI": "EST",
}

print("→ Conectando ao MongoDB...")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db["funcionarios"]

print("→ Buscando dados do banco...")
data = list(collection.find({}, {"_id": 0, "idade": 1, "salario": 1, "cargo": 1}))

df = pd.DataFrame(data)

print(f"→ Total de registros carregados: {len(df)}")

print("\n→ Verificando valores nulos...")
print(df.isnull().sum())


df = df.dropna()
print("✔ Dados limpos.")


df["cargo_abrev"] = df["cargo"].map(CARGO_ABREV)

X = df[["idade"]]  
y = df["salario"] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)

print("\n✔ Modelo treinado com sucesso!")
print(f"Coeficiente anual: {model.coef_[0]:.2f}")
print(f"Intercepto: {model.intercept_:.2f}")

idades_prever = [[25], [30], [40], [50], [60]]

print("\n→ Previsões de salário:")
for idade in idades_prever:
    pred = model.predict([idade])[0]
    print(f"  Idade {idade[0]} → R$ {pred:.2f}")

plt.figure(figsize=(10, 6))
plt.scatter(df["idade"], df["salario"])
plt.xlabel("Idade")
plt.ylabel("Salário")
plt.title("Relação Idade × Salário")

x_line = np.linspace(df["idade"].min(), df["idade"].max(), 100)
y_line = model.predict(x_line.reshape(-1, 1))
plt.plot(x_line, y_line)

plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))

media_por_cargo = df.groupby("cargo_abrev")["salario"].mean().sort_values()
plt.bar(media_por_cargo.index, media_por_cargo.values)

plt.title("Média Salarial por Cargo (Abreviado)")
plt.xlabel("Cargo (Abrev.)")
plt.ylabel("Salário Médio (R$)")
plt.grid(axis="y")

plt.show()

print("\n→ LEGENDA DOS CARGOS (ABREVIADOS):")
for cargo, abrev in CARGO_ABREV.items():
    print(f"  {abrev} = {cargo}")

plt.figure(figsize=(12, 6))
df.boxplot(column="salario", by="cargo_abrev", grid=True, rot=45)

plt.title("Distribuição Salarial por Cargo")
plt.suptitle("")  
plt.xlabel("Cargo (Abrev.)")
plt.ylabel("Salário (R$)")

plt.show()

print("\n→ Estatísticas gerais:")
print(df["salario"].describe())

client.close()
print("\n✔ Conexão com o MongoDB encerrada.")
