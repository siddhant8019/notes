#!/usr/bin/env python3
"""
Teamcast Email Sender

Sends HTML emails via Gmail SMTP. Used as fallback/complement to Gmail MCP drafts.

Usage:
    python3 scripts/send_email.py --subject "Subject" --body-file /tmp/report.html
    python3 scripts/send_email.py --subject "Subject" --body "<h1>Test</h1>"
    python3 scripts/send_email.py --subject "Subject" --body-file /tmp/report.html --attach /tmp/report.pdf
"""

import os
import sys
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GMAIL_USER = os.environ.get("LEADGEN_GMAIL_USER", "")
GMAIL_PASS = "".join(os.environ.get("LEADGEN_GMAIL_PASS", "").split())
TO_EMAIL = os.environ.get("LEADGEN_TO_EMAIL", GMAIL_USER)


def send_email(subject: str, html_body: str, to: str = None, attachments: list = None) -> bool:
    """Send an HTML email via Gmail SMTP. Returns True on success."""
    recipient = to or TO_EMAIL

    if not GMAIL_USER or not GMAIL_PASS:
        print("ERROR: LEADGEN_GMAIL_USER and LEADGEN_GMAIL_PASS must be set in .env",
              file=sys.stderr)
        return False

    if attachments:
        # Use "mixed" outer container when there are attachments
        msg = MIMEMultipart("mixed")
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(html_body, "html"))
        msg.attach(alt)
        for filepath in attachments:
            path = Path(filepath)
            if not path.exists():
                print(f"WARNING: Attachment not found, skipping: {filepath}", file=sys.stderr)
                continue
            with open(path, "rb") as f:
                part = MIMEApplication(f.read(), Name=path.name)
            part["Content-Disposition"] = f'attachment; filename="{path.name}"'
            msg.attach(part)
    else:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(html_body, "html"))

    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, recipient, msg.as_string())
        attached_note = f" with {len(attachments)} attachment(s)" if attachments else ""
        print(f"Email sent successfully to {recipient}{attached_note}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed. Check LEADGEN_GMAIL_USER "
              "and LEADGEN_GMAIL_PASS in .env. Use a Gmail App Password, "
              "not your regular password.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Failed to send email: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Send HTML email via Gmail SMTP")
    parser.add_argument("--subject", required=True, help="Email subject line")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="Inline HTML body")
    group.add_argument("--body-file", help="Path to file containing HTML body")
    parser.add_argument("--to", help="Override recipient email")
    parser.add_argument("--attach", action="append", dest="attachments",
                        metavar="FILE", help="File to attach (can be used multiple times)")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file, "r") as f:
            html_body = f.read()
    else:
        html_body = args.body

    success = send_email(args.subject, html_body, args.to, args.attachments)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
