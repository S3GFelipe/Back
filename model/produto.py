from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    modelo = Column(String(140), unique=True)
    fabricante = Column(String(140), unique =False)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, modelo:str, fabricante:str, quantidade:int, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Adiciona um Produto

        Padrão:
            modelo: modelo do produto
            fabricante: fabricante do produto
            quantidade: quantidade do produto que será armazenada no estoque
            valor: valor de compra do produto adicionado
            data_insercao: data de quando o produto foi adicionado no estoque
        """
        self.modelo = modelo
        self.fabricante = fabricante
        self.quantidade = quantidade
        self.valor = valor

        # Se a data não for inserida, será a data do momento em que o produto foi adicionado
        if data_insercao:
            self.data_insercao = data_insercao

