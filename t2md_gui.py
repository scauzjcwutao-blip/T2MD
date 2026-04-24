#!/usr/bin/env python3
"""t2md GUI — Tkinter interface."""

import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext

# 使用 engine 接口
from engine import convert, convert_batch
from engine.classifier import DOCLING_EXTENSIONS, RULES_EXTENSIONS
from engine.lang import get_text


class T2mdGui:
    def __init__(self):
        self.lang = "en"
        self._running = False

        self.root = tk.Tk()
        self.root.title("t2md — Text to Markdown Converter")
        self.root.geometry("720x520")
        self.root.minsize(600, 400)

        self.src_var = tk.StringVar(value="./input")
        self.dst_var = tk.StringVar(value="./output")
        self.lang_var = tk.StringVar(value="en")
        self.recursive_var = tk.BooleanVar(value=False)
        self.batch_var = tk.BooleanVar(value=False)      # Batch Mode 开关

        self.status_var = tk.StringVar(value=get_text("ready", self.lang))

        self._widgets = {}
        self._build_ui()

    # ── UI ──────────────────────────────────────────────────────
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Source
        src_frame = ttk.LabelFrame(main, text=get_text("select_src", self.lang), padding=5)
        src_frame.pack(fill=tk.X, pady=(0, 5))
        self._widgets["src_frame"] = src_frame

        ttk.Entry(src_frame, textvariable=self.src_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(src_frame, text="📁", width=3, command=self._browse_src).pack(side=tk.RIGHT)

        # Destination
        dst_frame = ttk.LabelFrame(main, text=get_text("select_dst", self.lang), padding=5)
        dst_frame.pack(fill=tk.X, pady=(0, 5))
        self._widgets["dst_frame"] = dst_frame

        ttk.Entry(dst_frame, textvariable=self.dst_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(dst_frame, text="📁", width=3, command=self._browse_dst).pack(side=tk.RIGHT)

        # Options row
        opt_frame = ttk.Frame(main)
        opt_frame.pack(fill=tk.X, pady=(0, 5))

        lang_label = ttk.Label(opt_frame, text=get_text("language", self.lang) + ":")
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
        self._widgets["lang_label"] = lang_label

        # 保留所有五种语言（按你的要求）
        lang_cb = ttk.Combobox(
            opt_frame,
            textvariable=self.lang_var,
            values=["en", "zh", "ja", "de", "ko"],
            width=8,
            state="readonly",
        )
        lang_cb.pack(side=tk.LEFT, padx=(0, 15))
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        recursive_cb = ttk.Checkbutton(
            opt_frame, text=get_text("recursive", self.lang), variable=self.recursive_var
        )
        recursive_cb.pack(side=tk.LEFT, padx=(0, 15))
        self._widgets["recursive_cb"] = recursive_cb

        # Batch Mode 开关（必要时使用多进程）
        batch_cb = ttk.Checkbutton(
            opt_frame, text="Batch Mode (fast for large number of files)", variable=self.batch_var
        )
        batch_cb.pack(side=tk.LEFT)
        self._widgets["batch_cb"] = batch_cb

        # Start button
        start_btn = ttk.Button(main, text=get_text("start", self.lang), command=self._start)
        start_btn.pack(fill=tk.X, pady=(0, 5))
        self._widgets["start_btn"] = start_btn

        # Log area
        self.log = scrolledtext.ScrolledText(main, height=15, state=tk.DISABLED, font=("Courier", 10))
        self.log.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Status bar
        ttk.Label(main, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

    # Helpers（保持不变）
    def _browse_src(self):
        path = filedialog.askdirectory()
        if path:
            self.src_var.set(path)

    def _browse_dst(self):
        path = filedialog.askdirectory()
        if path:
            self.dst_var.set(path)

    def _on_lang_change(self, _event=None):
        self.lang = self.lang_var.get()
        self._refresh_ui_text()

    def _refresh_ui_text(self):
        lang = self.lang
        self._widgets["src_frame"].config(text=get_text("select_src", lang))
        self._widgets["dst_frame"].config(text=get_text("select_dst", lang))
        self._widgets["lang_label"].config(text=get_text("language", lang) + ":")
        self._widgets["recursive_cb"].config(text=get_text("recursive", lang))
        self._widgets["start_btn"].config(text=get
