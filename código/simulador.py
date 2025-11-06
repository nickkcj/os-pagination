"""
Interface de linha de comando para o simulador de gerenciamento de memória.
"""

import os
from gerenciador_memoria import GerenciadorMemoria
from configuracao import Configuracao


class Simulador:
    """Interface CLI para o simulador de gerenciamento de memória"""

    def __init__(self):
        """Inicializa o simulador"""
        # Solicitar configurações ao usuário
        self.configurar_sistema()

        # Criar gerenciador de memória
        self.gerenciador_memoria = GerenciadorMemoria(
            Configuracao.TAMANHO_MEMORIA_FISICA,
            Configuracao.TAMANHO_PAGINA
        )

    def configurar_sistema(self) -> None:
        """Solicita e configura os parâmetros do sistema"""
        print("\n" + "=" * 70)
        print("   CONFIGURACAO DO SISTEMA DE GERENCIAMENTO DE MEMORIA")
        print("=" * 70)
        print("\nTodos os valores devem ser potencias de 2 (ex: 64, 128, 256, 512, 1024...)")
        print()

        # Solicitar tamanho da memória física
        while True:
            try:
                mem_fisica = self.obter_entrada("Tamanho da memoria fisica (em bytes): ")
                mem_fisica = int(mem_fisica.strip())

                if not Configuracao.eh_potencia_de_dois(mem_fisica):
                    print("[ERRO] O valor deve ser potencia de 2!\n")
                    continue

                break
            except ValueError:
                print("[ERRO] Valor invalido! Digite um numero inteiro.\n")
            except (KeyboardInterrupt, EOFError):
                print("\n\nEncerrando configuracao...")
                exit(0)

        # Solicitar tamanho da página
        while True:
            try:
                tam_pagina = self.obter_entrada("Tamanho da pagina/quadro (em bytes): ")
                tam_pagina = int(tam_pagina.strip())

                if not Configuracao.eh_potencia_de_dois(tam_pagina):
                    print("[ERRO] O valor deve ser potencia de 2!\n")
                    continue

                if tam_pagina > mem_fisica:
                    print(f"[ERRO] A pagina nao pode ser maior que a memoria fisica ({mem_fisica} bytes)!\n")
                    continue

                break
            except ValueError:
                print("[ERRO] Valor invalido! Digite um numero inteiro.\n")
            except (KeyboardInterrupt, EOFError):
                print("\n\nEncerrando configuracao...")
                exit(0)

        # Solicitar tamanho máximo do processo
        while True:
            try:
                max_processo = self.obter_entrada("Tamanho maximo de um processo (em bytes): ")
                max_processo = int(max_processo.strip())

                if not Configuracao.eh_potencia_de_dois(max_processo):
                    print("[ERRO] O valor deve ser potencia de 2!\n")
                    continue

                if max_processo > mem_fisica:
                    print(f"[ERRO] O processo nao pode ser maior que a memoria fisica ({mem_fisica} bytes)!\n")
                    continue

                break
            except ValueError:
                print("[ERRO] Valor invalido! Digite um numero inteiro.\n")
            except (KeyboardInterrupt, EOFError):
                print("\n\nEncerrando configuracao...")
                exit(0)

        # Definir configurações
        try:
            Configuracao.definir_configuracao(mem_fisica, tam_pagina, max_processo)
            print("\n" + "=" * 70)
            print("[OK] Configuracao realizada com sucesso!")
            print("=" * 70)
        except ValueError as e:
            print(f"\n[ERRO] {e}")
            print("Encerrando programa...")
            exit(1)

    def exibir_menu(self) -> None:
        """Exibe o menu principal"""
        print("\n" + "═" * 60)
        print("       SIMULADOR DE GERENCIAMENTO DE MEMÓRIA - PAGINAÇÃO")
        print("═" * 60)
        print("\nConfigurações:")
        print(f"  • Memória física: {Configuracao.TAMANHO_MEMORIA_FISICA} bytes")
        print(f"  • Tamanho da página: {Configuracao.TAMANHO_PAGINA} bytes")
        print(f"  • Tamanho máximo do processo: {Configuracao.TAMANHO_MAXIMO_PROCESSO} bytes")
        print("\n" + "─" * 60)
        print("1. Visualizar memória física")
        print("2. Criar processo")
        print("3. Remover processo")
        print("4. Visualizar tabela de páginas")
        print("5. Traduzir endereço lógico para físico")
        print("6. Listar processos")
        print("7. Sair")
        print("─" * 60)

    def obter_entrada(self, prompt: str) -> str:
        """
        Solicita entrada do usuário.

        Args:
            prompt: Mensagem a ser exibida

        Returns:
            String com a entrada do usuário
        """
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\n\nEncerrando simulador...")
            exit(0)

    def visualizar_memoria(self) -> None:
        """Opção 1: Visualizar memória física"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.gerenciador_memoria.exibir_memoria()
        self.obter_entrada("\nPressione ENTER para continuar...")

    def menu_criar_processo(self) -> None:
        """Opção 2: Menu de criação de processo"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "─" * 60)
        print("CRIAR NOVO PROCESSO")
        print("─" * 60)

        # Solicitar ID do processo
        texto_id = self.obter_entrada("\nInforme o ID do processo (número inteiro): ")

        try:
            id_processo = int(texto_id.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Solicitar tamanho do processo
        texto_tamanho = self.obter_entrada(
            f"Informe o tamanho do processo em bytes (máx {Configuracao.TAMANHO_MAXIMO_PROCESSO}): "
        )

        try:
            tamanho = int(texto_tamanho.strip())
        except ValueError:
            print("\n[ERRO] Tamanho inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Validar tamanho
        while tamanho <= 0 or tamanho > Configuracao.TAMANHO_MAXIMO_PROCESSO:
            if tamanho > Configuracao.TAMANHO_MAXIMO_PROCESSO:
                print(f"\n[ERRO] Tamanho excede o máximo de {Configuracao.TAMANHO_MAXIMO_PROCESSO} bytes!")
            else:
                print("\n[ERRO] Tamanho deve ser maior que zero!")

            texto_tamanho = self.obter_entrada(
                f"Informe um tamanho válido (1-{Configuracao.TAMANHO_MAXIMO_PROCESSO} bytes): "
            )

            try:
                tamanho = int(texto_tamanho.strip())
            except ValueError:
                print("\n[ERRO] Tamanho inválido! Deve ser um número inteiro.")
                self.obter_entrada("\nPressione ENTER para continuar...")
                return

        # Criar processo
        self.gerenciador_memoria.criar_processo(id_processo, tamanho, Configuracao.TAMANHO_MAXIMO_PROCESSO)
        self.obter_entrada("\nPressione ENTER para continuar...")

    def menu_remover_processo(self) -> None:
        """Opção 3: Menu de remoção de processo"""
        print("\n" + "─" * 60)
        print("REMOVER PROCESSO")
        print("─" * 60)

        # Listar processos disponíveis
        if not self.gerenciador_memoria.processos:
            print("\n[AVISO] Nenhum processo em execução.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.gerenciador_memoria.processos.keys())))

        # Solicitar ID do processo
        texto_id = self.obter_entrada("\nInforme o ID do processo a remover: ")

        try:
            id_processo = int(texto_id.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Remover processo
        self.gerenciador_memoria.remover_processo(id_processo)
        self.obter_entrada("\nPressione ENTER para continuar...")

    def menu_exibir_tabela_paginas(self) -> None:
        """Opção 4: Menu de visualização de tabela de páginas"""
        print("\n" + "─" * 60)
        print("VISUALIZAR TABELA DE PÁGINAS")
        print("─" * 60)

        # Listar processos disponíveis
        if not self.gerenciador_memoria.processos:
            print("\n[AVISO] Nenhum processo em execução.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.gerenciador_memoria.processos.keys())))

        # Solicitar ID do processo
        texto_id = self.obter_entrada("\nInforme o ID do processo: ")

        try:
            id_processo = int(texto_id.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Exibir tabela de páginas
        self.gerenciador_memoria.exibir_tabela_paginas(id_processo)
        self.obter_entrada("\nPressione ENTER para continuar...")

    def menu_traduzir_endereco(self) -> None:
        """Opção 5: Menu de tradução de endereços"""
        print("\n" + "─" * 60)
        print("TRADUZIR ENDEREÇO LÓGICO PARA FÍSICO")
        print("─" * 60)

        # Listar processos disponíveis
        if not self.gerenciador_memoria.processos:
            print("\n[AVISO] Nenhum processo em execução.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.gerenciador_memoria.processos.keys())))

        # Solicitar ID do processo
        texto_id = self.obter_entrada("\nInforme o ID do processo: ")

        try:
            id_processo = int(texto_id.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Verificar se processo existe
        if id_processo not in self.gerenciador_memoria.processos:
            print(f"\n[ERRO] Processo {id_processo} não encontrado!")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        processo = self.gerenciador_memoria.processos[id_processo]

        # Solicitar endereço lógico
        texto_endereco = self.obter_entrada(
            f"\nInforme o endereço lógico (0-{processo.tamanho - 1}): "
        )

        try:
            endereco_logico = int(texto_endereco.strip())
        except ValueError:
            print("\n[ERRO] Endereço inválido! Deve ser um número inteiro.")
            self.obter_entrada("\nPressione ENTER para continuar...")
            return

        # Traduzir endereço
        resultado = self.gerenciador_memoria.traduzir_endereco(id_processo, endereco_logico)

        if resultado:
            print("\n" + "=" * 60)
            print("RESULTADO DA TRADUÇÃO")
            print("=" * 60)
            print(f"Endereço lógico:     {resultado['endereco_logico']}")
            print(f"Número da página:    {resultado['numero_pagina']}")
            print(f"Deslocamento:        {resultado['deslocamento']}")
            print(f"Número do quadro:    {resultado['numero_quadro']}")
            print(f"Endereço físico:     {resultado['endereco_fisico']}")
            print(f"Valor armazenado:    0x{resultado['valor']:02x} ({resultado['valor']})")
            print("=" * 60)

        self.obter_entrada("\nPressione ENTER para continuar...")

    def menu_listar_processos(self) -> None:
        """Opção 6: Listar processos"""
        self.gerenciador_memoria.listar_processos()
        self.obter_entrada("\nPressione ENTER para continuar...")

    def executar(self) -> None:
        """Loop principal do simulador"""
        print("\n>>> Iniciando Simulador de Gerenciamento de Memória...\n")

        executando = True

        while executando:
            self.exibir_menu()
            escolha = self.obter_entrada("\nEscolha uma opção: ").strip()

            if escolha == '1':
                self.visualizar_memoria()

            elif escolha == '2':
                self.menu_criar_processo()

            elif escolha == '3':
                self.menu_remover_processo()

            elif escolha == '4':
                self.menu_exibir_tabela_paginas()

            elif escolha == '5':
                self.menu_traduzir_endereco()

            elif escolha == '6':
                self.menu_listar_processos()

            elif escolha == '7':
                print("\nEncerrando simulador...\n")
                executando = False

            else:
                print("\n[ERRO] Opção inválida! Por favor, escolha uma opção de 1 a 7.")
                self.obter_entrada("\nPressione ENTER para continuar...")
