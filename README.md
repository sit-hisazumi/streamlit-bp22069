[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=22079233)
# Streamlit Template

**Streamlitアプリケーション開発用テンプレート**

GitHub CodespacesとVSCodeでの開発に最適化されたStreamlitアプリのテンプレートプロジェクトです。

## 🚀 クイックスタート

### GitHub Codespaces（推奨）

1. **このリポジトリをフォーク**
2. **Codespace作成**: 緑の「Code」ボタン → 「Create codespace on main」
3. **自動セットアップ完了を待機**
4. **アプリ実行**:
   ```bash
   streamlit run hello_world.py
   ```

### ローカル環境

#### uv使用（推奨）
```bash
git clone <your-repo-url>
cd streamlit-template
uv sync
uv run streamlit run hello_world.py
```

#### pip使用
```bash
git clone <your-repo-url>
cd streamlit-template
pip install -r requirements.txt
streamlit run hello_world.py
```

## 📁 プロジェクト構造

```
streamlit-template/
├── hello_world.py             # サンプルアプリ（Hello World）
├── .devcontainer/             # GitHub Codespaces設定
├── .vscode/                   # VSCode設定
├── .streamlit/                # Streamlit設定・シークレット
├── pyproject.toml             # プロジェクト設定（uv対応）
├── requirements.txt           # pip互換依存関係
├── requirements-dev.txt       # 開発用依存関係
└── .gitignore                 # Git除外設定
```

## 🎯 サンプルアプリケーション

### sample1: 製造ライン稼働状況ダッシュボード

```bash
streamlit run sample1/app.py
```

製造ラインの設備稼働率をリアルタイムで監視するダッシュボード。

- 設備ごとの稼働率カード表示（稼働中/注意/停止の状態表示）
- 過去24時間の稼働率推移グラフ（Altair）
- CSVファイルからのデータ読み込み対応

---

### sample2: センサーモニタリングダッシュボード

```bash
streamlit run sample2/app.py
```

温度・湿度・CO2濃度などのセンサーデータを監視するダッシュボード。

- リアルタイムセンサー値の表示（正常/警告の状態判定）
- 適正範囲を可視化したグラフ表示
- 表示期間の切り替え（1時間〜12時間）
- 統計情報（最高/最低/平均値）
- 5秒ごとの自動更新オプション

---

### sample3: 絵文字キャンバス

```bash
streamlit run sample3/app.py
```

絵文字を使ってドット絵を作成できるツール。

- 8x8〜24x24のキャンバスサイズ
- 8カテゴリの絵文字パレット（自然、動物、食べ物、天気、顔、乗り物、建物、記号）
- クリア・元に戻す・塗りつぶし機能
- テキスト形式でのエクスポート

---

### sample4: カラーパレット生成器

```bash
streamlit run sample4/app.py
```

配色理論に基づいたカラーパレットを生成するツール。

- 6種類の配色タイプ（ランダム、類似色、補色、トライアド、モノクロマティック、分裂補色）
- ベースカラーの選択、色数の調整（3〜8色）
- プレビュー（グラデーション、UIサンプル、テキスト）
- エクスポート（HEX、CSS変数、Tailwind設定）

---

### hello_world.py

```bash
streamlit run hello_world.py
```

シンプルなStreamlitアプリの例。名前を入力するとメッセージを表示。

## 🛠️ 開発環境

### 含まれる設定

- **GitHub Codespaces**: 自動環境構築
- **VSCode設定**: Python開発最適化
- **Code Formatter**: Black
- **Linter**: Ruff
- **Streamlit設定**: 開発モード有効

### 推奨VSCode拡張機能

- Python
- Black Formatter
- Ruff
- Pylint

## 🔧 カスタマイズ

### 依存関係の追加

```bash
# uv使用
uv add package-name

# pip使用
pip install package-name
echo "package-name" >> requirements.txt
```

### Streamlit設定

- **基本設定**: `.streamlit/config.toml`
- **シークレット**: `.streamlit/secrets.toml` (gitignoreに含まれます)

### VSCode設定

- **エディタ設定**: `.vscode/settings.json`
- **推奨拡張**: `.vscode/extensions.json`

## 🔐 セキュリティ

- **`.streamlit/secrets.toml`** は自動的にgitignoreされます
- **APIキー**は secrets.toml で管理してください
- **本番環境**では環境変数を使用してください

## 📦 デプロイ

### Streamlit Community Cloud

1. GitHubにプッシュ
2. [share.streamlit.io](https://share.streamlit.io) でデプロイ
3. メインファイル: `hello_world.py` または作成したアプリファイル

### その他のプラットフォーム

- Heroku
- Railway
- Render
- Docker

## 🤝 貢献

プルリクエストやイシューを歓迎します！

## 📄 ライセンス

MIT License

---

**🌟 Happy Streamlit Development!**
