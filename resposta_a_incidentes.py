import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


# Função para registrar e classificar um incidente
def registrar_incidente():
    descricao = input("Descreva o incidente: ")
    gravidades = {
        "1": "baixa",
        "2": "média",
        "3": "alta",
        "4": "gravíssima"
    }

    print("Selecione a gravidade do incidente:")
    for opcao, gravidade in gravidades.items():
        print(f"{opcao}. {gravidade}")

    opcao_gravidade = input("Opção: ")
    while opcao_gravidade not in gravidades:
        print("Opção inválida. Escolha uma das opções listadas.")
        opcao_gravidade = input("Opção: ")

    gravidade = gravidades[opcao_gravidade]
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conexao = sqlite3.connect('incidentes.db')
    conexao.execute('''
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            gravidade TEXT,
            status TEXT,
            etapas TEXT,
            data_hora TEXT
        )
    ''')
    conexao.execute('INSERT INTO incidentes (descricao, gravidade, data_hora) VALUES (?, ?, ?)', (descricao, gravidade, data_hora))
    conexao.commit()
    conexao.close()

    print("Incidente registrado com sucesso!")


# Função para listar todas as gravidades disponíveis
def listar_gravidades():
    gravidades = ["baixa", "média", "alta", "gravíssima"]
    print("Gravidades disponíveis:")
    for gravidade in gravidades:
        print(gravidade)


# Função para listar todos os incidentes
def listar_incidentes():
    conexao = sqlite3.connect('incidentes.db')
    cursor = conexao.execute('SELECT id, descricao, gravidade, status, data_hora FROM incidentes')
    resultados = cursor.fetchall()
    conexao.close()

    if not resultados:
        print("Nenhum incidente registrado.")
        return

    df = pd.DataFrame(resultados, columns=['ID', 'Descrição', 'Gravidade', 'Status', 'Data/Hora'])
    print(df)


# Função para atualizar o status de um incidente
def atualizar_status_incidente():
    incidente_id = input("Informe o ID do incidente que deseja atualizar o status: ")

    print("Escolha o novo status do incidente:")
    print("1. Suspeita")
    print("2. Suspeita confirmada")
    print("3. Suspeita sem confirmação")
    print("4. Investigação em andamento")
    print("5. Investigação concluída")
    print("6. Correção em progresso")
    print("7. Correção implementada")
    print("8. Encerrado")
    print("9. Sem ação necessária")
    print("10. Outra opção")

    opcao_status = input("Opção: ")
    while opcao_status not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        print("Opção inválida. Escolha uma das opções listadas.")
        opcao_status = input("Opção: ")

    if opcao_status == "1":
        novo_status = "Suspeita"
    elif opcao_status == "2":
        novo_status = "Suspeita confirmada"
    elif opcao_status == "3":
        novo_status = "Suspeita sem confirmação"
    elif opcao_status == "4":
        novo_status = "Investigação em andamento"
    elif opcao_status == "5":
        novo_status = "Investigação concluída"
    elif opcao_status == "6":
        novo_status = "Correção em progresso"
    elif opcao_status == "7":
        novo_status = "Correção implementada"
    elif opcao_status == "8":
        novo_status = "Encerrado"
    elif opcao_status == "9":
        novo_status = "Sem ação necessária"
    else:
        novo_status = input("Informe o novo status do incidente: ")

    conexao = sqlite3.connect('incidentes.db')
    conexao.execute('UPDATE incidentes SET status = ? WHERE id = ?', (novo_status, incidente_id))
    conexao.commit()
    conexao.close()

    print("Status do incidente atualizado com sucesso!")


# Função para apagar um incidente
def apagar_incidente():
    incidente_id = input("Informe o ID do incidente que deseja apagar: ")

    conexao = sqlite3.connect('incidentes.db')
    conexao.execute('DELETE FROM incidentes WHERE id = ?', (incidente_id,))
    conexao.commit()
    conexao.close()

    print("Incidente apagado com sucesso!")


# Função para gerar o relatório de incidentes com gráficos
def gerar_relatorio():
    conexao = sqlite3.connect('incidentes.db')
    cursor = conexao.execute('SELECT gravidade, COUNT(*) FROM incidentes GROUP BY gravidade')
    resultados = cursor.fetchall()
    conexao.close()

    if not resultados:
        print("Nenhum incidente registrado para gerar o relatório.")
        return

    gravidades = []
    counts = []

    for gravidade, count in resultados:
        gravidades.append(gravidade)
        counts.append(count)

    df = pd.DataFrame({'Gravidade': gravidades, 'Quantidade': counts})
    df.set_index('Gravidade', inplace=True)

    df.plot(kind='bar')
    plt.xlabel('Gravidade')
    plt.ylabel('Quantidade')
    plt.title('Relatório de Incidentes por Gravidade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Função principal para executar o programa
def main():
    while True:
        print('========================================')
        print("=== Sistema de Resposta a Incidentes ===")
        print('========================================')
        print("1. Registrar incidente")
        print("2. Listar incidentes")
        print("3. Atualizar status de incidente")
        print("4. Listar gravidades")
        print("5. Apagar incidente")
        print("6. Gerar relatório de incidentes")
        print("7. Sair")
        print('========================================')

        opcao = input("Opção: ")
        print()

        if opcao == "1":
            registrar_incidente()
        elif opcao == "2":
            listar_incidentes()
        elif opcao == "3":
            atualizar_status_incidente()
        elif opcao == "4":
            listar_gravidades()
        elif opcao == "5":
            apagar_incidente()
        elif opcao == "6":
            gerar_relatorio()
        elif opcao == "7":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Escolha uma opção válida.\n")


if __name__ == "__main__":
    main()
