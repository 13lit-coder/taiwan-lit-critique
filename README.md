# taiwan-lit-critique — 台灣文學批判閱讀 skill

一個給 Claude Code 用的 **skill**：把 Claude Code 當成「研究工作台」，對台灣文學做
研究生層級的批判閱讀。核心信念是——研究生的批判思考有兩層：**批判文本**，以及
**批判 AI 對文本的詮釋**；第二層才是重點。

> 本 repo 只包含**方法本身（skill）**，不含任何分析成果或範例文章，以免與已完成、
> 已查證的研究混淆。

## 這個 skill 做什麼

- **模式 A — 細讀**：逐段拆解語言、敘事、結構與多語現象。
- **模式 B — 理論透鏡對讀**：選 2–3 個會互相矛盾的視角各讀一遍，看見「換透鏡就換結論」。
- **模式 C — 遠讀（數位人文）**：跨文本詞頻／關鍵詞量化，結果須回扣細讀。
- **模式 D — 批判 AI 的詮釋**：自我反駁、查證引文、抓套版話術、標記需人工補充的在地脈絡。

證據紀律：每個詮釋附文本行號；區分「文本事實／詮釋推論／理論套用」；拒絕無證據的概括。

## 結構

```
skill/taiwan-lit-critique/
├── SKILL.md                       # 主流程 SOP
├── references/
│   ├── theory-lenses.md           # 8 通用理論透鏡 + 9 個在地 meta-lens
│   ├── taiwan-lit-context.md      # 台灣文學脈絡與版權護欄
│   └── distant-reading.md         # 數位人文遠讀 recipes
├── scripts/
│   └── keyword_lens_analysis.py   # 關鍵詞頻率／共現分析工具
└── data/
    └── field-keywords.txt         # 9 個在地透鏡的來源語料（見下）
```

## 安裝

```bash
cp -r skill/taiwan-lit-critique ~/.claude/skills/
```

之後對 Claude 說「用批判角度讀某篇台灣文學」即會自動觸發。

## 在地透鏡的來源

`references/theory-lenses.md` 的 9 個「在地 meta-lens」，是從 `data/field-keywords.txt`
（888 組論文關鍵詞）的頻率分析中煉出的。可重現：

```bash
python3 skill/taiwan-lit-critique/scripts/keyword_lens_analysis.py \
    skill/taiwan-lit-critique/data/field-keywords.txt --top 55 --cooc 35
```

**語料來源**：取自《臺灣文學研究學報》、《文化研究》、《台灣學誌》三種期刊之期刊論文
「關鍵詞」欄位，皆為公開書目資料（僅取關鍵詞，未使用論文全文）。
