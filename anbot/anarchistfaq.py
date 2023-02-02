import warnings
from urllib.request import urlopen
import bs4
from tqdm import tqdm

URLS = [
        *[
            f'https://www.anarchistfaq.org/afaq/section{section}.html'
            for section in 'ABCDEFGHIJ'
        ],
        'https://www.anarchistfaq.org/afaq/append2.html'
    ]

def fetch(urls = URLS):
    for url in urls:
        with urlopen(url) as doc, warnings.catch_warnings():
            # suppress beautifulsoup's warning regarding selecting the best available parser
            warnings.filterwarnings('ignore', category=bs4.GuessedAtParserWarning)
            soup = bs4.BeautifulSoup(doc)
        # sections preceded by <a name=
        paras = []
        for para in soup.find_all('p'):
            strings = []
            for string in para.get_text().split('\n'):
                string = string.strip()
                if string:
                    strings.append(string)
            paras.append(' '.join(strings))
        yield ('\n\n'.join(paras), dict(source=url))

if __name__ == '__main__':
    import os
    import json
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import FAISS
    from langchain.docstore.document import Document
    from langchain.docstore import InMemoryDocstore
    from .open_ai import embeddings, llm
    def save_faiss(vectordb, name):
        docstore_id_to_index = {value: key for key, value in vectordb.index_to_docstore_id.items()}
        os.makedirs(name + '-docstore', exist_ok=True)
        for id, document in vectordb.docstore._dict.items():
            with open(f'{name}-docstore/{id}.json', 'w') as fh:
                json.dump(
                        dict(
                                metadata = document.metadata,
                                page_content = document.page_content,
                                index = docstore_id_to_index[id],
                        ),
                        fh
                    )
        vectordb.save_local(f'{name}.faiss')
    def load_faiss(name, embeddings):
        vectordb = FAISS(embeddings.embed_query, None, None, {})
        vectordb.load_local(f'{name}.faiss')
        vectordb.docstore = InMemoryDocstore({})
        folder = os.path.abspath(os.path.dirname(name))
        for fn in os.listdir(name+'-docstore'):
            if fn.endswith('.json'):
                id = fn[:-len('.json')]
                with open(os.path.join(name+'-docstore', fn)) as f:
                    document_fields = json.load(f)
                    vectordb.index_to_docstore_id[document_fields.pop('index')] = id
                    document = Document(**document_fields)
                    vectordb.docstore.add({id: document})
        return vectordb
    try:
        vectordb = load_faiss('anarchistfaq', embeddings)
    except RuntimeError:
        print('Downloading documents and calculating embeddings; this can take a while ...')
        text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '. ', ' '],
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
        unzip = lambda iter: zip(*iter)
        texts, metadatas = unzip(fetch())
        documents = text_splitter.create_documents(texts, metadatas=metadatas)
        vectordb = FAISS.from_documents(documents, embeddings)
        save_faiss(vectordb, 'anarchistfaq')
    print('4 portions that relate to "the future":')
    print(vectordb.similarity_search('the future'))
    #for id, doc in vectordb.docstore._dict.items():
    #    print(id)
    #    print(doc)
