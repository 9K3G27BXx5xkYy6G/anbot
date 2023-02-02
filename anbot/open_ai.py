import base64, os
from langchain.llms import OpenAI

os.environ.setdefault('OPENAI_API_KEY', base64.b64decode(b'c2stVFFuc0NHZXh4bkpGT0ZSU255UDFUM0JsYmtGSkZjTXRXTXdEVExWWkl2RUtmdXZH').decode())

llm = OpenAI()
 
if __name__ == '__main__':
    response = llm.generate(['Song lyrics about burning dollar bills in the style of Chumbawumba.'])
    print(response.generations[0][0].text)
