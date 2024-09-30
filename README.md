# File Api

## Descrição
O objetivo foi criar uma `api` para processamento de arquivos CSVs de cobranças. O foco principal é que o processamento fosse independente e ocorresse de abaixo dos 60s.

## Tecnologias
- Python
- Django
- Django Rest Framework
- Postgres
- Docker
- Docker Compose

## Como rodar
1. Clone o repositório
2. Entre na pasta do projeto
3. Execute o comando `docker-compose up -d --build` para subir os containers do projeto
4. Execute o comando `docker-compose exec web python manage.py migrate` para rodar as migrações
5. Utilize o arquivo `client.py` para fazer uma requisição para a api. O comando retorna o tempo da requisição.
Lembre-se que para executar o comando é necessário criar uma virtualenv e instalar as dependências do arquivo `requirements.txt`. `python -m venv venv`, ative a venv com `source venv/bin/activate` e `pip install -r requirements.txt`.
6. Para rodar os testes execute o comando `docker-compose exec web python manage.py test`