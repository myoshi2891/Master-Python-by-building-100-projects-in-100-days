# コードをリファクタリングして、より保守性が高く、エラーハンドリングが充実したバージョン

```python

import tkinter as tk
import pandas as pd
import random
import os
from typing import Dict, List, Optional, Any

class FlashCardApp:
    """フラッシュカードアプリケーションのメインクラス"""

    # 定数
    BACKGROUND_COLOR = "#B1DDC6"
    CARD_WIDTH = 800
    CARD_HEIGHT = 526
    FLIP_DELAY = 3000  # ミリ秒

    # ファイルパス
    ORIGINAL_DATA_FILE = "data/french_words.csv"
    PROGRESS_DATA_FILE = "data/words_to_learn.csv"

    # 画像ファイルパス
    FRONT_IMAGE_PATH = "images/card_front.png"
    BACK_IMAGE_PATH = "images/card_back.png"
    WRONG_IMAGE_PATH = "images/wrong.png"
    RIGHT_IMAGE_PATH = "images/right.png"

    def __init__(self):
        """アプリケーションの初期化"""
        self.current_card: Dict[str, Any] = {}
        self.to_learn: List[Dict[str, Any]] = []  # 型を修正
        self.flip_timer: Optional[str] = None

        # 画像オブジェクトの初期化
        self.front_image: Optional[tk.PhotoImage] = None
        self.back_image: Optional[tk.PhotoImage] = None
        self.wrong_image: Optional[tk.PhotoImage] = None
        self.right_image: Optional[tk.PhotoImage] = None

        # データの読み込み
        self._load_data()

        # UIの初期化
        self._setup_window()
        self._load_images()
        self._create_widgets()
        self._layout_widgets()

        # 最初のカードを表示
        self.next_card()

    def _load_data(self) -> None:
        """学習データの読み込み"""
        try:
            # 進捗ファイルが存在する場合はそれを読み込み
            if os.path.exists(self.PROGRESS_DATA_FILE):
                data = pd.read_csv(self.PROGRESS_DATA_FILE)
                print(f"進捗ファイルを読み込みました: {len(data)} 単語")
            else:
                # 進捗ファイルがない場合は元データを読み込み
                data = pd.read_csv(self.ORIGINAL_DATA_FILE)
                print(f"元データを読み込みました: {len(data)} 単語")

            # 型キャストを明示的に行う
            records = data.to_dict(orient="records")
            self.to_learn = [
                {str(k): str(v) for k, v in record.items()}
                for record in records
            ]

            if not self.to_learn:
                raise ValueError("学習データが空です")

        except FileNotFoundError as e:
            self._show_error(f"データファイルが見つかりません: {e}")
            self.to_learn = []
        except Exception as e:
            self._show_error(f"データの読み込みエラー: {e}")
            self.to_learn = []

    def _setup_window(self) -> None:
        """メインウィンドウの設定"""
        self.window = tk.Tk()
        self.window.title("Flashy - フラッシュカード学習アプリ")
        self.window.config(
            padx=50,
            pady=50,
            bg=self.BACKGROUND_COLOR
        )
        self.window.resizable(False, False)

        # ウィンドウを画面中央に配置
        self.window.geometry("900x750+100+50")

    def _load_images(self) -> None:
        """画像ファイルの読み込み"""
        try:
            self.front_image = tk.PhotoImage(file=self.FRONT_IMAGE_PATH)
            self.back_image = tk.PhotoImage(file=self.BACK_IMAGE_PATH)
            self.wrong_image = tk.PhotoImage(file=self.WRONG_IMAGE_PATH)
            self.right_image = tk.PhotoImage(file=self.RIGHT_IMAGE_PATH)
        except (tk.TclError, FileNotFoundError) as e:
            self._show_error(f"画像ファイルの読み込みエラー: {e}")
            # フォールバック: 画像なしで動作
            self.front_image = None
            self.back_image = None
            self.wrong_image = None
            self.right_image = None

    def _create_widgets(self) -> None:
        """ウィジェットの作成"""
        # キャンバスの作成
        self.canvas = tk.Canvas(
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
            bg=self.BACKGROUND_COLOR,
            highlightthickness=0
        )

        # カード背景の作成
        if self.front_image:
            self.card_background = self.canvas.create_image(
                self.CARD_WIDTH // 2,
                self.CARD_HEIGHT // 2,
                image=self.front_image
            )
        else:
            # 画像がない場合のフォールバック
            self.card_background = self.canvas.create_rectangle(
                50, 50, self.CARD_WIDTH - 50, self.CARD_HEIGHT - 50,
                fill="white", outline="gray", width=2
            )

        # テキスト要素の作成
        self.card_title = self.canvas.create_text(
            self.CARD_WIDTH // 2, 150,
            text="",
            font=("Arial", 40, "italic"),
            fill="black"
        )

        self.card_word = self.canvas.create_text(
            self.CARD_WIDTH // 2, self.CARD_HEIGHT // 2,
            text="",
            font=("Arial", 60, "bold"),
            fill="black"
        )

        # ボタンの作成（修正版）
        if self.wrong_image:
            self.wrong_button = tk.Button(
                image=self.wrong_image,
                highlightthickness=0,
                command=self.next_card,
                bg=self.BACKGROUND_COLOR,
                relief="flat"
            )
        else:
            self.wrong_button = tk.Button(
                text="❌",
                highlightthickness=0,
                command=self.next_card,
                bg=self.BACKGROUND_COLOR,
                relief="flat",
                font=("Arial", 20)
            )

        if self.right_image:
            self.right_button = tk.Button(
                image=self.right_image,
                highlightthickness=0,
                command=self.mark_as_known,
                bg=self.BACKGROUND_COLOR,
                relief="flat"
            )
        else:
            self.right_button = tk.Button(
                text="✅",
                highlightthickness=0,
                command=self.mark_as_known,
                bg=self.BACKGROUND_COLOR,
                relief="flat",
                font=("Arial", 20)
            )

        # 進捗表示ラベル
        self.progress_label = tk.Label(
            text="",
            bg=self.BACKGROUND_COLOR,
            font=("Arial", 12),
            fg="gray"
        )

    def _layout_widgets(self) -> None:
        """ウィジェットのレイアウト"""
        self.canvas.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        self.wrong_button.grid(row=1, column=0, padx=20, pady=(10, 5))
        self.right_button.grid(row=1, column=1, padx=20, pady=(10, 5))
        self.progress_label.grid(row=2, column=0, columnspan=2, pady=(5, 10))

    def _update_progress_display(self) -> None:
        """進捗表示の更新"""
        remaining = len(self.to_learn)
        self.progress_label.config(text=f"残り単語数: {remaining}")

    def _cancel_flip_timer(self) -> None:
        """フリップタイマーのキャンセル"""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
            self.flip_timer = None

    def next_card(self) -> None:
        """次のカードを表示"""
        if not self.to_learn:
            self._show_completion_message()
            return

        # 既存のタイマーをキャンセル
        self._cancel_flip_timer()

        # ランダムにカードを選択
        self.current_card = random.choice(self.to_learn)

        # フランス語面を表示
        self._show_front_side()

        # 3秒後に英語面に切り替え
        self.flip_timer = self.window.after(self.FLIP_DELAY, self.flip_card)

        # 進捗表示を更新
        self._update_progress_display()

    def _show_front_side(self) -> None:
        """カードの表面（フランス語）を表示"""
        self.canvas.itemconfig(self.card_title, text="French", fill="black")
        self.canvas.itemconfig(
            self.card_word,
            text=self.current_card.get("French", ""),
            fill="black"
        )

        if self.front_image:
            self.canvas.itemconfig(self.card_background, image=self.front_image)
        else:
            self.canvas.itemconfig(self.card_background, fill="white")

    def flip_card(self) -> None:
        """カードを裏面（英語）に切り替え"""
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(
            self.card_word,
            text=self.current_card.get("English", ""),
            fill="white"
        )

        if self.back_image:
            self.canvas.itemconfig(self.card_background, image=self.back_image)
        else:
            self.canvas.itemconfig(self.card_background, fill="lightblue")

    def mark_as_known(self) -> None:
        """単語を「知っている」としてマーク"""
        if not self.current_card or not self.to_learn:
            return

        try:
            # 現在のカードを学習リストから削除
            if self.current_card in self.to_learn:
                self.to_learn.remove(self.current_card)

            # 進捗を保存
            self._save_progress()

            # 次のカードを表示
            self.next_card()

        except Exception as e:
            self._show_error(f"進捗保存エラー: {e}")

    def _save_progress(self) -> None:
        """学習進捗をファイルに保存"""
        try:
            if self.to_learn:
                # データフレームに変換して保存
                df = pd.DataFrame(self.to_learn)

                # ディレクトリが存在しない場合は作成
                os.makedirs(os.path.dirname(self.PROGRESS_DATA_FILE), exist_ok=True)

                df.to_csv(self.PROGRESS_DATA_FILE, index=False)
                print(f"進捗を保存しました: {len(self.to_learn)} 単語")
            else:
                # 全て完了した場合は進捗ファイルを削除
                if os.path.exists(self.PROGRESS_DATA_FILE):
                    os.remove(self.PROGRESS_DATA_FILE)
                    print("全ての単語を学習完了！進捗ファイルを削除しました。")

        except Exception as e:
            print(f"進捗保存エラー: {e}")

    def _show_completion_message(self) -> None:
        """学習完了メッセージの表示"""
        self.canvas.itemconfig(self.card_title, text="完了！", fill="green")
        self.canvas.itemconfig(
            self.card_word,
            text="全ての単語を\n学習しました！",
            fill="green"
        )
        self.progress_label.config(text="🎉 学習完了！お疲れ様でした！")

        # ボタンを無効化
        self.wrong_button.config(state="disabled")
        self.right_button.config(state="disabled")

    def _show_error(self, message: str) -> None:
        """エラーメッセージの表示"""
        print(f"エラー: {message}")
        # 実際のアプリケーションでは、tkinter.messagebox を使用することも可能

    def run(self) -> None:
        """アプリケーションの実行"""
        if not self.to_learn:
            self._show_error("学習データがありません。アプリケーションを終了します。")
            return

        self.window.mainloop()


def main() -> None:
    """メイン関数"""
    try:
        app = FlashCardApp()
        app.run()
    except Exception as e:
        print(f"アプリケーション起動エラー: {e}")


if __name__ == "__main__":
    main()

```

