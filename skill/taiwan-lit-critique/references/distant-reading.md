# 遠讀 / 數位人文 recipes

用量化證據支援（不是取代）細讀。核心原則：**每個數字都要回扣文本解釋**，
否則只是漂亮的圖表。分析中文文本前，先注意斷詞問題。

## 中文斷詞的前提
中文沒有空格，詞頻分析前需斷詞。用 `jieba`（`pip install jieba`）。注意：
- 台灣文學含**台語、日語、舊詞彙、人名地名**，通用詞典會斷錯。準備一份自訂詞典
  （`jieba.load_userdict`）補入關鍵詞（如「本島人」「內地」「保正」「大人」）。
- 繁簡：語料多為繁體，確認詞典與編碼（UTF-8）一致。
- 標點、注音、日文假名要先清理或保留視分析目的而定。

## Recipe 1：詞頻與關鍵詞比較
問題：某詞在不同作者/年代的出現密度。
步驟：讀入語料 → 斷詞 → 計數 → **以每千字標準化**（篇幅不同不能比絕對數）→ 比較。
輸出：表格或長條圖，並回答「這個分布說明了什麼詮釋問題」。

## Recipe 2：關鍵詞脈絡（KWIC, Keyword-in-Context）
問題：某關鍵詞（如「祖國」「番」「祖國」「文明」）**每次出現時的上下文**。
做法：對每個命中位置，抓前後 N 個字/詞印出，附 `檔名:行號`。
這是量化與細讀的橋樑——用它找出「同一個詞的意義如何隨脈絡變化」。
（快速版可直接用 Grep 抓行 + 前後文，不必寫程式。）

## Recipe 3：TF-IDF 找特徵詞
問題：某篇/某作者相對於整個語料庫的**特徵詞**是什麼。
用 `scikit-learn` 的 `TfidfVectorizer`（配合 jieba 斷詞當 tokenizer）。
輸出每個文本的 top 特徵詞，用來對比作家風格或主題偏向。

## Recipe 4：共現與主題
- 詞共現網路：哪些詞常一起出現（可用 window 內共現計數）。
- 若語料夠大再考慮主題模型（LDA），但小語料 LDA 不穩，別過度解讀。

## 落地建議
- 小程式放 `scripts/`，讓分析可重複執行、可被檢查。
- 每個量化結果，都在札記「四、遠讀證據」段落配一句細讀式解釋。
- 樣本小（幾篇）時，量化只是「提示」而非「證明」——講話要保留，別用統計語氣掩蓋薄弱證據。
  這本身也是模式 D（批判 AI 詮釋）要盯的：不要被自己產出的數字唬住。
```python
# 最小骨架範例：標準化詞頻
import jieba, collections, pathlib
jieba.load_userdict("scripts/tw_lit_dict.txt")  # 自訂台文詞典
text = pathlib.Path("corpus/賴和/一桿稱仔.txt").read_text(encoding="utf-8")
tokens = [t for t in jieba.cut(text) if t.strip()]
freq = collections.Counter(tokens)
per_1000 = {w: c / len(tokens) * 1000 for w, c in freq.most_common(30)}
```
