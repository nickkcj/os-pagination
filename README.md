# Projeto: Simulador de Gerenciamento de Memória — Paginação

Este projeto é uma implementação educativa de paginação (alocação não contígua) em Python.

Conteúdo
- `main.py` — entrada do simulador (interface interativa CLI)
- `simulador.py` — menu e interação com o usuário
- `gerenciador_memoria.py` — lógica de alocação, remoção e tradução de endereços
- `processo.py` — modelo de processo com memória lógica e tabela de páginas
- `tabela_paginas.py` — estrutura da tabela de páginas
- `configuracao.py` — validação e armazenamento das configurações
- `teste_demo.py` — script não interativo que demonstra as operações e já foi usado para gerar exemplos de saída
- `RELATORIO.md` — relatório do trabalho (rascunho final incluído)

Requisitos
- Python 3.x

Como executar
- Rodar o simulador interativo (o programa pedirá as configurações):

```bash
python3 main.py
```

- Rodar o script de demonstração (gera uma execução pré-definida e imprime a saída):

```bash
python3 teste_demo.py
```

Empacotar para submissão
- O arquivo `ENTREGA_os-pagination.zip` pode ser gerado a partir da raiz do projeto contendo todos os arquivos fontes e o `RELATORIO.md`.

Observações
- Substitua os placeholders em `RELATORIO.md` pelos dados reais do(s) integrante(s) e o link para o vídeo antes de submeter.
- Se quiser, eu posso gerar o ZIP pronto para você agora.
