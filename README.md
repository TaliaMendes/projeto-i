# Projeto de Data Warehouse(projeto-i)

O projeto corrente tem como principal objetivo implementar um data warehouse uilizando Python para realizar  o processo de extração , transformação e carga a partir de dados existentes em arquivos CSV e no banco de dados MongoDB, e realizar a persistência desses dados no PostgreSQL seguindo um modelo dimensional.

## Tecnologias Utilizadas
 - Python
 - Docker e Docker Compose
 - PostgreSQL
 - MongoDB

 ## Estrutura do Projeto

 - `docker-compose.yml`: Arquivo para configurar os servições necessários para criação do data wharehouse.(PostgreSQL,MOngoDB, e Python).
 - `Dockerfile`: Arquivo de configuração para criação da imagem python.
 - `etl_script.py`: Script Python responsável pelo processo de extração dos dados dos arquivos de origem, manipulação dos dados para a definição dos relacionamentos e a persistências desses dados no banco de destino(PostgreSQL).
 - `input/`: Diretório responsável por armazenar os arquivos CSV's de entrada.
 - `requirements.txt`: Arquivo com as dependeencias necessárias no script Python.

## Como Executar
- Instale o Docker
- Baixe o repositório na sua maquina
- Navegue até o diretório
- Execute o comando `dockre-compose up --build `
- Faça a conexao com o banco de dados PostgreSQL para visualizar os dados.

## Modelagem de Dados

A modelagem dimensional foi realizada criando as seguintes tabelas:

- Dimensões:
  - `dim_product`: Informações sobre produtos.
  - `dim_customer`: Informações sobre clientes.
  - `dim_payment`: Informações sobre pagamentos.
  - `dim_item`: Informações sobre itens de pedidos.
- Fatos:
  - `fact_order`: Informações sobre pedidos.
- Outras:
  - `order_reviews`: Informações sobre avaliações de pedidos.