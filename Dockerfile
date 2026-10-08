FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml* poetry.loc* ./

RUN poetry config virtualenvs.create false
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]