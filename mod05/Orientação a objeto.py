
import datetime
import math
#%%
# __init__ = inicializador da classe, ele é executado toda vez que vc instaciar uma classe 
# self.nome = nome significa que a pessoa vai ter um atributo chamado nome e que vai receber o valor que está no inicializador
# @property = atributos derivados, coisas que não altera. Uma propriedade.
# def __stf__(self) -> str: definir uma string
class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos!"

Eduardo = Pessoa(nome='Eduardo', sobrenome='Jesus', data_de_nascimento=datetime.date(2002, 4, 29))

print (Eduardo)
print (Eduardo.nome)
print (Eduardo.sobrenome)
print (Eduardo.idade)


