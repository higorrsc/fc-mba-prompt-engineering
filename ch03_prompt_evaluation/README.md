# Chapter 03: Prompt Evaluation

Este diretório explora técnicas fundamentais e avançadas para a **Avaliação de Prompts**, cobrindo desde validações determinísticas de formato até métricas de classificação (Precisão/Recall) e avaliações comparativas (Pairwise).

## Visão Geral

A avaliação é o pilar da Engenharia de Prompts. Sem métricas claras, é impossível saber se uma alteração no prompt realmente melhorou o sistema ou apenas introduziu novos comportamentos. Este capítulo demonstra como utilizar o **LangSmith** para medir a qualidade das respostas de forma sistemática, utilizando o contexto de revisão de código Go como caso de estudo.

## Estrutura do Projeto

| Diretório | Foco | Descrição |
| :--- | :--- | :--- |
| [`p01_basic/`](./p01_basic) | **Técnicas Básicas** | Avaliações de formato (JSON Schema), critérios binários/pontuados, corretude e distância de embedding. |
| [`p02_precision/`](./p02_precision) | **Métricas de Classificação** | Foco em Precisão, Recall e F1-Score para medir a eficácia na detecção de bugs reais vs. alarmes falsos. |
| [`p03_pairwise/`](./p03_pairwise) | **Avaliação Comparativa** | Técnica de "LLM Judge" para comparar dois prompts diferentes e decidir qual é superior para um dado cenário. |
| [`shared/`](./shared) | **Infraestrutura** | Componentes compartilhados: clientes (OpenAI/LangSmith), evaluators customizados e parsers. |
| [`utils/`](./utils) | **Utilitários** | Scripts para gerenciamento de datasets (upload/reset) e cálculo de métricas matemáticas. |

---

## Detalhamento das Estratégias

### 1. Avaliação Determinística vs. Baseada em LLM

Diferenciamos validações rápidas e baratas (como `JSON Schema` ou `Embedding Distance`) de avaliações semânticas que utilizam um segundo LLM (Judge) para analisar a qualidade, tom e utilidade da resposta.

### 2. O Trade-off de Precisão e Recall

Exploramos como diferentes instruções de prompt afetam a detecção de vulnerabilidades:

* **Conservador:** Alta precisão (poucos erros), mas baixo recall (perde muitos bugs).
* **Agressivo:** Alto recall (acha tudo), mas baixa precisão (muito ruído).
* **Balanceado:** O ponto ideal que maximiza o F1-Score para uso em produção.

### 3. Pairwise Evaluation (A/B Testing)

Demonstramos como colocar dois modelos ou prompts em "combate" técnico, onde um juiz imparcial decide qual saída foi mais útil, permitindo uma evolução iterativa e baseada em dados.

---

## Como Executar

A execução dos experimentos depende da configuração do **LangSmith**. Certifique-se de que suas chaves de API estão no `.env`.

### 1. Preparação dos Dados

Cada laboratório possui seu próprio `dataset.jsonl`. Utilize o script de upload para carregar os dados:

```bash
# Exemplo: Carregando dados do laboratório de precisão
uv run python ch03_prompt_evaluation/utils/upload.py \
    --dataset-dir ch03_prompt_evaluation/p02_precision \
    --dataset-name evaluation_precision_dataset
```

### 2. Execução dos Scripts

Execute os scripts utilizando o módulo Python para garantir que os caminhos e imports sejam resolvidos corretamente:

```bash
# Executar avaliação básica de formato
uv run -m ch03_prompt_evaluation.p01_basic.p01_format_eval

# Executar comparação Pairwise
uv run -m ch03_prompt_evaluation.p03_pairwise.run
```

## Infraestrutura de Avaliação

Para manter os laboratórios limpos, toda a lógica de "boilerplate" está centralizada no diretório `shared/`:

* **`evaluators.py`**: Helpers para preparar dados para o LangChain.
* **`prompts.py`**: Carregamento dinâmico de templates YAML.
* **`clients.py`**: Configuração centralizada de rastreamento e modelos.

---

## Benefícios da Avaliação Sistemática

1. **Reprodutibilidade:** Testes baseados em datasets garantem que os resultados não são frutos do acaso.
2. **Confiança:** Permite deploy de novos prompts com a certeza de que métricas críticas (como segurança) não regrediram.
3. **Visibilidade:** O LangSmith fornece traces detalhados de cada decisão do juiz, facilitando o debugging do prompt.
