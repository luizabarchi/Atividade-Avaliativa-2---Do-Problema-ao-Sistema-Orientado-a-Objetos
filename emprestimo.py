
#Atividade AValiativa 2: Do Problema ao Sistema Orientado a Objetos
# Classes de dados: Equipamentos, Pessoa (Aluno/Servidor) e Regras
# Classes de comportamento: Controle, Painel e Empréstimo

from abc import ABC, abstractmethod
from datetime import date, timedelta

#CLASSES DE DADOS

class Equipamento:

    def __init__ (self, nome, identificacao, disponibilidade):
        self.nome = nome
        self.identificacao = identificacao
        self.disponibilidade = disponibilidade

    def __str__ (self):
        return f"Equipamento {self.nome}, código {self.identificacao}, Disponível {self.disponibilidade}"

class Pessoa(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def limite_emprestimos(self):
        pass

class Aluno(Pessoa):
    pass

class Servidor(Pessoa):
    pass

class RegrasEmprestimo:

    def __init__(self, prazo, quantidadeMax, cuidados):
        self.prazo = prazo
        self.quantidadeMax = quantidadeMax
        self.cuidados = cuidados 

    def listar_regras(self):
        pass

#CLASSES DE COMPORTAMENTO



if __name__ == "__main__":
    bola = Equipamento("Bola de vôlei", 3, True)
    print(bola)