## 主なリファクタリング内容と変更点

### 1. **クラスベース設計への変更**

- 全ての機能を `FlashCardApp` クラスにカプセル化
- グローバル変数を排除し、インスタンス変数として管理
- コードの再利用性と保守性が向上

### 2. **型ヒントの追加**

```python
from typing import Dict, List, Optional
```

- 全ての変数と関数に適切な型ヒントを追加
- コードの可読性と IDE サポートが向上

### 3. **定数の整理**

```python
BACKGROUND_COLOR = "#B1DDC6"
CARD_WIDTH = 800
CARD_HEIGHT = 526
FLIP_DELAY = 3000
```

- マジックナンバーを定数として定義
- 設定変更が容易になり、保守性が向上

### 4. **エラーハンドリングの強化**

- ファイル読み込み時の例外処理
- 画像ファイルが見つからない場合のフォールバック
- データが空の場合の処理

### 5. **メソッドの分割と責任の明確化**

- `_load_data()`: データ読み込み専用
- `_setup_window()`: ウィンドウ設定専用
- `_load_images()`: 画像読み込み専用
- `_create_widgets()`: ウィジェット作成専用
- `_layout_widgets()`: レイアウト専用

### 6. **進捗表示機能の追加**

```python
def _update_progress_display(self) -> None:
    remaining = len(self.to_learn)
    self.progress_label.config(text=f"残り単語数: {remaining}")
```

