import sys
import pickle
from math import ceil

class SistemaArquivos:
    def __init__(self, tamanho) -> None:
        self.caminho_fs = "furgfs.fs"

        # 0.04MB = 40.96KB || 4 blocos
        if tamanho < 0.04:
            raise Exception("Escolha um tamanho maior para o sistema.")

        self.espaco = round(tamanho * 1024 * 1024)  # 1 MB = 1048576 B
        self.tamanho_bloco = 4 * 1024  # 4 KB = 4096 B
        self.total_blocos = self.espaco // self.tamanho_bloco  # 200 MB / 4096 B = 51.200 blocos
        self.sistema_arquivos = [b"0" * self.tamanho_bloco] * self.total_blocos
        self.tamanho_cabecalho_blocos = 1

        tamanho_fat_blocos = self.preparar_fat()
        endereco_fat = self.tamanho_cabecalho_blocos
        endereco_raiz, tamanho_raiz_blocos = self.preparar_raiz(tamanho_fat_blocos)
        endereco_dados = endereco_raiz + tamanho_raiz_blocos

        self.preparar_cabecalho(endereco_fat, endereco_raiz, endereco_dados)

        self.salvar()

    def __str__(self) -> str:
        blocos_sistema = self.ler_bloco(0)[5] + 1
        bytes_sistema = blocos_sistema * self.tamanho_bloco

        string = f"\n" \
                 f"{'*' * 50}\n" \
                 f"{self.caminho_fs}\n" \
                 f"Espaço total: {self.espaco}B | {self.espaco // 1024}KB | {self.espaco // 1048576}MB\n" \
                 f"Dados do sistema: {bytes_sistema}B | {bytes_sistema // 1024}KB | {bytes_sistema / 1048576:.1f}MB\n" \
                 f"Tamanho do bloco: {round(self.tamanho_bloco / 1024)}KB\n" \
                 f"Quantidade total de blocos: {self.total_blocos}\n" \
                 f"Quantidade de blocos para o sistema: {blocos_sistema}\n" \
                 f"Quantidade de blocos para os dados: {self.total_blocos - blocos_sistema}\n" \
                 f"{'*' * 50}\n"
        return string

    def salvar(self) -> None:
        with open(self.caminho_fs, "wb") as arquivo_fs:
            pickle.dump(self, arquivo_fs)

    def ler_bloco(self, bloco: int):
        return pickle.loads(self.sistema_arquivos[bloco])
    
    def atualizar_fs(self, folha_atualizacao: dict):
        for chave, valor in folha_atualizacao.items():
            self.sistema_arquivos[chave] = valor
        self.salvar()


    def preparar_cabecalho(self, endereco_fat: int, endereco_raiz: int, endereco_dados: int) -> None:
        cabecalho = (
            self.tamanho_cabecalho_blocos,
            self.espaco,
            self.tamanho_bloco,
            endereco_fat,
            endereco_raiz,
            endereco_dados
        )
        self.sistema_arquivos[0] = pickle.dumps(cabecalho)

    def preparar_fat(self) -> int:
        tamanho_fat = self.total_blocos - 1
        tamanho_fat_blocos = ceil(sys.getsizeof([0] * tamanho_fat) / self.tamanho_bloco)

        # Cada bloco pode conter uma lista de n-1 elementos
        n = 0
        while True:
            n += 1
            tamanho_blocos = ceil(sys.getsizeof([-1] * n) / self.tamanho_bloco)
            if tamanho_blocos > 1:
                break

        vazio = [-2] * (n - 1)
        for i in range(1, 1 + tamanho_fat_blocos):
            self.sistema_arquivos[i] = pickle.dumps(vazio)

        return tamanho_fat_blocos


    def preparar_raiz(self, tamanho_fat_blocos: int) -> tuple:
        tamanho_max_nome_arquivo = 64  # 64 B

        tamanho_raiz = self.total_blocos - self.tamanho_cabecalho_blocos - tamanho_fat_blocos
        tamanho_raiz_blocos = ceil(sys.getsizeof({str(i): i for i in range(tamanho_raiz)}) / self.tamanho_bloco)
        endereco_raiz = self.tamanho_cabecalho_blocos + tamanho_fat_blocos
        for i in range(endereco_raiz, endereco_raiz + tamanho_raiz_blocos):
            self.sistema_arquivos[i] = pickle.dumps(dict())

        return endereco_raiz, tamanho_raiz_blocos


    def copiar_para_fs(self, caminho_arquivo: str) -> None:
        planilha_atualizacao = dict()
        cabecalho = self.ler_bloco(0)
        endereco_fat = cabecalho[3]
        endereco_raiz = cabecalho[4]
        endereco_dados = cabecalho[5]
        tamanho_secao_fat = len(self.ler_bloco(endereco_fat))

        # Testar se o arquivo já está no sistema
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            if caminho_arquivo in secao_raiz:
                raise Exception(f"O arquivo '{caminho_arquivo}' já existe no sistema.")

        # Dividir o arquivo em blocos
        with open(caminho_arquivo, "r") as f:
            conteudo_arquivo = f.read()
        conteudo_serializado = pickle.dumps(conteudo_arquivo)
        tamanho_conteudo = len(conteudo_serializado)
        fatias_dados = [conteudo_serializado[i:i + self.tamanho_bloco] for i in range(0, tamanho_conteudo, self.tamanho_bloco)]

        # Encontrar blocos vazios
        indices_blocos = list()
        blocos_necessarios = len(fatias_dados)
        for indice_secao_fat in range(endereco_fat, endereco_raiz):
            secao_fat = self.ler_bloco(indice_secao_fat)
            for i, entrada in enumerate(secao_fat):
                if len(indices_blocos) == blocos_necessarios:
                    break
                if entrada == -2:
                    indices_blocos.append(i + ((indice_secao_fat - 1) * tamanho_secao_fat))
            if len(indices_blocos) == blocos_necessarios:
                break
        if len(indices_blocos) != blocos_necessarios:
            raise Exception(f"Não há espaço suficiente para salvar o arquivo '{caminho_arquivo}'")

        # Atualizar FAT
        indice_secao_fat = int()
        secao_fat = list()
        for i, indice_bloco in enumerate(indices_blocos):
            if indice_secao_fat != endereco_fat + (indice_bloco // tamanho_secao_fat):
                indice_secao_fat = endereco_fat + (indice_bloco // tamanho_secao_fat)
                secao_fat = self.ler_bloco(indice_secao_fat)
            try:
                secao_fat[indice_bloco % tamanho_secao_fat] = indices_blocos[i + 1]
            except IndexError:
                secao_fat[indice_bloco % tamanho_secao_fat] = -1
            planilha_atualizacao[endereco_fat + (indice_bloco // tamanho_secao_fat)] = pickle.dumps(secao_fat)

        # Atualizar dados
        for i, fatia_dado in enumerate(fatias_dados):
            planilha_atualizacao[indices_blocos[i] + endereco_dados] = fatia_dado

        # Atualizar raiz
        secao_raiz = dict()
        indice_secao_raiz = int()
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            limite_secao_raiz = (self.total_blocos - self.tamanho_cabecalho_blocos - endereco_raiz - endereco_fat) // (
                    endereco_dados - endereco_raiz)
            if len(secao_raiz) < limite_secao_raiz:
                break
        secao_raiz[caminho_arquivo] = indices_blocos[0]
        planilha_atualizacao[indice_secao_raiz] = pickle.dumps(secao_raiz)

        self.atualizar_fs(planilha_atualizacao)


    def copiar_do_fs(self, nome_arquivo: str) -> None:
        cabecalho = self.ler_bloco(0)
        endereco_fat = cabecalho[3]
        endereco_raiz = cabecalho[4]
        endereco_dados = cabecalho[5]
        tamanho_secao_fat = len(self.ler_bloco(endereco_fat))

        # Localizar o arquivo no sistema
        primeiro_bloco = -1
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            if nome_arquivo in secao_raiz:
                primeiro_bloco = secao_raiz[nome_arquivo]
                break
        if primeiro_bloco == -1:
            raise Exception(f"O arquivo '{nome_arquivo}' não existe.")

        # Encontrar os blocos do arquivo e uni-los
        conteudo_serializado = b""
        bloco_atual = primeiro_bloco
        secao_fat = self.ler_bloco(endereco_fat + primeiro_bloco // tamanho_secao_fat)
        while bloco_atual != -1:
            fatia_dados = self.sistema_arquivos[bloco_atual + endereco_dados]
            conteudo_serializado += fatia_dados
            bloco_atual = secao_fat[bloco_atual]

        # Escrever os conteúdos em um arquivo
        conteudo_arquivo = pickle.loads(conteudo_serializado)
        with open(nome_arquivo, 'w') as arquivo_texto:
            arquivo_texto.write(str(conteudo_arquivo))

    def renomear(self, nome_antigo: str, nome_novo: str) -> None:
        planilha_atualizacao = dict()
        cabecalho = self.ler_bloco(0)
        endereco_raiz = cabecalho[4]
        endereco_dados = cabecalho[5]

        # Localizar o arquivo no sistema
        indice_secao_raiz = -1
        secao_raiz = dict()
        encontrado = False
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            if nome_antigo in secao_raiz:
                encontrado = True
                secao_raiz[nome_novo] = secao_raiz.pop(nome_antigo)
                break
        if not encontrado:
            raise Exception(f"O arquivo '{nome_antigo}' não existe.")

        planilha_atualizacao[indice_secao_raiz] = pickle.dumps(secao_raiz)
        self.atualizar_fs(planilha_atualizacao)

    def remover(self, nome_arquivo: str) -> None:
        planilha_atualizacao = dict()
        cabecalho = self.ler_bloco(0)
        endereco_fat = cabecalho[3]
        endereco_raiz = cabecalho[4]
        endereco_dados = cabecalho[5]
        tamanho_secao_fat = len(self.ler_bloco(endereco_fat))

        # Localizar o arquivo no sistema e limpar a entrada da raiz
        indice_secao_raiz = -1
        secao_raiz = dict()
        primeiro_bloco = -1
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            if nome_arquivo in secao_raiz:
                primeiro_bloco = secao_raiz[nome_arquivo]
                del secao_raiz[nome_arquivo]
                break
        if primeiro_bloco == -1:
            raise Exception(f"O arquivo '{nome_arquivo}' não existe.")
        planilha_atualizacao[indice_secao_raiz] = pickle.dumps(secao_raiz)

        # Limpar as entradas da FAT
        bloco_atual = primeiro_bloco
        indice_secao_fat = endereco_fat + (bloco_atual // tamanho_secao_fat)
        secao_fat = self.ler_bloco(indice_secao_fat)
        while bloco_atual != -1:
            if indice_secao_fat != endereco_fat + (bloco_atual // tamanho_secao_fat):
                planilha_atualizacao[indice_secao_fat] = pickle.dumps(secao_fat)
                indice_secao_fat = endereco_fat + bloco_atual // tamanho_secao_fat
                secao_fat = self.ler_bloco(indice_secao_fat)
            proximo_bloco = secao_fat[bloco_atual % tamanho_secao_fat]
            secao_fat[bloco_atual % tamanho_secao_fat] = -2
            bloco_atual = proximo_bloco
        planilha_atualizacao[indice_secao_fat] = pickle.dumps(secao_fat)

        self.atualizar_fs(planilha_atualizacao)

    def listar_arquivos(self) -> tuple:
        cabecalho = self.ler_bloco(0)
        endereco_raiz = cabecalho[4]
        endereco_dados = cabecalho[5]

        # Iterar sobre a raiz
        arquivos = list()
        for indice_secao_raiz in range(endereco_raiz, endereco_dados):
            secao_raiz = self.ler_bloco(indice_secao_raiz)
            for nome_arquivo in secao_raiz.keys():
                arquivos.append(nome_arquivo)

        print("\n")
        print(f"Total de arquivos: {len(arquivos)}")
        for arquivo in arquivos:
            print(arquivo)

        return tuple(arquivos)


    def informacao_uso(self) -> tuple:
        cabecalho = self.ler_bloco(0)
        endereco_fat = cabecalho[3]
        endereco_raiz = cabecalho[4]

        blocos_em_uso = int()

        for indice_secao_fat in range(endereco_fat, endereco_raiz):
            secao_fat = self.ler_bloco(indice_secao_fat)
            for entrada in secao_fat:
                if entrada != -2:
                    blocos_em_uso += 1

        espaco_usado = (blocos_em_uso * self.tamanho_bloco) / 1048576
        espaco_total = self.espaco / 1048576
        espaco_livre = espaco_total - espaco_usado

        print("\n")
        if espaco_total >= 1:
            print(f"{espaco_livre:.1f}MB livres de {espaco_total:.1f}MB")
        else:
            print(f"{espaco_livre * 1024:.1f}KB livres de {espaco_total * 1024:.1f}KB")
        print(f"{(espaco_usado / espaco_total) * 100:.1f}% do espaço ocupado")

        return espaco_usado, espaco_livre


if __name__ == "__main__":
    fs = SistemaArquivos
    # fs = SistemaArquivos(200)
    # 200MB ADDRESSES - Header: 0 | FAT: 1 | Root: 102 | Data: 572