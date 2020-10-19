FROM python:3.8-slim
ARG DEBIAN_FRONTEND="noninteractive"
ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"
RUN apt-get update \
    && apt-get install --yes --quiet --no-install-recommends \
        ca-certificates \
        git \
        git-annex \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/neuronets/trained-models
ENV AMS_MODEL_FILE="/opt/neuronets/trained-models/models/sig/ams/meningioma_T1wc_128iso_v1.h5"
RUN git clone https://github.com/neuronets/trained-models.git . \
    && git config user.email "ams" \
    && git config user.name "ams" \
    && git-annex get --quiet "$AMS_MODEL_FILE"

WORKDIR /opt/neuronets/ams
COPY . .
# Only difference between this and gpu Dockerfile is this line (and base image).
RUN pip install --use-feature=2020-resolver --no-cache-dir --editable .[cpu]

# Convert to TFLITE.
ENV AMS_MODEL_FILE_TFLITE="/opt/neuronets/trained-models/models/sig/ams/meningioma_T1wc_128iso_v1_tflite"
RUN python ./scrtipts/convert_to_tflite.py "$AMS_MODEL_FILE" "$AMS_MODEL_FILE_TFLITE"

ENV FREESURFER_HOME="/opt/neuronets/ams/freesurfer"
ENV PATH="$FREESURFER_HOME/bin:$PATH"

WORKDIR /data
ENTRYPOINT ["ams"]
LABEL maintainer="Jakub Kaczmarzyk <jakub.kaczmarzyk@gmail.com>"
