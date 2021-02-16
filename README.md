# Projeto Venda - Projeto de Backend com PostGres e Django Rest;


***Pré-requisitos
* Django 2 ou superior.
* Postgres ou semelhante SGBD.
* Pip
* Desejável usar virtualenv

## Instruções de instalaçao e execução:

# Clonar este repositório com git clone <urldorepositorio>.
  
## Baixar dependências:
  - Preferencialmente, Crie uma virtualenv para instalar os requisitos desse projeto:
  - Abra um terminal/cmd e ative sua virtualenv.
  - Na pasta raiz do projeto, rode o comando " pip install -r requirements.txt ".
  - Altere nos settings.py os dados de Database para usar suas credenciais de acesso ao banco ( aqui foi usado Postgres).
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'vendasdb',
          'USER': 'SEU_USER',
          'PASSWORD': 'SEU_PASSWORD',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  - E então, crie um novo Database vazio no Postgre Admin, com o nome vendasdb.
  - Volte ao terminal/cmd, e rode o comando " python manage.py migrate" para criar as tabelas do banco.
  - Acesse as urls da api por 127.0.0.1:8000/adm/
  - Para preencher dados de test, Abra o arquivo Dados_api.txt que está na raíz desse projeto, onde você terá dados para cadastrar Vendedor, Cliente e ProdutoServico para preencher o banco e ter dados básicos para realizar vendas. Exemplo: Pegue o json de cadastro de produtos em dados_api.txt, acesse http://127.0.0.1:8000/adm/produto_servico/ e entre na opçao "Raw Data", cole esse json e aperte o botão Post para cadastrar os dados.
  


