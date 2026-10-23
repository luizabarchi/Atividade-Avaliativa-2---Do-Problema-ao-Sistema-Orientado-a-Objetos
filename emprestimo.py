
#Atividade Avaliativa 2: Do Problema ao Sistema Orientado a Objetos
# Classes de dados: Equipamentos, Pessoa (Aluno/Servidor) e Regras
# Classes de comportamento: Controle, Painel e Empréstimo

from abc import ABC, abstractmethod
from datetime import date, timedelta

#CLASSES DE DADOS

class Equipamento(ABC):

    def __init__ (self, nome, identificacao, disponibilidade=True):
        self.__nome = nome
        self.__identificacao = identificacao
        self.__disponibilidade = disponibilidade

    @property
    def nome(self):
        return self.__nome

    @property
    def identificacao(self):
        return self.__identificacao

    @property
    def disponibilidade(self):
        return self.__disponibilidade

    def __str__ (self):
            estado = "Disponível" if self.disponibilidade else "Emprestado"
            return f"Equipamento: {self.nome}, código: {self.identificacao}, Situação: {estado}"

    def emprestar(self):
        if not self.__disponibilidade:
            return False
        self.__disponibilidade = False
        return True

    def devolver(self):
        if self.__disponibilidade:
            return False
        self.__disponibilidade = True
        return True

    @abstractmethod
    def prazo_dias(self):
        pass

class Bola(Equipamento):
    def prazo_dias(self):
        return 0

class Colete(Equipamento):
    def prazo_dias(self):
        return 0

class Raquete(Equipamento):
    def prazo_dias(self):
        return 2

class Bicicleta(Equipamento):
    def prazo_dias(self):
        return 7


class Pessoa(ABC):
    def __init__(self, registro, nome):
        self.__registro = registro
        self.__nome = nome
        self.__bloqueado_ate = None

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

    def bloquear_por(self, dias):
        self.__bloqueado_ate = date.today() + timedelta(days=dias)
    
    def esta_bloqueada(self):
        return self.__bloqueado_ate is not None and date.today() < self.__bloqueado_ate

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
        if pessoa.esta_bloqueada():
         return False, "Pessoa bloqueada por atraso em empréstimo anterior"
        return True, "Empréstimo permitido"
        
class Emprestimo:
    def __init__(self, pessoa, equipamento):
        self.__pessoa = pessoa
        self.__equipamento = equipamento
        self.__data_retirada = date.today()
        self.__data_limite = self.__data_retirada + timedelta(days=equipamento.prazo_dias())
        self.__data_devolucao = None

    @property
    def pessoa(self):
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

    def registrar_devolucao(self):
        self.__data_devolucao = date.today()

    def dias_de_atraso(self):
        fim = self.__data_devolucao if self.__data_devolucao else date.today()
        return max(0, (fim - self.__data_limite).days) 

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
        pessoa = self.buscar_pessoa(registro)
        equipamento = self.buscar_equipamento(codigo)

        pode, motivo = self.__regras.pode_emprestar(pessoa, equipamento, self.__contar_ativos(pessoa))

        if not pode:
            raise ValueError(motivo)

        equipamento.emprestar()
        emprestimo = Emprestimo(pessoa, equipamento)
        self.__emprestimos.append(emprestimo)
        return emprestimo
    

    def devolver(self, codigo):
        for emprestimo in self.__emprestimos:
            if emprestimo.esta_ativo() and emprestimo.equipamento.identificacao == codigo:
                emprestimo.registrar_devolucao()
                emprestimo.equipamento.devolver()
                atraso = emprestimo.dias_de_atraso()
                if atraso > 0:
                    emprestimo.pessoa.bloquear_por(atraso)
                return emprestimo
        raise ValueError("Não há empréstimo ativo para esse código.")


    def __contar_ativos(self, pessoa):
        total = 0
        for emprestimo in self.__emprestimos:
            if emprestimo.esta_ativo() and emprestimo.pessoa.registro == pessoa.registro:
              total += 1
        return total

    def buscar_pessoa(self, registro):
        if registro not in self.__pessoas:
             raise ValueError("Nenhuma pessoa encontrada com esse registro.")
        return self.__pessoas[registro]

    def buscar_equipamento(self, codigo):
        if codigo not in self.__equipamento:
            raise ValueError("Nenhum equipamento encontrado com esse código.")
        return self.__equipamento[codigo]

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

    def __emprestar(self):
        registro = input("Digite o registro da pessoa: ").strip()
        codigo = int(input("Digite o código do equipamento: "))
        emprestimo = self.__controle.emprestar(registro, codigo)
        print(f"Empréstimo realizado! Devolver até {emprestimo.data_limite.strftime('%d/%m')}.")

    def __devolver(self):
        codigo = int(input("Digite o código do equipamento: "))
        emprestimo = self.__controle.devolver(codigo)
        atraso = emprestimo.dias_de_atraso()
        if atraso > 0:
            print(f"Devolvido com {atraso} dia(s) de atraso. A pessoa ficará bloqueada por {atraso} dia(s).")
        else:
            print("Devolução registrada. Obrigado!")

    def __cadastrar_equipamentos_iniciais(self):
        self.__controle.cadastrar_equipamento(Bola("Bola de vôlei", 1))
        self.__controle.cadastrar_equipamento(Raquete("Raquete de tênis", 2))
        self.__controle.cadastrar_equipamento(Colete("Colete", 3))
        self.__controle.cadastrar_equipamento(Bicicleta("Bicicleta", 4))


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

    tipos = {1: Bola, 2: Raquete, 3: Colete, 4: Bicicleta}

    try:
     tipo = int(input("Tipo:\n1 - Bola\n2 - Raquete\n3 - Colete\n4 - Bicicleta\n"))
    except:
        raise ValueError("Tipo inválido. Digite um número de 1 a 4.")

    nome = input("Digite o nome do equipamento: ")
    identificacao = int(input("Digite o código de identificação: "))

    novo_equipamento = tipos[tipo](nome, identificacao)
    controle.cadastrar_equipamento(novo_equipamento)

    print("Cadastro concluído\n")
    print(novo_equipamento)

if __name__ == "__main__":
    menu = MenuEmprestimo()
    menu.executar()
