from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto



class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser cadastrado no estoque deve ser representado
    """
    modelo: str = "Disjuntor 2P 40A curva C"
    fabricante: str = "Schneider"
    quantidade: Optional[int] = 7
    valor: float = 49.82


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por produtos no estoque. 
    Que será feita apenas com base no modelo.
    """
    produto_id: int = 1


class ListagemProdutosSchema(BaseModel):
    """ Define como a lista produtos cadastrados no estoque será apresentada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto cadastrado no estoque seguindo o schema definido em 
    ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "modelo": produto.modelo,
            "fabricante": produto.fabricante,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado:
    """
    id: int = 1
    nome: str = "Disjuntor 2P 40A curva C"
    fabricante: str = "Schneider"
    quantidade: Optional[int] = 7
    valor: float = 49.82
    

class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de um produto do estoque.
    """
    mesage: str
    modelo: str

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto cadastrado no estoque seguindo o 
        schema definido em ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "modelo": produto.modelo,
        "fabricante": produto.fabricante,
        "quantidade": produto.quantidade,
        "valor": produto.valor
    }
