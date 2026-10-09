"""Gradio 包裝：把九九乘法對戰（index.html）整頁嵌進 Gradio，部署在 Hugging Face Spaces。

遊戲本體是純前端的 index.html。這支程式優先讀取同資料夾的 index.html；
沒有的話就從 GitHub 抓最新版（每 5 分鐘更新一次），所以遊戲改版只要推到 GitHub。
本機執行：python app.py
"""
import html
import time
import urllib.request
from pathlib import Path

import gradio as gr

try:  # Hugging Face 免費方案的 ZeroGPU 硬體要求至少有一個 @spaces.GPU 函式
    import spaces
except ImportError:
    spaces = None

LOCAL = Path(__file__).with_name("index.html")
REMOTE = "https://raw.githubusercontent.com/Lee200202/multiplication-battle/main/index.html"
PAGES = "https://lee200202.github.io/multiplication-battle/"
TTL = 300  # 秒
_cache = {"at": 0.0, "page": ""}

IFRAME = (
    '<iframe {src} title="九九乘法對戰" allow="autoplay; vibrate" '
    'style="width:100%;height:100dvh;border:0;display:block"></iframe>'
)

# 拿掉 Gradio 預設的邊距與頁尾，讓遊戲佔滿整個畫面
CSS = """
footer{display:none!important}
.gradio-container,.gradio-container main,.gradio-container .wrap,.gradio-container .contain{
  padding:0!important;margin:0!important;max-width:none!important;gap:0!important}
html,body{margin:0;overflow:hidden}
"""


def fetch_remote():
    if time.time() - _cache["at"] > TTL:
        try:
            with urllib.request.urlopen(REMOTE, timeout=10) as r:
                _cache["page"] = r.read().decode("utf-8")
            _cache["at"] = time.time()
        except OSError:
            _cache["at"] = time.time() - TTL + 30  # 抓不到就沿用舊內容，30 秒後再試
    return _cache["page"]


def game_html():
    page = LOCAL.read_text(encoding="utf-8") if LOCAL.exists() else fetch_remote()
    if not page:  # 一次都沒抓到時，直接嵌入 GitHub Pages
        return IFRAME.format(src=f'src="{PAGES}"')
    return IFRAME.format(src=f'srcdoc="{html.escape(page, quote=True)}"')


if spaces:
    @spaces.GPU
    def zerogpu_placeholder():
        return None


with gr.Blocks(title="九九乘法對戰", fill_width=True) as demo:
    gr.HTML(game_html, padding=False)  # 傳函式：每次開頁面都重新取得內容

if __name__ == "__main__":
    demo.launch(css=CSS)
