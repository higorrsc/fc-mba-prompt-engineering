# Evaluation Utilities

Este diretório contém os recursos e scripts utilitários necessários para preparar o ambiente de avaliação e gerenciar os datasets de teste.

## Recursos Principal

### `dataset.jsonl`

Este arquivo contém os exemplos de teste utilizados nos experimentos de avaliação.

- Cada linha é um objeto JSON com campos:
  - **`inputs`**: A entrada que será passada para o modelo (ex: código fonte para análise).
  - **`outputs`**: A saída de referência ou "Ground Truth" esperada.
  - **`metadata`**: Informações adicionais (ex: `language`, `complexity`) que podem ser usadas para filtrar resultados no LangSmith.

## Scripts de Gerenciamento

### 1. `upload.py`

Script para sincronizar o arquivo `dataset.jsonl` local com a plataforma **LangSmith**.

- Carrega o dataset local.
- Cria o dataset remotamente se ele não existir.
- Limpa versões antigas para garantir consistência.
- Preserva metadados dos exemplos.
- **Execução**: `python ch03_prompt_evaluation/utils/upload.py`

### 2. `reset.py`

Script utilitário para "limpeza profunda" do ambiente LangSmith.

- Localiza o dataset principal (`evaluation_basic_dataset`).
- Exclui o dataset e todos os seus históricos de experimentos associados.
- Útil para reinicializar o laboratório do zero.
- **Execução**: `python ch03_prompt_evaluation/utils/reset.py`

## Fluxo de Trabalho Recomendado

Antes de iniciar qualquer experimento no diretório `p01_basic`, certifique-se de que o dataset está carregado e atualizado executando o script de upload:

```bash
uv run python ch03_prompt_evaluation/utils/upload.py
```
