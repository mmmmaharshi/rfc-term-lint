FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir "mcp>=2"
COPY server.py rfc_terms.json domain_terms.json ./
ENV TRANSPORT=streamable-http PORT=8000
EXPOSE 8000
CMD ["python", "server.py"]
