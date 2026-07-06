import os
import sys
import requests

# 監視対象の商品ページURL(何個でも追加可能)
TARGET_URLS = [


# ブラウザからのアクセスに見せるためのヘッダー
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def check_stock():
    if not WEBHOOK_URL:
        print("ERROR: DISCORD_WEBHOOK_URL が設定されていません。")
        sys.exit(1)

    if not TARGET_URLS:
        print("ERROR: TARGET_URLS が空です。監視したいURLを追加してください。")
        sys.exit(1)

    for url in TARGET_URLS:
        check_single_url(url)


def check_single_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"[{url}] リクエストエラー: {e}")
        return

    print(f"[{url}] ステータスコード: {response.status_code}")

    # 404以外(ページが存在する)なら復活とみなして通知
    if response.status_code == 200:
        notify_discord(url)
    else:
        print(f"[{url}] 在庫はまだ復活していません。")


def notify_discord(url):
    message = {
        "content": (
            "🚨 **在庫復活を検知しました!** 🚨\n"
            f"{url}\n"
            "急いで確認してください!"
        )
    }
    try:
        res = requests.post(WEBHOOK_URL, json=message, timeout=10)
        if res.status_code in (200, 204):
            print(f"[{url}] Discordに通知を送信しました。")
        else:
            print(f"[{url}] Discord通知の送信に失敗しました: {res.status_code} {res.text}")
    except requests.RequestException as e:
        print(f"[{url}] Discord通知エラー: {e}")


if __name__ == "__main__":
    check_stock()
