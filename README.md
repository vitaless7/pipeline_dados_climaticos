# Pipeline de Dados Climáticos com Airflow ☁️📊

Este projeto é um pipeline criado em **Apache Airflow** para coletar dados climáticos da cidade de **Boston** semanalmente.  
Os dados são obtidos através da API do **Visual Crossing Weather** e salvos como arquivos CSV organizados por semana.

---

## ⚙️ Estrutura do Pipeline

- 🗂️ **Criação de Pasta**: Cria uma pasta baseada na semana da execução.
- 📥 **Extração de Dados**: Baixa os dados climáticos e salva:
  - `dados_brutos.csv` (todos os dados)
  - `temperaturas.csv` (dados de temperatura mínima, média e máxima)
  - `condicoes.csv` (descrição do clima e ícones)

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python
- 🎈 Apache Airflow
- 🐼 Pandas
- 🕰️ Pendulum
- 🌦️ Visual Crossing Weather API

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/vitaless7/pipeline_dados_climaticos.git
   cd pipeline_dados_climaticos
