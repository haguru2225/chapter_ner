import re
from pathlib import Path
from collections import Counter
import pandas as pd
import spacy


###############################################################################
# 1) 設定
###############################################################################
INPUT_FILE = "pg49445.txt"          # ここを処理したい .txt に変更するだけでOK
N_HEAD_CHARS = 3000                # 各章の先頭から何文字 spaCy 解析するか
TOP_N_ENTS   = 10                  # 章ごとに表示する固有名詞トップ件数


###############################################################################
# 2) Gutenberg ボイラープレートを除去
###############################################################################
def strip_gutenberg_boilerplate(text: str) -> str:
    """Project Gutenberg の START/END マーカー間を抽出"""
    start = re.search(r"\*{3}\s*START OF (THE|THIS) PROJECT GUTENBERG", text, re.I)
    end   = re.search(r"\*{3}\s*END OF (THE|THIS) PROJECT GUTENBERG",   text, re.I)
    if start and end and start.end() < end.start():
        return text[start.end(): end.start()]
    return text


###############################################################################
# 3) 章見出し抽出用の正規表現
###############################################################################
# - CHAPTER THE FIRST.
# - CHAPTER I.
# - Chapter III. Some Subtitle
CHAPTER_PAT = re.compile(
    r"^\s*(?:CHAPTER|Chapter)\s+([IVXLCDM]+|THE\s+\w+|\w+)"  # 番号部分
    r"\.?[^\n]*$",                                           # ピリオド＆改行まで
    flags=re.MULTILINE
)


def split_into_chapters(text: str):
    """CHAPTER_PAT に基づいて (title, body) リストを返す"""
    indexes = [m.start() for m in CHAPTER_PAT.finditer(text)]
    titles  = [m.group().strip() for m in CHAPTER_PAT.finditer(text)]

    chapters = []
    for i, idx in enumerate(indexes):
        start = idx
        end   = indexes[i+1] if i+1 < len(indexes) else len(text)
        body  = text[start:end]
        chapters.append((titles[i], body))
    return chapters


###############################################################################
# 4) spaCy 初期化
###############################################################################
nlp = spacy.load("en_core_web_sm")


###############################################################################
# 5) メイン処理
###############################################################################
def main():
    # 5-1. 入力ファイル読みこみ
    raw_text = Path(INPUT_FILE).read_text(encoding="utf-8", errors="ignore")
    core_text = strip_gutenberg_boilerplate(raw_text)

    # 5-2. 章ごとに分割
    chapters = split_into_chapters(core_text)
    if not chapters:
        print("⚠️  章タイトルが検出できませんでした。正規表現を見直してください。")
        return

    # 5-3. 各章を spaCy で解析し、固有名詞カウント
    rows = []
    for title, body in chapters:
        doc = nlp(body[:N_HEAD_CHARS])
        ents = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "GPE", "ORG"}]
        counts = Counter(ents)
        top = ", ".join(f"{ent}({cnt})" for ent, cnt in counts.most_common(TOP_N_ENTS))
        rows.append({"chapter": title, "top_entities": top})

    # 5-4. 結果を DataFrame で表示
    df = pd.DataFrame(rows)
    pd.set_option("display.max_colwidth", None)
    print(df.to_string(index=False))


###############################################################################
if __name__ == "__main__":
    main()
