#!/usr/bin/env python3
"""t2md GUI — Tkinter interface."""

import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext

# === 关键修复：使用我们已有的 engine 接口 ===
from engine import convert          # 主转换函数
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
        self.status_var = tk.StringVar(value=get_text("ready", self.lang))

        self._widgets = {}
        self._build_ui()

    # ── UI ──────────────────────────────────────────────────────
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Source
        src_frame = ttk.LabelFrame(
            main, text=get_text("select_src", self.lang), padding=5
        )
        src_frame.pack(fill=tk.X, pady=(0, 5))
        self._widgets["src_frame"] = src_frame

        ttk.Entry(src_frame, textvariable=self.src_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(src_frame, text="📁", width=3, command=self._browse_src).pack(
            side=tk.RIGHT
        )

        # Destination
        dst_frame = ttk.LabelFrame(
            main, text=get_text("select_dst", self.lang), padding=5
        )
        dst_frame.pack(fill=tk.X, pady=(0, 5))
        self._widgets["dst_frame"] = dst_frame

        ttk.Entry(dst_frame, textvariable=self.dst_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(dst_frame, text="📁", width=3, command=self._browse_dst).pack(
            side=tk.RIGHT
        )

        # Options row
        opt_frame = ttk.Frame(main)
        opt_frame.pack(fill=tk.X, pady=(0, 5))

        lang_label = ttk.Label(opt_frame, text=get_text("language", self.lang) + ":")
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
        self._widgets["lang_label"] = lang_label

        # 支持所有语言（en/zh/ja/de/ko）
        lang_cb = ttk.Combobox(
            opt_frame,
            textvariable=self.lang_var,
            values=["en", "zh", "ja", "de", "ko"],
            width=6,
            state="readonly",
        )
        lang_cb.pack(side=tk.LEFT, padx=(0, 15))
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        recursive_cb = ttk.Checkbutton(
            opt_frame, text=get_text("recursive", self.lang), variable=self.recursive_var
        )
        recursive_cb.pack(side=tk.LEFT)
        self._widgets["recursive_cb"] = recursive_cb

        # Start button
        start_btn = ttk.Button(
            main, text=get_text("start", self.lang), command=self._start
        )
        start_btn.pack(fill=tk.X, pady=(0, 5))
        self._widgets["start_btn"] = start_btn

        # Log area
        self.log = scrolledtext.ScrolledText(
            main, height=15, state=tk.DISABLED, font=("Courier", 10)
        )
        self.log.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Status bar
        ttk.Label(main, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

    # ── Helpers ─────────────────────────────────────────────────
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
        self._widgets["start_btn"].config(text=get_text("start", lang))
        self.status_var.set(get_text("ready", lang))

    def _log(self, msg: str):
        """统一日志输出（带 [T2MD] 前缀，保持项目风格）"""
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"[T2MD] {msg}\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def _collect_files(self):
        """收集支持的文件（兼容 docling + rules 引擎）"""
        src = Path(self.src_var.get())
        files = []
        supported = DOCLING_EXTENSIONS | RULES_EXTENSIONS

        if src.is_file():
            if src.suffix.lower() in supported:
                files.append(src)
        elif src.is_dir():
            pattern = "**/*" if self.recursive_var.get() else "*"
            for ext in supported:
                files.extend(src.glob(f"{pattern}{ext}"))
        return sorted(set(files))

    def _validate_paths(self) -> bool:
        src = Path(self.src_var.get())
        if not src.exists():
            messagebox.showerror("Error", get_text("src_not_found", self.lang))
            return False

        dst = Path(self.dst_var.get())
        if not dst.exists():
            try:
                dst.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                messagebox.showerror("Error", str(e))
                return False
        return True

    # ── Conversion ──────────────────────────────────────────────
    def _start(self):
        if self._running:
            return
        if not self._validate_paths():
            return

        self._running = True
        self._widgets["start_btn"].config(state=tk.DISABLED)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        dst = self.dst_var.get()
        lang = self.lang   # 当前界面语言（仅用于 UI 提示，不影响转换）

        self.root.after(0, lambda: self.status_var.set(get_text("converting", lang)))
        self.root.after(0, lambda: self._log(f"--- {get_text('start', lang)} ---"))

        files = self._collect_files()
        if not files:
            self.root.after(0, lambda: self._log(get_text("no_files", lang)))
            self._finish()
            return

        success = 0
        for f in files:
            try:
                # 调用我们真实的 convert 函数（单文件转换）
                convert(str(f), dst)          # ← 核心调用
                msg = f"✅ {f.name} 转换成功"
                success += 1
            except Exception as e:
                msg = f"❌ {f.name} — {e}"
            self.root.after(0, lambda m=msg: self._log(m))

        done_msg = f"{get_text('complete', lang)}: {success} {get_text('files_processed', lang)}"
        self.root.after(0, lambda: self._log(done_msg))
        self.root.after(0, lambda: self.status_var.set(done_msg))
        self._finish()

    def _finish(self):
        self._running = False
        self.root.after(0, lambda: self._widgets["start_btn"].config(state=tk.NORMAL))

    def run(self):
        self.root.mainloop()


def main():
    app = T2mdGui()
    app.run()


if __name__ == "__main__":
    main()
