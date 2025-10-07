# Day 53 サンプル解答（`main_answer.py`）

## 概要

`main_answer.py` は Zillow クローンの物件情報を Google フォームへ送信する講義用リファレンス実装です。`requests` と BeautifulSoup でデータを収集し、固定 XPath の Selenium 操作でフォームを埋めます。実行すると授業動画で使用したデータセットが再現されます。

## 主な処理

1. **スクレイピング**
   - `https://appbrewery.github.io/Zillow-Clone/` をブラウザ相当のヘッダーで取得します。
   - CSS セレクタ `.StyledPropertyCardDataWrapper a/address` と `.PropertyCardWrapper span` でリンク・住所・価格をそれぞれ収集します。
   - 住所は改行を除去し、価格は `/mo` や `+` を取り除く程度の簡易クリーニングを行い、デバッグ用に出力します。
2. **フォーム入力**
   - Chrome を起動し（`detach=True` によって処理後もウィンドウを保持）、
   - 各物件ごとに `GOOGLE_FORM_LINK` へ移動 →2 秒待機 →3 つの短答欄を XPath で指定して入力 → 送信ボタンをクリック、という流れを繰り返します。

## 必要条件と準備

- `.env` に環境変数 `GOOGLE_FORM_LINK` を定義しておきます。
- 使用ライブラリは `beautifulsoup4`、`requests`、`selenium`、`python-dotenv`。著者検証時のバージョンはファイル冒頭に記載しています。
- ChromeDriver はローカルの Chrome バージョンと一致させ、`PATH` から参照できるようにしてください。

## 使い方

```bash
cd Day53
python main_answer.py
```

XPath ロケータがハードコードされているため（例: `//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]...`）、Google フォームの構成は授業テンプレートと同一である必要があります。フォームをカスタマイズした場合は XPath も合わせて更新してください。

## main_answer_refactored.py のリファクタリングポイント

- Pylance での型補完を高めるために `Listing` データクラスと `Final` 定数を導入し、スクレイピング結果と固定値を明確化しました。
- スクレイピング・フォーム送信・ドライバー生成を `fetch_listings` / `submit_listings` / `create_driver` に分離し、引数と戻り値に型を付けて処理責務を整理しています。
- Selenium 操作では `ChromeWebDriver` と `WebElement` を明示し、フォーム入力を `fill_form` に切り出すことで再利用性とテスト容易性を向上させました。
- `detach=True` を既定にしつつ、例外時にもリソースを確実に解放できるようドライバーライフサイクルを管理する形に改良しています。
