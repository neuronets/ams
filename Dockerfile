FROM continuumio/conda-ci-linux-64-python3.8:latest as base

ARG AMS_COMMITISH="19e69299"

USER root

RUN apt-get update \
    && apt-get install --yes --quiet --no-install-recommends \
        ca-certificates \
        git \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN conda install -c conda-forge --yes git-annex && conda clean --all

RUN pip install --quiet --no-cache-dir datalad datalad-osf

WORKDIR /opt/neuronets/trained-models
ENV AMS_MODEL_FILE="/opt/neuronets/trained-models/neuronets/ams/0.1.0/meningioma_T1wc_128iso_v1.h5"

RUN datalad clone https://github.com/neuronets/trained-models.git . \
    && git config user.name "ams" \ 
    && git config user.email "ams" \   
    && datalad get -s osf-storage "$AMS_MODEL_FILE" \
    && git checkout "$AMS_COMMITISH"


FROM python:3.8-slim
ARG DEBIAN_FRONTEND="noninteractive"

COPY --from=base /opt/neuronets/trained-models /opt/neuronets/trained-models

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN apt-get update \
    && apt-get install --yes --quiet --no-install-recommends \
        ca-certificates \
        libgomp1 \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/neuronets/ams
COPY . .

ENV AMS_MODEL_FILE="/opt/neuronets/trained-models/neuronets/ams/0.1.0/meningioma_T1wc_128iso_v1.h5"

# Only difference between this and gpu Dockerfile is this line.
RUN pip install --use-feature=2020-resolver --no-cache-dir --editable .[cpu]

ENV FREESURFER_HOME="/opt/neuronets/ams/freesurfer"
ENV PATH="$FREESURFER_HOME/bin:$PATH"

WORKDIR /data
ENTRYPOINT ["ams"]
LABEL maintainer="Jakub Kaczmarzyk <jakub.kaczmarzyk@gmail.com>"
