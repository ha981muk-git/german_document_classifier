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
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN pip install --no-cache-dir uvicorn

# Dependencies Layer --no-dev 
COPY pyproject.toml uv.lock* /srv/
RUN uv sync --frozen --no-install-project --no-dev || \
    uv pip install --system $(python -c "import tomllib; print(' '.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))")

# Application Code Layer
# Because of .dockerignore, this will NOW only copy the files we want
COPY . /srv/

# Install the package (Removed '-e')
RUN uv pip install --system .

ENV PYTHONPATH=/srv
ENV PATH="/srv/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"]

#COPY ./models/bert-base-german-cased/ /srv/models/bert-base-german-cased/

# docker build -t german-document-classifier .
# docker run -p 8000:8000 german-document-classifier
# docker run -it --rm german-document-classifier /bin/bash


# clean up failed builds and old images
# docker system prune -a 
# docker build -t german-classifier:debug .
# docker build --no-cache -t german-classifier:debug .
# docker run -it --rm german-classifier:debug /bin/bash
# docker run -p 8000:8000 german-classifier:debug
# curl http://localhost:8000/models


# docker build -t myapp:latest .
# docker tag myapp:latest usr6706/myapp:latest
# docker push usr6706/myapp:latest
