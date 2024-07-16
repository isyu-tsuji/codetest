以下に、Dockerfileを使った構成を提案します。この構成では、Dockerコンテナ内で音声データを文字起こしし、補正する環境を作成します。これにより、一貫した開発環境を提供し、依存関係の管理が容易になります。

### フォルダ構成

```
project-root/
│
├── audio/                   # 音声ファイルを格納するディレクトリ
│   └── example_audio.wav    # 例: 音声ファイル
│
├── transcriptions/          # 文字起こし結果を格納するディレクトリ
│   └── example_audio.txt    # 例: Whisperによる文字起こし結果
│
├── corrected_transcriptions/# 校正後の文字起こし結果を格納するディレクトリ
│   └── example_audio_corrected.txt # 例: BERTによる校正結果
│
├── scripts/                 # 各ステップのスクリプトを格納するディレクトリ
│   ├── transcribe.py        # 文字起こしを行うスクリプト
│   ├── correct.py           # 文字起こしを校正するスクリプト
│   └── main.py              # 全体のプロセスを管理するスクリプト
│
├── Dockerfile               # Dockerfile
└── requirements.txt         # 必要なパッケージを記載するファイル
```

### `requirements.txt`

必要なPythonパッケージを記載します。

```txt
transformers
torch
whisper
language_tool_python
```

### `Dockerfile`

Dockerfileを作成して、必要な依存関係をインストールします。

```Dockerfile
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

# スクリプトをコピー
COPY scripts/ scripts/
COPY audio/ audio/
COPY transcriptions/ transcriptions/
COPY corrected_transcriptions/ corrected_transcriptions/
COPY main.py .

# エントリーポイント
CMD ["python", "main.py"]
```

### スクリプトの実装

#### `transcribe.py`

```python
import whisper
import os

def transcribe_audio(file_path, output_dir):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".wav", ".txt"))
    with open(output_file, "w") as f:
        f.write(result['text'])
    return output_file

if __name__ == "__main__":
    audio_dir = "audio"
    transcription_dir = "transcriptions"
    if not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".wav"):
            transcribe_audio(os.path.join(audio_dir, audio_file), transcription_dir)
```

#### `correct.py`

```python
import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
import os

# Load pre-trained tokenizer and model
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
model = BertForMaskedLM.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

def correct_speech_text(text):
    # Tokenize input text and create masked tokens
    tokens = tokenizer.tokenize(text)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    masked_input_ids = [tokenizer.mask_token_id if token == tokenizer.cls_token else token_id for token, token_id in zip(tokens, input_ids)]

    # Convert to PyTorch tensors
    input_ids = torch.tensor([input_ids])
    masked_input_ids = torch.tensor([masked_input_ids])

    # Get predictions from BERT model
    with torch.no_grad():
        outputs = model(input_ids, labels=masked_input_ids)
        predictions = outputs.logits

    # Get the predicted tokens
    predicted_token_ids = predictions.argmax(dim=-1).tolist()[0]
    predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_token_ids)

    # Reconstruct the corrected text
    corrected_text = tokenizer.convert_tokens_to_string(predicted_tokens)
    return corrected_text

def process_file(file_path, output_dir):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    corrected_text = correct_speech_text(text)

    output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".txt", "_corrected.txt"))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(corrected_text)
    return output_file

if __name__ == "__main__":
    transcription_dir = "transcriptions"
    corrected_dir = "corrected_transcriptions"
    if not os.path.exists(corrected_dir):
        os.makedirs(corrected_dir)

    for transcription_file in os.listdir(transcription_dir):
        if transcription_file.endswith(".txt"):
            process_file(os.path.join(transcription_dir, transcription_file), corrected_dir)
```

#### `main.py`

```python
import os
from scripts.transcribe import transcribe_audio
from scripts.correct import process_file

def main():
    audio_dir = "audio"
    transcription_dir = "transcriptions"
    corrected_dir = "corrected_transcriptions"

    if not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir)
    if not os.path.exists(corrected_dir):
        os.makedirs(corrected_dir)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".wav"):
            transcription_file = transcribe_audio(os.path.join(audio_dir, audio_file), transcription_dir)
            process_file(transcription_file, corrected_dir)

if __name__ == "__main__":
    main()
```

### Dockerコンテナのビルドと実行

1. **Dockerイメージをビルド**:
   プロジェクトルートディレクトリで以下のコマンドを実行してDockerイメージをビルドします。

   ```sh
   docker build -t speech-to-text gizi_okosi
   ```

2. **Dockerコンテナを実行**:
   ビルドが完了したら、以下のコマンドを実行してコンテナを起動します。

   ```sh
   docker run --rm -v $(pwd)/audio:/app/audio -v $(pwd)/transcriptions:/app/transcriptions -v $(pwd)/corrected_transcriptions:/app/corrected_transcriptions speech-to-text
   ```

   このコマンドでは、ホストマシンの `audio`、`transcriptions`、`corrected_transcriptions` ディレクトリをコンテナ内の対応するディレクトリにマウントしています。

### まとめ

この構成では、Dockerを使用して一貫した開発環境を提供し、依存関係を管理します。音声データの文字起こしと補正を行うためのスクリプトを実行するためのDockerコンテナを作成しました。これにより、ローカル環境の影響を受けずにプロジェクトを実行できます。