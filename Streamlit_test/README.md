### Streamlit Webアプリ
このプロジェクトは、Streamlitを使用して作成されたWebアプリケーションです。

### Streamlit_testのフォルダ構成

```
project-root/
│
├── app/
│ └── main.py
├── Dockerfile
├── requirements.txt
└── README.md

```

### インストール
* Dockerを使用して環境を構築します。
* 必要なパッケージをインストールします。

### 使用方法
* Dockerコンテナを起動します。
* Webブラウザでアプリにアクセスします。

### コード例
```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## タイトルを追加
st.title('Streamlit Webページ')

## テキストを追加
st.write('これはStreamlitを使用して作成したWebページです.')

## データフレームを表示
df = pd.DataFrame({
    '名前': ['Alice', 'Bob', 'Charlie'],
    '年齢': [25, 30, 35]
})
st.write('データフレームの表示:')
st.write(df)

## グラフを描画
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('sin@grafu')
st.pyplot(plt)
```

### 実行コマンド
```bash
docker build -t streamlit-app Streamlit_test
docker run -p 8501:8501 streamlit-app
```