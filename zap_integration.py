from zapv2 import ZAPv2
import time
import os
import webbrowser

ZAP_API = 'http://localhost:8080'
zap = ZAPv2(proxies={'http': ZAP_API, 'https': ZAP_API})

def send_and_scan(target_url, payloads):
    print(f"[ZAP] 🔗 Target: {target_url}")
    
    # Start fresh session
    zap.core.new_session(name="auto_session", overwrite=True)
    zap.context.include_in_context("Default Context", target_url + ".*")
    time.sleep(2)

    # Access the URL first
    zap.urlopen(target_url)
    time.sleep(2)
    print("[ZAP] 🧹 New session created.")
    print("[ZAP] 🎯 Target URL added to context.")

    # Disable all scanners, then enable selected few
    print("[ZAP] 🚫 Disabling all scanners...")
    zap.ascan.disable_all_scanners()

    selected_scanners = "40012,40018,40019,40020,90020"
    print(f"[ZAP] ✅ Enabling scanners: {selected_scanners}")
    zap.ascan.enable_scanners(selected_scanners)

    print("[ZAP] 🚀 Starting active scan...")
    scan_id = zap.ascan.scan(target_url)
    
    timeout = time.time() + 120  # max wait 2 min
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"[ZAP] 🔍 Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(2)
        if time.time() > timeout:
            print("[ZAP] ⏳ Scan timed out.")
            break

    print("[ZAP] ✅ Scan complete or timed out.")
    export_zap_report()

def export_zap_report():
    report_html = zap.core.htmlreport()
    output_dir = "output"
    output_path = os.path.join(output_dir, "zap_report.html")

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_html)
        print(f"[ZAP] 💾 Report saved to: {output_path}")
    except Exception as e:
        print(f"[ZAP] ❌ Failed to save report: {e}")

def open_zap_report():
    output_path = os.path.abspath("output/zap_report.html")
    if os.path.exists(output_path):
        print(f"[ZAP] 🌐 Opening report: {output_path}")
        webbrowser.open(f"file://{output_path}")
    else:
        print("[ZAP] ⚠️ Report not found.")