- 残り単語数の表示
- 学習完了時の祝福メッセージ
- ユーザーのモチベーション向上

### 7. **タイマー管理の改善**

```python
def _cancel_flip_timer(self) -> None:
    if self.flip_timer:
        self.window.after_cancel(self.flip_timer)
        self.flip_timer = None
```

- タイマーの重複実行を防止
- メモリリークの防止
- より安定した動作

### 8. **ファイル管理の強化**

```python
def _save_progress(self) -> None:
    try:
        if self.to_learn:
            df = pd.DataFrame(self.to_learn)
            os.makedirs(os.path.dirname(self.PROGRESS_DATA_FILE), exist_ok=True)
            df.to_csv(self.PROGRESS_DATA_FILE, index=False)
        else:
            if os.path.exists(self.PROGRESS_DATA_FILE):
                os.remove(self.PROGRESS_DATA_FILE)
    except Exception as e:
        print(f"進捗保存エラー: {e}")
```

- ディレクトリの自動作成
- 学習完了時の進捗ファイル削除
- 例外処理による安全な保存

### 9. **UI/UXの向上**

- 画像が読み込めない場合のフォールバック表示
- ボタンの視覚的改善（絵文字フォールバック）
- ウィンドウサイズの固定とセンタリング
- 学習完了時のボタン無効化

