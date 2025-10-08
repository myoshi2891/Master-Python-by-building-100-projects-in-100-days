# Day 53 自動化（`main.py`）

## 概要

`main.py` は App Brewery の Zillow クローンから賃貸物件リストをスクレイピングし、Selenium を使って Google フォームへ 1 件ずつ送信します。全件送信が終わるとフォーム編集者の回答タブを開き、Sheets アイコンをクリックしてスプレッドシートに書き出します。コマンド 1 つで物件一覧シートを生成できる構成です。

## 設定

- `.env`
  - `GOOGLE_FORM_LINK`（必須）: 物件情報を受け付ける Google フォームの _viewform_ 共有リンク。
  - `GOOGLE_FORM_FIELD_ORDER`（任意）: フォームの質問順を表すカンマ区切りリスト。既定値は `address,price,link` で、質問配置を変更した場合に更新します。
  - `GOOGLE_FORM_SHEET_BUTTON_LABELS` / `GOOGLE_FORM_SHEET_CONFIRM_TEXTS`（任意）: Sheets アイコンや確認ボタンを検出する際のラベル候補。英語と日本語の代表的な表現を既定で含めています。
- Chrome プロファイル
  - リポジトリ直下の `chrome_profile` をユーザーデータとして読み込むため、フォーム編集者アカウントでサインイン済みであることを確認してください。未ログインだとシート作成が拒否されます。

## 実行フロー

1. **物件データの取得**
   - `requests` が Zillow クローンをブラウザに近いヘッダーで取得します。
   - BeautifulSoup が `links`・`addresses`・`prices` を抽出し、余分な空白や重複を除去します。
2. **送信データの整形**
   - `compose_listings` が 3 つのリストを `Listing` データクラスへまとめ、もっとも短い件数にそろえつつ不一致をログに警告します。
3. **Selenium による送信**
   - `create_chrome_driver` が同梱プロファイル付きで Chrome を起動します。
   - `locate_question_inputs` で表示中の入力欄を動的に特定し、`FIELD_ORDER` の順で各 `Listing` を入力します。
   - 送信後は確認ページの読み込みを待ってから次の物件に進みます。
4. **スプレッドシート作成**
   - 最後の送信後に `create_sheet_from_responses` が回答タブを開き、Sheets アイコンをクリックして既存シートの起動または新規作成を実行します。

## 使い方

```bash
cd Day53
python main.py
```

各送信の進捗やスプレッドシート作成の状況はログに表示されます。ネットワークや認証で失敗した場合は（VPN や Chrome へのログインなど）原因を解消してから再実行してください。中断したいときは Ctrl+C を押すと処理終了後に Chrome が自動で閉じます。

## main_refactored.py のリファクタリングポイント

- Pylance が型を解釈しやすいよう `Final` や `list[str]` を明示し、Selenium 関連は `ChromeWebDriver` と `WebElement` を直接指定して補完性と静的解析の精度を高めました。
- 各関数に簡潔な docstring とローカル変数の型を追加し、処理の責務が読み取りやすくなるように整理しました。
- フォーム入力では `zip(..., strict=False)` を使って項目順の対応を保ちつつ、入力フィールド検出ロジックを関数に切り出して再利用性を上げています。
- これらの変更は既存の実行手順を維持しながら、型チェックの警告を解消し、保守性を向上させることを目的としています。
