---
title: 九九乘法對戰
emoji: ✖️
colorFrom: indigo
colorTo: yellow
sdk: gradio
sdk_version: 6.3.0
app_file: app.py
pinned: false
---

# 九九乘法對戰

九九乘法表對戰遊戲，免安裝，手機、平板、電腦打開網址就能玩。

## 玩法

| 模式 | 說明 |
| --- | --- |
| 🧒 單人挑戰 | 限時內答對越多越好，會記錄最高分 |
| ⚔️ 雙人對戰 | 同一台裝置兩人比賽，可選「面對面（上下）」或「並排（左右）」 |
| 🤖 挑戰電腦 | 和電腦比賽，三種難度 |
| 🎰 拉霸口答 | 按一下出一題、用說的回答，計算限時內的次數 |

可調整的設定：遊戲時間（30／60／90／120 秒或自訂 10～600 秒）、乘法範圍（1～9 任選）、作答方式（四選一／數字鍵盤）、答錯是否扣分；雙人對戰可選兩人「相同題目」或「不同題目」（防止偷看）。

外觀：電腦寬螢幕會用滿整個版面（設定攤成多欄、單人模式題目在左作答在右）；主選單可切換深色／淺色，預設跟隨系統。

英雄榜：單人、雙人、挑戰電腦結束後輸入名字即可上榜，依秒數分開排名，同一個名字只留最高分。每台裝置的瀏覽器都會存一份；從 Hugging Face Space 開啟時另外有全站英雄榜（所有人都看得到，由 `app.py` 存成 `heroes.json`）。

鍵盤操作：單人按 `1 2 3 4`；雙人對戰四選一時玩家 1 按 `Q W A S`、玩家 2 按 `I O K L`，數字鍵盤時玩家 1 用上排數字鍵、玩家 2 用右側數字鍵盤；拉霸口答按空白鍵或 Enter。

## 檔案

- `index.html`：遊戲本體，單一檔案、純前端，不需要伺服器。
- `app.py`：Gradio 包裝，把同資料夾的 `index.html` 嵌進 Gradio 頁面，並提供全站英雄榜的讀寫端點。Space 掛載儲存桶到 `/data` 時紀錄會永久保存，否則 Space 重啟就清空。

## 網址與部署

- **GitHub Pages**：https://lee200202.github.io/multiplication-battle/ （`main` 分支根目錄的 `index.html`）
- **Hugging Face Spaces（Gradio）**：https://huggingface.co/spaces/Hsun0500/multiplication-battle 。Space 裡放 `app.py` 和 `index.html` 兩個檔案。
- 本機執行 Gradio 版：`pip install gradio` 後執行 `python app.py`。
