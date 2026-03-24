from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .utils import print_llm_result

load_dotenv()

MSG_1 = "What's Brazil's capital?"
MSG_2 = """Find the user intent in the following text:
I'm looking for a restaurant around São Paulo who has a good rating for Japanese food.
"""
MSG_3 = "What's Brazil's capital? Respond only with the city name."

llm = ChatOpenAI(model="gpt-5-nano")
response1 = llm.invoke(MSG_1)
response2 = llm.invoke(MSG_2)
response3 = llm.invoke(MSG_3)

print_llm_result(MSG_1, response1)
print_llm_result(MSG_2, response2)
print_llm_result(MSG_3, response3)
