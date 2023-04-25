# api-web-scraping
Esta API destina-se a coleta de dados de notebooks via scraping e gestão dos dados coletados.
## Montar o app

1. Para executar o projeto é necessário clonar o repositório `git clone https://github.com/lacerdarenato/API-Python-scrapping.git` dentro do diretório em deseja instalá-lo.
2. Instale as dependências contidas no arquivo requirements.txt através do comando `pip install -r requirements.txt`
3. Iniciar a aplicação executando o comando `python app.py` no diretório onde o projeto foi clonado
4. Para conferir se a API está executando e tambem montar o banco, execute uma requisição na API que roda na rota `http://127.0.0.1:5000/`. Caso esteja tudo ok aparecerá a mensagem: `API Funcionando` e a estrutura do banco estará montada
5. Para ter acesso aos recursos da API é necessário criar um usuário comum fazendo uma requisição POST através da rota `http://127.0.0.1:5000/signup` ou usuário com direito de administrador através da rota `http://127.0.0.1:5000/admin` em ambas é preciso informar o seguinte corpo na requisição:
    Exemplo de Json:

        ```json
        "name": "exemplo",
        "email": "exemplo@email.com",
        "password": "digite_sua_senha"
        ```
6. Com o usuário criado efetue um login através da rota `http://127.0.0.1:5000/login` essa rota lhe devolverá um token Bearer que será utilizado em em todos os recursos que precisam de autenticação.
7. Para executar o webscrap através da API execute uma requisição GET na rota `http://127.0.0.1:5000/scrap`
8. As coleções usadas nos testes estão na pasta `./postman` na raiz do projeto.
