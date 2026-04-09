# Chapter 03 - P02: Precision, Recall and F1-Score

Este diretório explora a avaliação de prompts sob a ótica de métricas de classificação, comparando diferentes estratégias de análise de código (Conservadora, Agressiva e Balanceada) e medindo sua precisão e cobertura.

## Visão Geral

Ao projetar prompts para tarefas de extração ou detecção (como revisão de código), existe um trade-off clássico entre ser muito rigoroso (evitando falsos positivos) ou muito abrangente (evitando falsos negativos). Este laboratório demonstra como quantificar esse comportamento usando Precision, Recall e F1-Score no LangSmith.

## Estrutura do Projeto

| Script | Estratégia | Descrição |
| :--- | :--- | :--- |
| `p01_conservative_high_precision.py` | **High Precision** | Foca em reportar apenas bugs críticos e óbvios com 100% de certeza. Minimiza ruído, mas ignora muitos problemas. |
| `p02_aggressive_high_recall.py` | **High Recall** | Reporta absolutamente tudo que *possa* ser um problema. Garante que nada passe, mas gera muitos alarmes falsos. |
| `p03_balanced_best_f1.py` | **Balanced (Best F1)** | Busca o equilíbrio ideal. Usa camadas de prioridade e instruções de confiança para maximizar a utilidade real. |

---

## Detalhamento das Estratégias

### 1. High Precision (Conservative)

O prompt instrui o modelo a ser um especialista extremamente cauteloso.

* **Foco:** Vulnerabilidades críticas (SQL Injection, XSS, Command Injection).
* **Regra de Ouro:** "Prefira não reportar do que gerar um falso positivo."
* **Resultado esperado:** Precisão próxima de 100%, mas Recall baixo (muitos bugs reais não são detectados).

### 2. High Recall (Aggressive)

O prompt instrui o modelo a suspeitar de tudo e reportar qualquer possibilidade remota.

* **Foco:** Cobertura total de todos os tipos de problemas mapeados.
* **Regra de Ouro:** "É melhor reportar demais do que perder um bug."
* **Resultado esperado:** Recall alto, mas Precisão baixa (o desenvolvedor perde tempo filtrando ruído).

### 3. Balanced (Best F1)

A estratégia mais sofisticada, utilizando camadas de análise e critérios de confiança explícitos (ex: "Reporte apenas se tiver 80%+ de confiança").

* **Foco:** Maximização do F1-Score através de taxonomia clara e guia de severidade.
* **Técnica:** Organiza a análise em camadas (Segurança, Robustez, Qualidade) e fornece exemplos de padrões positivos/negativos.
* **Resultado esperado:** O melhor equilíbrio para uso em produção, capturando bugs importantes com ruído controlado.

---

## Dataset de Teste

### `dataset.jsonl`

Este arquivo contém o conjunto de dados para avaliação de precisão e recall. Diferente do laboratório básico, o gabarito aqui foca estritamente em pares `(type, severity)` para permitir o cálculo exato de métricas de classificação.

* **Inputs**: Trechos de código Go (os mesmos do laboratório básico).
* **Outputs**: `expected_findings` contendo apenas o `type` e a `severity` esperada para cada bug real.
* **Metadata**: Categorias como `security`, `performance`, `robustness` e níveis de dificuldade.

## Como Executar

### 1. Preparação (Upload do Dataset)

Você pode carregar os dados para o LangSmith usando o `Makefile` na raiz do projeto ou executando o script diretamente com `uv`. O nome do dataset deve ser `evaluation_precision_dataset`.

**Opção A: Via Makefile (Recomendado)**

```bash
# Upload do dataset
make upload DIR=ch03_prompt_evaluation/p02_precision NAME=evaluation_precision_dataset

# Reset do dataset (opcional)
make reset NAME=evaluation_precision_dataset
```

**Opção B: Via Comando uv**

```bash
# Upload do dataset
uv run -m ch03_prompt_evaluation.utils.upload \
    --dataset-dir ch03_prompt_evaluation/p02_precision \
    --dataset-name evaluation_precision_dataset

# Reset do dataset (opcional)
uv run -m ch03_prompt_evaluation.utils.reset \
    --dataset-name evaluation_precision_dataset
```

### 2. Execução dos Experimentos

Com o ambiente virtual ativo, execute os scripts de análise:

```bash
# Estratégia Conservadora (High Precision)
uv run -m ch03_prompt_evaluation.p02_precision.p01_conservative_high_precision

# Estratégia Agressiva (High Recall)
uv run -m ch03_prompt_evaluation.p02_precision.p02_aggressive_high_recall

# Estratégia Balanceada (Best F1)
uv run -m ch03_prompt_evaluation.p02_precision.p03_balanced_best_f1
```

## Métricas de Avaliação

Os experimentos utilizam o avaliador customizado `bug_detection_summary`, que compara:

1. **Tipo do Achado:** Deve ser exatamente igual ao esperado (ex: `sql_injection`).
2. **Severidade:** Deve coincidir com o gabarito.

Isso garante que o modelo não seja apenas "premiado" por achar um bug, mas por classificá-lo corretamente conforme o padrão de engenharia definido.
