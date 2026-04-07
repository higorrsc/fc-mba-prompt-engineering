# Shared Evaluation Infrastructure

Este diretório contém os componentes compartilhados e a infraestrutura básica para execução e avaliação de prompts utilizando plataformas como LangSmith e Langfuse.

## Componentes

### 1. `clients.py`

Gerencia a inicialização e configuração de clientes para LLMs e plataformas de observabilidade.

- **`get_openai_client()`**: Retorna um cliente OpenAI configurado com rastreamento automático para o LangSmith.
- **`get_langsmith_client()` / `get_langfuse_client()`**: Fábricas para instanciar os clientes das respectivas plataformas.
- **Configuração**: Utiliza variáveis de ambiente (`LLM_MODEL`, `LLM_TEMPERATURE`) para padronizar o comportamento dos modelos nos experimentos.

### 2. `datasets.py`

Abstrai a lógica de upload e sincronização de datasets.

- Suporta formatos **JSONL** com metadados personalizados.
- **`upload_langsmith_dataset()`**: Sincroniza arquivos locais com o LangSmith, lidando com a limpeza de versões anteriores e preservação de metadados.
- **`upload_langfuse_dataset()`**: Funcionalidade equivalente para a plataforma Langfuse.

### 3. `evaluators.py`

Contém funções auxiliares (`prepare_data`) para adaptar as saídas dos modelos e os dados dos datasets para os diversos tipos de avaliadores do LangChain.

- **`prepare_prediction_only`**: Para avaliações determinísticas de formato (JSON validity).
- **`prepare_with_input`**: Para critérios que analisam a resposta em relação à pergunta original (ex: utilidade).
- **`prepare_with_reference`**: Para avaliações comparativas que exigem uma "resposta correta" ou referência (ex: embedding distance, correctness).

### 4. `parsers.py`

Utilitários para processamento de respostas dos LLMs.

- **`parse_json_response()`**: Extrai e valida objetos JSON de strings retornadas pelo modelo, lidando de forma robusta com blocos de código markdown (```json ...```).

### 5. `prompts.py`

Gerencia o carregamento e execução de templates de prompts.

- **`load_yaml_prompt()`**: Carrega prompts definidos em arquivos YAML (formato LangChain).
- **`execute_text_prompt()` / `execute_chat_prompt()`**: Abstrai a chamada à API da OpenAI, cuidando da formatação dos inputs e parâmetros do modelo.

## Uso Comum

Os scripts nos diretórios de exercícios (como `p01_basic`) importam estes módulos para manter o código de avaliação focado na técnica que está sendo demonstrada, evitando repetição de código de "boilerplate".
