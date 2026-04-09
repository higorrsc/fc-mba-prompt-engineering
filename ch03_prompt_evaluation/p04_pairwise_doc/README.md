# Chapter 03 - P04: Pairwise Documentation Evaluation

Este diretório explora a avaliação de prompts para geração de documentação técnica, utilizando tanto métricas de conformidade com uma referência (*ground truth*) quanto a técnica de **Pairwise Comparison** (LLM-as-a-Judge) para comparar diferentes estratégias de escrita.

## Visão Geral

Avaliar documentação gerada por IA é desafiador, pois não existe apenas uma "resposta correta". Este laboratório demonstra como combinar:

1. **Métricas de Alinhamento:** Avaliadores especializados que comparam o estilo, estrutura e tom da documentação gerada com uma referência.
2. **LLM-as-a-Judge (Pairwise):** Um modelo "juiz" que analisa duas saídas simultaneamente e decide qual atende melhor aos critérios de qualidade definidos, utilizando a referência como guia.

## Estrutura do Projeto

| Script / Arquivo | Tipo | Descrição |
| :--- | :--- | :--- |
| `create_prompts.py` | Setup | Registra os prompts `prompt_doc_a` e `prompt_doc_b` no LangSmith Hub. |
| `run.py` | Execução | Realiza a avaliação individual de cada prompt e a comparação pairwise final. |
| `doc_evaluators.py` | Lógica | Define a suíte de 7 avaliadores especializados em qualidade de documentação. |
| `helpers.py` | Lógica | Implementa o juiz de comparação pairwise com lógica de pontuação e justificativa. |
| `prompts/` | Config | Contém as definições YAML dos prompts de geração e do prompt do juiz. |

---

## Estratégias de Documentação

### 1. Prompt A (Structured Technical)

Focado em gerar uma documentação técnica completa, estruturada e detalhada.

* **Foco:** Overview, módulos, fluxo de dados, assinaturas de funções e detalhes de implementação (ex: LangChain, SQL).
* **Estilo:** Técnico, factual e organizado em seções Markdown claras.

### 2. Prompt B (Narrative/High-level)

Focado em uma explicação narrativa e de alto nível para desenvolvedores.

* **Foco:** Funcionalidade geral e utilidade do projeto.
* **Restrição:** Evita especificidades técnicas, exemplos de código ou detalhes de frameworks internos.

---

## Avaliação e Métricas

### Avaliadores de Documentação (Reference-based)

A suíte em `doc_evaluators.py` mede o alinhamento com a referência em 7 eixos:

1. **Conciseness:** Se a verbosidade condiz com a referência.
2. **Detail Level:** Se a profundidade técnica (parâmetros, tipos) é equivalente.
3. **Tone & Style:** Alinhamento de formalidade e complexidade de linguagem.
4. **Structure:** Conformidade de seções, ordem e hierarquia de headers.
5. **Content Coverage:** Se os tópicos essenciais da referência foram abordados.
6. **Terminology:** Consistência no uso de termos técnicos e nomenclaturas.
7. **Faithfulness:** Fidelidade ao código (garante que não houve alucinação de funções).

### Juiz Pairwise (LLM-as-a-Judge)

O juiz (`llm_judge_pairwise.yaml`) compara A e B simultaneamente em 5 dimensões (0-10):

* Completude Estrutural
* Precisão Técnica (Peso maior)
* Clareza e Utilidade
* Alinhamento com a Referência (Peso maior)
* Equilíbrio entre Concisão e Detalhe

---

## Dataset de Teste

### `dataset.jsonl`

O dataset `dataset_docgen` contém:

* **Inputs**: Dicionários contendo o código fonte de múltiplos arquivos Python (ex: `prompts.py`, `utils.py`).
* **Outputs**: `reference` contendo a documentação "padrão ouro" escrita por um especialista para aquele conjunto de arquivos.

---

## Como Executar

### 1. Preparação (Upload do Dataset e Prompts)

Carregue o dataset para o LangSmith e registre os prompts no Hub:

```bash
# Upload do dataset
make upload DIR=ch03_prompt_evaluation/p04_pairwise_doc NAME=dataset_docgen

# Registro dos prompts no LangSmith Hub
uv run -m ch03_prompt_evaluation.p04_pairwise_doc.create_prompts
```

### 2. Execução dos Experimentos

Execute o script principal para rodar as avaliações individuais e a comparação:

```bash
uv run -m ch03_prompt_evaluation.p04_pairwise_doc.run
```

O script executará o seguinte fluxo:

1. Avalia o **Prompt A** contra a referência usando os 7 avaliadores especializados.
2. Avalia o **Prompt B** contra a referência da mesma forma.
3. Realiza a **Comparação Pairwise** entre os resultados de A e B, utilizando o LLM como juiz para gerar um relatório de preferência e justificativas detalhadas no LangSmith.