### 10. **コードの可読性向上**

- プライベートメソッド（`_`プレフィックス）の使用
- 明確なメソッド名とドキュメント文字列
- 論理的なメソッドの分割
- 一貫したコーディングスタイル

### 11. **保守性とスケーラビリティ**

- 設定値の定数化により、カスタマイズが容易
- クラス設計により、機能拡張が簡単
- 各機能の独立性により、テストが容易
- エラーハンドリングにより、予期しない状況への対応

### 12. **パフォーマンスの改善**

- 不要なグローバル変数の排除
- 適切なリソース管理
- メモリ効率の向上

## 使用方法

### 基本的な使い方

1. アプリケーションを起動
2. フランス語の単語が表示される
3. 3秒後に自動的に英語の意味が表示される
4. 知っている単語なら「✅」ボタン、知らない単語なら「❌」ボタンをクリック
5. 進捗が自動保存され、次回起動時に続きから学習可能

### ファイル構成

```text
project/
├── main.py                    # メインアプリケーション
├── data/
│   ├── french_words.csv      # 元の学習データ
│   └── words_to_learn.csv    # 進捗データ（自動生成）
└── images/
    ├── card_front.png        # カード表面画像
    ├── card_back.png         # カード裏面画像
    ├── wrong.png             # ❌ボタン画像
    └── right.png             # ✅ボタン画像
```

## 今後の拡張可能性

### 追加可能な機能

1. **統計機能**: 学習時間、正答率の記録
2. **復習機能**: 間違えた単語の優先表示
3. **カテゴリ分け**: 単語の難易度別学習
4. **音声機能**: 発音の再生
5. **テーマ変更**: UI カラーテーマの切り替え
6. **データベース対応**: SQLite での進捗管理
7. **マルチユーザー対応**: 複数ユーザーの進捗管理

このリファクタリングにより、元のコードの機能を保持しながら、より堅牢で拡張しやすいアプリケーションになりました。

エラーの原因と修正方法を説明します。

## エラーの原因

### 1. **型ヒントの不一致**

`pd.read_csv().to_dict(orient="records")` は `list[dict[Hashable, Any]]` を返しますが、型ヒントでは `List[Dict[str, str]]` を期待しています。

### 2. **PhotoImage の None 値**

画像読み込みに失敗した場合、`None` を `tk.Button` の `image` パラメータに渡そうとしています。

## 修正版コード

