# Guilherme Azambuja - 149429
# Pablo Guaicurus - 149449
# Rafaela Barcelos - 149438
# https://github.com/gvlk/file-system
# Leia o README.md

from Sistema_Arquivos import SistemaArquivos
from pickle import load
from time import sleep


def exibir_menu1():
    print("\nMenu:")
    print("1. Criar um novo sistema de arquivos")
    print("2. Utilizar arquivo .fs existente")


def exibir_menu2():
    print("\nMenu:")
    print("1. Copiar arquivo para o sistema")
    print("2. Copiar arquivo do sistema")
    print("3. Renomear arquivo")
    print("4. Remover arquivo")
    print("5. Listar arquivos")
    print("6. Mostrar informações de espaço ocupado")
    print("7. Sair")


def criar_sistema_arquivos():
    try:
        tamanho = float(input("Informe o tamanho do sistema em bytes: "))
        sistema = SistemaArquivos(tamanho)
        print(f"\nSistema de arquivos criado com sucesso! {sistema}")
        return sistema
    except ValueError:
        print("Tamanho inválido. Por favor, insira um valor numérico válido.")
        return None


def carregar_sistema_arquivos():
    try:
        nome = input("Informe o nome do arquivo: ")
        with open(nome, "rb") as arquivo:
            sistema = load(arquivo)
        print(f"\nSistema de arquivos acessado! {sistema}")
        return sistema
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o nome e tente novamente.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o sistema de arquivos: {str(e)}")
        return None


def realizar_operacoes_arquivos(sistema: SistemaArquivos):
    while True:
        sleep(1)
        exibir_menu2()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            caminho_arquivo = input("Informe o caminho do arquivo a ser copiado: ")
            try:
                sistema.copy_to_fs(caminho_arquivo)
                print("\nArquivo copiado para o sistema com sucesso!")
            except Exception as e:
                print(f"\nErro ao copiar arquivo para o sistema: {str(e)}")

        elif escolha == "2":
            nome_arquivo = input("Informe o nome do arquivo a ser copiado do sistema: ")
            try:
                sistema.copy_from_fs(nome_arquivo)
                print("Arquivo copiado do sistema com sucesso!")
            except Exception as e:
                print(f"Erro ao copiar arquivo do sistema: {str(e)}")

        elif escolha == "3":
            nome_antigo = input("Informe o nome antigo do arquivo: ")
            nome_novo = input("Informe o novo nome do arquivo: ")
            try:
                sistema.rename(nome_antigo, nome_novo)
                print("Arquivo renomeado com sucesso!")
            except Exception as e:
                print(f"Erro ao renomear arquivo: {str(e)}")

        elif escolha == "4":
            nome_arquivo = input("Informe o nome do arquivo a ser removido: ")
            try:
                sistema.remove(nome_arquivo)
                print("Arquivo removido com sucesso!")
            except Exception as e:
                print(f"Erro ao remover arquivo: {str(e)}")

        elif escolha == "5":
            sistema.list_files()

        elif escolha == "6":
            sistema.usage_info()

        elif escolha == "7":
            print("Encerrando o programa...")
            break

        else:
            print("Escolha uma opção válida.")


def main():
    sistema = None

    while True:
        sleep(1)
        exibir_menu1()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            sistema = criar_sistema_arquivos()
            if sistema:
                break

        elif escolha == "2":
            sistema = carregar_sistema_arquivos()
            if sistema:
                break

        else:
            print("\nEscolha uma opção válida.")

    if sistema:
        realizar_operacoes_arquivos(sistema)


if __name__ == "__main__":
    main()
