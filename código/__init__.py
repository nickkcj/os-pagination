"""
Simulador de Gerenciamento de Memória com Paginação
"""

__version__ = "1.0.0"
__author__ = "Sistemas Operacionais"

from .configuracao import Configuracao
from .tabela_paginas import TabelaPaginas, EntradaTabelaPaginas
from .processo import Processo
from .gerenciador_memoria import GerenciadorMemoria
from .simulador import Simulador

__all__ = [
    'Configuracao',
    'TabelaPaginas',
    'EntradaTabelaPaginas',
    'Processo',
    'GerenciadorMemoria',
    'Simulador'
]
