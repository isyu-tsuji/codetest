# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# ローカルのrequirements.txtをコンテナ内にコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコンテナ内にコピー
COPY . .

# コンテナ起動時に実行されるコマンド
CMD ["python", "app/main.py"]
