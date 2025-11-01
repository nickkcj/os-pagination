"""
Ponto de entrada principal do simulador de gerenciamento de memória.

Para executar:
    python main.py

Você pode modificar as configurações no arquivo config.py
"""

from simulator import Simulator


def main():
    """Função principal"""
    try:
        simulator = Simulator()
        simulator.run()
    except KeyboardInterrupt:
        print("\n\nSimulador interrompido pelo usuário.\n")
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}\n")
        raise


if __name__ == "__main__":
    main()