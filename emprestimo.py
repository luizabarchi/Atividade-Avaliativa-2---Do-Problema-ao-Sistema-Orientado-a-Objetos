
#Atividade AValiativa 2: Do Problema ao Sistema Orientado a Objetos
# Classes de dados: Equipamentos, Pessoa (Aluno/Servidor) e Regras
# Classes de comportamento: Controle, Painel e Empréstimo

from abc import ABC, abstractmethod
from datetime import date, timedelta

#CLASSES DE DADOS

class Equipamento:

    def __init__ (self, nome, identificacao, disponibilidade=True):
        self.nome = nome
        self.identificacao = identificacao
        self.disponibilidade = disponibilidade

    def __str__ (self):
            estado = "Disponível" if self.disponibilidade else "Emprestado"
            return f"Equipamento: {self.nome}, código: {self.identificacao}, Situação: {estado}"

    def emprestar(self):
        if not self.disponibilidade:
            return False 
        self.disponibilidade = False
        return True

    def devolver(self):
        if self.disponibilidade:
            return False
        self.disponibilidade = True 
        return True


class Pessoa(ABC):
    def __init__(self, registro, nome):
        self.registro = registro
        self.nome = nome

    @property #encapsulamento
    def registro(self):
        return self.registro

    @property
    def nome(self):
        return self.nome

    @abstractmethod
    def categoria(self):
        pass
    

    @abstractmethod
    def limites_emprestimos(self):
        pass

    def __str__(self):
        return f'Nome:{self.nome} - Categoria:{self.categoria()} - Limites de itens emprestados:{self.limites_emprestimos()}'


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

