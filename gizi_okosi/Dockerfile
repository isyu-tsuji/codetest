# ベースイメージを指定
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# 必要なPythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# fugashiモジュールをインストール
RUN pip install fugashi
RUN pip install ipadic
RUN pip install yt-dlp
RUN yt-dlp -x --audio-format mp3 https://www.youtube.com/watch?v=XLuocBQIiXA
RUN pip install git+https://github.com/openai/whisper.git
# スクリプトをコピー
COPY scripts/ scripts/
COPY audio/ audio/
COPY transcriptions/ transcriptions/
COPY corrected_transcriptions/ corrected_transcriptions/
COPY main.py .

# エントリーポイント
CMD ["python", "main.py"]
