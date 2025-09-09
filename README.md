# Master Python by building 100 projects in 100 days

## 概要

このリポジトリは、100日間で100のプロジェクトを構築しながらPythonプログラミングを習得する構造化された学習コレクションです。基本的なスクリプトから本格的なデスクトップアプリケーション（GUI、APIインテグレーション、自動メール送信システム）まで、段階的に複雑化する完全な実装例を提供します。

## 学習領域

ここでは5つの学習領域を説明しています：

- 📧 **Email & Communication Systems（メール・通信システム）**
- 🖥️ **Desktop GUI Applications（デスクトップGUIアプリケーション）**  
- 🎮 **Games & Interactive Applications（ゲーム・インタラクティブアプリケーション）**
- 📊 **Data Processing & Utilities（データ処理・ユーティリティ）**
- 🌐 **API Integration Systems（APIインテグレーションシステム）**

各領域では、学習者が手続き型プログラミングからオブジェクト指向設計へと進歩する過程で、異なるPythonライブラリ、設計パターン、アーキテクチャアプローチを習得できます。

## リポジトリ構成とファイル一覧

```
📦 Archive/
├── 📁 Day 25/
│   ├── 🎯 day-25-us-states-game-start/
│   │   ├── 50_states.csv
│   │   ├── blank_states_img.gif
│   │   ├── main.py
│   │   └── missing_states.csv
│   └── 📊 pandas_basic/
│       ├── 2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv
│       ├── main.py
│       ├── new_data.csv
│       ├── squirrel_fur_color_data.csv
│       └── weather_data.csv
├── 📁 Day 28/
│   └── ⏰ pomodoro-start/
│       ├── main.py
│       ├── main_refactored.py
│       └── tomato.png
├── 📁 Day 29/
│   └── 🔒 password-manager-start/
│       ├── README.md
│       ├── logo.png
│       ├── main.py
│       ├── main_refactored.py
│       └── secret.txt
└── 📁 Day 32/
    ├── 🎂 Birthday Wisher (Day 32) start/
    │   ├── main.py
    │   ├── quotes.txt
    │   └── requirements.txt
    └── 💌 birthday-wisher-extrahard-start/
        ├── README.md
        ├── birthday_emailer.py
        ├── birthdays.csv
        ├── letter_templates/
        │   ├── letter_1.txt
        │   ├── letter_2.txt
        │   └── letter_3.txt
        └── main.py
```

## システム複雑度分布

```
🏗️ システムアーキテクチャ（学習複雑度別）

高複雑度 (7.0+) ████████████████████ 
├── 📧 Birthday Emailer System (7.66)
└── 🌐 ISS Tracking Notifications (7.2)

中複雑度 (5.0-7.0) ████████████████
├── 🔒 Password Manager (6.8)  
├── ⏰ Pomodoro Timer (6.2)
├── 🎯 Flash Card Learning App (5.9)
└── 🐍 Snake Game (5.4)

低複雑度 (3.0-5.0) ████████
├── 🎮 Turtle Graphics Games (4.2)
├── 📊 NATO Phonetic Converter (3.8)
└── 📈 CSV Data Processing (3.5)

基礎レベル (<3.0) ████
└── 🐢 Basic Turtle Graphics (2.1)
```

## アーキテクチャ進化パターン

```
📈 学習パス全体のアーキテクチャ進化

レベル 1: 基礎スクリプト
┌─────────────────┐
│ 手続き型コード    │
│ ・基本構文       │
│ ・単純な関数      │ 
└─────────────────┘
         ↓
レベル 2: 構造化プログラム  
┌─────────────────┐
│ モジュール分割    │
│ ・関数分離        │
│ ・データ構造      │
└─────────────────┘
         ↓
レベル 3: オブジェクト指向
┌─────────────────┐
│ クラスベース設計   │
│ ・カプセル化      │
│ ・継承とポリモー   │
│ ・エラーハンドリング │
└─────────────────┘
```

## 主要システムカテゴリ

