FROM python:3.10-slim

WORKDIR /srv

# System Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-deu \
        libgl1 \
        poppler-utils \
        build-essential \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install UV
# Pin the version of uv for reproducible builds, 0.1.41
COPY --from=ghcr.io/astral-sh/uv:0.1.41 /uv /bin/uv

# Dependencies Layer --no-dev 
COPY pyproject.toml uv.lock* /srv/

# Install dependencies with pip via uv
#    '--system' to install into the main Python environment
#    '--extra-index-url' to find CPU versions of Torch
#    '-r pyproject.toml' so uv reads requirements directly 
RUN uv pip install --system --no-cache \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r pyproject.toml
# Application Code Layer
# Because of .dockerignore, this will NOW only copy the files 
COPY . /srv/

# Install the package (Removed '-e')
RUN uv pip install --system --no-deps .

ENV PYTHONPATH=/srv

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /srv

USER appuser


EXPOSE 8080

CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8080"]

#COPY ./models/bert-base-german-cased/ /srv/models/bert-base-german-cased/

# docker build -t german-document-classifier .
# docker run -p 8080:8080 german-document-classifier
# docker run -it --rm german-document-classifier /bin/bash


# clean up failed builds and old images
# docker system prune -a 
# docker build -t german-classifier:debug .
# docker build --no-cache -t german-classifier:debug .
# docker run -it --rm german-classifier:debug /bin/bash
# docker run -p 8080:8080 german-classifier:debug
# curl http://localhost:8080/models


# docker build --platform linux/amd64 -t myapp . # testing in digital ocean or other linux platforms
# docker tag myapp:latest usr6706/myapp:latest
# docker push usr6706/myapp:latest
