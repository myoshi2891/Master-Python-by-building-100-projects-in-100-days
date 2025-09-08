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
