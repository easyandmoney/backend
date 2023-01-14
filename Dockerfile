FROM python:3.10.9-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
COPY easymoney /app/easymoney
CMD ["python", "-m", "easymoney"]
