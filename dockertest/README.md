# DockerでPythonの環境構築ガイド

## 目的
Pythonの環境をDockerで作成し、練習用のプロジェクトをセットアップする。

## フォルダ構成
以下は提案されるシンプルなフォルダ構成です。

```
my-python-project/
├── app/
│   └── main.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## 各ファイルの説明
- **app/main.py**: Pythonのメインスクリプト
- **Dockerfile**: Dockerイメージをビルドするための設定ファイル
- **requirements.txt**: Pythonの依存関係を記述するファイル
- **README.md**: プロジェクトの説明や使い方を書いたドキュメント（任意）

## Dockerfileの例
```Dockerfile
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
```

## requirements.txtの例
```
flask
requests
```

## app/main.pyの例
```python
print("Hello, Docker!")
```

## Docker環境のセットアップ手順
1. フォルダ構成の準備:
   - 上記のフォルダ構成とファイルを作成します。
2. Dockerイメージのビルド:
   - ターミナルを開き、my-python-projectディレクトリに移動します。
   - `docker build -t example_image:1.0 dockertest` を実行してDockerイメージをビルドします。
3. Dockerコンテナの実行:
   - `docker run --rm example_image:1.0` を実行してDockerコンテナを起動します。コンテナが起動し、"Hello, Docker!"というメッセージが表示されます。

このガイドでは、Pythonの環境を作成するための基本的なフォルダ構成とDockerfileの例を示しました。プロジェクトをセットアップし、Dockerを使ったPythonの環境構築を練習してください。