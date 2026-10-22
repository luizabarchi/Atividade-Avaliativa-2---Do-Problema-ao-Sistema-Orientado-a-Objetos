
#Atividade Avaliativa 2: Do Problema ao Sistema Orientado a Objetos
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

    def calcular_limite_data(self, equipamento):
        nome = equipamento.nome.lower() #evita erro de letra maiúscula
        if "bicicleta" in nome:
            dias = 7
        elif "raquete" in nome:
            dias = 2
        else:
            dias = 0
        return date.today() + timedelta(days=dias) #calcula o dia que deverá ser entregue

class Emprestimo:
    def __init__(self, pessoa, equipamento, data_limite):
        self.__pessoa = pessoa
        self.__equipamento = equipamento
        self.__data_limite = data_limite
        self.__data_devolucao = None #Ao realizar o empréstimo, a pessoa aind anão devolveu

    @property
    def pessoa (self):
        return self.__pessoa

    @property
    def equipamento(self):
        return self.__equipamento

    @property
    def data_limite(self):
        return self.__data_limite

    @property 
    def data_devolucao(self):
        return self.__data_devolucao

    def esta_ativo(self):
        return self.__data_devolucao is None

    def registrar_devolucao(self, data=None):
        if not self.esta_ativo():
            return False #nesse caso já tinha sido devolvido
        self.__data_devolucao = data if data else date.today()
        return True #nesse caso ainda não houve devolução  

#CLASSES DE COMPORTAMENTO

class ControleEmprestimo:

    def __init__(self):
        self.__pessoas = {}
        self.__equipamento = {}
        self.__emprestimos = []
        self.__bloqueios = {}
        self.__regras = RegrasEmprestimo()

    def cadastrar_pessoa(self, pessoa):
        if pessoa.registro in self.__pessoas:
            raise ValueError("Esse registro já está cadastrado")
        self.__pessoas[pessoa.registro] = pessoa

    def cadastrar_equipamento(self, equipamento):
        if equipamento.identificacao in self.__equipamento:
            raise ValueError("Esse código de registro já está cadastrado")
        
        self.__equipamento[equipamento.identificacao] = equipamento        

    def listar_equipamento(self):
        return list(self.__equipamento.values())

    def listar_emprestimos(self):
        return list(self.__emprestimos)
    
    def emprestar(self, registro, codigo):
        if registro not in self.__pessoas:
            raise ValueError("Pessoa não cadastrada")
        if codigo not in self.__equipamento:
            raise ValueError("Equipamento não cadastrado")

        pessoa = self.__pessoas[registro]
        equipamento = self.__equipamento[codigo]

    def devolver(self):
        pass
    
class PainelEmprestimo:

    def __init__(self, controle):
        self._controle = controle

    def equipamento_disponiveis(self):
        linhas = ["\nEQUIPAMENTOS DISPONÍVEIS:"]

        for equipamento in self._controle.listar_equipamento():
            if equipamento.disponibilidade:
                linhas.append(str(equipamento))

        if len(linhas) == 1:
            linhas.append("Nenhum equipamento disponível no momento\n")

        return "\n".join(linhas)

    def emprestimos_ativos(self):
        linhas = ["\nEMPRÉSTIMOS ATIVOS:"]
        for emprestimo in self._controle.listar_emprestimos():
            if emprestimo.esta_ativo():
               linhas.append(f"{emprestimo.equipamento.nome}, com {emprestimo.pessoa.nome}, até {emprestimo.data_limite.strftime('%d/%m')}")
        if len(linhas) == 1:
            linhas.append("Nenhum empréstimo ativo no momento")
        return "\n".join(linhas)

    def historico_equipamento(self, codigo):
        linhas = [f"\nHISTÓRICO DO EQUIPAMENTO {codigo}:"]
        for emprestimo in self._controle.listar_emprestimos():
            if emprestimo.equipamento.identificacao == codigo:
                if emprestimo.data_devolucao is None:
                    situacao = "ainda emprestado"
                else:
                    situacao = f"devolvido em {emprestimo.data_devolucao.strftime('%d/%m')}"
                linhas.append(f"{emprestimo.pessoa.nome}: {situacao}")

        if len(linhas) == 1:
            linhas.append("Nenhum empréstimo registrado para esse equipamento")
        return "\n".join(linhas)

class MenuEmprestimo:
    def __init__(self):
        self.__controle = ControleEmprestimo()
        self.__painel = PainelEmprestimo(self.__controle)
        self.__regras = RegrasEmprestimo()
        self.__cadastrar_equipamentos_iniciais()

    def __cadastrar_equipamentos_iniciais(self):
        self.__controle.cadastrar_equipamento(Equipamento("Bola de vôlei", 1))
        self.__controle.cadastrar_equipamento(Equipamento("Raquete de tênis", 2))
        self.__controle.cadastrar_equipamento(Equipamento("Colete", 3))
        self.__controle.cadastrar_equipamento(Equipamento("Bicicleta", 4))

    def __mostrar_opcoes(self):
        print("\nEMPRÉSTIMOS - ATLÉTICA")
        print("1- Cadastrar um usuário")
        print("2- Cadastrar um novo equipamento")
        print("3- Emprestar")
        print("4 - Devolver")
        print("5 - Equipamentos disponíveis")
        print("6 - Empréstimos ativos")
        print("7 - Histórico de um equipamento")
        print("8 - Regras")
        print("0 - Sair")

    def executar(self):
        while True:
            self.__mostrar_opcoes()
            try:
                opcao = int(input("Escolha uma opção: "))
                if opcao == 0:
                    print("Até logo!")
                    break
                self.__tratar_opcao(opcao)
            except ValueError as erro:
                print(f"Entrada inválida: {erro}")

    def __tratar_opcao(self, opcao):
        if opcao == 1:
            cadastro(self.__controle)
        elif opcao == 2:
            cadastro_equipamento(self.__controle)
        elif opcao == 3:
            self.__emprestar()
        elif opcao == 4:
            self.__devolver()
        elif opcao == 5:
            print(self.__painel.equipamento_disponiveis())
        elif opcao == 6:
            print(self.__painel.emprestimos_ativos())
        elif opcao == 7:
            self.__historico()
        elif opcao == 8:
            print(self.__regras.listar_regras())
        else:
            print("Opção inválida!")

    def __historico(self):
        codigo = int(input("Digite o código do equipamento: "))
        print(self.__painel.historico_equipamento(codigo))

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

def cadastro_equipamento(controle):
    print("Cadastro de novos equipamentos\n")

    nome = input("Digite o nome do equipamento: ")
    identificacao = int(input("Digite o código de identificação: "))

    novo_equipamento = Equipamento(nome, identificacao, True)
    controle.cadastrar_equipamento(novo_equipamento)

    print("Cadastro concluído\n")
    print(novo_equipamento)

if __name__ == "__main__":
    menu = MenuEmprestimo()
    menu.executar()
