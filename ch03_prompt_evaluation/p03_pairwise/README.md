# Chapter 03 - P03: Pairwise Evaluation (A/B Testing)

Este diretório explora a técnica de **Pairwise Evaluation**, onde um "LLM Judge" (Juiz) compara diretamente as saídas de dois prompts diferentes (A e B) para determinar qual oferece maior valor técnico para um dado cenário.

## Visão Geral

Diferente das avaliações determinísticas ou pontuadas, a avaliação pareada (pairwise) simula um teste A/B. Ela é especialmente útil quando queremos comparar especialidades diferentes (ex: Segurança vs. Performance) ou validar se uma nova versão de um prompt (V2) é de fato superior à anterior (V1) em termos de utilidade e clareza.

## Estrutura do Projeto

| Script | Função | Descrição |
| :--- | :--- | :--- |
| `create_prompts.py` | **Setup de Prompts** | Carrega os prompts iniciais (Security Expert e Performance Expert) para o LangSmith Hub. |
| `run.py` | **Execução do Torneio** | Roda os dois prompts contra o dataset e invoca o Juiz para comparar os resultados. |
| `update_prompts.py` | **Evolução (V2)** | Demonstra o ciclo de melhoria, subindo uma versão combinada (Security + Performance) do prompt. |
| `helpers.py` | **Infraestrutura** | Contém o `create_pairwise_evaluator`, que encapsula a lógica de decisão do Juiz (A vs B vs Tie). |

---

## Detalhamento das Estratégias

### 1. Os Especialistas (A e B)

Neste laboratório, comparamos dois perfis distintos:

* **Prompt A (Security Expert):** Focado estritamente em vulnerabilidades como SQL Injection, XSS e Command Injection.
* **Prompt B (Performance Expert):** Focado em gargalos como N+1 queries, vazamentos de memória e concorrência ineficiente.

### 2. O Juiz (Impartial Judge)

O Juiz é um terceiro prompt instruído a ser imparcial. Ele recebe o código original e as duas análises, utilizando os seguintes critérios:

* **Existência Real:** Os achados são fatos ou alucinações?
* **Impacto:** Qual conjunto de problemas tem maior impacto na qualidade do software?
* **Actionability:** Qual feedback é mais claro e fácil para o desenvolvedor aplicar?

---

## Dataset de Teste

### `dataset.jsonl`

Conjunto de dados diversificado contendo exemplos de código Go que misturam falhas de segurança e problemas de performance de alta complexidade.

* **Inputs:** Código Go e linguagem de programação.
* **Outputs:** `expected_findings` apenas para referência humana durante o debug.
* **Metadata:** Categoria predominante e nível de complexidade.

---

## Como Executar

### 1. Preparação (Prompts e Dataset)

Primeiro, envie os prompts para o LangSmith Hub e carregue o dataset:

**Opção A: Via Makefile (Recomendado)**

```bash
# Upload do dataset
make upload DIR=ch03_prompt_evaluation/p03_pairwise NAME=pairwise_initial_comparison

# Reset do dataset (opcional)
make reset NAME=evaluation_precision_dataset
```

**Opção B: Via Comando uv**

```bash
# Criar prompts no Hub
uv run -m ch03_prompt_evaluation.p03_pairwise.create_prompts

# Upload do dataset (usando o utilitário compartilhado)
uv run -m ch03_prompt_evaluation.utils.upload \
    --dataset-dir ch03_prompt_evaluation/p03_pairwise \
    --dataset-name pairwise_initial_comparison
```

### 2. Execução da Comparação

O script `run.py` executará ambos os experimentos e, em seguida, criará um terceiro experimento de comparação (Comparative Experiment) no LangSmith:

```bash
uv run -m ch03_prompt_evaluation.p03_pairwise.run
```

### 3. Ciclo de Melhoria

Após analisar que um especialista ignora problemas do outro, você pode atualizar o prompt para a versão V2 (combinada):

```bash
uv run -m ch03_prompt_evaluation.p03_pairwise.update_prompts
```

## Visualização dos Resultados

Os resultados da comparação pareada são visualizados na aba **"Pairwise Experiments"** do LangSmith.

* **A wins:** A resposta do Security Expert foi considerada melhor.
* **B wins:** A resposta do Performance Expert foi considerada melhor.
* **Tie:** Ambas foram equivalentes em valor.

Esta técnica permite identificar "blind spots" (pontos cegos) em prompts especializados e orientar a criação de prompts mais generalistas e robustos.
