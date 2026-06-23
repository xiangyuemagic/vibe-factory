#!/usr/bin/env python3
"""Netlify 部署用的 Python 脚本 - 只在本地测试/开发时使用"""
from flask import Flask, send_from_directory
app = Flask(__name__, static_url_path="", static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
