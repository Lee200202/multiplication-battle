"""Gradio 包裝：把九九乘法對戰（index.html）整頁嵌進 Gradio，部署在 Hugging Face Spaces。

遊戲本體是同資料夾的 index.html（純前端、單一檔案），這支程式只負責把它放進 Gradio 頁面。
要改遊戲就改 index.html。本機執行：python app.py
"""
import html
from pathlib import Path

import gradio as gr

try:  # Hugging Face 免費方案的 ZeroGPU 硬體要求至少有一個 @spaces.GPU 函式
    import spaces
except ImportError:
    spaces = None

PAGE = Path(__file__).with_name("index.html")

# 用 position:fixed 蓋滿整個視窗，不受 Gradio 版面邊距影響
IFRAME = (
    '<iframe srcdoc="{page}" title="九九乘法對戰" allow="autoplay; vibrate" '
    'style="position:fixed;inset:0;width:100vw;height:100dvh;border:0;z-index:5;background:var(--mb-bg,#eef1fb)"></iframe>'
)

CSS = """
footer{display:none!important}
html,body{margin:0;overflow:hidden}
.gradio-container{background:var(--mb-bg,#eef1fb)!important}  /* --mb-bg 由遊戲依深淺色模式設定 */
/* 直接開 hf.space 網址時右上角有 Hugging Face 的浮動標籤，讓出上方空間以免蓋到計時器 */
body:has(#huggingface-space-header) iframe{top:58px!important;height:calc(100dvh - 58px)!important}
"""


def game_html():
    return IFRAME.format(page=html.escape(PAGE.read_text(encoding="utf-8"), quote=True))


if spaces:
    @spaces.GPU
    def zerogpu_placeholder():
        return None


with gr.Blocks(title="九九乘法對戰", fill_width=True) as demo:
    gr.HTML(game_html, padding=False)  # 傳函式：每次開頁面都重新讀取 index.html

if __name__ == "__main__":
    demo.launch(css=CSS)
