import instructor
import requests
from openai.lib.azure import AzureOpenAI
from pydantic import BaseModel

from utils import logger, settings, search_client


def get_completions(
    messages: list,
    azure_openai_deployment_name: str = settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    azure_openai_endpoint: str = settings.AZURE_OPENAI_ENDPOINT,
    azure_openai_api_key: str = settings.AZURE_OPENAI_API_KEY,
    azure_openai_api_version: str = settings.AZURE_OPENAI_API_VERSION,
    stream: bool = False,
    response_model: BaseModel = None,
    max_tokens: int = 1000,
    temperature: int = 0,
    top_p: int = 1,
    seed: int = 100,
    full_response: bool = False,
) -> str | BaseModel | None:
    """Returns a response from the azure openai model.

    Args:
        messages:
        azure_openai_deployment_name:
        azure_openai_endpoint:
        azure_openai_api_key:
        azure_openai_api_version:
        stream:
        response_model:
        max_tokens:
        temperature:
        top_p:
        seed:
        full_response:

    Returns:
        response : str | BaseModel | None :
    """
    input_dict = {
        "model": azure_openai_deployment_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "seed": seed,
        "stream": stream,
    }
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
    )

    if stream:
        raise NotImplementedError("Stream is not supported right now. Please set stream to False.")

    if response_model:
        client = instructor.from_openai(client)
        input_dict["response_model"] = response_model

    try:
        response = client.chat.completions.create(**input_dict)
    except Exception as e:
        logger.exception(f"Error in chat GPT: {e}")
        logger.error("chat GPT response: None")
        return None

    if full_response or response_model:
        return response
    else:
        return response.choices[0].message.content


def get_related_document_ai_search(question):
    logger.info(f"Azure AI search - find related documents: {question}")

    logger.info("Reformulate QUERY")
    system_prompt = "Tu es un modèle qui a pour fonction de convertir des questions utilisateur en phrase affirmative pour faciliter la recherche par similarité dans une base documentaire vectorielle. Modifiez la phrase utilisateur suivante en ce sens et retirez tout ce qui n'est pas pertinent, comment Bonjour, merci etc. Si c'est dans une autre langue que le Français, traduis la question en Français:"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Convertis cette phrase en affirmative " + question},
    ]
    new_question = get_completions(
        messages=messages,
    )
    logger.debug(f"{question} ==> {new_question}")
    content_docs = []
    results = search_client.search(
        search_text=new_question,
        query_type="semantic",
        query_answer="extractive",
        semantic_configuration_name=settings.SEMENTIC_CONFIGURATION_NAME,
        top=settings.AZURE_SEARCH_TOP_K or 2,
        query_answer_count=settings.AZURE_SEARCH_TOP_K or 2,
        include_total_count=True,
        query_caption="extractive|highlight-true",
    )
    for i, result in enumerate(results):
        for cap in result["@search.captions"]:
            # data = f"Document {i + 1}: {cap.text} \nRéférence: {result['filename']}\n==="
            data = f"Numéro document: {i + 1} - nom document:{result['title']}  - text:{cap.text} \n==="
            content_docs.append(data)
    context = "\n".join(content_docs)
    return context


def get_rag_response(user_input):
    """Return the response after running RAG.

    Args:
        user_input:
        settings:
        conversation_id:

    Returns:
        response:

    """
    logger.info(f"Running RAG")

    context = get_related_document_ai_search(user_input)
    formatted_user_input = f"question :{user_input}, \n\n contexte : \n{context}."
    logger.info(f"RAG - final formatted prompt: {formatted_user_input}")

    response = get_completions(
        messages=[
            {
                "role": "system",
                "content": "Tu est un chatbot qui répond aux questions.",
            },
            {"role": "user", "content": formatted_user_input},
        ],
    )
    return response


def run_azure_ai_search_indexer():
    """Run the azure ai search index.

    Returns:
            res: response
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": settings.AZURE_SEARCH_API_KEY,
    }
    params = {"api-version": "2024-07-01"}
    url = f"{settings.AZURE_SEARCH_SERVICE_ENDPOINT}/indexers('{settings.AZURE_SEARCH_INDEXER_NAME}')/run"

    res = requests.post(url=url, headers=headers, params=params)
    logger.debug(f"run_azure_ai_search_index response: {res.status_code}")
    return res


if __name__ == "__main__":
    print(run_azure_ai_search_indexer())
