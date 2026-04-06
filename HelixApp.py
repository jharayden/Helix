import os
import sys
import time
import threading
import uvicorn
import webview
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 导入你原本写好的 api.py 中的核心引擎
from api import app as api_app

# --- 1. 将前端网页强行融合进后端 ---
# 这样不仅能解决跨域问题，还能让 App 独立运行
api_app.mount("/assets", StaticFiles(directory="."), name="assets")

@api_app.get("/")
def serve_ui():
    # 自动寻找你目录下的 index.html
    return FileResponse("index.html")

# --- 2. 定义后台引擎的静默启动程序 ---
def run_server():
    # 强制在本地 8000 端口启动，屏蔽所有终端日志输出 (log_level="critical")
    uvicorn.run(api_app, host="127.0.0.1", port=8000, log_level="critical")

if __name__ == '__main__':
    # --- 3. 开启幽灵线程 ---
    # 让你的 API 引擎在后台跑起来，不阻塞界面
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # 稍微等 1.5 秒钟，确保引擎启动完毕
    time.sleep(1.5)

    # --- 4. 召唤原生 App 窗口！ ---
    window = webview.create_window(
        title='Project Helix v4.5', 
        url='http://127.0.0.1:8000',
        width=1280, 
        height=800,
        resizable=True,
        background_color='#050505' # 完美契合你的 Matrix 纯黑底色
    )
    
    # 正式启动无边框软件界面
    webview.start()