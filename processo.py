"""
Implementação da classe Processo.
"""

import random
import math
from tabela_paginas import TabelaPaginas


class Processo:
    """Representa um processo com sua memória lógica e tabela de páginas"""

    def __init__(self, id_processo: int, tamanho: int, tamanho_pagina: int):
        """
        Inicializa um processo.

        Args:
            id_processo: Identificador único do processo
            tamanho: Tamanho da memória lógica em bytes
            tamanho_pagina: Tamanho de cada página em bytes
        """
        self.id = id_processo
        self.tamanho = tamanho
        self.tamanho_pagina = tamanho_pagina
        self.tabela_paginas = TabelaPaginas()
        self.num_paginas = math.ceil(tamanho / tamanho_pagina)
        self.memoria_logica = self._inicializar_memoria_logica(tamanho)

    def _inicializar_memoria_logica(self, tamanho: int) -> list:
        """
        Inicializa a memória lógica com valores aleatórios.

        Args:
            tamanho: Tamanho da memória em bytes

        Returns:
            Lista de bytes com valores aleatórios (0-255)
        """
        return [random.randint(0, 255) for _ in range(tamanho)]

    def obter_dados_pagina(self, numero_pagina: int) -> list:
        """
        Retorna os dados de uma página específica.

        Args:
            numero_pagina: Número da página

        Returns:
            Lista de bytes da página ou None se inválida
        """
        if numero_pagina < 0 or numero_pagina >= self.num_paginas:
            return None

        inicio = numero_pagina * self.tamanho_pagina
        fim = min(inicio + self.tamanho_pagina, self.tamanho)
        return self.memoria_logica[inicio:fim]

    def __repr__(self):
        return f"Processo(id={self.id}, tamanho={self.tamanho}, paginas={self.num_paginas})"
