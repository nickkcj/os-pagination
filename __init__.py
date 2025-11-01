"""
Simulador de Gerenciamento de Memória com Paginação
"""

__version__ = "1.0.0"
__author__ = "Sistemas Operacionais"

from .config import Config
from .page_table import PageTable, PageTableEntry
from .process import Process
from .memory_manager import MemoryManager
from .simulator import Simulator

__all__ = [
    'Config',
    'PageTable',
    'PageTableEntry',
    'Process',
    'MemoryManager',
    'Simulator'
]