```python
import tkinter as tk
import pandas as pd
import random
import os
from typing import Dict, List, Optional, Any, Union

class FlashCardApp:
    """フラッシュカードアプリケーションのメインクラス"""

    # 定数
    BACKGROUND_COLOR = "#B1DDC6"
    CARD_WIDTH = 800
    CARD_HEIGHT = 526
    FLIP_DELAY = 3000  # ミリ秒

    # ファイルパス
    ORIGINAL_DATA_FILE = "data/french_words.csv"
    PROGRESS_DATA_FILE = "data/words_to_learn.csv"

    # 画像ファイルパス
    FRONT_IMAGE_PATH = "images/card_front.png"
    BACK_IMAGE_PATH = "images/card_back.png"
    WRONG_IMAGE_PATH = "images/wrong.png"
    RIGHT_IMAGE_PATH = "images/right.png"

    def __init__(self):
        """アプリケーションの初期化"""
        self.current_card: Dict[str, Any] = {}
        self.to_learn: List[Dict[str, Any]] = []  # 型を修正
        self.flip_timer: Optional[str] = None

        # 画像オブジェクトの初期化
        self.front_image: Optional[tk.PhotoImage] = None
        self.back_image: Optional[tk.PhotoImage] = None
        self.wrong_image: Optional[tk.PhotoImage] = None
        self.right_image: Optional[tk.PhotoImage] = None

        # データの読み込み
        self._load_data()

        # UIの初期化
        self._setup_window()
        self._load_images()
        self._create_widgets()
        self._layout_widgets()

        # 最初のカードを表示
        self.next_card()

    def _load_data(self) -> None:
        """学習データの読み込み"""
        try:
            # 進捗ファイルが存在する場合はそれを読み込み
            if os.path.exists(self.PROGRESS_DATA_FILE):
                data = pd.read_csv(self.PROGRESS_DATA_FILE)
                print(f"進捗ファイルを読み込みました: {len(data)} 単語")
            else:
                # 進捗ファイルがない場合は元データを読み込み
                data = pd.read_csv(self.ORIGINAL_DATA_FILE)
                print(f"元データを読み込みました: {len(data)} 単語")

            # 型キャストを明示的に行う
            records = data.to_dict(orient="records")
            self.to_learn = [
                {str(k): str(v) for k, v in record.items()}
                for record in records
            ]

            if not self.to_learn:
                raise ValueError("学習データが空です")

        except FileNotFoundError as e:
            self._show_error(f"データファイルが見つかりません: {e}")
            self.to_learn = []
        except Exception as e:
            self._show_error(f"データの読み込みエラー: {e}")
            self.to_learn = []

    def _setup_window(self) -> None:
        """メインウィンドウの設定"""
        self.window = tk.Tk()
        self.window.title("Flashy - フラッシュカード学習アプリ")
        self.window.config(
            padx=50,
            pady=50,
            bg=self.BACKGROUND_COLOR
        )
        self.window.resizable(False, False)

        # ウィンドウを画面中央に配置
        self.window.geometry("900x700+100+50")

    def _load_images(self) -> None:
        """画像ファイルの読み込み"""
        try:
            self.front_image = tk.PhotoImage(file=self.FRONT_IMAGE_PATH)
            self.back_image = tk.PhotoImage(file=self.BACK_IMAGE_PATH)
            self.wrong_image = tk.PhotoImage(file=self.WRONG_IMAGE_PATH)
            self.right_image = tk.PhotoImage(file=self.RIGHT_IMAGE_PATH)
        except (tk.TclError, FileNotFoundError) as e:
            self._show_error(f"画像ファイルの読み込みエラー: {e}")
            # フォールバック: 画像なしで動作
            self.front_image = None
            self.back_image = None
            self.wrong_image = None
            self.right_image = None

    def _create_widgets(self) -> None:
        """ウィジェットの作成"""
        # キャンバスの作成
        self.canvas = tk.Canvas(
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
            bg=self.BACKGROUND_COLOR,
            highlightthickness=0
        )

        # カード背景の作成
        if self.front_image:
            self.card_background = self.canvas.create_image(
                self.CARD_WIDTH // 2,
                self.CARD_HEIGHT // 2,
                image=self.front_image
            )
        else:
            # 画像がない場合のフォールバック
            self.card_background = self.canvas.create_rectangle(
                50, 50, self.CARD_WIDTH - 50, self.CARD_HEIGHT - 50,
                fill="white", outline="gray", width=2
            )

        # テキスト要素の作成
        self.card_title = self.canvas.create_text(
            self.CARD_WIDTH // 2, 150,
            text="",
            font=("Arial", 40, "italic"),
            fill="black"
        )

        self.card_word = self.canvas.create_text(
            self.CARD_WIDTH // 2, self.CARD_HEIGHT // 2,
            text="",
            font=("Arial", 60, "bold"),
            fill="black"
        )

        # ボタンの作成（修正版）
        if self.wrong_image:
            self.wrong_button = tk.Button(
                image=self.wrong_image,
                highlightthickness=0,
                command=self.next_card,
                bg=self.BACKGROUND_COLOR,
                relief="flat"
            )
        else:
            self.wrong_button = tk.Button(
                text="❌",
                highlightthickness=0,
                command=self.next_card,
                bg=self.BACKGROUND_COLOR,
                relief="flat",
                font=("Arial", 20)
            )

        if self.right_image:
            self.right_button = tk.Button(
                image=self.right_image,
                highlightthickness=0,
                command=self.mark_as_known,
                bg=self.BACKGROUND_COLOR,
                relief="flat"
            )
        else:
            self.right_button = tk.Button(
                text="✅",
                highlightthickness=0,
                command=self.mark_as_known,
                bg=self.BACKGROUND_COLOR,
                relief="flat",
                font=("Arial", 20)
            )

        # 進捗表示ラベル
        self.progress_label = tk.Label(
            text="",
            bg=self.BACKGROUND_COLOR,
            font=("Arial", 12),
            fg="gray"
        )

    def _layout_widgets(self) -> None:
        """ウィジェットのレイアウト"""
        self.canvas.grid(row=0, column=0, columnspan=2, pady=20)
        self.wrong_button.grid(row=1, column=0, padx=20)
        self.right_button.grid(row=1, column=1, padx=20)
        self.progress_label.grid(row=2, column=0, columnspan=2, pady=10)

    def _update_progress_display(self) -> None:
        """進捗表示の更新"""
        remaining = len(self.to_learn)
        self.progress_label.config(text=f"残り単語数: {remaining}")

    def _cancel_flip_timer(self) -> None:
        """フリップタイマーのキャンセル"""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
            self.flip_timer = None

    def next_card(self) -> None:
        """次のカードを表示"""
        if not self.to_learn:
            self._show_completion_message()
            return

        # 既存のタイマーをキャンセル
        self._cancel_flip_timer()

        # ランダムにカードを選択
        self.current_card = random.choice(self.to_learn)

        # フランス語面を表示
        self._show_front_side()

        # 3秒後に英語面に切り替え
        self.flip_timer = self.window.after(self.FLIP_DELAY, self.flip_card)

        # 進捗表示を更新
        self._update_progress_display()

    def _show_front_side(self) -> None:
        """カードの表面（フランス語）を表示"""
        self.canvas.itemconfig(self.card_title, text="French", fill="black")
        self.canvas.itemconfig(
            self.card_word,
            text=self.current_card.get("French", ""),
            fill="black"
        )

        if self.front_image:
            self.canvas.itemconfig(self.card_background, image=self.front_image)
        else:
            self.canvas.itemconfig(self.card_background, fill="white")

    def flip_card(self) -> None:
        """カードを裏面（英語）に切り替え"""
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(
            self.card_word,
            text=self.current_card.get("English", ""),
            fill="white"
        )

        if self.back_image:
            self.canvas.itemconfig(self.card_background, image=self.back_image)
        else:
            self.canvas.itemconfig(self.card_background, fill="lightblue")

    def mark_as_known(self) -> None:
        """単語を「知っている」としてマーク"""
        if not self.current_card or not self.to_learn:
            return

        try:
            # 現在のカードを学習リストから削除
            if self.current_card in self.to_learn:
                self.to_learn.remove(self.current_card)

            # 進捗を保存
            self._save_progress()

            # 次のカードを表示
            self.next_card()

        except Exception as e:
            self._show_error(f"進捗保存エラー: {e}")

    def _save_progress(self) -> None:
        """学習進捗をファイルに保存"""
        try:
            if self.to_learn:
                # データフレームに変換して保存
                df = pd.DataFrame(self.to_learn)

                # ディレクトリが存在しない場合は作成
                os.makedirs(os.path.dirname(self.PROGRESS_DATA_FILE), exist_ok=True)

                df.to_csv(self.PROGRESS_DATA_FILE, index=False)
                print(f"進捗を保存しました: {len(self.to_learn)} 単語")
            else:
                # 全て完了した場合は進捗ファイルを削除
                if os.path.exists(self.PROGRESS_DATA_FILE):
                    os.remove(self.PROGRESS_DATA_FILE)
                    print("全ての単語を学習完了！進捗ファイルを削除しました。")

        except Exception as e:
            print(f"進捗保存エラー: {e}")

    def _show_completion_message(self) -> None:
        """学習完了メッセージの表示"""
        self.canvas.itemconfig(self.card_title, text="完了！", fill="green")
        self.canvas.itemconfig(
            self.card_word,
            text="全ての単語を\n学習しました！",
            fill="green"
        )
        self.progress_label.config(text="🎉 学習完了！お疲れ様でした！")

        # ボタンを無効化
        self.wrong_button.config(state="disabled")
        self.right_button.config(state="disabled")

    def _show_error(self, message: str) -> None:
        """エラーメッセージの表示"""
        print(f"エラー: {message}")
        # 実際のアプリケーションでは、tkinter.messagebox を使用することも可能

    def run(self) -> None:
        """アプリケーションの実行"""
        if not self.to_learn:
            self._show_error("学習データがありません。アプリケーションを終了します。")
            return

        self.window.mainloop()


def main() -> None:
    """メイン関数"""
    try:
        app = FlashCardApp()
        app.run()
    except Exception as e:
        print(f"アプリケーション起動エラー: {e}")


if __name__ == "__main__":
    main()
```

