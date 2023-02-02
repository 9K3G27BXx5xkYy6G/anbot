import base64, os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import TransformChain, LLMChain, SequentialChain

os.environ.setdefault('OPENAI_API_KEY', base64.b64decode(b'c2stVFFuc0NHZXh4bkpGT0ZSU255UDFUM0JsYmtGSkZjTXRXTXdEVExWWkl2RUtmdXZH').decode())

import openai
class RetryingOpenAIEmbeddings(OpenAIEmbeddings):
    # the langchain funcs that use embeddings don't resume, meaning lost work, so retry on errors
    def _embedding_func(self, *params, **kwparams):
        while True:
            try:
                return super()._embedding_func(*params, **kwparams)
            except openai.error.APIError as er:
                warnings.warn(f'{type(er)}{er.args}')
embeddings = RetryingOpenAIEmbeddings()

llm = OpenAI(temperature=0, frequency_penalty=0.25, max_tokens=256)

_prompt_template = """Use the following pieces of context to answer the question at the end with {answer_form}. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer ({answer_form}):"""

llm_chain = LLMChain.from_string(llm=llm, template=_prompt_template)

## Access was briefly available to purportedly the ChatGPT model via this engine.
##  The outputs needed extra processing.
#CHATGPT_ENGINE = "text-chat-davinci-002-20230126"
#def chatgpt_output_trim(inputs):
#    text = inputs['text']
#    text = text.lstrip()
#    if text.startswith('"'):
#        text = text[1:]
#    if text.endswith('<|im_end|>'):
#        text = text[:-len('<|im_end|>')]
#    if text.endswith('"'):
#        text = text[:-1]
#    return dict(trimmed_text = text)

#llm_chain = SequentialChain(
#        input_variables=["context", "question", "answer_form"],
#        chains=[
#            LLMChain(
#                    llm=llm,
#                    prompt=PromptTemplate(
#                            template=_prompt_template,
#                            input_variables=["context", "question", "answer_form"]
#                        )
#                ),
#            TransformChain(
#                    input_variables=["text"],
#                    output_variables=["trimmed_text"],
#                    transform=chatgpt_output_trim
#                ),
#        ],
#        output_variables=['trimmed_text']
#    )
 
if __name__ == '__main__':
    # caching
    import sqlalchemy
    import langchain
    from langchain.cache import SQLAlchemyCache
    langchain.llm_cache = SQLAlchemyCache(sqlalchemy.create_engine(f"sqlite:///anbot.sqlite"))

    # evaluating
    question = 'What is the best fiscal policy?'
    print(question)
    response = llm_chain.run(
            answer_form='song lyrics in the style of Chumbawumba',
            question=question,
            context='The solution to every problem is burning all wealth and killing all leaders.'
        )
    print(response)
