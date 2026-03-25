# Chapter 01: Prompt Engineering Techniques

Este diretório contém uma série de exemplos práticos que exploram diferentes técnicas de **Prompt Engineering**, aplicadas principalmente a cenários de desenvolvimento de software (Go, Backend, APIs e Arquitetura).

## Visão Geral e Estrutura

Os scripts utilizam a biblioteca `LangChain` com modelos da `OpenAI` para demonstrar como diferentes estratégias de escrita de prompts podem influenciar a qualidade, o raciocínio e o formato das respostas do LLM.

| Script | Técnica | Descrição |
| :--- | :--- | :--- |
| `p01_role_prompting.py` | **Role Prompting** | Define personas (ex: Professor Senior vs. Estudante) para mudar o tom e o nível técnico da resposta. |
| `p02_zero_shot.py` | **Zero-Shot** | Solicita uma tarefa diretamente ao modelo, sem fornecer exemplos prévios. |
| `p03_one_few_shot.py` | **One/Few-Shot** | Fornece um ou mais exemplos (shots) para guiar o modelo no formato e estilo desejados. |
| `p04_chain_of_thought.py` | **Chain of Thought (CoT)** | Força o modelo a "pensar passo a passo" antes de chegar à conclusão, melhorando o raciocínio lógico. |
| `p04a_chain_of_thought_self_consistency.py` | **Self-Consistency** | Gera múltiplos caminhos de raciocínio para o mesmo problema e escolhe a resposta mais consistente. |
| `p05_tree_of_thoughts.py` | **Tree of Thoughts (ToT)** | Explora múltiplos ramos de pensamento como uma árvore, avaliando hipóteses antes de decidir a melhor. |
| `p06_skeleton_of_thought.py` | **Skeleton of Thought** | Gera primeiro o "esqueleto" da resposta (tópicos) e depois expande cada ponto detalhadamente. |
| `p07_react.py` | **ReAct** | Combina raciocínio (*Thought*) com ações concretas (*Action*) e observações (*Observation*) para resolver problemas complexos. |
| `p08_prompt_chaining.py` | **Prompt Chaining** | Quebra uma tarefa complexa em uma sequência de chamadas ao LLM, onde a saída de uma alimenta a próxima. |
| `p09_least_to_most.py` | **Least-to-Most** | Decompõe um problema complexo em subproblemas menores e os resolve incrementalmente. |

### Utilitários
- `utils.py`: Contém funções auxiliares para formatar e exibir os resultados no terminal (utilizando a biblioteca `rich`), incluindo a contagem de tokens utilizados.

## Como Executar

Os scripts devem ser executados como módulos Python a partir da **raiz do projeto** para que as importações relativas funcionem corretamente.

### Pré-requisitos

1.  Certifique-se de ter um arquivo `.env` na raiz do projeto com sua chave da OpenAI:
    ```env
    OPENAI_API_KEY=sua_chave_aqui
    ```
2.  Instale as dependências (recomendado usar `uv` ou `pip`):
    ```bash
    uv sync
    # ou
    pip install -r requirements.txt
    ```

### Execução dos Scripts

Execute os scripts utilizando o comando `python -m` seguido pelo caminho do módulo:

```bash
# Exemplo: Role Prompting
python -m ch01_prompts_types.p01_role_prompting

# Exemplo: ReAct
python -m ch01_prompts_types.p07_react

# Exemplo: Tree of Thoughts
python -m ch01_prompts_types.p05_tree_of_thoughts
```

---
*Dica: Execute a partir da pasta raiz do repositório.*
