"""阿里云 FC 自定义容器事件入口。

FC 通过 HTTP POST 调用容器（CAPort 9000）：
- POST 任何路径 -> 同步执行一次签到任务，返回退出码
- GET  任何路径 -> 健康检查，直接返回 ok
"""
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

RUN_LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def _reply(self, body: bytes, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        print("====== FC 触发签到任务开始 ======", flush=True)
        with RUN_LOCK:
            result = subprocess.run(
                [sys.executable, "main.py", "--config", "/app/state/config.yaml", "run"],
                cwd="/app",
            )
        print(f"====== 任务执行完毕，退出码: {result.returncode} ======", flush=True)
        self._reply(f"miyouqian exit={result.returncode}".encode())

    def do_GET(self):
        self._reply(b"ok")

    def log_message(self, *args):
        pass  # 静默默认访问日志，减少 SLS 噪音


if __name__ == "__main__":
    port = int(__import__("os").environ.get("FC_SERVER_PORT", "9000"))
    print(f"[fc-server] listening on 0.0.0.0:{port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
