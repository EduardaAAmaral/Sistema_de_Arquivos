import os
import pickle
import math

class SistemaArquivos:
    def __init__(self, tamanho_mb):
        if tamanho_mb < 0.04:
            raise ValueError("O tamanho do sistema de arquivos deve ser maior ou igual a 0,04 MB.")

        self.tamanho_total = tamanho_mb * 1024 * 1024  # Tamanho total em bytes
        self.tamanho_bloco = 4096  # Cada bloco tem 4 KB
        self.num_blocos = math.ceil(self.tamanho_total / self.tamanho_bloco)

        self.header = {
            "tamanho_total": self.tamanho_total,
            "tamanho_bloco": self.tamanho_bloco,
            "num_blocos": self.num_blocos,
            "endereco_fat": 1,
            "endereco_raiz": 2,
            "endereco_dados": 3
        }

        self.fat = [-2] * self.num_blocos  # -2 indica bloco livre
        self.raiz = {}  # Armazena {"nome_arquivo": bloco_inicial}
        self.dados = [None] * self.num_blocos

        self.salvar_sistema()

    def salvar_sistema(self):
        with open("sistema_arquivos.fs", "wb") as arquivo:
            pickle.dump((self.header, self.fat, self.raiz, self.dados), arquivo)

    def carregar_sistema(self):
        with open("sistema_arquivos.fs", "rb") as arquivo:
            self.header, self.fat, self.raiz, self.dados = pickle.load(arquivo)

    def copiar_para_sistema(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError("O arquivo especificado não existe.")

        tamanho_arquivo = os.path.getsize(caminho_arquivo)
        blocos_necessarios = math.ceil(tamanho_arquivo / self.tamanho_bloco)
        blocos_livres = [i for i, estado in enumerate(self.fat) if estado == -2]

        if len(blocos_livres) < blocos_necessarios:
            raise ValueError("Espaço insuficiente no sistema de arquivos.")

        with open(caminho_arquivo, "rb") as arquivo:
            conteudo = arquivo.read()

        nome_arquivo = os.path.basename(caminho_arquivo)
        bloco_inicial = blocos_livres[0]
        self.raiz[nome_arquivo] = bloco_inicial

        bloco_atual = bloco_inicial
        for i in range(blocos_necessarios):
            inicio = i * self.tamanho_bloco
            fim = inicio + self.tamanho_bloco
            self.dados[bloco_atual] = conteudo[inicio:fim]

            if i < blocos_necessarios - 1:
                proximo_bloco = blocos_livres[i + 1]
                self.fat[bloco_atual] = proximo_bloco
                bloco_atual = proximo_bloco
            else:
                self.fat[bloco_atual] = -1  # Indica fim do arquivo

        self.salvar_sistema()

    def copiar_do_sistema(self, nome_arquivo):
        if nome_arquivo not in self.raiz:
            raise FileNotFoundError("O arquivo especificado não está no sistema.")

        bloco_atual = self.raiz[nome_arquivo]
        conteudo = b""

        while bloco_atual != -1:
            conteudo += self.dados[bloco_atual]
            bloco_atual = self.fat[bloco_atual]

        with open(nome_arquivo, "wb") as arquivo:
            arquivo.write(conteudo)

    def renomear_arquivo(self, nome_antigo, nome_novo):
        if nome_antigo not in self.raiz:
            raise FileNotFoundError("O arquivo especificado não existe.")
        if nome_novo in self.raiz:
            raise ValueError("Um arquivo com o novo nome já existe.")

        self.raiz[nome_novo] = self.raiz.pop(nome_antigo)
        self.salvar_sistema()

    def remover_arquivo(self, nome_arquivo):
        if nome_arquivo not in self.raiz:
            raise FileNotFoundError("O arquivo especificado não existe.")

        bloco_atual = self.raiz.pop(nome_arquivo)

        while bloco_atual != -1:
            proximo_bloco = self.fat[bloco_atual]
            self.fat[bloco_atual] = -2  # Libera o bloco
            self.dados[bloco_atual] = None
            bloco_atual = proximo_bloco

        self.salvar_sistema()

    def listar_arquivos(self):
        return list(self.raiz.keys())

    def __str__(self):
        return (
            f"Sistema de Arquivos:\n"
            f"Tamanho Total: {self.header['tamanho_total'] / (1024 * 1024):.2f} MB\n"
            f"Tamanho do Bloco: {self.header['tamanho_bloco']} bytes\n"
            f"Blocos Totais: {self.header['num_blocos']}\n"
            f"Arquivos: {', '.join(self.raiz.keys()) if self.raiz else 'Nenhum'}\n"
        )

# Exemplo de uso
if __name__ == "__main__":
    sistema = SistemaArquivos(tamanho_mb=1)  # Cria um sistema de arquivos com 1 MB
    print(sistema)

    # Adicionar arquivo
    sistema.copiar_para_sistema("teste.txt")
    print("Arquivos no sistema:", sistema.listar_arquivos())

    # Recuperar arquivo
    sistema.copiar_do_sistema("teste.txt")

    # Renomear arquivo
    sistema.renomear_arquivo("teste.txt", "novo_teste.txt")
    print("Arquivos no sistema após renomear:", sistema.listar_arquivos())

    # Remover arquivo
    sistema.remover_arquivo("novo_teste.txt")
    print("Arquivos no sistema após remover:", sistema.listar_arquivos())
