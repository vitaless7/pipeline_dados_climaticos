from airflow import DAG
import pendulum
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add # Embora importado, não é usado na função extrai_dados
import os
import pandas as pd
from datetime import datetime, timedelta

with DAG(
    'dados_climaticos',
    start_date=pendulum.datetime(2025, 3, 31, tz='UTC'),
    schedule_interval='0 0 * * 1',  # toda segunda-feira
    catchup=False,
) as dag:

    tarefa_1 = BashOperator(
        task_id='cria_pasta',
        bash_command='mkdir -p "/home/vitaless/Documentos/airflowalura/semana={{ data_interval_end.strftime("%Y-%m-%d") }}"'
    )

    def extrai_dados(data_interval_end):
        # data_interval_end é passado como uma STRING pelo Airflow via op_kwargs
        city = 'Boston'
        key = '8GVJSDTBA9LBT44JXM5Q4XZSL'

        # CONVERTE a string data_interval_end para um objeto datetime
        # Usamos fromisoformat() que lida com o formato ISO 8601 (incluindo tempo e fuso horário)
        try:
            data_interval_end_dt = datetime.fromisoformat(data_interval_end)
        except ValueError as e:
            print(f"Error parsing data_interval_end string: {e}")
            print(f"String received: {data_interval_end}")
            raise # Re-lança a exceção se o parsing falhar

        # Calcula a data de 7 dias depois usando timedelta com o objeto datetime
        end_date_dt = data_interval_end_dt + timedelta(days=7)

        # Formata as datas para a URL (agora a partir dos objetos datetime)
        start_date_str = data_interval_end_dt.strftime("%Y-%m-%d")
        end_date_str = end_date_dt.strftime("%Y-%m-%d")

        URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date_str}/{end_date_str}?unitGroup=metric&include=days&key={key}&contentType=csv'

        print(f"Fetching data from URL: {URL}") # Adicionado para debug

        try:
            dados = pd.read_csv(URL)
        except Exception as e:
            print(f"Error fetching data from URL: {e}")
            raise # Re-lança a exceção para que o Airflow marque a task como falha

        # Cria o caminho do arquivo usando a data formatada
        file_path = f'/home/vitaless/Documentos/airflowalura/semana={start_date_str}'
        os.makedirs(file_path, exist_ok=True)

        # Salva os dados em arquivos CSV
        dados.to_csv(os.path.join(file_path, 'dados_brutos.csv'), index=False)
        dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(os.path.join(file_path, 'temperaturas.csv'), index=False)
        dados[['datetime', 'description', 'icon']].to_csv(os.path.join(file_path, 'condicoes.csv'), index=False)

        print(f"Data successfully saved to {file_path}") # Adicionado para debug


    tarefa_2 = PythonOperator(
        task_id='extrai_dados',
        python_callable=extrai_dados,
        # Passa data_interval_end como STRING (o Airflow faz a renderização Jinja)
        op_kwargs={'data_interval_end': '{{ data_interval_end }}'}
    )

    tarefa_1 >> tarefa_2
