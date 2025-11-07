Trabalho 2 — Gerenciamento de Memória com Paginação

O nosso simulador trabalha com alocação não contígua e permite configurar o tamanho da memória física, o tamanho das páginas (quadros) e o limite máximo de tamanho de um processo.
Também é possível criar e remover processos, visualizar o estado da memória física, consultar as tabelas de páginas e traduzir endereços lógicos para físicos.

Estrutura do Repositório:

- `main.py` — ponto principal do sistema, responsável por iniciar o simulador.  
- `simulador.py` — interface de linha de comando (menu interativo) que faz a comunicação com o usuário.  
- `gerenciador_memoria.py` — responsável pela lógica de gerenciamento da memória (alocação, liberação, tradução e exibição).  
- `processo.py` — define a classe `Processo`, que contém a memória lógica e a tabela de páginas associada.  
- `tabela_paginas.py` — implementa a `TabelaPaginas` e suas entradas (`EntradaTabelaPaginas`).  
- `configuracao.py` — cuida da validação e armazenamento das configurações (todos os tamanhos devem ser potências de 2).


Objetivos do Trabalho

- Simular o funcionamento da paginação com alocação não contígua de quadros.
- Permitir configurar:
  - tamanho da memória física;
  - tamanho da página/quadro;
  - tamanho máximo de um processo.  
- Implementar uma tabela de páginas por processo (armazenando apenas o número do quadro por entrada).  
- Manter uma estrutura que controle os quadros livres (utilizando um `set`).

Entradas e Saídas (Contrato)

Entradas:
- Valores inteiros informados pelo usuário via CLI ou script de teste:  
  `TAMANHO_MEMORIA_FISICA`, `TAMANHO_PAGINA`, `TAMANHO_MAXIMO_PROCESSO`, ID do processo, tamanho do processo e endereço lógico.

Saídas:
- Mensagens informando sucesso ou erro.  
- Exibição do estado da memória física.  
- Tabelas de páginas dos processos.  
- Resultado da tradução de endereços lógicos para físicos.


Principais Classes e Estruturas:

Configuracao (configuracao.py)
Responsável por validar se os tamanhos informados são potências de dois e armazenar as configurações globais do sistema.

Processo (processo.py)
Representa um processo com os seguintes atributos:
- `id` — identificador do processo.  
- `tamanho` — tamanho da memória lógica (em bytes).  
- `tamanho_pagina` — tamanho da página (em bytes).  
- `tabela_paginas` — instância da classe `TabelaPaginas`.  
- `memoria_logica` — lista de bytes gerada aleatoriamente.  
- `num_paginas` — número total de páginas (calculado com `ceil(tamanho / tamanho_pagina)`).

Método principal:
- `obter_dados_pagina(numero_pagina)` — retorna os bytes da página solicitada.

TabelaPaginas (tabela_paginas.py)
Implementa a tabela de páginas como uma lista de `EntradaTabelaPaginas`.

Métodos principais:
- `adicionar_entrada(numero_quadro)` — adiciona o mapeamento entre página e quadro.  
- `obter_numero_quadro(numero_pagina)` — retorna o número do quadro associado.  
- `exibir()` — gera uma representação visual da tabela.

GerenciadorMemoria (gerenciador_memoria.py)
Gerencia toda a memória física do sistema.

Atributos principais:
- `memoria_fisica` — lista de bytes que representa toda a memória física.  
- `tamanho_pagina` — tamanho do quadro em bytes.  
- `total_quadros` — quantidade total de quadros disponíveis.  
- `quadros_livres` — conjunto (`set`) com os índices dos quadros livres.  
- `alocacao_quadros` — mapeia cada quadro para o processo que o ocupa.  
- `processos` — mapeia cada ID de processo para sua instância correspondente.

Principais operações:
- `criar_processo(id, tamanho, max_processo)` — cria um novo processo, verifica se há quadros livres e carrega suas páginas.  
- `remover_processo(id)` — libera os quadros ocupados e limpa a área correspondente da memória física.  
- `traduzir_endereco(id, endereco_logico)` — converte endereço lógico em físico e retorna o valor armazenado.  
- `exibir_memoria()` / `exibir_tabela_paginas(id)` / `listar_processos()` — funções de exibição e depuração.


Fluxo de Alocação de Memória

1. O usuário solicita a criação de um processo, informando ID e tamanho.  
2. O `GerenciadorMemoria` cria uma instância de `Processo` (com bytes aleatórios na memória lógica).  
3. O sistema verifica se há quadros livres suficientes para as páginas do processo.  
4. Cada página é carregada em um quadro livre, o mapeamento é registrado na tabela de páginas e os dados são copiados para a memória física.  
5. Os quadros usados são marcados como ocupados e removidos do conjunto de quadros livres.


Limitações e Considerações

- A tabela de páginas contém apenas o número do quadro (sem bits de controle, como presença ou modificação).  
- Não há substituição de páginas — se a memória estiver cheia, a criação de novos processos falha.  
- A memória lógica é inicializada com bytes aleatórios.  
- O programa é controlado de forma interativa pelo arquivo `main.py`.

Como Executar
Pré-requisito: ter o Python 3.x instalado.

Para rodar o simulador interativo:

```bash
python3 main.py
```

O programa pedirá as configurações iniciais (todas devem ser potências de 2) e exibirá o menu principal.

Sugestões de Casos de Teste

Configuração inicial:
- Memória física: 256 bytes
- Tamanho da página: 32 bytes
- Tamanho máximo do processo: 128 bytes

Passos:
1. Criar processo ID 1 (100 bytes → 4 páginas).
2. Criar processo ID 2 (64 bytes → 2 páginas).
3. Visualizar memória física (verificar quadros alocados para cada PID).
4. Exibir tabelas de páginas dos processos.
5. Traduzir endereço lógico 10 do PID 1.
6. Remover o PID 1 e confirmar a liberação dos quadros.
7. Criar um processo maior que TAMANHO_MAXIMO_PROCESSO → deve gerar erro.
8. Criar processo quando não houver quadros livres suficientes → deve gerar erro de memória insuficiente.

Demonstração Automatizada
O repositório inclui o script teste_demo.py, que executa automaticamente as operações de teste e gera uma saída pronta para inclusão no relatório.

Integrantes do Grupo
- Nicholas Derham
- Nícolas Michielon
- Nicholas Jasper

Vídeo de Apresentação
O vídeo (entre 5 e 10 minutos) pode ser acessado pelo seguinte link:
- `https://drive.google.com/file/d/1rkUozx8ARE9N66H9FD8VEmoAII9tkCeF/view?usp=sharing`

Exemplo de Saída (gerada pelo teste_demo.py)
(trecho real da execução, configuração: 256B de memória física, 32B por página, 128B de tamanho máximo de processo)

(segue o mesmo exemplo completo do original)