## 修正された主要なポイント

### 1. **型ヒントの修正**

```python
# 修正前
self.to_learn: List[Dict[str, str]] = []

# 修正後
self.to_learn: List[Dict[str, Any]] = []
```

- `pd.read_csv().to_dict(orient="records")` は `Any` 型の値を含む可能性があるため、`Dict[str, Any]` に変更

### 2. **データ型変換の明示化**

```python
# 型キャストを明示的に行う
records = data.to_dict(orient="records")
self.to_learn = [
    {str(k): str(v) for k, v in record.items()}
    for record in records
]
```

- pandasから取得したデータを明示的に文字列に変換
- 型安全性を確保

### 3. **画像ボタンの条件分岐**

```python
# 修正前（エラーの原因）
self.wrong_button = tk.Button(
    image=self.wrong_image if self.wrong_image else None,  # None は _ImageSpec に割り当てできない
    text="❌" if not self.wrong_image else "",
    # ...
)

# 修正後
if self.wrong_image:
    self.wrong_button = tk.Button(
        image=self.wrong_image,
        # ...
    )
else:
    self.wrong_button = tk.Button(
        text="❌",
        # ...
    )
```

- `None` を `image` パラメータに渡すことを回避
- 画像の有無で完全に分岐させることで型エラーを解決

