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
  - Acesse as urls da api por 127.0.0.1:8000/adm/. 
   Será necessário criar ao menos 1 cliente, 1 vendedor e 1 produto_servico, para posteriormente usar o front de realizar venda.
 
  ## Exemplos de json para usar no modo Post :
      # Produto (http://localhost:8000/adm/produto_servico/)
      {
        "descricao": "Tênis Adidas",
        "codigo_barras": 221,
        "preco_unitario": "200.00",
        "comissao": "4.00"
      }
     # Vendedor (http://localhost:8000/adm/vendedor/)
     {
      "nome": "Luciano Kane",
      "telefone": "2798635680"
     }
     # Cliente (http://localhost:8000/adm/cliente/)
     {
       "nome": "Philipe Lahn",
       "telefone": "2798638970"
     }

  - Com esse projeto em modo runserver, agora deve-se instalar o projeto frontend angular no repositório: https://github.com/marcosafonso/caixa_livre ;
  Após configurar o projeto angular caixa_livre, deixe rodando com ng_serve, acessando localhost:4200/venda para usar o front.
  
  
## Todas as Urls disponíveis na API são:
    "produto_servico": "http://localhost:8000/adm/produto_servico/",
    "vendedor": "http://localhost:8000/adm/vendedor/",
    "cliente": "http://localhost:8000/adm/cliente/",
    "venda": "http://localhost:8000/adm/venda/",
    "lista_venda": "http://localhost:8000/adm/lista_venda/",
    "item_venda": "http://localhost:8000/adm/lista_item_venda/",
    "lista_item_venda": "http://localhost:8000/adm/lista_item_venda/"

# Urls de consultas solicitadas:
1 - Dado um intervalo de tempo, quanto de comissão um vendedor tem direito?
        Ir na Url: 127.0.0.1:8000/adm/pesquisa_comissao_vendedor
        Exemplo de json de requisicao: 
        {
            "data_inicio": "10/02/2021",
            "data_fim": "14/02/2021",
            "vendedor": "2798635640" # pesquisado pelo telefone vendedor.
        }

# 2 - Quais produtos e serviços um determinado cliente comprou num intervalo de tempo?
        Ir na Url: 127.0.0.1:8000/adm/pesquisa_compras_cliente
        {
            "data_inicio": "10/02/2021",
            "data_fim": "14/02/2021",
            "cliente": "33280968" # usado telefone para pesquisar cliente.
        }

# 3. Quais os produtos e serviços mais vendidos num dado intervalo de datas? Listar em ordem decrescente
        Ir Url: 127.0.0.1:8000/adm/pesquisa_mais_vendidos
        Exemplo do json de requisição dos produtos mais vendidos: 
        {
           "data_inicio": "10/02/2021",
           "data_fim": "14/02/2021"
        }

