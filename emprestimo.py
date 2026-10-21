
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
        self.__registro = registro
        self.__nome = nome

    @property #encapsulamento
    def registro(self):
        return self.__registro

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def categoria(self):
        pass
    

    @abstractmethod
    def limites_emprestimos(self):
        pass

    def __str__(self):
        return f'Nome:{self.nome} - Categoria:{self.categoria()} - Limites de itens emprestados:{self.limites_emprestimos()}'
    
class Aluno(Pessoa):
    def categoria(self):
        return "Aluno"
        
    def limites_emprestimos(self):
        return 2
        
class Servidor(Pessoa):
    def categoria(self):
        return "Servidor"
    
    def limites_emprestimos(self):
        return 4

class RegrasEmprestimo:

    def listar_regras(self):
        aluno = Aluno("0", "exemplo") # o 0 vai para o registro e o exemplo para um nome 
        servidor = Servidor("0", "exemplo") #evitar escrever 2 e 4

        linhas = ["\nREGRAS DE EMPRÉSTIMO:"]

        linhas.append(f"Aluno: até {aluno.limites_emprestimos()} itens ao mesmo tempo")
        linhas.append(f"Servidor: até {servidor.limites_emprestimos()} itens ao mesmo tempo")
        linhas.append("Tempo limite de empréstimo:\n -Bolas e coletes até o fim do dia\n -Raquetes até 2 dias\n -Bicicletas até 7 dias (com vistoria na devolução - pneu, freio e corrente)")
        linhas.append("Atraso na devolução: caso haja atraso, a pessoa será bloqueado por 1 dia para cada dia de atraso")
        return "\n".join(linhas)

    def pode_emprestar(self, pessoa, equipamento, quantidadeAtual):
        if not equipamento.disponibilidade:
            return False, "Equipamento indisponível"
        if quantidadeAtual >= pessoa.limites_emprestimos():
            return False, "Já atingiu o limite de empréstimos"
        return True, "Empréstimo permitido"

#CLASSES DE COMPORTAMENTO

class ControleEmprestimo:

    def __init__(self):
        self.__pessoas = {}
        self.equipamentos = {}

    def cadastrar_pessoa(self, pessoa):
        if pessoa.registro in self.__pessoas:
            raise ValueError("Esse registro já está cadastrado")
        self.__pessoas[pessoa.registro] = pessoa

    def cadastrar_equipamento(self, equipamento):
        if equipamento.identificacao in self.equipamento:
            raise ValueError("Esse registro já está cadastrado")
        
        self.equipamentos[equipamento.identificacao] = equipamento
            

    def emprestar(self):
        pass

    def devolver(self):
        pass
    
class PainelEmprestimo:
    pass


class MenuEmprestimo:
    pass

def cadastro(controle_cadastros):
   print("Cadastro para o empréstimo de equipamentos\n")
   opcao = int(input("Digite sua categoria:\n1 - Aluno\n2 - Servidor\n"))
  
   if opcao != 1 and opcao != 2:
       print("Opção Inválida!")
       return


   nome = input("Digite seu nome: ")
   registro = input("Digite seu registro: ")
  
   match opcao:
       case 1:
        pessoa = Aluno(registro, nome)
       case 2:
        pessoa = Servidor(registro, nome)
       case _:
        print("Erro inesperado!")
        
   controle_cadastros.cadastrar_pessoa(pessoa)
   
   print("Cadastro Concluído\n")
   print(pessoa)

def cadastro_equipamentos(controle_equipamentos):
    print("Cadastros de novos equipamentos\n")
    
    nome = input("Digite o nome do equipamento: ")
    identificacao = int(input("Digite o código de identificação"))

    novo_equipamento = Equipamento(nome, identificacao, True)    
    
    controle_equipamentos.cadastrar_equipamento(novo_equipamento)
    
    print("Cadastro concluído\n")
    print(novo_equipamento)
        
            


if __name__ == "__main__":
    bola = Equipamento("Bola de vôlei", 3)
    controle_cadastros = ControleEmprestimo()
    cadastro(controle_cadastros)


