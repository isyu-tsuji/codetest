import streamlit as st

st.title('Streamlit Webページ')

# テキストを追加
st.write('これはStreamlitを使用して作成したWebページです.')

# データフレームを表示
import pandas as pd
df = pd.DataFrame({
    '名前': ['Alice', 'Bob', 'Charlie'],
    '年齢': [25, 30, 35]
})
st.write('データフレームの表示:')
st.write(df)

# グラフを描画
import matplotlib.pyplot as plt
import numpy as np
# フォントの設定
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('sin@grafu')
st.pyplot(plt)