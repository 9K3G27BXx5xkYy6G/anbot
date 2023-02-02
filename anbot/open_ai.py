if __name__ == '__main__':
    import os
    os.environ.setdefault('OPENAI_API_KEY', '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')
    from langchain.llms import OpenAI
    openai = OpenAI()
    response = openai.generate(['Song lyrics about burning dollar bills in the style of Chumbawumba.'])
    print(response.generations[0][0].text)
