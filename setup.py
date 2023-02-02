from distutils.core import setup

setup(
    name="anbot",
    version="0.0.1",
    description="A chatbot that uses smart caching to interact with upstream API's, such as ChatGPT and GPT-3",
    author="",
    copyright="2023",
    license="GPLv3",
    maintainer="xloem",
    maintainer_email="",
    url="https://github.com/9K3G27BXx5xkYy6G/anbot",
    packages=["anbot"],
    install_requires=["matrix_bot_api", "langchain>=0.0.76", "openai"],
)
