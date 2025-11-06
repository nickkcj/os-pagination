# Trabalho 2 — Gerenciamento de Memória com Paginação

## Resumo
Este relatório descreve a implementação de um simulador de gerenciamento de memória com paginação (alocação não contígua) desenvolvido em Python. O simulador permite configurar a memória física, o tamanho de página/quadro e o tamanho máximo de processo; criar e remover processos; visualizar a memória física; exibir tabelas de páginas; e traduzir endereços lógicos para físicos.

## Estrutura do Repositório
- `main.py` — ponto de entrada que executa o simulador.
- `simulador.py` — interface de linha de comando (menu) que interage com o usuário.
- `gerenciador_memoria.py` — implementação do gerenciador de memória (alocação, liberação, tradução de endereços, exibição).
- `processo.py` — classe `Processo` que contém a memória lógica e a `TabelaPaginas`.
- `tabela_paginas.py` — implementação da `TabelaPaginas` e `EntradaTabelaPaginas`.
- `configuracao.py` — validação e armazenamento das configurações (tamanhos em potências de 2).

## Objetivos do Trabalho
- Simular paginação com alocação de quadros não contígua.
- Permitir configuração de: tamanho da memória física, tamanho da página/quadro e tamanho máximo de processo.
- Implementar tabela de páginas por processo (apenas número do quadro por entrada).
- Manter estrutura para quadros livres (usado: `set` de quadros livres).

## Contrato (Inputs / Outputs)
- Inputs: valores inteiros pelo usuário (via CLI) ou via script de teste — `TAMANHO_MEMORIA_FISICA`, `TAMANHO_PAGINA`, `TAMANHO_MAXIMO_PROCESSO`, ID do processo, tamanho do processo, endereço lógico.
- Outputs: mensagens informando sucesso/erro, exibição do estado da memória física, tabela de páginas, resultado da tradução de endereço.

## Descrição das Principais Classes e Estruturas
- `Configuracao` (`configuracao.py`): valida potência de dois e armazena configurações globais.

- `Processo` (`processo.py`): representa um processo com os atributos:
  - `id` — identificador inteiro.
  - `tamanho` — tamanho da memória lógica em bytes.
  - `tamanho_pagina` — tamanho de página em bytes.
  - `tabela_paginas` — instância de `TabelaPaginas`.
  - `memoria_logica` — lista de bytes inicializada aleatoriamente.
  - `num_paginas` — número de páginas (ceil(tamanho / tamanho_pagina)).

  Métodos:
  - `obter_dados_pagina(numero_pagina)` — retorna os bytes da página solicitada.

- `TabelaPaginas` (`tabela_paginas.py`): lista de `EntradaTabelaPaginas`.
  - `adicionar_entrada(numero_quadro)` — adiciona mapeamento página -> quadro.
  - `obter_numero_quadro(numero_pagina)` — retorna quadro mapeado.
  - `exibir()` — gera representação tabular da tabela.

- `GerenciadorMemoria` (`gerenciador_memoria.py`): gerencia a memória física:
  - `memoria_fisica` — lista de bytes do tamanho total da memória física.
  - `tamanho_pagina` — bytes por quadro.
  - `total_quadros` — número total de quadros.
  - `quadros_livres` — `set` com índices de quadros livres.
  - `alocacao_quadros` — mapa `numero_quadro -> id_processo`.
  - `processos` — mapa `id_processo -> Processo`.

  Operações principais:
  - `criar_processo(id, tamanho, max_processo)` — cria `Processo`, verifica quadros livres e carrega páginas nos quadros livres (sem substituição).
  - `remover_processo(id)` — libera quadros e limpa memória física.
  - `traduzir_endereco(id, endereco_logico)` — calcula página, deslocamento, obtém quadro e retorna endereço físico + valor.
  - `exibir_memoria()` / `exibir_tabela_paginas(id)` / `listar_processos()`.

## Fluxo de Alocação
1. Usuário solicita criação de um processo com ID e tamanho.
2. `GerenciadorMemoria` instancia `Processo` (gera memória lógica aleatória).
3. Verifica se há quadros livres suficientes: `num_paginas` do processo.
4. Para cada página do processo: pega um quadro livre, registra em `tabela_paginas` e copia bytes da página para `memoria_fisica`.
5. Marca quadros como ocupados em `alocacao_quadros` e remove de `quadros_livres`.

## Limitações e Observações
- Não há bits auxiliares (presente/ausente, modificado, protegido) na tabela de páginas — apenas o número do quadro.
- Não há algoritmo de substituição de páginas; se memória insuficiente, a criação falha.
- A memória lógica do processo é inicializada com bytes aleatórios.
- A interface principal é interativa via `main.py` -> `Simulador`.

## Como executar
Pré-requisito: Python 3.x instalado.

Executar o simulador interativo:

```bash
python3 main.py
```

O simulador pedirá as configurações (todos os valores devem ser potências de dois) e então exibirá o menu.

