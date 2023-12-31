"""Main entry point for NoteBot."""

import argparse
import os
from typing import Callable

import gradio as gr
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import GitLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import MarkdownTextSplitter
from langchain.vectorstores import FAISS

from notebot.constants import DB_PATH, NOTE_REPO_URL, NOTES_PATH


class NoteBot:
    """Base class for interacting with NoteBot."""

    def __init__(self, chain) -> None:
        self.chain = chain

    def get_response(self, question: str) -> dict:
        return self.chain({"question": question})

    def chat(self, message: str, history: list) -> str:
        response = self.get_response(question=message)

        return response["answer"]


def filter_notes(file_path: str) -> bool:
    """
    Filter out none markdown notes and READMEs.

    Args:
        file_path (str): Path to file

    Returns:
        bool: Whether to filter out a note
    """
    return file_path.endswith(".md") and not file_path.endswith("README.md")


def load_and_ingest_notes(note_repo_url: str, embedding) -> None:
    """
    Load markdown notes from Git repo and ingest them into vector store.

    Args:
        note_repo_url (str): URL of Git repo to load notes from
        embeddings: Embeddings to use for vector store
    """
    loader = GitLoader(
        repo_path=str(NOTES_PATH),
        clone_url=note_repo_url,
        file_filter=filter_notes,
    )
    splitter = MarkdownTextSplitter()
    docs = loader.load_and_split(text_splitter=splitter)
    db = FAISS.from_documents(documents=docs, embedding=embedding)
    db.save_local(folder_path=str(DB_PATH))


def get_chain(db):
    """
    Get LangChain to interact with notes.

    Args:
        db: Vector store

    Returns:
        LangChain chain
    """
    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=db.as_retriever(), memory=memory
    )

    return chain


def get_ui(chat_function: Callable) -> gr.ChatInterface:
    """
    Create NoteBot user interface

    Args:
        chat_function (Callable): Function to chat with NoteBot

    Returns:
        gr.ChatInterface: User Interface
    """
    ui = gr.ChatInterface(
        fn=chat_function,
        title="NoteBot",
        examples=[
            "List the title of all notes I can ask you about",
            "Generate a brief summary of my LangChain notes",
            "Do I have some notes related to COBOL?",
        ],
        cache_examples=False,
    )

    return ui


def get_parser() -> argparse.ArgumentParser:
    """
    Get argument parser for CLI options.

    Returns:
        argparse.ArgumentParser: Parser
    """
    parser = argparse.ArgumentParser(description="Welcome to NoteBot")
    parser.add_argument(
        "--note-repo-url", help="URL of Git repo to load notes from", default=NOTE_REPO_URL
    )
    parser.add_argument("--llm", help="LLM used by NoteBot", choices=["GPT"], default="GPT")
    parser.add_argument("--openai-api-key", help="API key to interact with OpenAI models")

    return parser


def set_openai_api_key(key: str | None) -> None:
    """
    Set OpenAI API key enviroment variable if it has not been set already.

    Args:
        key (str | None): OpenAI API key
    """
    if not os.environ.get("OPENAI_API_KEY"):
        if key:
            os.environ["OPENAI_API_KEY"] = key
        else:
            load_dotenv()


def app(run_local: bool = True):
    """
    Launch NoteBot app.

    Args:
        run_local (bool, optional): Whether to launch Notebook locally. Defaults to True.
    """
    if run_local:
        parser = get_parser()
        args = parser.parse_args()
        repo_url = args.note_repo_url
        set_openai_api_key(args.openai_api_key)
    else:
        repo_url = NOTE_REPO_URL
        set_openai_api_key(key=None)

    embedding = OpenAIEmbeddings()  # pyright: ignore[reportGeneralTypeIssues]

    if not NOTES_PATH.exists() and not DB_PATH.exists():
        load_and_ingest_notes(note_repo_url=repo_url, embedding=embedding)

    db = FAISS.load_local(folder_path=str(DB_PATH), embeddings=embedding)
    chain = get_chain(db=db)
    notebot = NoteBot(chain=chain)
    ui = get_ui(chat_function=notebot.chat)

    ui.launch()


if __name__ == "__main__":
    app()
