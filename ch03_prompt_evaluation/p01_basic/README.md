# Basic Prompt Evaluation Techniques

Este diretório contém laboratórios práticos focados em diferentes técnicas de avaliação de prompts, desde validações determinísticas até avaliações semânticas avançadas e detecção de comportamentos indesejados.

## Estrutura de Experimentos

### 1. Validações Determinísticas (Sem LLM Judge)

Scripts que validam a saída do modelo de forma objetiva e rápida:

- **`p01_format_eval.py`**: Valida se a resposta é um JSON válido e se segue estritamente um schema (usando `jsonschema`).
- **`p06_embedding_distance_eval.py`**: Utiliza vetores de embedding para medir a similaridade semântica entre a resposta do modelo e uma resposta de referência (Ground Truth).

### 2. Avaliações Baseadas em Critérios (Binary & Scored)

Usa um LLM (Judge) para analisar a resposta sob critérios específicos:

- **`p02_criteria_binary_eval.py`**: Avaliação do tipo "Passa/Falha" para critérios simples como concisão ou tom.
- **`p03_criteria_score_eval.py`**: Atribui uma pontuação (ex: 1 a 5) para critérios subjetivos como "Utilidade" ou "Relevância".
- **`p05_additional_criteria.py`**: Demonstra como criar e testar critérios personalizados (ex: "Clareza", "Acurácia Técnica").

### 3. Avaliações de Corretude (Labeled)

- **`p04_correctness_eval.py`**: Compara a resposta do modelo com uma resposta de referência utilizando um LLM para decidir se a resposta está correta, mesmo que expressa com palavras diferentes.

### 4. Exemplos de Falhas Comuns ("Bad" Prompts)

Série de scripts que demonstram como os avaliadores detectam problemas típicos de prompts mal estruturados:

- **`p07_bad_text_before.py`**: Problemas com verbosidade desnecessária ou texto antes do formato solicitado.
- **`p08_bad_verbose.py`**: Respostas excessivamente longas que ignoram instruções de concisão.
- **`p09_bad_hallucination.py`**: Detecta quando o modelo inventa informações não presentes no contexto original.
- **`p10_bad_not_helpful.py`**: Respostas que, embora tecnicamente corretas em formato, não resolvem o problema do usuário.

## Subdiretório `prompts/`

Contém as definições dos prompts de sistema e usuários em formato YAML. Estes prompts são carregados pelos scripts para garantir reprodutibilidade e facilitar ajustes de engenharia de prompt sem alterar o código Python.

## Como Executar os Experimentos

1. **Requisito**: Ter configurado as chaves de API (`OPENAI_API_KEY` e `LANGSMITH_API_KEY`) no arquivo `.env`.
2. **Preparação**: Certifique-se de que o dataset base está carregado (veja `utils/README.md`).
3. **Execução**:

    ```bash
    uv run python ch03_prompt_evaluation/p01_basic/p01_format_eval.py
    ```

4. **Visualização**: Os resultados detalhados (traces, scores, comentários do judge) serão enviados para o seu workspace no **LangSmith**.
