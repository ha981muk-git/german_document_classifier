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

# Install UV and uvicorn
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Dependencies Layer (copied before application code for better caching)
COPY pyproject.toml uv.lock* /srv/

# Install dependencies with uv
# '--system' installs into the main Python environment (no venv needed in containers)
# '--extra-index-url' finds CPU versions of PyTorch
RUN uv pip install --system --no-cache \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r pyproject. toml

# Application Code Layer
# . dockerignore ensures only necessary files are copied
COPY . /srv/

# Install the package itself (--no-deps prevents reinstalling dependencies)
RUN uv pip install --system --no-deps . 

# Environment variables
ENV PYTHONPATH=/srv

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser: appuser /srv
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["uvicorn", "app.api. api:app", "--host", "0.0.0.0", "--port", "8080"]

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