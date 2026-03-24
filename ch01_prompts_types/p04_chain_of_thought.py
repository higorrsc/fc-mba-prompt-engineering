from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .utils import print_llm_result

load_dotenv()

MSG_1 = """
Classify the log severity.

Input: "Disk usage at 85%."
Answer only with INFO, WARNING, or ERROR.
"""

MSG_2 = """
Classify the log severity.

Input: "Disk usage at 85%."
Think step by step about why this is INFO, WARNING, or ERROR.
At the end, give only the final answer after "Answer:".
"""


MSG_3 = """
Question: How many "r" are in the word "strawberry"?
Answer only with the number of "r".
"""

MSG_4 = """
Question: How many "r" are in the word "strawberry"?
Explain step by step by breaking down each letter in bullet points,
pointing out the "r" before giving the final answer.
Give the final result after "Answer:".
"""

llm = ChatOpenAI(model="gpt-3.5-turbo")
# llm = ChatOpenAI(model="gpt-4o")
# llm = ChatOpenAI(model="gpt-5-nano")  # reasoning model


response1 = llm.invoke(MSG_1)
response2 = llm.invoke(MSG_2)
response3 = llm.invoke(MSG_3)
response4 = llm.invoke(MSG_4)

print_llm_result(MSG_1, response1)
print_llm_result(MSG_2, response2)
print_llm_result(MSG_3, response3)
print_llm_result(MSG_4, response4)
