import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

class Cadastro:
    def __init__(self, nomeInvestimento, tipo, valor, data, id=None):
        self.nomeInvestimento = nomeInvestimento
        self.tipo = tipo
        self.valor = float(valor)
        self.data = data
        self.id = id

class BancoDeDados:
    def __init__(self, nome_banco):
        self.conn = sqlite3.connect(nome_banco)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        print("Banco de dados aberto com sucesso!")

    def criar_tabela(self):
        sql = """CREATE TABLE IF NOT EXISTS Cadastro (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nomeInvestimento TEXT,
                 tipo TEXT,
                 valor REAL,
                 data TEXT)"""
        self.cursor.execute(sql)
        self.conn.commit()

    def inserir_conta(self, cadastro):
        # Validação do valor
        if cadastro.valor <= 0:
            print("Erro: O valor deve ser positivo.")
            return

        # Validação da data
        try:
            data_inserida = datetime.strptime(cadastro.data, "%d/%m/%Y")
            data_limite = datetime.strptime("15/03/2025", "%d/%m/%Y")

            if data_inserida > data_limite:
                print("Erro: A data não pode ser posterior a 15/03/2025.")
                return
        except ValueError:
            print("Erro: Formato de data inválido. Use o formato DD/MM/AAAA.")
            return

        # Inserção no banco de dados
        sql = """INSERT INTO Cadastro (nomeInvestimento, tipo, valor, data)
                VALUES (?, ?, ?, ?)"""
        valores = (cadastro.nomeInvestimento, cadastro.tipo, cadastro.valor, cadastro.data)

        try:
            self.cursor.execute(sql, valores)
            self.conn.commit()
            print("Conta inserida com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao inserir conta no banco de dados: {erro}")

    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM Cadastro")
        registros = self.cursor.fetchall()
        
        print("\nLista de Investimentos:")
        print("---------------------------------------------")
        for registro in registros:
            print(f"ID: {registro[0]} | Investimento: {registro[1]} | Tipo: {registro[2]} | Valor: R$ {registro[3]} | Data: {registro[4]}")
        print("---------------------------------------------")

    def excluir_conta(self, id):
        try:
            # Verifica se o ID existe antes de excluir
            self.cursor.execute("SELECT id FROM Cadastro WHERE id = ?", (id,))
            if not self.cursor.fetchone():
                print(f"Erro: Conta com ID {id} não encontrada.")
                return
            
            # Executa a exclusão
            self.cursor.execute("DELETE FROM Cadastro WHERE id = ?", (id,))
            self.conn.commit()
            print(f"Conta ID {id} excluída com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao excluir conta: {erro}")

    
    def atualizar_conta(self,id):
        print("1.nome\n2.tipo\n3.valor\n4.data")
        op = int(input("Qual campo deseja atualizar?"))
        if op == 1:
            nome = input("Digite o novo nome:")
            self.cursor.execute("UPDATE Cadastro SET nomeInvestimento = ? WHERE id = ?",(nome,id))
            self.conn.commit()
        elif op == 2:
            tipo = input("Digite o novo tipo:")
            self.cursor.execute("UPDATE Cadastro SET tipo = ? WHERE id = ?",(tipo,id))
            self.conn.commit()
        elif op == 3:
            valor = float(input("Digite o novo valor:"))
            if valor <=0:
                print("Valor inválido")
                return
            else:
                self.cursor.execute("UPDATE Cadastro SET valor = ? WHERE id = ?",(valor,id))
                self.conn.commit()
        elif op == 4:
            data = input("Digite a nova data:")
            try:
                data_inserida = datetime.strptime(data,"%d/%m/%Y")
                data_limite = datetime.strptime("15/03/2025","%d/%m/%Y")
                if data_inserida > data_limite:
                    print("Data inválida")
                    return
                else:
                    self.cursor.execute("UPDATE Cadastro SET data = ? WHERE id = ?",(data,id))
                    self.conn.commit()
            except:
                print("Data inválida")
                return
        else:
            print("Opção inválida")
    def grafico(self):
        self.cursor.execute("SELECT tipo, SUM(valor) FROM Cadastro GROUP BY tipo")
        registros = self.cursor.fetchall()
        tipos = []
        valores = []
        for registro in registros:
            tipos.append(registro[0])
            valores.append(registro[1])
        plt.bar(tipos,valores)
        plt
        plt.show()
    


    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    bd = BancoDeDados("Cadastro.db")
    while True:

        print("\nMenu de opções:")
        print("1. Inserir investimento")
        print("2. Listar investimentos")
        print("3. Excluir investimento")
        print("4. Atualizar investimento")
        print("5. Gráfico")
        print("6. Sair")
        op = int(input("Escolha uma opção: "))
        if op == 1:
            nomeInvestimento = input("Digite o nome do investimento: ")
            tipo = input("Digite o tipo do investimento: ")
            valor = float(input("Digite o valor do investimento: "))
            data = input("Digite a data do investimento(Dia/Mês/Ano): ")
            investimento = Cadastro(nomeInvestimento, tipo, valor, data)
            bd.inserir_conta(investimento)
        elif op == 2:
            bd.listar_clientes()
        elif op == 3:
            ID = int(input("Digite o ID do investimento que deseja excluir: "))
            bd.excluir_conta(ID)
        elif op == 4:
            ID = int(input("Digite o ID do investimento que deseja atualizar: "))
            bd.atualizar_conta(ID)
        elif op == 5:
            print("Gráfico")
            bd.grafico()
        elif op == 6:
            break
        else:
            print("Opção inválida")
    