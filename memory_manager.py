"""
Implementação do gerenciador de memória com paginação.
"""

from process import Process


class MemoryManager:
    """Gerenciador de memória física com suporte a paginação"""
    
    def __init__(self, physical_memory_size: int, page_size: int):
        """
        Inicializa o gerenciador de memória.
        
        Args:
            physical_memory_size: Tamanho da memória física em bytes
            page_size: Tamanho de cada página/quadro em bytes
        """
        self.page_size = page_size
        self.total_frames = physical_memory_size // page_size
        self.physical_memory = [0] * physical_memory_size
        self.free_frames = set(range(self.total_frames))
        self.processes = {}  # process_id -> Process
        self.frame_allocation = {}  # frame_number -> process_id
    
    def create_process(self, process_id: int, size: int, max_process_size: int) -> bool:
        """
        Cria um novo processo e aloca memória para ele.
        
        Args:
            process_id: Identificador do processo
            size: Tamanho do processo em bytes
            max_process_size: Tamanho máximo permitido para um processo
            
        Returns:
            True se o processo foi criado com sucesso, False caso contrário
        """
        # Verificar se processo já existe
        if process_id in self.processes:
            print(f"\n[ERRO] Processo {process_id} já existe!")
            return False
        
        # Verificar tamanho máximo
        if size > max_process_size:
            print(f"\n[ERRO] Tamanho excede o máximo permitido ({max_process_size} bytes)")
            return False
        
        # Criar processo
        process = Process(process_id, size, self.page_size)
        
        # Verificar se há quadros livres suficientes
        if len(self.free_frames) < process.num_pages:
            print(f"\n[ERRO] Memória insuficiente!")
            print(f"   Necessário: {process.num_pages} quadros")
            print(f"   Disponível: {len(self.free_frames)} quadros")
            return False
        
        # Alocar quadros e carregar páginas
        free_frames_list = sorted(list(self.free_frames))
        
        for page_num in range(process.num_pages):
            frame_num = free_frames_list[page_num]
            
            # Remover quadro da lista de livres
            self.free_frames.remove(frame_num)
            self.frame_allocation[frame_num] = process_id
            
            # Adicionar entrada na tabela de páginas
            process.page_table.add_entry(frame_num)
            
            # Carregar página na memória física
            page_data = process.get_page_data(page_num)
            frame_start = frame_num * self.page_size
            
            for offset, byte_value in enumerate(page_data):
                self.physical_memory[frame_start + offset] = byte_value
        
        # Adicionar processo ao dicionário
        self.processes[process_id] = process

        print(f"\n[OK] Processo {process_id} criado com sucesso!")
        print(f"   Tamanho: {size} bytes")
        print(f"   Páginas alocadas: {process.num_pages}")

        return True

    def remove_process(self, process_id: int) -> bool:
        """
        Remove um processo e libera sua memória.

        Args:
            process_id: Identificador do processo

        Returns:
            True se o processo foi removido com sucesso, False caso contrário
        """
        if process_id not in self.processes:
            print(f"\n[ERRO] Processo {process_id} não encontrado!")
            return False

        process = self.processes[process_id]

        # Liberar todos os quadros do processo
        for entry in process.page_table.entries:
            frame_num = entry.frame_number
            self.free_frames.add(frame_num)
            del self.frame_allocation[frame_num]

            # Limpar memória física (opcional, mas bom para segurança)
            frame_start = frame_num * self.page_size
            for i in range(self.page_size):
                self.physical_memory[frame_start + i] = 0

        # Remover processo do dicionário
        del self.processes[process_id]

        print(f"\n[OK] Processo {process_id} removido com sucesso!")
        print(f"   {process.num_pages} quadros liberados")

        return True

    def translate_address(self, process_id: int, logical_address: int) -> dict:
        """
        Traduz um endereço lógico para endereço físico.

        Args:
            process_id: Identificador do processo
            logical_address: Endereço lógico a ser traduzido

        Returns:
            Dicionário com informações da tradução ou None se inválido
        """
        if process_id not in self.processes:
            print(f"\n[ERRO] Processo {process_id} não encontrado!")
            return None

        process = self.processes[process_id]

        # Verificar se endereço está dentro do espaço lógico
        if logical_address < 0 or logical_address >= process.size:
            print(f"\n[ERRO] Endereço lógico {logical_address} fora do espaço de endereçamento!")
            print(f"   Espaço válido: 0-{process.size - 1}")
            return None

        # Calcular número da página e deslocamento
        page_number = logical_address // self.page_size
        offset = logical_address % self.page_size

        # Obter número do quadro da tabela de páginas
        frame_number = process.page_table.get_frame_number(page_number)

        if frame_number is None:
            print(f"\n[ERRO] Página {page_number} não encontrada na tabela!")
            return None

        # Calcular endereço físico
        physical_address = frame_number * self.page_size + offset

        # Obter valor armazenado
        value = self.physical_memory[physical_address]

        return {
            'logical_address': logical_address,
            'page_number': page_number,
            'offset': offset,
            'frame_number': frame_number,
            'physical_address': physical_address,
            'value': value
        }
    
    def display_memory(self) -> None:
        """Exibe o estado atual da memória física"""
        used_frames = self.total_frames - len(self.free_frames)
        percent_free = (len(self.free_frames) / self.total_frames) * 100
        percent_used = (used_frames / self.total_frames) * 100
        
        print("\n" + "=" * 60)
        print("                    MEMÓRIA FÍSICA")
        print("=" * 60)
        print(f"Tamanho total: {len(self.physical_memory)} bytes")
        print(f"Tamanho do quadro: {self.page_size} bytes")
        print(f"Total de quadros: {self.total_frames}")
        print(f"Quadros livres: {len(self.free_frames)} ({percent_free:.2f}%)")
        print(f"Quadros usados: {used_frames} ({percent_used:.2f}%)")
        print("=" * 60)
        
        for frame_num in range(self.total_frames):
            start_addr = frame_num * self.page_size
            end_addr = start_addr + self.page_size - 1
            
            if frame_num in self.free_frames:
                status = "LIVRE"
            else:
                pid = self.frame_allocation[frame_num]
                status = f"PID {pid}"
            
            print(f"\nQuadro {frame_num:2d} [{start_addr:4d}-{end_addr:4d}] - {status}")
            
            # Mostrar primeiros bytes do quadro (apenas se estiver ocupado)
            if frame_num not in self.free_frames:
                frame_data = self.physical_memory[start_addr:start_addr + 16]
                hex_values = " ".join(f"{byte:02x}" for byte in frame_data)
                print(f"  Dados: {hex_values} ...")
        
        print("\n" + "=" * 60)
    
    def display_page_table(self, process_id: int) -> None:
        """
        Exibe a tabela de páginas de um processo.
        
        Args:
            process_id: Identificador do processo
        """
        if process_id not in self.processes:
            print(f"\n[ERRO] Processo {process_id} não encontrado!")
            return
        
        process = self.processes[process_id]
        
        print("\n" + "=" * 50)
        print(f"        TABELA DE PÁGINAS - PROCESSO {process_id}")
        print("=" * 50)
        print(f"Tamanho do processo: {process.size} bytes")
        print(f"Número de páginas: {process.num_pages}")
        print(process.page_table.display())
        print("=" * 50)
    
    def list_processes(self) -> None:
        """Lista todos os processos em execução"""
        if not self.processes:
            print("\n[AVISO] Nenhum processo em execução.")
            return
        
        print("\n" + "=" * 50)
        print("                PROCESSOS EM EXECUÇÃO")
        print("=" * 50)
        
        for process_id, process in sorted(self.processes.items()):
            print(f"\nProcesso ID: {process_id}")
            print(f"  Tamanho: {process.size} bytes")
            print(f"  Páginas: {process.num_pages}")
            
            # Mostrar quadros alocados
            frames = [entry.frame_number for entry in process.page_table.entries]
            print(f"  Quadros: {frames}")
        
        print("\n" + "=" * 50)
    
    def get_statistics(self) -> dict:
        """
        Retorna estatísticas sobre o uso de memória.
        
        Returns:
            Dicionário com estatísticas
        """
        used_frames = self.total_frames - len(self.free_frames)
        
        return {
            'total_frames': self.total_frames,
            'free_frames': len(self.free_frames),
            'used_frames': used_frames,
            'percent_free': (len(self.free_frames) / self.total_frames) * 100,
            'percent_used': (used_frames / self.total_frames) * 100,
            'num_processes': len(self.processes)
        }