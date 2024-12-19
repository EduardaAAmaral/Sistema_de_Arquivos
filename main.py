# Edurda Alves Amaral - 155563
# Bruno Machado Lobato - 156966
# Leia o README.md


from Sistema_Arquivos import SistemaArquivos
from pickle import load, dump
from time import sleep


def mostrar_menu1():
    print("\nMenu:")
    print("1. Criar um novo sistema de arquivos")
    print("2. Utilizar arquivo .fs existente")


def mostrar_menu2():
    print("\nMenu:")
    print("1. Copiar arquivo para o sistema")
    print("2. Copiar arquivo do sistema")
    print("3. Renomear arquivo")
    print("4. Remover arquivo")
    print("5. Listar arquivos")
    print("6. Mostrar informações de espaço ocupado")
    print("7. Salvar sistema de arquivos")
    print("8. Sair")


def main():
    sistema_arquivos = None

    while True:
        sleep(1)
        mostrar_menu1()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            try:
                tamanho = float(input("Informe o tamanho do sistema em bytes: "))
                sistema_arquivos = SistemaArquivos(tamanho)
                print(f"\nSistema de arquivos criado com sucesso! {sistema_arquivos}")
            except ValueError:
                print("Por favor, insira um tamanho válido para o sistema de arquivos.")
            break

        elif escolha == "2":
            nome_arquivo = input("Informe o nome do arquivo: ")
            try:
                with open(nome_arquivo, "rb") as arquivo:
                    sistema_arquivos = load(arquivo)
                print(f"\nSistema de arquivos acessado! {sistema_arquivos}")
            except FileNotFoundError:
                print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
            break

        else:
            print("\nEscolha uma opção válida.")

    while True:
        sleep(1)
        mostrar_menu2()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            caminho_arquivo = input("Informe o caminho do arquivo a ser copiado: ")
            try:
                sistema_arquivos.copiar_para_fs(caminho_arquivo)
                print("\nArquivo copiado para o sistema com sucesso!")
            except Exception as e:
                print(f"\nErro ao copiar arquivo para o sistema: {str(e)}")

        elif escolha == "2":
            nome_arquivo = input("Informe o nome do arquivo a ser copiado do sistema: ")
            try:
                sistema_arquivos.copiar_do_fs(nome_arquivo)
                print("Arquivo copiado do sistema com sucesso!")
            except Exception as e:
                print(f"Erro ao copiar arquivo do sistema: {str(e)}")

        elif escolha == "3":
            nome_antigo = input("Informe o nome antigo do arquivo: ")
            nome_novo = input("Informe o novo nome do arquivo: ")
            try:
                sistema_arquivos.renomear(nome_antigo, nome_novo)
                print("Arquivo renomeado com sucesso!")
            except Exception as e:
                print(f"Erro ao renomear arquivo: {str(e)}")

        elif escolha == "4":
            nome_arquivo = input("Informe o nome do arquivo a ser removido: ")
            try:
                sistema_arquivos.remover(nome_arquivo)
                print("Arquivo removido com sucesso!")
            except Exception as e:
                print(f"Erro ao remover arquivo: {str(e)}")

        elif escolha == "5":
            sistema_arquivos.listar_arquivos()

        elif escolha == "6":
            sistema_arquivos.informacao_uso()

        elif escolha == "7":
            nome_arquivo = input("Informe o nome para salvar o arquivo: ")
            try:
                with open(nome_arquivo, "wb") as arquivo:
                    dump(sistema_arquivos, arquivo)
                print("Sistema de arquivos salvo com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar o sistema de arquivos: {str(e)}")

        elif escolha == "8":
            print("Encerrando o programa...")
            break

        else:
            print("Escolha uma opção válida.")


if __name__ == "__main__":
    main()
