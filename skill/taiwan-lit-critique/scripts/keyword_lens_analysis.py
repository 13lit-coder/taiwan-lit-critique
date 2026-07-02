#!/usr/bin/env python3
"""
把「一堆論文關鍵詞」煉成透鏡:頻率排行 + 共現分析。

輸入:一個文字檔,內容是一組一組的關鍵詞群(每篇論文一組)。
     組與組之間用空白行分隔;組內關鍵詞用 、 , ，｜ 或換行分隔。
     中英對照沒關係,預設只統計含中日文字的詞(--all 可全計)。

用法:
    python keyword_lens_analysis.py corpus/field-keywords.txt
    python keyword_lens_analysis.py corpus/field-keywords.txt --top 60 --cooc 40
"""
import sys, re, argparse, collections, itertools

CJK = re.compile(r'[㐀-鿿぀-ヿ]')          # 中日文字
SPLIT = re.compile(r'[、,，;；｜\n]+')                      # 關鍵詞分隔符
STRIP = '「」『』""\'\'（）() 　\t﻿'                    # 要去掉的邊緣字元

def load_clusters(path):
    raw = open(path, encoding='utf-8').read()
    # 忽略以 # 開頭的註解/來源說明行
    raw = '\n'.join(l for l in raw.splitlines() if not l.lstrip().startswith('#'))
    # 以「一個或多個空白行」切成關鍵詞群
    blocks = re.split(r'\n\s*\n', raw)
    clusters = []
    for b in blocks:
        b = b.replace('關鍵字', '')            # 常見的表頭雜訊
        toks = [t.strip(STRIP) for t in SPLIT.split(b)]
        toks = [t for t in toks if t and t != '＂']
        if toks:
            clusters.append(toks)
    return clusters

def is_cjk(tok):
    return bool(CJK.search(tok))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--top', type=int, default=50, help='頻率排行前 N 名')
    ap.add_argument('--cooc', type=int, default=30, help='共現配對前 N 名')
    ap.add_argument('--all', action='store_true', help='連純英文詞也統計')
    ap.add_argument('--min-cooc', type=int, default=3, help='共現至少出現幾次才列出')
    args = ap.parse_args()

    clusters = load_clusters(args.file)
    keep = (lambda t: True) if args.all else is_cjk

    freq = collections.Counter()
    cooc = collections.Counter()
    for toks in clusters:
        uniq = sorted({t for t in toks if keep(t)})
        freq.update(uniq)
        for a, b in itertools.combinations(uniq, 2):
            cooc[(a, b)] += 1

    print(f"# 語料:{len(clusters)} 組關鍵詞群,{len(freq)} 個相異關鍵詞\n")

    print(f"## 頻率排行(前 {args.top})──浮現的核心議題")
    for w, c in freq.most_common(args.top):
        print(f"{c:>4}  {w}")

    print(f"\n## 高頻共現配對(前 {args.cooc},至少 {args.min_cooc} 次)──概念常綁在一起 = meta-lens")
    pairs = [(p, c) for p, c in cooc.most_common() if c >= args.min_cooc][:args.cooc]
    for (a, b), c in pairs:
        print(f"{c:>4}  {a} ── {b}")

if __name__ == '__main__':
    main()
