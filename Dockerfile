# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /azure-rag

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ARG STREAMLIT_PORT
ENV STREAMLIT_PORT=${STREAMLIT_PORT:-8000}
# EXPOSE IS JUST FOR DOCUMENTATION. IT DOES NOT PUBLISH THE PORT. YOU need to use -p flag to publish the port
EXPOSE ${STREAMLIT_PORT}

HEALTHCHECK CMD curl --fail http://localhost:${STREAMLIT_PORT}/_stcore/health

CMD ["make", "run_all"]
