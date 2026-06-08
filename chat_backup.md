# Regulation Agent Chat Backup

Date: 2026-06-08

## 目的
備份本次與 Copilot Chat 的對話重點，方便日後查閱專案調整與 GitHub Actions 設定。

## 已完成修改
- 新增 GitHub Actions workflow：`.github/workflows/tg_debug.yml`
- 新增 Telegram 測試檢查腳本：`scripts/tg_check_and_send.py`
- 修正 `main.py` 中 `tg.send_telegram` 的呼叫與回傳判斷
- 改善 `notifier/telegram.py`：使用 `os.getenv` 讀取 `BOT_TOKEN` / `CHAT_ID`，並回傳 success flag
- 改善 `db/database.py`：明確捕捉 `sqlite3.IntegrityError`，避免裸 `except`
- 更新 `test_telegram.py`：移除硬編碼 token，改用環境變數
- 新增 `requirements.txt`

## 主要問題
- GitHub Actions 執行時，Telegram API 回傳 `403 Forbidden: the bot can't send messages to the bot`
- 原因：`CHAT_ID` 設成了 Bot 本身的 id，而不是目標使用者或群組 id

## 解決方案
1. 在 GitHub Secrets 中設定 `BOT_TOKEN` 與 `CHAT_ID`
2. 若是私人聊天，先對 bot 傳一則訊息，例如 `/start`
3. 透過 `getUpdates` 或 Telegram 工具取得正確的 `chat_id`
4. 重新執行 workflow，檢查 `sendMessage` 是否成功

## 重要備註
- 這個檔案是手動備份的對話重點，並不等同於 Copilot Chat 的原始記錄。
- `BOT_TOKEN` 和 `CHAT_ID` 不能寫入程式碼或 commit；應該放在 GitHub Secrets 中。
- 本專案的修改需要 commit 並 push 到 GitHub 才會真正備份遠端倉庫。
