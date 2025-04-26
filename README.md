# ☁️ Dados Climáticos com Apache Airflow

Este projeto utiliza Apache Airflow para automatizar a extração de dados climáticos da API do Visual Crossing e salvá-los em arquivos CSV. O DAG é configurado para rodar semanalmente, buscando dados para um período de 7 dias.

## 📋 Pré-requisitos

Para rodar este DAG, você precisará ter instalado e configurado o seguinte ambiente:

* **Apache Airflow:** A plataforma utilizada para orquestrar o fluxo de trabalho.
* **Python 3.x:** A linguagem de programação na qual o DAG foi escrito.
* **Bibliotecas Python:** As dependências do projeto, especificadas no arquivo `dados_climaticos.py`. As principais são:
    * `pendulum`
    * `apache-airflow`
    * `pandas`
    * `requests`
* **Chave de API do Visual Crossing:** Você precisará obter uma chave de API gratuita ou paga no site do Visual Crossing ([https://www.visualcrossing.com/](https://www.visualcrossing.com/)) para acessar os dados climáticos.

## ⚙️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/vitaless7/pipeline_dados_climaticos.git
   cd pipeline_dados_climaticos

2.  **Instale as dependências do Python:** Navegue até o diretório do projeto e instale as bibliotecas necessárias. É altamente recomendável usar um ambiente virtual (`venv` ou `conda`).

    ```bash
    pip install pendulum apache-airflow pandas requests
    ```

    *(Note: `apache-airflow` pode exigir dependências adicionais dependendo da sua configuração. Consulte a documentação oficial do Airflow para mais detalhes.)*

3.  **Configure o Airflow:**

    * Copie o arquivo `dados_climaticos.py` para o diretório `dags` configurado no seu ambiente Airflow.

4.  **Configure a Chave de API do Visual Crossing:**

    * Abra o arquivo `dados_climaticos.py`.
    * Localize a linha que define a variável `key` dentro da função `extrai_dados`.
    * Substitua o valor placeholder pela sua chave de API do Visual Crossing.

    ```python
    key = 'SUA_CHAVE_AQUI' # Substitua SUA_CHAVE_AQUI pela sua chave real
    ```

    * **Alternativa (Recomendado para produção):** Considere armazenar sua chave de API como uma Connection ou Variable no Airflow para maior segurança, em vez de deixá-la diretamente no código do DAG.

## ▶️ Como Rodar

Este DAG é gerenciado e executado pelo Apache Airflow.

1.  **Inicie o Airflow:** Inicie o webserver e o scheduler do Airflow.

    ```bash
    airflow webserver -p 8080
    airflow scheduler
    ```

    *(O comando para iniciar pode variar dependendo da sua instalação do Airflow.)*

2.  **Acesse a UI do Airflow:** Abra seu navegador e acesse a interface web do Airflow (geralmente em `http://localhost:8080`).

3.  **Encontre o DAG:** Na lista de DAGs, procure por `dados_climaticos`.

4.  **Habilite o DAG:** Clique no botão de toggle para habilitar o DAG.

5.  **Execução Automática:** O DAG está configurado com um `schedule_interval='0 0 * * 1'`, o que significa que ele será executado automaticamente toda segunda-feira à meia-noite (UTC, conforme definido no `start_date`).

6.  **Execução Manual (Opcional):** Você pode acionar o DAG manualmente clicando no botão "Trigger DAG" na UI do Airflow. Ao acionar manualmente, o Airflow utilizará a `start_date` e o `data_interval_end` para determinar o período de execução.

## 📁 Estrutura de Arquivos de Saída

O DAG criará pastas e salvará os arquivos CSV no seguinte formato:
 1. └── semana=YYYY-MM-DD/
 2. ├── dados_brutos.csv
 3. ├── temperaturas.csv
 4. └── condicoes.csv<br>
Onde `YYYY-MM-DD` representa a data de início do intervalo de 7 dias para o qual os dados foram extraídos (correspondente ao `data_interval_end` da execução do DAG).

* `dados_brutos.csv`: Contém todos os dados retornados pela API do Visual Crossing para o período.
* `temperaturas.csv`: Contém as colunas `datetime`, `tempmin`, `temp` e `tempmax`.
* `condicoes.csv`: Contém as colunas `datetime`, `description` e `icon`.

## ⚠️ Possíveis Problemas e Soluções

* **Erro na Chave de API:** Verifique se a chave de API no arquivo `dados_climaticos.py` (ou na Connection/Variable do Airflow) está correta.
* **Problemas de Permissão:** Certifique-se de que o usuário que executa o worker do Airflow tenha permissão para criar diretórios e arquivos no caminho especificado (`/home/vitaless/Documentos/airflowalura/`).
* **Falha na Conexão com a API:** Verifique sua conexão com a internet e se o serviço do Visual Crossing está disponível. A função `extrai_dados` inclui tratamento de erro básico para falhas na requisição.
* **Formato de Data:** O DAG utiliza `data_interval_end` fornecido pelo Airflow. A função `extrai_dados` tenta converter esta string para um objeto `datetime`. Erros de formato podem ocorrer se o Airflow ou a configuração de data/hora do sistema não estiverem corretos.
* **`ModuleNotFoundError`:** Certifique-se de que todas as bibliotecas Python necessárias foram instaladas no ambiente onde o Airflow worker está sendo executado.

---

