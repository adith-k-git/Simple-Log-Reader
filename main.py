"""A small desktop tool for finding ERROR and WARNING lines in text logs."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class SimpleLogReader:
    LEVELS = ("ALL", "ERROR", "WARNING")

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simple Log Reader")
        self.root.geometry("900x620")
        self.root.minsize(640, 420)
        self.root.configure(bg="#f3f5f9")

        self.entries: list[tuple[int, str, str]] = []
        self.current_file: Path | None = None
        self.filter_level = tk.StringVar(value="ALL")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f5f9")
        style.configure("TLabel", background="#f3f5f9", foreground="#172033", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 23, "bold"))
        style.configure("Hint.TLabel", foreground="#697589")
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Accent.TButton", background="#3457d5", foreground="white")
        style.map("Accent.TButton", background=[("active", "#2846b5")])

        page = ttk.Frame(root, padding=24)
        page.pack(fill="both", expand=True)

        ttk.Label(page, text="Simple Log Reader", style="Title.TLabel").pack(anchor="w")
        ttk.Label(page, text="Open a .txt log and quickly find errors and warnings.", style="Hint.TLabel").pack(anchor="w", pady=(4, 18))

        toolbar = ttk.Frame(page)
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Button(toolbar, text="Open log file", style="Accent.TButton", command=self.open_file).pack(side="left")
        ttk.Label(toolbar, text="Show:").pack(side="left", padx=(20, 8))
        self.filter_buttons: dict[str, ttk.Button] = {}
        for level in self.LEVELS:
            button = ttk.Button(toolbar, text=level.title(), command=lambda value=level: self.set_filter(value))
            button.pack(side="left", padx=(0, 6))
            self.filter_buttons[level] = button

        self.file_label = ttk.Label(page, text="No file selected", style="Hint.TLabel")
        self.file_label.pack(anchor="w", pady=(0, 8))

        counts = ttk.Frame(page)
        counts.pack(fill="x", pady=(0, 10))
        self.error_count = ttk.Label(counts, text="Errors: 0", foreground="#b42318")
        self.error_count.pack(side="left", padx=(0, 18))
        self.warning_count = ttk.Label(counts, text="Warnings: 0", foreground="#a15c00")
        self.warning_count.pack(side="left")

        results_frame = ttk.Frame(page)
        results_frame.pack(fill="both", expand=True)
        self.results = tk.Text(
            results_frame, wrap="none", state="disabled", font=("Consolas", 10),
            bg="#ffffff", fg="#253047", relief="solid", borderwidth=1,
            padx=12, pady=10,
        )
        y_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        x_scroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results.xview)
        self.results.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.results.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        self.results.tag_configure("ERROR", foreground="#b42318")
        self.results.tag_configure("WARNING", foreground="#a15c00")
        self.results.tag_configure("line_number", foreground="#8993a4")

        self.status = ttk.Label(page, text="Choose a text log file to get started.", style="Hint.TLabel")
        self.status.pack(anchor="w", pady=(10, 0))
        self.root.bind("<Control-o>", lambda _event: self.open_file())

    def open_file(self) -> None:
        filename = filedialog.askopenfilename(
            title="Open a text log", filetypes=[("Text log files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return
        path = Path(filename)
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError as exc:
            messagebox.showerror("Could not open file", str(exc))
            return

        self.current_file = path
        self.entries = []
        for line_number, line in enumerate(lines, start=1):
            upper_line = line.upper()
            if "ERROR" in upper_line:
                self.entries.append((line_number, "ERROR", line))
            elif "WARNING" in upper_line:
                self.entries.append((line_number, "WARNING", line))

        errors = sum(1 for _, level, _ in self.entries if level == "ERROR")
        warnings = sum(1 for _, level, _ in self.entries if level == "WARNING")
        self.file_label.configure(text=str(path))
        self.error_count.configure(text=f"Errors: {errors}")
        self.warning_count.configure(text=f"Warnings: {warnings}")
        self.render_results()

    def set_filter(self, level: str) -> None:
        self.filter_level.set(level)
        self.render_results()

    def render_results(self) -> None:
        level = self.filter_level.get()
        visible = [entry for entry in self.entries if level == "ALL" or entry[1] == level]
        self.results.configure(state="normal")
        self.results.delete("1.0", "end")
        for line_number, entry_level, text in visible:
            self.results.insert("end", f"{line_number:>6}  ", "line_number")
            self.results.insert("end", f"[{entry_level}] ", entry_level)
            self.results.insert("end", text + "\n", entry_level)
        if not visible:
            message = "Open a .txt log file to see matching lines." if self.current_file is None else f"No {level.lower()} messages found."
            self.results.insert("end", message)
        self.results.configure(state="disabled")
        if self.current_file is None:
            self.status.configure(text="Choose a text log file to get started.")
        else:
            self.status.configure(text=f"Showing {len(visible)} of {len(self.entries)} matching lines · Ctrl+O to open another file")


def main() -> None:
    root = tk.Tk()
    SimpleLogReader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
