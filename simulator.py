"""
Interface de linha de comando para o simulador de gerenciamento de memória.
"""

import os
from memory_manager import MemoryManager
from config import Config


class Simulator:
    """Interface CLI para o simulador de gerenciamento de memória"""

    def __init__(self):
        """Inicializa o simulador"""
        # Solicitar configurações ao usuário
        self.configure_system()

        # Criar gerenciador de memória
        self.memory_manager = MemoryManager(
            Config.PHYSICAL_MEMORY_SIZE,
            Config.PAGE_SIZE
        )

    def configure_system(self) -> None:
        """Solicita e configura os parâmetros do sistema"""
        print("\n" + "=" * 70)
        print("   CONFIGURACAO DO SISTEMA DE GERENCIAMENTO DE MEMORIA")
        print("=" * 70)
        print("\nTodos os valores devem ser potencias de 2 (ex: 64, 128, 256, 512, 1024...)")
        print()

        # Solicitar tamanho da memória física
        while True:
            try:
                mem_fisica = self.get_input("Tamanho da memoria fisica (em bytes): ")
                mem_fisica = int(mem_fisica.strip())

                if not Config.is_power_of_two(mem_fisica):
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
                tam_pagina = self.get_input("Tamanho da pagina/quadro (em bytes): ")
                tam_pagina = int(tam_pagina.strip())

                if not Config.is_power_of_two(tam_pagina):
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
                max_processo = self.get_input("Tamanho maximo de um processo (em bytes): ")
                max_processo = int(max_processo.strip())

                if not Config.is_power_of_two(max_processo):
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
            Config.set_configuration(mem_fisica, tam_pagina, max_processo)
            print("\n" + "=" * 70)
            print("[OK] Configuracao realizada com sucesso!")
            print("=" * 70)
        except ValueError as e:
            print(f"\n[ERRO] {e}")
            print("Encerrando programa...")
            exit(1)
    
    def display_menu(self) -> None:
        """Exibe o menu principal"""
        print("\n" + "═" * 60)
        print("       SIMULADOR DE GERENCIAMENTO DE MEMÓRIA - PAGINAÇÃO")
        print("═" * 60)
        print("\nConfigurações:")
        print(f"  • Memória física: {Config.PHYSICAL_MEMORY_SIZE} bytes")
        print(f"  • Tamanho da página: {Config.PAGE_SIZE} bytes")
        print(f"  • Tamanho máximo do processo: {Config.MAX_PROCESS_SIZE} bytes")
        print("\n" + "─" * 60)
        print("1. Visualizar memória física")
        print("2. Criar processo")
        print("3. Remover processo")
        print("4. Visualizar tabela de páginas")
        print("5. Traduzir endereço lógico para físico")
        print("6. Listar processos")
        print("7. Sair")
        print("─" * 60)
    
    def get_input(self, prompt: str) -> str:
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
    
    def visualize_memory(self) -> None:
        """Opção 1: Visualizar memória física"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.memory_manager.display_memory()
        self.get_input("\nPressione ENTER para continuar...")
    
    def create_process_menu(self) -> None:
        """Opção 2: Menu de criação de processo"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "─" * 60)
        print("CRIAR NOVO PROCESSO")
        print("─" * 60)
        
        # Solicitar ID do processo
        id_str = self.get_input("\nInforme o ID do processo (número inteiro): ")

        try:
            process_id = int(id_str.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return
        
        # Solicitar tamanho do processo
        size_str = self.get_input(
            f"Informe o tamanho do processo em bytes (máx {Config.MAX_PROCESS_SIZE}): "
        )
        
        try:
            size = int(size_str.strip())
        except ValueError:
            print("\n[ERRO] Tamanho inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return
        
        # Validar tamanho
        while size <= 0 or size > Config.MAX_PROCESS_SIZE:
            if size > Config.MAX_PROCESS_SIZE:
                print(f"\n[ERRO] Tamanho excede o máximo de {Config.MAX_PROCESS_SIZE} bytes!")
            else:
                print("\n[ERRO] Tamanho deve ser maior que zero!")
            
            size_str = self.get_input(
                f"Informe um tamanho válido (1-{Config.MAX_PROCESS_SIZE} bytes): "
            )
            
            try:
                size = int(size_str.strip())
            except ValueError:
                print("\n[ERRO] Tamanho inválido! Deve ser um número inteiro.")
                self.get_input("\nPressione ENTER para continuar...")
                return
        
        # Criar processo
        self.memory_manager.create_process(process_id, size, Config.MAX_PROCESS_SIZE)
        self.get_input("\nPressione ENTER para continuar...")

    def remove_process_menu(self) -> None:
        """Opção 3: Menu de remoção de processo"""
        print("\n" + "─" * 60)
        print("REMOVER PROCESSO")
        print("─" * 60)

        # Listar processos disponíveis
        if not self.memory_manager.processes:
            print("\n[AVISO] Nenhum processo em execução.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.memory_manager.processes.keys())))

        # Solicitar ID do processo
        id_str = self.get_input("\nInforme o ID do processo a remover: ")

        try:
            process_id = int(id_str.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        # Remover processo
        self.memory_manager.remove_process(process_id)
        self.get_input("\nPressione ENTER para continuar...")

    def display_page_table_menu(self) -> None:
        """Opção 3: Menu de visualização de tabela de páginas"""
        print("\n" + "─" * 60)
        print("VISUALIZAR TABELA DE PÁGINAS")
        print("─" * 60)
        
        # Listar processos disponíveis
        if not self.memory_manager.processes:
            print("\n[AVISO] Nenhum processo em execução.")
            self.get_input("\nPressione ENTER para continuar...")
            return
        
        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.memory_manager.processes.keys())))
        
        # Solicitar ID do processo
        id_str = self.get_input("\nInforme o ID do processo: ")
        
        try:
            process_id = int(id_str.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        # Exibir tabela de páginas
        self.memory_manager.display_page_table(process_id)
        self.get_input("\nPressione ENTER para continuar...")
    
    def translate_address_menu(self) -> None:
        """Opção 5: Menu de tradução de endereços"""
        print("\n" + "─" * 60)
        print("TRADUZIR ENDEREÇO LÓGICO PARA FÍSICO")
        print("─" * 60)

        # Listar processos disponíveis
        if not self.memory_manager.processes:
            print("\n[AVISO] Nenhum processo em execução.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        print("\nProcessos disponíveis:", end=" ")
        print(", ".join(str(pid) for pid in sorted(self.memory_manager.processes.keys())))

        # Solicitar ID do processo
        id_str = self.get_input("\nInforme o ID do processo: ")

        try:
            process_id = int(id_str.strip())
        except ValueError:
            print("\n[ERRO] ID inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        # Verificar se processo existe
        if process_id not in self.memory_manager.processes:
            print(f"\n[ERRO] Processo {process_id} não encontrado!")
            self.get_input("\nPressione ENTER para continuar...")
            return

        process = self.memory_manager.processes[process_id]

        # Solicitar endereço lógico
        addr_str = self.get_input(
            f"\nInforme o endereço lógico (0-{process.size - 1}): "
        )

        try:
            logical_address = int(addr_str.strip())
        except ValueError:
            print("\n[ERRO] Endereço inválido! Deve ser um número inteiro.")
            self.get_input("\nPressione ENTER para continuar...")
            return

        # Traduzir endereço
        result = self.memory_manager.translate_address(process_id, logical_address)

        if result:
            print("\n" + "=" * 60)
            print("RESULTADO DA TRADUÇÃO")
            print("=" * 60)
            print(f"Endereço lógico:     {result['logical_address']}")
            print(f"Número da página:    {result['page_number']}")
            print(f"Deslocamento:        {result['offset']}")
            print(f"Número do quadro:    {result['frame_number']}")
            print(f"Endereço físico:     {result['physical_address']}")
            print(f"Valor armazenado:    0x{result['value']:02x} ({result['value']})")
            print("=" * 60)

        self.get_input("\nPressione ENTER para continuar...")

    def list_processes_menu(self) -> None:
        """Opção 6: Listar processos"""
        self.memory_manager.list_processes()
        self.get_input("\nPressione ENTER para continuar...")
    
    def run(self) -> None:
        """Loop principal do simulador"""
        print("\n>>> Iniciando Simulador de Gerenciamento de Memória...\n")
        
        running = True
        
        while running:
            self.display_menu()
            choice = self.get_input("\nEscolha uma opção: ").strip()
            
            if choice == '1':
                self.visualize_memory()

            elif choice == '2':
                self.create_process_menu()

            elif choice == '3':
                self.remove_process_menu()

            elif choice == '4':
                self.display_page_table_menu()

            elif choice == '5':
                self.translate_address_menu()

            elif choice == '6':
                self.list_processes_menu()

            elif choice == '7':
                print("\nEncerrando simulador...\n")
                running = False

            else:
                print("\n[ERRO] Opção inválida! Por favor, escolha uma opção de 1 a 7.")
                self.get_input("\nPressione ENTER para continuar...")
