# Flask × conda × pyenv 復旧＆運用まとめ（実録）

このドキュメントは、**/opt/anaconda3 の conda 環境**と**pyenv**が共存する macOS（zsh）で、
Flask の導入〜エラー復旧〜運用方針確立までを **今回のやり取りの全工程**として整理したものです。

---

## 0. ゴール

- **安全に Flask を使える仮想環境**（conda でも pyenv+venv でも）を用意
- “どの Python を使っているか迷子にならない” PATH/初期化設定
- 典型エラー（`anaconda-auth / No module named 'click'`等）の**即時復旧手順**

---

## 1. まず押さえる原則

- **同じ Python の pip を使う**（`python -m pip` で環境取り違えを防止）
- **base（/opt/anaconda3）を汚さない**：原則は**専用の仮想環境**で作業
- `type -a python` / `which python` / `python -c "import sys;print(sys.executable)"` で**現在地を可視化**
- zsh はコマンドキャッシュを持つ → 切替時は **`hash -r`**（または `rehash`）

---

## 2. 最初の状況と課題

- `/opt/anaconda3/bin/python -m pip install flask` を **base** に実行 → 一旦 Flask は入る

- その後、**conda のエントリポイントが click に依存**しているため、`click` を base から消した／見えない状態になり、

  ```text
  Error while loading conda entry point: anaconda-auth (No module named 'click')
  ```

  が発生

- さらに `.zshrc` に **conda initialize ブロックが二重**かつ `exec` の使い方により `(base)` が自動起動、
  pyenv のシムが PATH 先頭に来るため **conda が有効化されない** など、複合的に混線

---

## 3. エラー復旧の決定打

### 3.1 `click` を base に復旧（最短）

```bash
/opt/anaconda3/bin/python -m pip install "click>=8.1,<9"
# うまくいかない時は --force-reinstall や --no-cache-dir を付与
```

> pip が依存警告（Jinja2/blinker など）を出しても、**conda 起動には不要**なので先へ進んで OK。

### 3.2 認証系（エラーの呼び出し元）を整備

```bash
/opt/anaconda3/bin/conda install -n base anaconda-client anaconda-cloud-auth -y
/opt/anaconda3/bin/conda update  -n base conda -y
```

### 3.3 `click` の状態確認（復旧できたか）

```bash
/opt/anaconda3/bin/python - <<'PY'
import click, sys, inspect
print("click version:", getattr(click, "__version__", "unknown"))
print("loaded from   :", inspect.getfile(click))
print("python exec   :", sys.executable)
PY
```

---

## 4. conda が効かない/pyenv が勝つ時の切り替え

### 4.1 現在のシェルに conda を読み込む（**exec は使わない**）

```bash
eval "$(/opt/anaconda3/bin/conda shell.zsh hook)"
conda deactivate 2>/dev/null || true
conda activate flaskbasic
hash -r
```

### 4.2 まだ pyenv が勝つなら（どちらか実施）

- **一時的に pyenv を外す**

  ```bash
  pyenv shell --unset   # or: pyenv shell system
  hash -r
  ```

- **PATH で conda env を前に寄せる（応急）**

  ```bash
  export PATH="/opt/anaconda3/envs/flaskbasic/bin:/opt/anaconda3/bin:$PATH"
  hash -r
  ```

### 4.3 確認

```bash
which python
python -c "import sys; print(sys.executable)"
# 期待: /opt/anaconda3/envs/flaskbasic/bin/python
```

> 有効化なしでも実行だけしたい時は：
>
> ```bash
> /opt/anaconda3/bin/conda run -n flaskbasic python -V
> /opt/anaconda3/bin/conda run -n flaskbasic python -m flask --version
> ```

---

## 5. .zshrc の最終形（競合しない順序）

> **重要**: conda initialize **は一度だけ**。pyenv 初期化より**上**に配置。

