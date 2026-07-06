# 在庫復活監視ツール

指定した商品ページを5分おきに監視し、404(在庫切れ)→200(ページ復活)に
変わったタイミングでDiscordに通知するツールです。

## セットアップ手順

1. このリポジトリの内容をGitHubの自分のリポジトリにアップロードする
   - `check_stock.py`
   - `.github/workflows/check_stock.yml`
2. リポジトリの `Settings` → `Secrets and variables` → `Actions` を開く
3. `New repository secret` で以下を登録
   - Name: `DISCORD_WEBHOOK_URL`
   - Secret: DiscordのWebhook URL
4. `Actions` タブを開き、ワークフローが有効になっていることを確認
   (Forkしたリポジトリの場合は明示的に有効化が必要な場合あり)

## 動作確認

`Actions` タブ → `Stock Watcher` → `Run workflow` で手動実行し、
ログに `ステータスコード: 404` などと表示されれば正常に動いています。

## 監視対象を追加・変更する場合

`check_stock.py` の中の `TARGET_URLS` はリスト形式になっているので、
監視したいURLをカンマ区切りで追加してください。

```python
TARGET_URLS = [
    "https://aeonretail.com/product/0/P-2135500002815",
    "https://aeonretail.com/product/0/P-xxxxxxxxxxxxx",
    "https://aeonretail.com/product/0/P-yyyyyyyyyyyyy",
]
```

何個追加しても、1回の実行でまとめて順番にチェックされます。
在庫復活を検知したURLだけ、個別にDiscord通知が届きます。

## 注意事項

- GitHub Actionsのスケジュール実行(cron)は「必ず5分ちょうど」ではなく、
  サーバーの混雑状況によって数分程度ずれることがあります。
- publicリポジトリなら無料枠は実質無制限、privateリポジトリでも
  無料枠(月2,000分)内であれば無料で動作します。