## Casos de Teste (sugestões)
1. Configuração: memória física 256 bytes, página 32 bytes, máximo processo 128 bytes.
   - Crie processo ID 1, tamanho 100 bytes (4 páginas).
   - Crie processo ID 2, tamanho 64 bytes (2 páginas).
   - Visualize memória física (deve mostrar quadros alocados a PID 1 e PID 2).
   - Exiba tabela de páginas dos processos.
   - Traduza endereço lógico 10 do PID 1 e verifique valor retornado.
   - Remova PID 1 e verifique que quadros foram liberados.

2. Tentar criar processo maior que `TAMANHO_MAXIMO_PROCESSO` (deve falhar com mensagem de erro).
3. Tentar criar processo quando quadros insuficientes (deve falhar com mensagem de memória insuficiente).

## Exemplo de Saída (demo não interativo)
O repositório contém um script `teste_demo.py` (exemplo) que automatiza a configuração e execução de algumas operações para capturar saídas que podem ser incluídas no relatório.

## Nomes dos integrantes do grupo
- Nicholas Derham, Nícolas Michielon, Nicholas Jasper

## Link para vídeo de apresentação

O vídeo de apresentação (5–10 minutos) está incluído no pacote de entrega como arquivo MP4:

`video_do_projeto.mp4`

## Saída de Exemplo (saída real do `teste_demo.py`)

Segue abaixo um trecho da saída gerada pelo script de demonstração `teste_demo.py` (configuração: memória física 256 bytes, página 32 bytes, max processo 128 bytes):

```
=== DEMO: configuracao definida: 256B mem, pagina 32B, max processo 128B ===

-> Criando processo 1 (100 bytes)

[OK] Processo 1 criado com sucesso!
   Tamanho: 100 bytes
   Páginas alocadas: 4

-> Criando processo 2 (64 bytes)

[OK] Processo 2 criado com sucesso!
   Tamanho: 64 bytes
   Páginas alocadas: 2

-> Exibindo memoria fisica:

============================================================
                    MEMÓRIA FÍSICA
============================================================
Tamanho total: 256 bytes
Tamanho do quadro: 32 bytes
Total de quadros: 8
Quadros livres: 2 (25.00%)
Quadros usados: 6 (75.00%)
============================================================

Quadro  0 [   0-  31] - PID 1
  Dados: e5 c9 83 67 06 4b ca c0 5a 17 55 e2 00 15 78 3d ...

Quadro  1 [  32-  63] - PID 1
  Dados: af 94 4c 81 02 93 65 20 bf 56 40 b4 b4 fa 1c da ...

Quadro  2 [  64-  95] - PID 1
  Dados: 18 8d 1e 43 42 3d a8 51 b1 d4 65 59 aa 7e 14 67 ...

Quadro  3 [  96- 127] - PID 1
  Dados: 48 b0 8b 57 00 00 00 00 00 00 00 00 00 00 00 00 ...

Quadro  4 [ 128- 159] - PID 2
  Dados: 52 54 9e 3f b6 5b fe f0 17 50 06 61 25 12 c4 36 ...

Quadro  5 [ 160- 191] - PID 2
  Dados: 37 e2 05 19 57 e6 1a 13 8f aa 21 20 cd 0f f4 b5 ...

Quadro  6 [ 192- 223] - LIVRE

Quadro  7 [ 224- 255] - LIVRE

============================================================

-> Tabela de paginas do processo 1:

==================================================
        TABELA DE PÁGINAS - PROCESSO 1
==================================================
Tamanho do processo: 100 bytes
Número de páginas: 4

+--------------+--------------+
| No da Pagina | No do Quadro |
+--------------+--------------+
|            0 |            0 |
|            1 |            1 |
|            2 |            2 |
|            3 |            3 |
+--------------+--------------+
==================================================

-> Traduzindo enderecos do processo 1:
  L 0 -> Q0 + d0 = F0 (valor=0xe5)
  L 10 -> Q0 + d10 = F10 (valor=0x55)
  L 50 -> Q1 + d18 = F50 (valor=0x7c)
  L 99 -> Q3 + d3 = F99 (valor=0x57)

-> Removendo processo 1

[OK] Processo 1 removido com sucesso!
   4 quadros liberados

-> Exibindo memoria apos remocao:

============================================================
                    MEMÓRIA FÍSICA
============================================================
Tamanho total: 256 bytes
Tamanho do quadro: 32 bytes
Total de quadros: 8
Quadros livres: 6 (75.00%)
Quadros usados: 2 (25.00%)
============================================================

Quadro  0 [   0-  31] - LIVRE

Quadro  1 [  32-  63] - LIVRE

Quadro  2 [  64-  95] - LIVRE

Quadro  3 [  96- 127] - LIVRE

Quadro  4 [ 128- 159] - PID 2
  Dados: 52 54 9e 3f b6 5b fe f0 17 50 06 61 25 12 c4 36 ...

Quadro  5 [ 160- 191] - PID 2
  Dados: 37 e2 05 19 57 e6 1a 13 8f aa 21 20 cd 0f f4 b5 ...

Quadro  6 [ 192- 223] - LIVRE

Quadro  7 [ 224- 255] - LIVRE

============================================================
```
