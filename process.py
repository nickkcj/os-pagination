"""
Implementação da classe Process (Processo).
"""

import random
import math
from page_table import PageTable


class Process:
    """Representa um processo com sua memória lógica e tabela de páginas"""
    
    def __init__(self, process_id: int, size: int, page_size: int):
        """
        Inicializa um processo.
        
        Args:
            process_id: Identificador único do processo
            size: Tamanho da memória lógica em bytes
            page_size: Tamanho de cada página em bytes
        """
        self.id = process_id
        self.size = size
        self.page_size = page_size
        self.page_table = PageTable()
        self.num_pages = math.ceil(size / page_size)
        self.logical_memory = self._initialize_logical_memory(size)
    
    def _initialize_logical_memory(self, size: int) -> list:
        """
        Inicializa a memória lógica com valores aleatórios.
        
        Args:
            size: Tamanho da memória em bytes
            
        Returns:
            Lista de bytes com valores aleatórios (0-255)
        """
        return [random.randint(0, 255) for _ in range(size)]
    
    def get_page_data(self, page_number: int) -> list:
        """
        Retorna os dados de uma página específica.
        
        Args:
            page_number: Número da página
            
        Returns:
            Lista de bytes da página ou None se inválida
        """
        if page_number < 0 or page_number >= self.num_pages:
            return None
        
        start = page_number * self.page_size
        end = min(start + self.page_size, self.size)
        return self.logical_memory[start:end]
    
    def __repr__(self):
        return f"Process(id={self.id}, size={self.size}, pages={self.num_pages})"