```zsh
########################################
# Homebrew
########################################
export PATH="/opt/homebrew/bin:$PATH"

########################################
# Conda initialize（1回だけ）
########################################
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if [[ -f "/opt/anaconda3/bin/conda" ]]; then
  __conda_setup="$('/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
  if [[ $? -eq 0 ]]; then
    eval "$__conda_setup"
  else
    if [[ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]]; then
      . "/opt/anaconda3/etc/profile.d/conda.sh"
    else
      export PATH="/opt/anaconda3/bin:$PATH"
    fi
  fi
  unset __conda_setup
fi
# <<< conda initialize <<<

########################################
# pyenv（Conda より後）
########################################
if [[ -d "$HOME/.pyenv" ]]; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
fi

# rbenv / nodebrew / bun / Tcl-Tk / alias などはこの下に…
```

- `.zshrc` に書いていた
  `conda config --set auto_activate_base false` は **削除**（これは一度だけ実行する設定コマンド）
- 起動時に (base) に入りたくない設定は、**既に保存済み**かを確認：

  ```bash
  conda config --show | grep -E '^auto_activate\b'
  # => auto_activate: False ならOK
  ```

---

## 6. Flask のインストールと確認（flaskbasic）

```bash
conda activate flaskbasic
python -m pip --version
python -m pip install --no-user "flask>=3.1,<3.2"
python -m flask --version
# 期待: Python 3.13.5 / Flask 3.1.x / Werkzeug 3.1.x
```

> `No module named flask` が出たら、その環境に入っていないだけ。上記を実施。

---

## 7. 運用方針（どちらでも OK／混在しないことが肝）

### 方針 A：**pyenv 主役**（軽量・わかりやすい）

- プロジェクト直下で venv を作成し隔離：

  ```bash
  ~/.pyenv/versions/3.13.5/bin/python -m venv .venv
  source .venv/bin/activate
  python -m pip install flask
  ```

- VS Code のインタプリタに `.venv/bin/python` を指定

### 方針 B：**conda 主役**

- `conda create -n flaskbasic python=3.13 -y`
- `conda activate flaskbasic` → `python -m pip install flask`

> 今回は **pyenv のまま使っても問題なし**。ただし **各プロジェクト専用の仮想環境（pyenv-virtualenv か venv）**を使うのがベスト。

---

## 8. 典型トラブルと一言回答

- **`anaconda-auth (No module named 'click')`**
  → base から `click` が消えた。`/opt/anaconda3/bin/python -m pip install "click>=8.1,<9"` で復旧。
  必要なら `anaconda-client / anaconda-cloud-auth` を conda で追加。

- **`exec $SHELL -l && conda activate ...` で (base) になる**
  → `exec` は**後続を実行しない**。`exec` 後に**改めて** `conda activate`。

- **`print(sys.executable)` が zsh でエラー**
  → シェルの `print` を呼んでる。**`python -c "..."`** で実行。

- **`type -a python` が pyenv→conda の順**
  → 一時的に `pyenv shell --unset`、`hash -r`、または PATH を前寄せ。

- **行内コメントでエラー（`conda info --envs # ← ...`）**
  → コマンドラインでは `#` 以降が**引数扱い**になるケースあり。**コメントなしで実行**。

---

## 9. 最終チェックリスト

```bash
# どの環境が有効か（* が付く）
conda info --envs

# いまの Python の実体
which python
python -c "import sys; print(sys.executable)"

# pip の所属（Location が flaskbasic か .venv か）
python -m pip --version

# Flask の有無
python -m flask --version
```

**OK 例**（conda の flaskbasic を利用）

- `/opt/anaconda3/envs/flaskbasic/bin/python` が出る
- `pip` Location が `/opt/anaconda3/envs/flaskbasic/...`
- `Flask 3.1.x / Werkzeug 3.1.x`

---

## 10. おまけ：最小 Flask アプリ

```python
# app.py
from flask import Flask
app = Flask(__name__)
@app.get("/")
def home():
    return "Hello Flask!"
if __name__ == "__main__":
    app.run(debug=True)
```

```bash
python app.py
# もしくは
# FLASK_APP=app.py flask run
```

---

### まとめ

- **いまは pyenv が主役でも問題なし**。その場合は **プロジェクトごとに venv/virtualenv** を作成して Flask を導入。
- conda を使う場合は **conda initialize は一度だけ**＋**pyenv より上**に配置し、混在を避ける。
- 迷ったら常に **`python -m pip`** と **確認 3 点セット**（`which python` / `print(sys.executable)` / `pip --version`）。

この運用で **再現性の高い環境**と**即時復旧**ができるようになりました。
