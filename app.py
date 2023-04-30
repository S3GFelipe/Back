from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from model import Session, Produto
from schemas import *


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos no estoque")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto no estoque

    Retorna uma representação dos produtos associados.
    """
    produto = Produto(
        modelo=form.modelo,
        fabricante=form.fabricante,
        quantidade=form.quantidade,
        valor=form.valor)

    try:
        # Conexão criada com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # Comando de adicionar um novo produto na tabela
        session.commit()
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # Para produtos de mesmo modelo sendo cadastrados no estoque, temos o IntegrityError:
        error_msg = "Produto de mesmo modelo já salvo na base!!!"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # Para erros não previstos, temos a seguinte mensagem:
        error_msg = "Não foi possível salvar novo item!!!"
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados no estoque

    Apresenta a lista de produtos presentes no estoque.
    """
    # Cria a conexão com a base
    session = Session()
    # Realiza a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # Caso não haja produtos cadastrados no estoque
        return {"produtos": []}, 200
    else:
        # Caso haja produtos retorna a representação dos mesmos
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Realiza a busca por um Produto através do seu ID

    Retorna com a representação dos produtos associados.
    """
    produto_id = query.produto_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não cadastrado no estoque!!!"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Remove um Produto do estoque a partir do seu ID

    Uma mensagem para confirmar a remoção aparece em seguida.
    """
    produto_id = query.produto_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.id == produto_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Produto removido", "ID": produto_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não cadastrado no estoque!!!"
        return {"mesage": error_msg}, 404
    

