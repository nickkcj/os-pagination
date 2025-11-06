## Simulador de Gerenciamento de Memória (Paginação)

Este projeto foi desenvolvido como parte de um trabalho acadêmico e tem como objetivo demonstrar o funcionamento da paginação na gerência de memória.
A implementação é feita em Python e usa alocação não contígua.

Conteúdo do Projeto

- main.py — ponto de entrada do simulador (interface interativa via CLI).
- simulador.py — responsável pelo menu e pela interação com o usuário.
- gerenciador_memoria.py — contém toda a lógica de alocação, liberação e tradução de endereços.
- processo.py — modela o processo com sua memória lógica e tabela de páginas.
- tabela_paginas.py — define a estrutura da tabela de páginas.
- configuracao.py — faz a validação e o armazenamento das configurações.
- teste_demo.py — script de execução automática usado para gerar saídas de exemplo.
- RELATORIO.md — documento principal com o relatório do trabalho.

Requisitos
Python 3.x instalado no sistema.

Como Executar
Para iniciar o simulador interativo:

```bash
python3 main.py
```

O programa pedirá as configurações de memória e, em seguida, exibirá o menu para criar e gerenciar processos.

Para rodar o script de demonstração automática:

```bash
python3 teste_demo.py
```

Esse modo executa um conjunto pré-definido de operações e mostra a saída completa no terminal.