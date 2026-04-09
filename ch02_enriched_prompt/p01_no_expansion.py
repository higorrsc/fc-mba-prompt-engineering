from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

load_dotenv()

llm = init_chat_model(model="openai:gpt-4o-mini", temperature=0.7)

prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are a technology assistant.\nAnswer the following question:\n\n{question}"
    ),
)

chain = prompt | llm | StrOutputParser()

QUESTION = "Explain about the LangChain and LangGraph"

answer = chain.invoke({"question": QUESTION})
print(answer)
print(len(answer))
