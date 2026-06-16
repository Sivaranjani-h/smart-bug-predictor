FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p data/raw data/processed models reports
RUN python src/generate_data.py
RUN python src/preprocess.py
RUN python src/train.py
EXPOSE 7860
CMD ["sh", "-c", "streamlit run app/streamlit_app.py --server.port 7860 --server.address 0.0.0.0"]