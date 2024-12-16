## Simulação de Sistema de Arquivos

Este projeto Python implementa uma simulação simples de sistema de arquivos, criando um sistema de arquivos personalizado dentro de um único arquivo armazenado em um sistema de arquivos real. A simulação suporta operações como copiar arquivos para o sistema, renomear arquivos, remover arquivos e mais.

## Funcionalidades
- Criar um sistema de arquivos personalizado dentro de um único arquivo.
- Copiar arquivos do sistema de arquivos real para o sistema de arquivos  simulado.
- Copiar arquivos do sistema de arquivos simulado para o sistema de arquivos real.
- Renomear arquivos dentro do sistema de arquivos simulado.
- Remover arquivos do sistema de arquivos simulado.
- Listar todos os arquivos armazenados no sistema de arquivos simulado.
- Exibir o espaço livre dentro do sistema de arquivos simulado.

## Uso

1. **Instalação:**
    - Clone o repositório: git clone https://github.com/gvlk/file-system.git
    -Navegue até o diretório do projeto: cd file-system

2. **Executar a Simulação:**

  - Execute o script principal com as opções desejadas:
    ```bash
    python main.py -s <tamanho_em_MB> -f <arquivo_fs> --copy_to_fs <caminho_arquivo>
    ```
3. **Opções de Linha de Comando:**
    -s, --size: Defina o tamanho do sistema de arquivos simulado em megabytes (padrão: 200).
    -f, --fs_file: Especifique o nome do arquivo do sistema de arquivos simulado (padrão: "furgfs.fs").
    --copy_to_fs: Copie um arquivo do sistema de arquivos real para o sistema de arquivos simulado.

# Licença
Este projeto está licenciado sob a Licença MIT.