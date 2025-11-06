"""
Arquivo de configuração do simulador de gerenciamento de memória.
Todos os tamanhos devem ser potências de 2.
As configurações são definidas pelo usuário em tempo de execução.
"""

class Configuracao:
    """Configurações globais do simulador"""

    # Configurações definidas pelo usuário (inicialmente None)
    TAMANHO_MEMORIA_FISICA = None
    TAMANHO_PAGINA = None
    TAMANHO_MAXIMO_PROCESSO = None

    @staticmethod
    def eh_potencia_de_dois(n):
        """Verifica se um número é potência de 2"""
        return n > 0 and (n & (n - 1)) == 0

    @staticmethod
    def definir_configuracao(tamanho_memoria_fisica, tamanho_pagina, tamanho_maximo_processo):
        """
        Define as configurações do sistema.

        Args:
            tamanho_memoria_fisica: Tamanho da memória física em bytes
            tamanho_pagina: Tamanho da página/quadro em bytes
            tamanho_maximo_processo: Tamanho máximo de um processo em bytes

        Raises:
            ValueError: Se algum valor não for potência de 2 ou inválido
        """
        if not Configuracao.eh_potencia_de_dois(tamanho_memoria_fisica):
            raise ValueError("Tamanho da memoria fisica deve ser potencia de 2")

        if not Configuracao.eh_potencia_de_dois(tamanho_pagina):
            raise ValueError("Tamanho da pagina deve ser potencia de 2")

        if not Configuracao.eh_potencia_de_dois(tamanho_maximo_processo):
            raise ValueError("Tamanho maximo do processo deve ser potencia de 2")

        if tamanho_maximo_processo > tamanho_memoria_fisica:
            raise ValueError("Tamanho maximo do processo nao pode ser maior que a memoria fisica")

        if tamanho_pagina > tamanho_memoria_fisica:
            raise ValueError("Tamanho da pagina nao pode ser maior que a memoria fisica")

        Configuracao.TAMANHO_MEMORIA_FISICA = tamanho_memoria_fisica
        Configuracao.TAMANHO_PAGINA = tamanho_pagina
        Configuracao.TAMANHO_MAXIMO_PROCESSO = tamanho_maximo_processo

    @staticmethod
    def esta_configurado():
        """Verifica se as configurações foram definidas"""
        return (Configuracao.TAMANHO_MEMORIA_FISICA is not None and
                Configuracao.TAMANHO_PAGINA is not None and
                Configuracao.TAMANHO_MAXIMO_PROCESSO is not None)
