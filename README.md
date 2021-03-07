# eldorado_challenge

Aplicação desenvolvida como resposta ao desafio proposto pelo Instituto Eldorado.

**Tecnologia utilizada na App:**
no front-end: Svelte com framework Sapper
no back-end: Node.js com Polka
Docker-Compose usando a image: node:latest

**Tecnologia utilizada na API:**
no back-end: Python com Flask
SGBD: PostgreSQL
Docker-Compose usando a image: postgres:latest e python:3.9.2

Desenvolvimento realizado no Windows 10 Home, com WSL2 executando Ubuntu 20.04.1 LTS 


## Funcionalidade 1: Cadastro de clientes
- Formulário reativo, com validação no front-end e no back-end.
- Endpoint: http://localhost:5000/costumer/
- Método: POST
- Retorna: o mesmo JSON acrescido de id e uuid
- Body JSON:
```json
{
    "id_city": 256,
    "id_genre": 1,
    "cpf": "14542774082",
    "full_name": "Lorrie Wasling",
    "birth_date": "1973-12-12",
    "phone_number": "(92) 98765-4321",
    "email": "lwaslingt@ucsd.edu",
    "address": "6 Butterfield Street",
    "postal_code": "69020160",
    "complement": "Parkway"
}
```
![Cadastro de clientes](https://raw.githubusercontent.com/guther/eldorado_challenge/main/img_doc/3.jpg  "Cadastro de clientes" )


## Funcionalidade 2: Cadastro de livros
- Formulário reativo, com validação no front-end e no back-end.
- Endpoint: http://localhost:5000/book/
- Retorna: o mesmo JSON acrescido de id
- Método: POST
- Body JSON:
```json
{
    "product_name": "Algebra Linear",
    "unit_price": 80.50
}
```
![Cadastro de livros](https://raw.githubusercontent.com/guther/eldorado_challenge/main/img_doc/2.jpg  "Cadastro de livros" )


## Funcionalidade 3: Registrar vendas
- A seleção dos clientes previamente cadastrados é realizada por busca por CPF em um selectbox reativo. Abordagem utilizada para evitar alto tráfego de dados. O selectbox dos médicos é hidratado no back-end e traz todos os médicos. Validação do formulário no front-end e no back-end.
- Endpoint: http://localhost:5000/sale/
- Retorna: o mesmo JSON acrescido de id e o valor atual do discount_percentage
- Método: POST
- Body JSON:
```json
{
    "id_costumer": 2,
    "products": [
        {
            "id_product": 2,
            "quantity": 3
        },
        {
            "id_product": 3,
            "quantity": 1
        },
        {
            "id_product": 4,
            "quantity": 2
        }
    ]
}
```

## Funcionalidade 4: Recuperar informações de clientes
Existem 03 tipos de recuperação de informação de cliente, sendo eles:
1. **Recuperar todos os registros**
   - Endpoint: http://localhost:5000/costumer/
   - Retorna: JSON com todos os registros de clientes
   - Método: GET
2. **Recuperar um registro, buscando pelo id**
   - Endpoint: http://localhost:5000/costumer/5
   - Retorna: JSON com o registro do cliente de id igual a 5
   - Método: GET
![Recuperar informações de clientes](https://raw.githubusercontent.com/guther/eldorado_challenge/main/img_doc/4.jpg  "Recuperar informações de clientes" )
3. **Recuperar um registro, buscando por parte do cpf**
   - Endpoint: http://localhost:5000/costumer/?field=cpf&val=722
   - Retorna: JSON com todos os registros dos cliente de CPF iniciado por 722
   - Método: GET
   
## Funcionalidade 5: Recuperar informações de livros
Existem 02 tipos de recuperação de informação de livros cadastrados, sendo eles:
1. **Recuperar todos os registros**
   - Endpoint: http://localhost:5000/book/
   - Retorna: JSON com todos os registros de livros
   - Método: GET
2. **Recuperar um registro, buscando pelo id**
   - Endpoint: http://localhost:5000/book/3
   - Retorna: JSON com o registro do livro de id igual a 3
   - Método: GET

## Funcionalidade 6: Recuperar informações de vendas
Existem 02 tipos de recuperação de informação de vendas cadastradas, sendo eles:
1. **Recuperar todos os registros**
   - Endpoint: http://localhost:5000/sale/
   - Retorna: JSON com todos os registros de vendas
   - Método: GET
2. **Recuperar um registro, buscando pelo id**
   - Endpoint: http://localhost:5000/sale/8
   - Retorna: JSON com o registro da venda de id igual a 8
   - Método: GET
   - 
## Funcionalidade 7: Um cliente pode comprar no máximo até 10 livros **`diferentes`** por venda realizada
Essa restrição foi implementada no/na:
- API: os dados passam por uma rotina de validação que impõe a restrição. Essa rotina organiza os dados e une dados de um mesmo produto, garantindo que somente diferentes livros serão contabilizados, ou seja:
   - Este JSON abaixo será tratado como a venda de 04 unidades de um mesmo livro de id 2.
```json
{
    "id_costumer": 2,
    "products": [
        {
            "id_product": 2,
            "quantity": 3
        },
        {
            "id_product": 2,
            "quantity": 1
        }
    ]
}
```
![Restrição de limite de livros por venda](https://raw.githubusercontent.com/guther/eldorado_challenge/main/img_doc/1.jpg  "Restrição de limite de livros por venda" )

- Banco de Dados: uma trigger `check_max_products_on_sales()` avalia as inserções de venda na base de dados antes que elas ocorram. Então, a restrição não está apenas sendo garantida pela aplicação, e mesmo que um INSERT seja executado diretamente na base, via SGBD, é preciso que a restrição seja obedecida. 
![Restrição de limite de livros por venda](https://raw.githubusercontent.com/guther/eldorado_challenge/main/img_doc/5.jpg  "Restrição de limite de livros por venda" )


## Funcionalidade 8: Dar ao cliente um desconto com base no valor total das vendas anteriores que ele já fez 
Foi criada uma função `order_discount(id_costumer)` no banco de dados para facilitar o cálculo de desconto. O desconto é realizado seguindo as regras propostas no desafio. É possível visualizar o desconto sendo aplicado durante um registro de venda na aplicação http://localhost:3000/.


## Como Iniciar a Aplicação

Entre no diretório `eldorado_web_challenge` e execute o comando:
$ docker-compose up

Ao final do comando, você verá:

```
api_container |  * Serving Flask app "server" (lazy loading)
api_container |  * Environment: production
api_container |    WARNING: This is a development server. Do not use it in a production deployment.
api_container |    Use a production WSGI server instead.
api_container |  * Debug mode: on
api_container |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
api_container |  * Restarting with stat
api_container |  * Debugger is active!
api_container |  * Debugger PIN: 131-979-641
```

Então já pode acessar a aplicação no endereço http://localhost:3000 e testar as funcionalidades.

## Modelo ER do Bando de Dados

![Modelo ER do Bando de Dados](https://raw.githubusercontent.com/guther/eldorado_challenge/main/app/db/db_schema.jpg "Modelo ER do Bando de Dados")


