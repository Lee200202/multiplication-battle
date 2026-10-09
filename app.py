"""Gradio 包裝：把 index.html 整頁嵌進 Gradio，方便部署到 Hugging Face Spaces。

遊戲本體是純前端（index.html），這支程式只負責把它放進 Gradio 頁面。
本機執行：python app.py
"""
import html
from pathlib import Path

import gradio as gr

PAGE = Path(__file__).with_name("index.html").read_text(encoding="utf-8")

IFRAME = (
    f'<iframe srcdoc="{html.escape(PAGE, quote=True)}" title="九九乘法對戰" '
    'allow="autoplay; vibrate" '
    'style="width:100%;height:100dvh;border:0;display:block"></iframe>'
)

# 拿掉 Gradio 預設的邊距與頁尾，讓遊戲佔滿整個畫面
CSS = """
footer{display:none!important}
.gradio-container,.gradio-container main,.gradio-container .wrap,.gradio-container .contain{
  padding:0!important;margin:0!important;max-width:none!important;gap:0!important}
html,body{margin:0;overflow:hidden}
"""

with gr.Blocks(title="九九乘法對戰", fill_width=True) as demo:
    gr.HTML(IFRAME, padding=False)

if __name__ == "__main__":
    demo.launch(css=CSS)
