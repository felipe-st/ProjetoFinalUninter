Projeto Final Uninter
Projeto básico do backend de sistema de gestão hospitalar
___________________________________________________________________________________________________________________________________________________________________________________________________________________

Tecnologias utlizadas:
Python (FastApi, SQLAlchemy);
PostgreSQL
___________________________________________________________________________________________________________________________________________________________________________________________________________________
Como utilizar:
Criar o ambiente e instalar as dependências do projeto, que encontram-se em requirements.txt;
No arquivo core.configs, preencha DB_URL com os dados do seu banco de dados, seguindo o exemplo e de acordo com a documentação do SQLAlchemy: str = "'postgresql+asyncpg://postgres:suasenha@localhost:5432/uninter'";
Ainda no arquivo core.configs preencha JWT_SECRET com um token que servirá de segredo para as senhas geradas na aplicação. Você pode utilizar a biblioteca "secrets" do próprio python assim:
no terminal: python 
import secrets
token: str = secrets.token_urlsafe(32)
token
O token gerado dever ser algo parecido com isso: 'JlcfqOq6_PP7j1L5DyUMqxAfB5ZQZ6_YWKIFYRvPdxA';
Execute o arquivo criar_tabelas.py. Se tudo correr bem, você terá criado a tabela no seu banco de dados com as columns para dados de paciente;
Execute o main.py;
Com o servidor sendo executado você já pode executar as operações básicas de crud. Acesse localhost:8000/docs para obter a documentação básica da API, com Swagger. É possível criar usuários, realizar login, cadastrar, editar e apagar pacientes;
Fiquem à vontade para aperfeiçoar a aplicação, bem como utiliza-la como base para criação de um front-end.
