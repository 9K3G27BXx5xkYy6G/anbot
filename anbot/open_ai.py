import base64, os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

os.environ.setdefault('OPENAI_API_KEY', base64.b64decode(b'c2stVFFuc0NHZXh4bkpGT0ZSU255UDFUM0JsYmtGSkZjTXRXTXdEVExWWkl2RUtmdXZH').decode())

llm = OpenAI(temperature=0, frequency_penalty=0.25, max_tokens=256)

_prompt_template = """Use the following pieces of context to answer the question at the end with {answer_form}. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer ({answer_form}):"""
ANSWER_PROMPT = PromptTemplate(
    template=_prompt_template, input_variables=["context", "question", "answer_form"]
)
 
if __name__ == '__main__':
    response = llm.generate(['Song lyrics about burning all wealth in the style of Chumbawumba.'])
    print(response.generations[0][0].text)
