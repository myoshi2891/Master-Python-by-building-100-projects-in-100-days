# Poetry × 単発スクリプト（main.py）運用プレイブック

最終更新: 2025-10-10 18:35

本メモは、`poetry install` 実行時のエラー

> `The current project could not be installed: No file/folder found for package <project-name>`

に対する対処を、**「依存管理だけする」** と **「きちんとパッケージにする」** の 2 路線で要点整理したもの。

---

## 1) 症状と原因

- プロジェクト構成が**単発スクリプト型**（`main.py` だけ、パッケージフォルダなし）。
- Poetry は `poetry install` 後に **自分自身のパッケージインストール**を試みる（Poetry 1.8+ の既定挙動）。
- しかし `pyproject.toml` の設定やディレクトリ構成が**パッケージの体裁を満たさず**、
  `No file/folder found for package <project-name>` が発生。

---

## 2) 解決方針（どちらか 1 つで OK）

### A. 依存管理だけ行う（パッケージ化しない）

- **おすすめ（最小コスト）**。自分自身のインストールをやめる。

**`pyproject.toml` 例（抜粋）**

```toml
[tool.poetry]
name = "nato-alphabet-end"
version = "0.1.0"
description = "NATO phonetic alphabet demo"
readme = "README.md"
package-mode = false        # ← これがポイント

[tool.poetry.dependencies]
python = "^3.12"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**コマンド**

```bash
poetry install
poetry run python main.py
```

> 一時的に済ませたいだけなら `poetry install --no-root` でも可。

---

### B. きちんとパッケージとして扱う（配布/CLI 化を視野）

- **src レイアウト**を採用し、Python パッケージを明示する。

**ディレクトリ**

```
.
├── pyproject.toml
├── README.md
├── nato_phonetic_alphabet.csv
└── src/
    └── nato_alphabet_end/      # ← パッケージ名はアンダースコア
        ├── __init__.py
        └── __main__.py
```

**`__main__.py` の例**

```python
def main():
    print("Hello NATO")

if __name__ == "__main__":
    main()
```

**`pyproject.toml` 例（抜粋）**

```toml
[tool.poetry]
name = "nato-alphabet-end"      # ← プロジェクト名（ハイフン可）
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.12"

packages = [{ include = "nato_alphabet_end", from = "src" }]

[tool.poetry.scripts]
nato = "nato_alphabet_end.__main__:main"  # 任意のCLI

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**コマンド**

```bash
poetry install
poetry run python -m nato_alphabet_end
# または
poetry run nato
```

---

## 3) よくある落とし穴

- **ハイフン/アンダースコア不一致**
  - プロジェクト名: `nato-alphabet-end`（ハイフン OK）
  - パッケージ名: `nato_alphabet_end`（ハイフン不可 → アンダースコア）
- **`__init__.py` が無い** → パッケージ認識されない。
- **`packages` 未指定（src レイアウト時）** → `include` と `from` を明記する。
- **Poetry の venv が意図と違う Python** → `poetry env use $(pyenv which python)` で 3.12 を明示。
- **pandas 1.5.x × Python 3.12 でビルドに固まる** → `pandas>=2.2` か **Python 3.11** に切替。

---

## 4) いまの構成（main.py のみ）での最短手順（今回の決着）

```bash
# 依存だけ入れる運用
poetry install                # package-mode=false を設定済みならOK
poetry run python main.py
```

