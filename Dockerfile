FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files and source (needed to build the local package)
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "ad_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
