"""
Script de demonstração não interativo para gerar saídas de exemplo.
Este script configura o sistema, cria alguns processos, exibe memória e tabelas,
traduz alguns endereços e remove um processo.

Executar:
    python3 teste_demo.py
"""

from configuracao import Configuracao
from gerenciador_memoria import GerenciadorMemoria


def main():
    # Definir configuração: memória física 256 B, página 32 B, max processo 128 B
    Configuracao.definir_configuracao(256, 32, 128)

    gm = GerenciadorMemoria(Configuracao.TAMANHO_MEMORIA_FISICA, Configuracao.TAMANHO_PAGINA)

    print("\n=== DEMO: configuracao definida: 256B mem, pagina 32B, max processo 128B ===\n")

    # Criar processo 1 (100 bytes)
    print("-> Criando processo 1 (100 bytes)")
    gm.criar_processo(1, 100, Configuracao.TAMANHO_MAXIMO_PROCESSO)

    # Criar processo 2 (64 bytes)
    print("\n-> Criando processo 2 (64 bytes)")
    gm.criar_processo(2, 64, Configuracao.TAMANHO_MAXIMO_PROCESSO)

    # Exibir memória
    print("\n-> Exibindo memoria fisica:")
    gm.exibir_memoria()

    # Exibir tabela de paginas do processo 1
    print("\n-> Tabela de paginas do processo 1:")
    gm.exibir_tabela_paginas(1)

    # Traduzir alguns endereços do processo 1
    print("\n-> Traduzindo enderecos do processo 1:")
    for addr in [0, 10, 50, 99]:
        res = gm.traduzir_endereco(1, addr)
        if res:
            print(f"  L {res['endereco_logico']} -> Q{res['numero_quadro']} + d{res['deslocamento']} = F{res['endereco_fisico']} (valor=0x{res['valor']:02x})")

    # Remover processo 1
    print("\n-> Removendo processo 1")
    gm.remover_processo(1)

    # Exibir memoria apos remocao
    print("\n-> Exibindo memoria apos remocao:")
    gm.exibir_memoria()


if __name__ == '__main__':
    main()
