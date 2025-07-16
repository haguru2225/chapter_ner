# Chapter‑NER

簡単に使える **章ごと固有名詞抽出ツール** です。Project Gutenberg などの英語プレーンテキストを読み込み、章単位で **人名 / 地名 / 組織名** の出現回数をカウントし、上位 N 件を一覧表示します。

---

## 0. ざっくりイメージ

```
chapter_ner.py → pg5225.txt

 CHAPTER I.            Anne(17), Marilla(9), Avonlea(5), ...
 CHAPTER II.           Matthew(15), Mrs. Spencer(6), ...
 ...
```

数行で実行できる “お手軽 NER” スクリプトです。

---

## 1. 特長

| 特長                       | 説明                                                   |
| ------------------------ | ---------------------------------------------------- |
| **章タイトルを自動検出**           | `CHAPTER I.` / `CHAPTER THE FIRST.` など大小さまざまな形式をサポート |
| **Gutenbergボイラープレートを除去** | START/END マーカー間だけを自動抽出                               |
| **spaCyでNER**            | `en_core_web_sm` で固有名詞を抽出（PERSON / GPE / ORG）        |
| **見やすい DataFrame 出力**    | pandas 表で “章タイトル & 上位固有名詞” を一覧化                      |
| **パラメータ一行設定**            | 解析文字数/上位件数を定数で簡単変更                                   |

---

## 2. セットアップ

```bash
# ① 任意：仮想環境を作成
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# ② 依存ライブラリ
pip install spacy pandas
python -m spacy download en_core_web_sm
```

---

## 3. ファイル配置例

```
chapter-ner/
├── chapter_ner.py    # スクリプト本体
├── LICENSE          # MIT License
├── README.md        # 本書
└── pg5225.txt       # 解析したいテキスト（例）
```

---

## 4. 使い方

1. **解析対象ファイルを用意** してフォルダに置く
2. `chapter_ner.py` の先頭でファイル名を指定

   ```python
   INPUT_FILE = "pg5225.txt"
   ```
3. 実行

   ```bash
   python chapter_ner.py
   ```
4. 結果がターミナルに表示されます。

### パラメータ調整

| 定数             | 役割              | デフォルト |
| -------------- | --------------- | ----- |
| `N_HEAD_CHARS` | 各章の冒頭何文字を解析するか  | 3000  |
| `TOP_N_ENTS`   | 章ごとに表示する上位固有名詞数 | 10    |

---

## 5. 出力例

```text
                 chapter                              top_entities
 CHAPTER I. TOOL-MAKING ANIMALS   Man(11), Tool(7), Europe(4), ...
 CHAPTER II. THE ANATOMY OF A MACHINE   Machine(12), Wheel(8), ...
 ...
```

---

## 6. ライセンス

### コード

このリポジトリのソースコードは **MIT License** で公開されています。詳細は [`LICENSE`](./LICENSE) を参照してください。
MIT ライセンス（参考訳）
本ソフトウェアおよび関連書類ファイル（以下「ソフトウェア」）の複製を取得するすべての人に対し、ソフトウェアを無制限に取り扱うことを無償で許可します。
これには、使用・コピー・改変・結合・出版・頒布・サブライセンス・販売およびソフトウェアを提供する相手に同じことを許可する権利が無制限に含まれます。
上記の著作権表示および本許諾表示は、ソフトウェアのすべての複製または重要な部分に記載するものとします。
ソフトウェアは「現状有姿」で提供され、明示黙示を問わずいかなる保証もありません。…

### 解析対象テキスト

Project Gutenberg 等のテキストは各自で著作権を確認し、ライセンスに従って使用してください。パブリックドメイン以外のテキストを商用利用する場合は特に注意してください。

---

## 7. 免責事項

本スクリプトは **現状のまま (as-is)** 提供されます。使用・改変によって生じたいかなる損害に対しても、著作権者は責任を負いません。

---

## 8. コントリビュート

バグ報告 / 機能提案 / ドキュメント改善など歓迎します！

1. Issue を立てる
2. Fork → branch で修正 → PR を送る

お気軽にどうぞ 🙌
