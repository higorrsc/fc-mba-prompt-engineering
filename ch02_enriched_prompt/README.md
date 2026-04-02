# Chapter 02: Enriched Prompting Techniques

Este diretório explora técnicas avançadas de **Enriched Prompting** (Prompts Enriquecidos), que vão além da estrutura estática do prompt para incluir ciclos de iteração, expansão de consultas e refinamento interativo de contexto.

## Visão Geral

Enquanto o Capítulo 1 focou em *formatar* o pensamento do modelo, este capítulo foca em *enriquecer* a base de conhecimento e o contexto fornecido ao modelo antes ou durante a geração da resposta final. As técnicas aqui demonstradas ajudam a evitar respostas genéricas ou incompletas, garantindo que o LLM tenha todas as informações necessárias para uma execução de alta qualidade.

## Estrutura do Projeto

| Script | Técnica | Descrição |
| :--- | :--- | :--- |
| `p01_no_expansion.py` | **Baseline (No Expansion)** | Execução direta de uma consulta sem qualquer técnica de enriquecimento, servindo como ponto de comparação. |
| `p02_iter_retgen.py` | **Iterative Retrieval-Generation** | Um ciclo de refinamento onde o modelo identifica lacunas de conhecimento (`[MISSING]`), busca informações e preenche os espaços até a resposta estar completa. |
| `p03_query_enrichment.py` | **Query Enrichment (Interactive)** | Transforma consultas vagas em solicitações detalhadas através de um diálogo interativo que extrai entidades e requisitos obrigatórios. |

---

## Detalhamento das Estratégias

### 1. No Expansion (Baseline)

O modo mais simples de interação. Útil para tarefas triviais onde o contexto já é autoevidente.

* **Benefício:** Baixa latência e menor custo de tokens.
* **Quando usar:** Quando a pergunta é direta e não requer dados externos ou especificações técnicas detalhadas.

### 2. Iterative Retrieval-Generation

Esta técnica implementa um processo de "auto-crítica" e expansão incremental.

* **Como funciona:**
    1. Gera um rascunho inicial marcando detalhes técnicos desconhecidos com `[MISSING: ...]`.
    2. Analisa os marcadores e gera "queries" internas para obter esses dados.
    3. Substitui os marcadores por informações reais em múltiplas rodadas.
    4. Expande o texto se detectar que novos detalhes podem ser adicionados.
* **Estratégia de Enriquecimento:** O prompt é enriquecido dinamicamente com os dados coletados em cada iteração, garantindo precisão técnica (versões, métricas, parâmetros).
* **Benefícios:** Reduz alucinações e garante que a resposta final seja exaustiva e fundamentada em fatos.

### 3. Query Enrichment (Interativo)

Focado em garantir que o *input* do usuário seja rico o suficiente para uma tarefa complexa (ex: revisão de código ou análise de logs).

* **Como funciona:**
    1. O modelo analisa a consulta inicial em busca de 6 campos obrigatórios (PR ID, Repo, Branch, Concerns, Style Guide, Test Requirements).
    2. Se faltarem informações, o sistema gera perguntas de esclarecimento.
    3. Após a coleta, o sistema reescreve a consulta original em uma "Natural Enriched Question" altamente detalhada.
* **Estratégia de Enriquecimento:** Extração de entidades e estruturação de contexto via JSON antes da execução da tarefa principal.
* **Benefícios:** Elimina a ambiguidade e garante que o LLM atenda a todos os requisitos de negócio e padrões do projeto.

---

## Como Executar

Certifique-se de estar na **raiz do repositório** e que o ambiente virtual esteja ativo.

### Execução dos Scripts

```bash
# Baseline: Sem expansão
python -m ch02_enriched_prompt.p01_no_expansion

# Refinamento Iterativo (Aguarde as rodadas de preenchimento)
python -m ch02_enriched_prompt.p02_iter_retgen

# Enriquecimento Interativo (O script solicitará inputs no terminal)
python -m ch02_enriched_prompt.p03_query_enrichment
```

## Benefícios do Enriquecimento

1. **Precisão:** Evita que o modelo "adivinhe" detalhes técnicos.
2. **Contexto:** Garante que informações específicas do domínio (como guias de estilo ou nomes de branches) estejam presentes.
3. **Qualidade:** Transforma prompts de uma linha em instruções de nível sênior, resultando em saídas muito mais úteis para o desenvolvedor.