### 📧 Email & Communication Systems
最も洗練されたシステムで、包括的なテンプレート処理、CSVデータインテグレーション、プロダクション対応SMTP処理を備えたBirthdayEmailerクラスが特徴です。

**キー実装:**
- `BirthdayEmailer.check_and_send_birthday_emails()` - メイン統制メソッド
- `BirthdayEmailer.load_birthdays()` - pandasを使用したCSVデータ処理
- `letter_templates/letter_*.txt` ファイルのテンプレートシステム
- `python-dotenv`による環境変数管理

### 🖥️ Desktop GUI Applications  
手続き型GUIプログラミングからクラスベースアーキテクチャへの進歩を実演するTkinterベースアプリケーション。

**アーキテクチャハイライト:**
- `PasswordManager._setup_window()` - ウィンドウ設定
- `PasswordManager._create_widgets()` - ウィジェット初期化・セットアップ  
- `PasswordManager.generate_password()` - 暗号学的に安全なパスワード生成
- 画像アセット不足時のフォールバック機能

### 🎮 Games & Interactive Applications
オブジェクト指向ゲーム開発パターン、衝突検知システム、状態管理を実演するTurtleグラフィックスベースゲーム。

**コアゲーム要素:**
- 複数ゲーム間で共有されるScoreboardクラス
- SnakeとPong実装の衝突検知アルゴリズム
- `window.after()`タイミング機構のゲームループパターン
- 動的ゲームエンティティのオブジェクトライフサイクル管理

### 📊 Data Processing & Utilities
実世界のデータ操作技法を実演するpandasベースのデータ分析・CSV処理ユーティリティ。

**データ処理パターン:**
- データロード用`pd.read_csv()`インテグレーション
- データ変換用辞書包括表記
- `pd.DataFrame.to_csv()`によるエクスポート機能  
- 不正形式入力のデータ検証・エラーハンドリング

## 技術スタックと依存関係

### コアPythonライブラリ

| ライブラリカテゴリ | 主要ライブラリ | 使用パターン |
|------------------|---------------|-------------|
| GUI開発 | tkinter, turtle | デスクトップアプリとゲーム |
| データ処理 | pandas, csv | データ分析とファイル処理 |
| ネットワーク・メール | smtplib, requests | メール自動化とAPIインテグレーション |
| システムインテグレーション | os, pathlib, datetime | ファイル操作とシステム連携 |
| 開発ツール | typing, logging | 型安全性とデバッグ |

### 外部依存関係アーキテクチャ

```
🔧 依存関係アーキテクチャとインテグレーションパターン

外部ライブラリ
├── 📊 pandas (データ分析)
│   ├── DataFrame操作
│   ├── CSV読み書き  
│   └── データ変換
├── 🌐 requests (HTTP通信)
│   ├── API呼び出し
│   ├── JSON処理
│   └── エラーハンドリング
├── 📧 python-dotenv (設定管理)
│   ├── 環境変数ロード
│   ├── 秘匿情報管理
│   └── 設定分離
└── 🎨 tkinter (標準ライブラリ)
    ├── ウィンドウ管理
    ├── ウィジェット制御
    └── イベントハンドリング
```

## 学習成果と技術進歩

このリポジトリ構造は、段階的複雑度導入によりPythonプログラミング習得を促進します。学習者は基本構文から高度なソフトウェアエンジニアリング実践まで進歩します：

### 📈 進歩項目

1. **エラーハンドリング進化**: 基本的なtry-catchブロックから、カスタムエラー型とログインテグレーションを備えた包括的例外階層まで

2. **アーキテクチャパターン**: 手続き型スクリプトから適切なカプセル化、継承、コンポジションを備えたオブジェクト指向設計への移行

3. **型安全性**: 基本アノテーションから複雑なジェネリック型やOptional処理まで、型ヒントの段階的導入

4. **テスト・検証**: 入力検証、データサニタイゼーション、防御的プログラミング実践

5. **プロダクション対応**: 環境変数管理、設定処理、デプロイメント考慮事項

最高複雑度システム（誕生日メールシステムなど）は、教育的明確性と段階的学習パスを維持しながら、エンタープライズレベルのPython開発実践を実演します。

