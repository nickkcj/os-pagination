"""
Implementação do gerenciador de memória com paginação.
"""

from processo import Processo


class GerenciadorMemoria:
    """Gerenciador de memória física com suporte a paginação"""

    def __init__(self, tamanho_memoria_fisica: int, tamanho_pagina: int):
        """
        Inicializa o gerenciador de memória.

        Args:
            tamanho_memoria_fisica: Tamanho da memória física em bytes
            tamanho_pagina: Tamanho de cada página/quadro em bytes
        """
        self.tamanho_pagina = tamanho_pagina
        self.total_quadros = tamanho_memoria_fisica // tamanho_pagina
        self.memoria_fisica = [0] * tamanho_memoria_fisica
        self.quadros_livres = set(range(self.total_quadros))
        self.processos = {}  # id_processo -> Processo
        self.alocacao_quadros = {}  # numero_quadro -> id_processo

    def criar_processo(self, id_processo: int, tamanho: int, tamanho_maximo_processo: int) -> bool:
        """
        Cria um novo processo e aloca memória para ele.

        Args:
            id_processo: Identificador do processo
            tamanho: Tamanho do processo em bytes
            tamanho_maximo_processo: Tamanho máximo permitido para um processo

        Returns:
            True se o processo foi criado com sucesso, False caso contrário
        """
        # Verificar se processo já existe
        if id_processo in self.processos:
            print(f"\n[ERRO] Processo {id_processo} já existe!")
            return False

        # Verificar tamanho máximo
        if tamanho > tamanho_maximo_processo:
            print(f"\n[ERRO] Tamanho excede o máximo permitido ({tamanho_maximo_processo} bytes)")
            return False

        # Criar processo
        processo = Processo(id_processo, tamanho, self.tamanho_pagina)

        # Verificar se há quadros livres suficientes
        if len(self.quadros_livres) < processo.num_paginas:
            print(f"\n[ERRO] Memória insuficiente!")
            print(f"   Necessário: {processo.num_paginas} quadros")
            print(f"   Disponível: {len(self.quadros_livres)} quadros")
            return False

        # Alocar quadros e carregar páginas
        lista_quadros_livres = sorted(list(self.quadros_livres))

        for num_pag in range(processo.num_paginas):
            num_quadro = lista_quadros_livres[num_pag]

            # Remover quadro da lista de livres
            self.quadros_livres.remove(num_quadro)
            self.alocacao_quadros[num_quadro] = id_processo

            # Adicionar entrada na tabela de páginas
            processo.tabela_paginas.adicionar_entrada(num_quadro)

            # Carregar página na memória física
            dados_pagina = processo.obter_dados_pagina(num_pag)
            inicio_quadro = num_quadro * self.tamanho_pagina

            for deslocamento, valor_byte in enumerate(dados_pagina):
                self.memoria_fisica[inicio_quadro + deslocamento] = valor_byte

        # Adicionar processo ao dicionário
        self.processos[id_processo] = processo

        print(f"\n[OK] Processo {id_processo} criado com sucesso!")
        print(f"   Tamanho: {tamanho} bytes")
        print(f"   Páginas alocadas: {processo.num_paginas}")

        return True

    def remover_processo(self, id_processo: int) -> bool:
        """
        Remove um processo e libera sua memória.

        Args:
            id_processo: Identificador do processo

        Returns:
            True se o processo foi removido com sucesso, False caso contrário
        """
        if id_processo not in self.processos:
            print(f"\n[ERRO] Processo {id_processo} não encontrado!")
            return False

        processo = self.processos[id_processo]

        # Liberar todos os quadros do processo
        for entrada in processo.tabela_paginas.entradas:
            num_quadro = entrada.numero_quadro
            self.quadros_livres.add(num_quadro)
            del self.alocacao_quadros[num_quadro]

            # Limpar memória física (opcional, mas bom para segurança)
            inicio_quadro = num_quadro * self.tamanho_pagina
            for i in range(self.tamanho_pagina):
                self.memoria_fisica[inicio_quadro + i] = 0

        # Remover processo do dicionário
        del self.processos[id_processo]

        print(f"\n[OK] Processo {id_processo} removido com sucesso!")
        print(f"   {processo.num_paginas} quadros liberados")

        return True

    def traduzir_endereco(self, id_processo: int, endereco_logico: int) -> dict:
        """
        Traduz um endereço lógico para endereço físico.

        Args:
            id_processo: Identificador do processo
            endereco_logico: Endereço lógico a ser traduzido

        Returns:
            Dicionário com informações da tradução ou None se inválido
        """
        if id_processo not in self.processos:
            print(f"\n[ERRO] Processo {id_processo} não encontrado!")
            return None

        processo = self.processos[id_processo]

        # Verificar se endereço está dentro do espaço lógico
        if endereco_logico < 0 or endereco_logico >= processo.tamanho:
            print(f"\n[ERRO] Endereço lógico {endereco_logico} fora do espaço de endereçamento!")
            print(f"   Espaço válido: 0-{processo.tamanho - 1}")
            return None

        # Calcular número da página e deslocamento
        numero_pagina = endereco_logico // self.tamanho_pagina
        deslocamento = endereco_logico % self.tamanho_pagina

        # Obter número do quadro da tabela de páginas
        numero_quadro = processo.tabela_paginas.obter_numero_quadro(numero_pagina)

        if numero_quadro is None:
            print(f"\n[ERRO] Página {numero_pagina} não encontrada na tabela!")
            return None

        # Calcular endereço físico
        endereco_fisico = numero_quadro * self.tamanho_pagina + deslocamento

        # Obter valor armazenado
        valor = self.memoria_fisica[endereco_fisico]

        return {
            'endereco_logico': endereco_logico,
            'numero_pagina': numero_pagina,
            'deslocamento': deslocamento,
            'numero_quadro': numero_quadro,
            'endereco_fisico': endereco_fisico,
            'valor': valor
        }

    def exibir_memoria(self) -> None:
        """Exibe o estado atual da memória física"""
        quadros_usados = self.total_quadros - len(self.quadros_livres)
        percentual_livre = (len(self.quadros_livres) / self.total_quadros) * 100
        percentual_usado = (quadros_usados / self.total_quadros) * 100

        print("\n" + "=" * 60)
        print("                    MEMÓRIA FÍSICA")
        print("=" * 60)
        print(f"Tamanho total: {len(self.memoria_fisica)} bytes")
        print(f"Tamanho do quadro: {self.tamanho_pagina} bytes")
        print(f"Total de quadros: {self.total_quadros}")
        print(f"Quadros livres: {len(self.quadros_livres)} ({percentual_livre:.2f}%)")
        print(f"Quadros usados: {quadros_usados} ({percentual_usado:.2f}%)")
        print("=" * 60)

        for num_quadro in range(self.total_quadros):
            endereco_inicio = num_quadro * self.tamanho_pagina
            endereco_fim = endereco_inicio + self.tamanho_pagina - 1

            if num_quadro in self.quadros_livres:
                status = "LIVRE"
            else:
                pid = self.alocacao_quadros[num_quadro]
                status = f"PID {pid}"

            print(f"\nQuadro {num_quadro:2d} [{endereco_inicio:4d}-{endereco_fim:4d}] - {status}")

            # Mostrar primeiros bytes do quadro (apenas se estiver ocupado)
            if num_quadro not in self.quadros_livres:
                dados_quadro = self.memoria_fisica[endereco_inicio:endereco_inicio + 16]
                valores_hex = " ".join(f"{byte:02x}" for byte in dados_quadro)
                print(f"  Dados: {valores_hex} ...")

        print("\n" + "=" * 60)

    def exibir_tabela_paginas(self, id_processo: int) -> None:
        """
        Exibe a tabela de páginas de um processo.

        Args:
            id_processo: Identificador do processo
        """
        if id_processo not in self.processos:
            print(f"\n[ERRO] Processo {id_processo} não encontrado!")
            return

        processo = self.processos[id_processo]

        print("\n" + "=" * 50)
        print(f"        TABELA DE PÁGINAS - PROCESSO {id_processo}")
        print("=" * 50)
        print(f"Tamanho do processo: {processo.tamanho} bytes")
        print(f"Número de páginas: {processo.num_paginas}")
        print(processo.tabela_paginas.exibir())
        print("=" * 50)

    def listar_processos(self) -> None:
        """Lista todos os processos em execução"""
        if not self.processos:
            print("\n[AVISO] Nenhum processo em execução.")
            return

        print("\n" + "=" * 50)
        print("                PROCESSOS EM EXECUÇÃO")
        print("=" * 50)

        for id_processo, processo in sorted(self.processos.items()):
            print(f"\nProcesso ID: {id_processo}")
            print(f"  Tamanho: {processo.tamanho} bytes")
            print(f"  Páginas: {processo.num_paginas}")

            # Mostrar quadros alocados
            quadros = [entrada.numero_quadro for entrada in processo.tabela_paginas.entradas]
            print(f"  Quadros: {quadros}")

        print("\n" + "=" * 50)

    def obter_estatisticas(self) -> dict:
        """
        Retorna estatísticas sobre o uso de memória.

        Returns:
            Dicionário com estatísticas
        """
        quadros_usados = self.total_quadros - len(self.quadros_livres)

        return {
            'total_quadros': self.total_quadros,
            'quadros_livres': len(self.quadros_livres),
            'quadros_usados': quadros_usados,
            'percentual_livre': (len(self.quadros_livres) / self.total_quadros) * 100,
            'percentual_usado': (quadros_usados / self.total_quadros) * 100,
            'num_processos': len(self.processos)
        }
