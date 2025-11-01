"""
Implementação da tabela de páginas e suas entradas.
"""

class PageTableEntry:
    """Entrada na tabela de páginas"""
    
    def __init__(self, frame_number: int):
        """
        Inicializa uma entrada da tabela de páginas.
        
        Args:
            frame_number: Número do quadro na memória física
        """
        self.frame_number = frame_number
    
    def __repr__(self):
        return f"PageTableEntry(frame={self.frame_number})"


class PageTable:
    """Tabela de páginas de um processo"""
    
    def __init__(self):
        """Inicializa uma tabela de páginas vazia"""
        self.entries = []
    
    def add_entry(self, frame_number: int) -> None:
        """
        Adiciona uma nova entrada na tabela de páginas.
        
        Args:
            frame_number: Número do quadro a ser mapeado
        """
        self.entries.append(PageTableEntry(frame_number))
    
    def get_frame_number(self, page_number: int) -> int:
        """
        Retorna o número do quadro para uma página específica.
        
        Args:
            page_number: Número da página lógica
            
        Returns:
            Número do quadro ou None se a página não existir
        """
        if 0 <= page_number < len(self.entries):
            return self.entries[page_number].frame_number
        return None
    
    def get_num_pages(self) -> int:
        """Retorna o número de páginas na tabela"""
        return len(self.entries)
    
    def display(self) -> str:
        """
        Retorna uma representação formatada da tabela de páginas.

        Returns:
            String com a tabela formatada
        """
        output = [
            "\n+--------------+--------------+",
            "| No da Pagina | No do Quadro |",
            "+--------------+--------------+"
        ]

        for page_num, entry in enumerate(self.entries):
            line = f"| {page_num:>12} | {entry.frame_number:>12} |"
            output.append(line)

        output.append("+--------------+--------------+")
        return "\n".join(output)
    
    def __repr__(self):
        return f"PageTable(entries={len(self.entries)})"