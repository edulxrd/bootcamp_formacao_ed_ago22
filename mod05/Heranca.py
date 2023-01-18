import datetime
import math
##
##class Pessoa:
##    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
##        self.nome = nome
##        self.sobrenome = sobrenome
##        self.data_de_nascimento = data_de_nascimento
##
##    @property
##    def idade(self) -> int:
##        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
##
##    def __str__(self) -> str:
##        return f"{self.nome} {self.sobrenome} tem {self.idade} anos!"
##
##class curriculo:
##    def __init__(self, pessoa: Pessoa, experiencias: list[str]):
##        self.pessoa = pessoa
##        self.experiencias = experiencias
##
##    @property
##    def quantidade_de_experiencias(self) -> int:
##        return len(self.experiencias)
##
##    #Propriedade para pegar a ultima experiencia, [-1]
##    @property 
##    def ultima_experiencia(self) -> str:
##        return self.experiencias[-1]
##
##    def adiciona_experiencia(self, experiencia: str) -> None:
##        self.experiencias.append(experiencia)
##
##    def __str__ (self):
##        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já" \
##               f"trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha na empresa {self.ultima_experiencia}"
##               
##eduardo = Pessoa(nome='Eduardo', sobrenome='Jesus', data_de_nascimento=datetime.date(2002, 4, 29))
##
##
##curriculo_eduardo = curriculo(
##    pessoa = eduardo, 
##    experiencias=['Bold', 'Cadoro', 'Casai']
##)
##    
##print(curriculo_eduardo)
##curriculo_eduardo.adiciona_experiencia("Totvs")
##print(curriculo_eduardo)

class vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez um ruido: {ruido}")

class pessoa_herenca(vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos!"

    def fala(self, frase: str):
        return self.emite_ruido(frase)

## classe super é para quando eu rodar o inicializador eu vou receber nome e data do cachorro, porem
## Primeiro vou chamar a classe vivente, classe mãe
## Não precisei colocar a propriedade de idade, porque utilizei a classe heranca(vivente
class cachorro(vivente):
    def __init__ (self, nome: str, raca: str, data_de_nascimento: datetime.date) -> str:
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def __str__(self) -> str:
        return f"{self.nome} é da raça {self.raca} tem {self.idade} anos!"

    def late(self):
        return self.emite_ruido('Au! Au!')

thor = cachorro(nome='Thor', raca='Lhasa', data_de_nascimento=datetime.date(2020, 10, 10))
print(thor)

eduardo2 = pessoa_herenca(nome='eduardo', data_de_nascimento=datetime.date(2002, 4 , 29))
print(eduardo2)

thor.late()
eduardo2.fala("Cala a boca!")
