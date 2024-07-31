import requests
import streamlit as st
from azure.storage.blob import BlobServiceClient

from ai import run_azure_ai_search_indexer
from utils import settings

import requests

st.write("# RAG & CHAT")

backend_url = f"http://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}/"

try:
    res = requests.get(backend_url).json()
    st.success(res)
except Exception as e:
    st.exception(f"Error: {e}")
    exit()


st.title("Documents disponibles")

from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={settings.AZURE_STORAGE_ACCOUNT_NAME};AccountKey={settings.AZURE_STORAGE_ACCOUNT_KEY}"
)
container_client = blob_service_client.get_container_client(container=settings.AZURE_CONTAINER_NAME)

blob_list = container_client.list_blobs()

for i, blob in enumerate(blob_list):
    print(f"Name: {blob.name}")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"- {blob.name}")
    with col2:
        if st.button("Supprimer", key=f"button_{i}"):
            container_client.delete_blob(blob.name)
            run_azure_ai_search_indexer()
            st.success("Document supprimé avec succès")


uploaded_file = st.file_uploader("Transférer vos documents")
if uploaded_file:
    blob_service_client = BlobServiceClient.from_connection_string(
        f"DefaultEndpointsProtocol=https;AccountName={settings.AZURE_STORAGE_ACCOUNT_NAME};AccountKey={settings.AZURE_STORAGE_ACCOUNT_KEY}"
    )
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_CONTAINER_NAME, blob=uploaded_file.name
    )
    blob_client.upload_blob(uploaded_file)

    res = run_azure_ai_search_indexer()

    if res.status_code != 202:
        st.error(f"Error: {res.text}")
    else:
        st.success(
            "Documents transférés avec succès. Les documents seront automatiquement supprimés de nos serveurs après la sauvegarde du formulaire"
        )

import streamlit as st


def create_form(questions: list, key: str):
    if f"{key}_responses" in st.session_state:
        responses = st.session_state[f"{key}_responses"]
        successes = st.session_state[f"{key}_success"]
    else:
        responses = {}
        successes = {}
        st.session_state[f"{key}_responses"] = responses
        st.session_state[f"{key}_success"] = successes

    for i, question in enumerate(questions):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- {question[0]}")
        with col2:
            if st.button("Envoyer", key=f"button_{i}_{question[0][:10]}"):
                try:
                    params = {"question": question[1]}
                    res = requests.get(f"{backend_url}/prefix_example/form/", params=params).json()
                    successes[i] = True
                except Exception as e:
                    res = f"Error: {e}"
                    successes[i] = False
                responses[i] = f"{res}"

                st.session_state[f"{key}_responses"][i] = responses[i]
                st.session_state[f"{key}_success"][i] = successes[i]

        if i in responses:
            if successes[i]:
                st.success(f"Réponse automatique:  {responses[i]}")
            else:
                st.error(f"Erreur {responses[i]}")


# the first element is the question displayed in the UI, the second element is the question detailed to be sent to the LLM.
questions = [
    (
        "Quelle est la date de naissance de la personne ?",
        "Quelle est la date de naissance de la personne ?",
    ),
]

st.header("Questions", divider="rainbow")

create_form(questions, key="general")

st.header("Chat", divider="rainbow")
col1, col2 = st.columns([3, 1])
with col1:
    q = st.text_input(key="chat", label="Posez votre question")

params = None
with col2:
    if st.button("Envoyer", key="button_chat"):
        params = {"question": q}

if params:
    try:
        res = requests.get(f"{backend_url}/prefix_example/form/", params=params).json()
        st.success(res)
    except Exception as e:
        res = f"Error: {e}"
        st.error(res)
