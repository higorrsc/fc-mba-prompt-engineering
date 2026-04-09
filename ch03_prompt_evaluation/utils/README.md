# Evaluation Utilities

Este diretório contém scripts utilitários necessários para gerenciar o ambiente de avaliação no LangSmith e calcular métricas de performance.

## Scripts de Gerenciamento

### 1. `upload.py`

Script para sincronizar arquivos `dataset.jsonl` locais com a plataforma **LangSmith**.

- Carrega o dataset de um diretório específico.
- Cria ou atualiza o dataset remotamente.
- Preserva metadados dos exemplos.
- **Execução**:
  ```bash
  python ch03_prompt_evaluation/utils/upload.py --dataset-dir <caminho_do_diretorio> --dataset-name <nome_no_langsmith>
  ```

### 2. `reset.py`

Script utilitário para exclusão de datasets no LangSmith.

- Exclui o dataset e todos os seus históricos de experimentos associados.
- **Execução**:
  ```bash
  python ch03_prompt_evaluation/utils/reset.py --dataset-name <nome_no_langsmith>
  ```

### 3. `metrics.py`

Biblioteca de funções para cálculo de métricas de avaliação.

- **`calculate_precision_recall_f1`**: Implementação genérica para calcular Precisão, Recall e F1-Score.
- **`extract_findings_comparable`**: Extrai campos estruturados (tipo e severidade) de saídas JSON para comparações exatas.
- Usado intensivamente no capítulo de Precisão e Recall.

## Fluxo de Trabalho Recomendado

Antes de iniciar qualquer experimento, certifique-se de que o dataset específico do laboratório foi carregado:

```bash
# Exemplo para o laboratório básico
uv run python ch03_prompt_evaluation/utils/upload.py \
    --dataset-dir ch03_prompt_evaluation/p01_basic \
    --dataset-name evaluation_basic_dataset
```
