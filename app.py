"""Gradio 包裝：把九九乘法對戰（index.html）整頁嵌進 Gradio，部署在 Hugging Face Spaces。

遊戲本體是同資料夾的 index.html（純前端、單一檔案），要改遊戲就改它。
這支程式負責兩件事：把遊戲放進 Gradio 頁面，以及提供全站英雄榜的讀寫端點。
本機執行：python app.py
"""
import html
import json
import re
import threading
import time
from pathlib import Path

import gradio as gr

try:  # Hugging Face 免費方案的 ZeroGPU 硬體要求至少有一個 @spaces.GPU 函式
    import spaces
except ImportError:
    spaces = None

HERE = Path(__file__).parent
PAGE = HERE / "index.html"



def pick_store():
    """全站英雄榜的存檔位置。Space 有掛載儲存桶（/data）而且真的寫得進去就存在那裡，重啟也不會消失；
    否則存在程式旁邊，Space 重啟或重新建置時會清空。"""
    for folder in (Path("/data"), HERE):
        try:
            probe = folder / ".write-test"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return folder / "heroes.json"
        except OSError:
            continue
    return HERE / "heroes.json"


SCORES = pick_store()
print(f"英雄榜存檔位置：{SCORES}", flush=True)
KEEP = 50  # 每種秒數最多保留幾筆
LOCK = threading.Lock()

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
    page = PAGE.read_text(encoding="utf-8")
    # 告訴遊戲這個頁面有全站英雄榜可用
    page = page.replace('<meta name="mb-api" content="">', '<meta name="mb-api" content="gradio">')
    return IFRAME.format(page=html.escape(page, quote=True))


def load():
    try:
        return json.loads(SCORES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []


def heroes() -> list:
    """全站英雄榜的全部紀錄。"""
    with LOCK:
        return load()


def hero_add(name: str, score: int, acc: int, secs: int, mode: str, input_mode: str, table_range: str) -> dict:
    """登記一筆成績。同一個名字在同一種秒數只留最高分（規則和 index.html 的 addHero 相同）。"""
    name = re.sub(r"[\x00-\x1f<>]", "", str(name)).strip()[:8]
    score, acc, secs = int(score), int(acc), int(secs)
    valid = (
        name
        and 10 <= secs <= 600
        and 0 < score <= secs * 2.5  # 每題至少要 0.4 秒，超過就不可能是真的成績
        and 0 <= acc <= 100
        and mode in ("solo", "duo", "cpu")
        and input_mode in ("choice", "pad")
        and re.fullmatch(r"[1-9～、]{1,17}", str(table_range))
    )
    if not valid:
        raise gr.Error("成績資料不正確")
    with LOCK:
        rows = load()
        old = next((r for r in rows if r["n"] == name and r["secs"] == secs), None)
        if old and old["s"] >= score:
            return {"rank": 0, "best": old["s"]}
        rec = {"n": name, "s": score, "acc": acc, "secs": secs, "mode": mode,
               "input": input_mode, "range": table_range, "t": int(time.time() * 1000)}
        same = [r for r in rows if r["secs"] == secs and r is not old] + [rec]
        same = sorted(same, key=lambda r: (-r["s"], -r["acc"], r["t"]))[:KEEP]
        rows = [r for r in rows if r["secs"] != secs] + same
        SCORES.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        return {"rank": next((i + 1 for i, r in enumerate(same) if r is rec), 0)}


if spaces:
    @spaces.GPU
    def zerogpu_placeholder():
        return None


with gr.Blocks(title="九九乘法對戰", fill_width=True) as demo:
    gr.HTML(game_html, padding=False)  # 傳函式：每次開頁面都重新讀取 index.html
    gr.api(heroes, api_name="heroes")
    gr.api(hero_add, api_name="hero_add")

if __name__ == "__main__":
    demo.launch(css=CSS)
