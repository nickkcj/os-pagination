"""
Implementação da tabela de páginas e suas entradas.
"""

class EntradaTabelaPaginas:
    """Entrada na tabela de páginas"""

    def __init__(self, numero_quadro: int):
        """
        Inicializa uma entrada da tabela de páginas.

        Args:
            numero_quadro: Número do quadro na memória física
        """
        self.numero_quadro = numero_quadro

    def __repr__(self):
        return f"EntradaTabelaPaginas(quadro={self.numero_quadro})"


class TabelaPaginas:
    """Tabela de páginas de um processo"""

    def __init__(self):
        """Inicializa uma tabela de páginas vazia"""
        self.entradas = []

    def adicionar_entrada(self, numero_quadro: int) -> None:
        """
        Adiciona uma nova entrada na tabela de páginas.

        Args:
            numero_quadro: Número do quadro a ser mapeado
        """
        self.entradas.append(EntradaTabelaPaginas(numero_quadro))

    def obter_numero_quadro(self, numero_pagina: int) -> int:
        """
        Retorna o número do quadro para uma página específica.

        Args:
            numero_pagina: Número da página lógica

        Returns:
            Número do quadro ou None se a página não existir
        """
        if 0 <= numero_pagina < len(self.entradas):
            return self.entradas[numero_pagina].numero_quadro
        return None

    def obter_num_paginas(self) -> int:
        """Retorna o número de páginas na tabela"""
        return len(self.entradas)

    def exibir(self) -> str:
        """
        Retorna uma representação formatada da tabela de páginas.

        Returns:
            String com a tabela formatada
        """
        saida = [
            "\n+--------------+--------------+",
            "| No da Pagina | No do Quadro |",
            "+--------------+--------------+"
        ]

        for num_pag, entrada in enumerate(self.entradas):
            linha = f"| {num_pag:>12} | {entrada.numero_quadro:>12} |"
            saida.append(linha)

        saida.append("+--------------+--------------+")
        return "\n".join(saida)

    def __repr__(self):
        return f"TabelaPaginas(entradas={len(self.entradas)})"
