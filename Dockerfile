# -----------------------------------------------------------------------------
# Base Image
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /srv

# -----------------------------------------------------------------------------
# LAYER 1: System Dependencies
# -----------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-deu \
        libgl1 \
        poppler-utils \
        build-essential \
        curl && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# LAYER 2: Install UV
# -----------------------------------------------------------------------------
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# -----------------------------------------------------------------------------
# LAYER 3: Python Dependencies (cached layer)
# -----------------------------------------------------------------------------
COPY pyproject.toml uv.lock* /srv/

# Install dependencies WITHOUT installing the package itself
RUN uv sync --frozen --no-install-project --no-dev || \
    uv pip install --system $(python -c "import tomllib; print(' '.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))")

# -----------------------------------------------------------------------------
# LAYER 4: Application Code
# -----------------------------------------------------------------------------
COPY . /srv/

# Now install the package in editable mode (fast, no dependency reinstall)
RUN uv pip install --system -e .

ENV PYTHONPATH=/srv
#ENV MODEL_DIR=/srv/models/
ENV PATH="/srv/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"]

#COPY ./models/bert-base-german-cased/ /srv/models/bert-base-german-cased/

# clean up failed builds and old images
# docker system prune -a 
# docker run -it --rm german-classifier:debug /bin/bash
# docker run -p 8000:8000 german-classifier:debug
# curl http://localhost:8000/models