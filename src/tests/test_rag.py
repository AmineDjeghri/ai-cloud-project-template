import os

from ai import get_related_document_ai_search, get_rag_response, run_azure_ai_search_indexer
from utils import logger

logger.info(f" working directory is {os.getcwd()}")


def test_get_related_document_ai_search():
    user_input = "What is the capital of France?"
    question_context = get_related_document_ai_search(user_input)

    assert type(question_context) == str


def test_get_rag_response():
    res = get_rag_response("What is the capital of France?")
    assert type(res) == str


def test_run_azure_ai_search_indexer():
    assert run_azure_ai_search_indexer().status_code == 202
