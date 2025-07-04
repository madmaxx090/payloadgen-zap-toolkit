import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import json
import subprocess
import webbrowser
import os
import zap_integration

OUTPUT_DIR = "output"

class PayloadGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PayloadGen & ZAP Scanner")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f4f4")

        title = tk.Label(root, text="💥 Payload Generator & Scanner 💥", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#2c3e50")
        title.pack(pady=10)

        step1 = tk.Label(root, text="Step 1: Generated Payloads", font=("Arial", 14, "bold"), bg="#f4f4f4")
        step1.pack(anchor="w", padx=20)

        self.payload_display = scrolledtext.ScrolledText(root, width=85, height=15, font=("Courier", 10))
        self.payload_display.pack(pady=5)
        self.display_payloads()

        step2 = tk.Label(root, text="Step 2: ZAP Scan", font=("Arial", 14, "bold"), bg="#f4f4f4")
        step2.pack(anchor="w", padx=20, pady=(10,0))

        self.url_entry = tk.Entry(root, width=60, font=("Arial", 12))
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "http://testphp.vulnweb.com")

        scan_btn = tk.Button(root, text="🚀 Start ZAP Scan", command=self.start_scan, font=("Arial", 12), bg="#3498db", fg="white")
        scan_btn.pack(pady=5)

        report_btn = tk.Button(root, text="📄 Show Scan Report", command=self.show_report, font=("Arial", 12), bg="#2ecc71", fg="white")
        report_btn.pack(pady=5)

        self.log_output = scrolledtext.ScrolledText(root, width=85, height=10, font=("Courier", 10), state="disabled")
        self.log_output.pack(pady=10)

    def log(self, message):
        self.log_output.configure(state="normal")
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.configure(state="disabled")
        self.log_output.see(tk.END)

    def display_payloads(self):
        self.payload_display.delete("1.0", tk.END)
        for name in ["xss", "sqli", "cmd"]:
            path = os.path.join(OUTPUT_DIR, f"{name}_payloads.json")
            if os.path.exists(path):
                with open(path) as f:
                    payloads = json.load(f)
                    self.payload_display.insert(tk.END, f"--- {name.upper()} PAYLOADS ---\n")
                    for payload in payloads:
                        self.payload_display.insert(tk.END, f"{payload}\n")
                    self.payload_display.insert(tk.END, "\n")

    def start_scan(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Input Error", "Please enter a target URL.")
            return

        self.log(f"[INFO] Starting scan on {url}...")
        payloads = []
        for name in ["xss", "sqli", "cmd"]:
            path = os.path.join(OUTPUT_DIR, f"{name}_payloads.json")
            if os.path.exists(path):
                with open(path) as f:
                    payloads.extend(json.load(f))

        zap_integration.send_and_scan(url, payloads)
        zap_integration.export_zap_report()
        self.log("[DONE] Scan complete. Report saved to output/zap_report.html")

    def show_report(self):
        report_path = os.path.join(OUTPUT_DIR, "zap_report.html")
        if os.path.exists(report_path):
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        else:
            messagebox.showerror("Error", "ZAP report not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PayloadGenGUI(root)
    root.mainloop()
