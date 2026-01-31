---
name: proton-bridge
description: >
  Use Proton Bridge's local IMAP/SMTP interface to read, organize, and send
  Proton Mail from scripts or email clients. Trigger terms: proton bridge,
  proton mail bridge, IMAP, SMTP, local email management, archive, spam, reply,
  inbox, mailbox details.
---

## When to Use
- Read, search, archive, spam, delete, or reply to Proton Mail locally
- Automate mail handling on the same machine where Proton Bridge runs
- Answer questions like "How many unread emails today?" or "List today's unread subjects"

## When NOT to Use
- Proton Bridge is not installed, not running, or not signed in
- Remote access from another device (Bridge is local only)

## Credentials (Local Only)

```json
{
  "imap": { "host": "127.0.0.1", "port": 1143, "security": "STARTTLS" },
  "smtp": { "host": "127.0.0.1", "port": 1025, "security": "SSL" },
  "password": "${PROTON_BRIDGE_PASSWORD}",
  "accounts": [
    { "username": "ben@lfglabs.dev", "from": "ben@lfglabs.dev" },
    { "username": "ben@starknet.id", "from": "ben@starknet.id" }
  ],
  "note": "Check both accounts when listing or searching for recent mail."
}
```

## Python: Fetch Emails

```python
import imaplib
import email
from email.header import decode_header

CREDS = {
    "host": "127.0.0.1",
    "port": 1143,
    "security": "STARTTLS",
    "password": "${PROTON_BRIDGE_PASSWORD}",
    "accounts": [
        {"username": "ben@lfglabs.dev"},
        {"username": "ben@starknet.id"},
    ],
}

def connect():
    if CREDS["security"] == "SSL":
        imap = imaplib.IMAP4_SSL(CREDS["host"], CREDS["port"])
    else:
        imap = imaplib.IMAP4(CREDS["host"], CREDS["port"])
        imap.starttls()
    return imap

def decode_header_value(val):
    if not val:
        return ""
    parts = decode_header(val)
    return "".join(p.decode(e or "utf-8", errors="replace") if isinstance(p, bytes) else p for p, e in parts)

for account in CREDS["accounts"]:
    imap = connect()
    imap.login(account["username"], CREDS["password"])
    imap.select("INBOX")

    # Get last N emails
    _, data = imap.search(None, "ALL")
    uids = data[0].split()[-5:][::-1]  # Last 5, newest first

    print(f"== {account['username']} ==")
    for uid in uids:
        _, msg_data = imap.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        msg = email.message_from_bytes(msg_data[0][1])
        print(f"From: {decode_header_value(msg['From'])}")
        print(f"Subject: {decode_header_value(msg['Subject'])}")
        print(f"Date: {msg['Date']}\n")

    imap.logout()
```

## Python: Send Email

```python
import smtplib
import ssl
from email.message import EmailMessage

SMTP = {
    "host": "127.0.0.1",
    "port": 1025,
    "password": "${PROTON_BRIDGE_PASSWORD}",
    "accounts": [
        {"username": "ben@lfglabs.dev", "from": "ben@lfglabs.dev"},
        {"username": "ben@starknet.id", "from": "ben@starknet.id"},
    ],
}

account = SMTP["accounts"][0]  # pick the account you want to send from

msg = EmailMessage()
msg["From"] = account["from"]
msg["To"] = "recipient@example.com"
msg["Subject"] = "Test"
msg.set_content("Hello from Proton Bridge.")

smtp = smtplib.SMTP_SSL(SMTP["host"], SMTP["port"], context=ssl.create_default_context())
smtp.login(account["username"], SMTP["password"])
smtp.send_message(msg)
smtp.quit()
```

## Common Operations

- **Archive**: `imap.uid("MOVE", uid, "Archive")`
- **Spam**: `imap.uid("MOVE", uid, "Spam")`
- **Delete**: `imap.uid("STORE", uid, "+FLAGS", "\\Deleted")` then `imap.expunge()`
- **Mark read**: `imap.uid("STORE", uid, "+FLAGS", "\\Seen")`
- **Search unread**: `imap.search(None, "UNSEEN")`
- **Search today**: `imap.search(None, "SINCE", datetime.now().strftime("%d-%b-%Y"))`

## Guardrails
- Confirm folder names with `imap.list()` before moving
- Ask confirmation before bulk deletes/moves
- Use UID-based operations for reliability