### 4. **エラーハンドリングの改善**

```python
except (tk.TclError, FileNotFoundError) as e:
    self._show_error(f"画像ファイルの読み込みエラー: {e}")
```

- `FileNotFoundError` も捕捉するように改善

## 動作確認のポイント

1. **データファイルの確認**
   - `data/french_words.csv` が存在することを確認
   - CSVファイルに `French` と `English` の列があることを確認

2. **画像ファイルの確認**
   - `images/` フォルダ内の画像ファイルが存在するか確認
   - 画像がなくても絵文字フォールバックで動作する

3. **進捗保存の確認**
   - 学習した単語が `data/words_to_learn.csv` に保存される
   - 全て完了すると進捗ファイルが削除される

この修正により、型エラーが解消され、安全に動作するフラッシュカードアプリケーションが完成します。

ボタンが切れている問題を解決するために、以下の箇所を調整する必要があります：

## 1. **ウィンドウサイズの調整**

```python
def _setup_window(self) -> None:
    """メインウィンドウの設定"""
    self.window = tk.Tk()
    self.window.title("Flashy - フラッシュカード学習アプリ")
    self.window.config(
        padx=50,
        pady=50,
        bg=self.BACKGROUND_COLOR
    )
    self.window.resizable(False, False)

    # ウィンドウサイズを調整（高さを増やす）
    self.window.geometry("900x750+100+50")  # 700 → 750に変更
```

