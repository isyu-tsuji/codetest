# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean \
    apt-get install fonts-noto-cjk

# Streamlitをインストール
RUN pip install streamlit

# その他の必要なPythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install matplotlib

# スクリプトをコピー
COPY app/ .

# コンテナ起動時に実行されるコマンド
CMD ["streamlit", "run", "main.py"]