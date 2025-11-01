"""
Arquivo de configuração do simulador de gerenciamento de memória.
Todos os tamanhos devem ser potências de 2.
As configurações são definidas pelo usuário em tempo de execução.
"""

class Config:
    """Configurações globais do simulador"""

    # Configurações definidas pelo usuário (inicialmente None)
    PHYSICAL_MEMORY_SIZE = None
    PAGE_SIZE = None
    MAX_PROCESS_SIZE = None

    @staticmethod
    def is_power_of_two(n):
        """Verifica se um número é potência de 2"""
        return n > 0 and (n & (n - 1)) == 0

    @staticmethod
    def set_configuration(physical_memory_size, page_size, max_process_size):
        """
        Define as configurações do sistema.

        Args:
            physical_memory_size: Tamanho da memória física em bytes
            page_size: Tamanho da página/quadro em bytes
            max_process_size: Tamanho máximo de um processo em bytes

        Raises:
            ValueError: Se algum valor não for potência de 2 ou inválido
        """
        if not Config.is_power_of_two(physical_memory_size):
            raise ValueError("Tamanho da memoria fisica deve ser potencia de 2")

        if not Config.is_power_of_two(page_size):
            raise ValueError("Tamanho da pagina deve ser potencia de 2")

        if not Config.is_power_of_two(max_process_size):
            raise ValueError("Tamanho maximo do processo deve ser potencia de 2")

        if max_process_size > physical_memory_size:
            raise ValueError("Tamanho maximo do processo nao pode ser maior que a memoria fisica")

        if page_size > physical_memory_size:
            raise ValueError("Tamanho da pagina nao pode ser maior que a memoria fisica")

        Config.PHYSICAL_MEMORY_SIZE = physical_memory_size
        Config.PAGE_SIZE = page_size
        Config.MAX_PROCESS_SIZE = max_process_size

    @staticmethod
    def is_configured():
        """Verifica se as configurações foram definidas"""
        return (Config.PHYSICAL_MEMORY_SIZE is not None and
                Config.PAGE_SIZE is not None and
                Config.MAX_PROCESS_SIZE is not None)