## 2. **レイアウトの調整**

```python
def _layout_widgets(self) -> None:
    """ウィジェットのレイアウト"""
    # キャンバスの配置（上部の余白を調整）
    self.canvas.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # ボタンの配置（下部の余白を調整）
    self.wrong_button.grid(row=1, column=0, padx=20, pady=(10, 5))
    self.right_button.grid(row=1, column=1, padx=20, pady=(10, 5))

    # 進捗ラベルの配置
    self.progress_label.grid(row=2, column=0, columnspan=2, pady=(5, 10))
```

## 3. **より詳細な調整が必要な場合**

もしさらに細かい調整が必要な場合は、以下のような変更も可能です：

```python
def _setup_window(self) -> None:
    """メインウィンドウの設定"""
    self.window = tk.Tk()
    self.window.title("Flashy - フラッシュカード学習アプリ")
    self.window.config(
        padx=30,  # 左右の余白を少し減らす
        pady=30,  # 上下の余白を少し減らす
        bg=self.BACKGROUND_COLOR
    )
    self.window.resizable(False, False)

    # ウィンドウサイズをさらに調整
    self.window.geometry("900x800+100+50")

def _layout_widgets(self) -> None:
    """ウィジェットのレイアウト"""
    # グリッドの重みを設定してレスポンシブにする
    self.window.grid_rowconfigure(0, weight=1)
    self.window.grid_columnconfigure(0, weight=1)
    self.window.grid_columnconfigure(1, weight=1)

    # キャンバスの配置
    self.canvas.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="n")

    # ボタンの配置（sticky="ew"で横幅を調整）
    self.wrong_button.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="e")
    self.right_button.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="w")

    # 進捗ラベルの配置
    self.progress_label.grid(row=2, column=0, columnspan=2, pady=(5, 0))
```

## 4. **ボタンサイズの調整**

ボタンが大きすぎる場合は、以下のように調整できます：

```python
def _create_widgets(self) -> None:
    """ウィジェットの作成"""
    # ... 既存のコード ...

    # ボタンの作成（サイズ調整版）
    if self.wrong_image:
        self.wrong_button = tk.Button(
            image=self.wrong_image,
            highlightthickness=0,
            command=self.next_card,
            bg=self.BACKGROUND_COLOR,
            relief="flat",
            width=100,  # 幅を指定
            height=100  # 高さを指定
        )
    else:
        self.wrong_button = tk.Button(
            text="❌",
            highlightthickness=0,
            command=self.next_card,
            bg=self.BACKGROUND_COLOR,
            relief="flat",
            font=("Arial", 20),
            width=6,   # テキストボタンの幅
            height=2   # テキストボタンの高さ
        )

    if self.right_image:
        self.right_button = tk.Button(
            image=self.right_image,
            highlightthickness=0,
            command=self.mark_as_known,
            bg=self.BACKGROUND_COLOR,
            relief="flat",
            width=100,  # 幅を指定
            height=100  # 高さを指定
        )
    else:
        self.right_button = tk.Button(
            text="✅",
            highlightthickness=0,
            command=self.mark_as_known,
            bg=self.BACKGROUND_COLOR,
            relief="flat",
            font=("Arial", 20),
            width=6,   # テキストボタンの幅
            height=2   # テキストボタンの高さ
        )
```

## 推奨する修正

まずは**1番目と2番目の修正**を試してみてください。これで大部分の問題が解決されるはずです。それでも調整が必要な場合は、3番目や4番目の修正を適用してください。

最も重要なのは：

- **ウィンドウの高さを増やす** (`geometry("900x750+100+50")`)
- **paddingを調整する** (`pady=(10, 20)` など)

これらの変更により、ボタンが適切に表示されるようになります。
