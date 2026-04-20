#!/usr/bin/env python3
"""t2md GUI — Tkinter interface."""

import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext

from engine.pipeline import convert_file, SUPPORTED_EXTENSIONS
from engine.lang import get_text


class T2mdGui:
    def __init__(self):
        self.lang = "en"

        self.root = tk.Tk()
        self.root.title("t2md — Text to Markdown Converter")
        self.root.geometry("720x520")
        self.root.minsize(600, 400)

        self.src_var = tk.StringVar(value="./input")
        self.dst_var = tk.StringVar(value="./output")
        self.lang_var = tk.StringVar(value="en")
        self.recursive_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value=get_text("ready", self.lang))

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
        ttk.Entry(dst_frame, textvariable=self.dst_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(dst_frame, text="📁", width=3, command=self._browse_dst).pack(
            side=tk.RIGHT
        )

        # Options row
        opt_frame = ttk.Frame(main)
        opt_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(opt_frame, text=get_text("language", self.lang) + ":").pack(
            side=tk.LEFT, padx=(0, 5)
        )
        lang_cb = ttk.Combobox(
            opt_frame,
            textvariable=self.lang_var,
            values=["en", "de"],
            width=5,
            state="readonly",
        )
        lang_cb.pack(side=tk.LEFT, padx=(0, 15))
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        ttk.Checkbutton(
            opt_frame,
            text=get_text("recursive", self.lang),
            variable=self.recursive_var,
        ).pack(side=tk.LEFT)

        # Start button
        ttk.Button(
            main, text=get_text("start", self.lang), command=self._start
        ).pack(fill=tk.X, pady=(0, 5))

        # Log area
        self.log = scrolledtext.ScrolledText(
            main, height=15, state=tk.DISABLED, font=("Courier", 10)
        )
        self.log.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Status bar
        ttk.Label(main, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(
            fill=tk.X
        )

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
        self.status_var.set(get_text("ready", self.lang))

    def _log(self, msg):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def _collect_files(self):
        src = Path(self.src_var.get())
        files = []
        if src.is_file():
            if src.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(src)
        elif src.is_dir():
            pattern = "**/*" if self.recursive_var.get() else "*"
            for ext in SUPPORTED_EXTENSIONS:
                files.extend(src.glob(f"{pattern}{ext}"))
        return sorted(set(files))

    # ── Conversion ──────────────────────────────────────────────
    def _start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        lang = self.lang
        dst = self.dst_var.get()

        self.root.after(0, lambda: self.status_var.set(get_text("converting", lang)))
        self.root.after(0, lambda: self._log(f"--- {get_text('start', lang)} ---"))

        files = self._collect_files()

        if not files:
            self.root.after(0, lambda: self._log(get_text("no_files", lang)))
            self.root.after(0, lambda: self.status_var.set(get_text("ready", lang)))
            return

        success = 0
        for f in files:
            try:
                result = convert_file(str(f), dst, lang)
                if result:
                    msg = f"✅ {f.name} → {result}"
                    success += 1
                else:
                    msg = f"⏭️  {f.name} — {get_text('skipped', lang)}"
            except Exception as e:
                msg = f"❌ {f.name} — {e}"
            self.root.after(0, lambda m=msg: self._log(m))

        done = f"{get_text('complete', lang)}: {success} {get_text('files_processed', lang)}"
        self.root.after(0, lambda: self._log(done))
        self.root.after(0, lambda: self.status_var.set(done))

    # ── Run ─────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()


def main():
    app = T2mdGui()
    app.run()


if __name__ == "__main__":
    main()
