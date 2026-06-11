from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "pulse_enterprise_pilot_one_pager.pdf"


CONTENT = [
    ("title", "Pulse AI Enterprise Training & Pilot Success One-Pager"),
    ("heading", "What Pulse AI Does"),
    ("body", "Pulse AI is a decisioning layer for lifecycle, CRM, growth, and retention teams using tools such as Braze, MoEngage, WebEngage, push, email, WhatsApp, SMS, or in-app messaging."),
    ("body", "It answers: What is the best action to take for this customer right now, considering revenue, fatigue, trust, intent, and business rules?"),
    ("body", "Pulse does not replace the campaign platform. It decides whether to send, suppress, recover trust, choose a channel, pick a send window, and explain the recommendation."),
    ("heading", "What Users See In The Action Centre"),
    ("body", "Each recommendation includes action, channel, send window, confidence, auto-approval status, expected value per communication, explanation, top signals, and alternatives ruled out."),
    ("body", "Confidence workflow: >80% auto-approval eligible; 60-80% observe or manually approve; <60% reject or keep out of execution."),
    ("body", "Example: Riya Sharma has high intent and low fatigue. Pulse recommends a wishlist nudge by push at 7:40 PM with 92% confidence, Rs 312 expected value, and an explanation based on product interest, low fatigue, and push responsiveness."),
    ("heading", "What To Expect In The First Two Weeks"),
    ("body", "The first two weeks should prove decision quality, not full autonomous optimization."),
    ("body", "Expected outputs: connected sample event, CRM, and communication data; mapped event taxonomy; behavioral states for a pilot cohort; Action Centre recommendations; suppression, service recovery, channel, timing, and content decisions; first readout against a control group or historical baseline."),
    ("body", "Recommended pilot scope: 1 lifecycle journey or product area; 5,000 to 50,000 users if available; 2 to 4 channels; 3 to 5 intervention types; 1 primary goal such as conversion, revenue, retention, or fatigue reduction."),
    ("heading", "North Star Business Metrics"),
    ("body", "These business outcomes should be measured after the pilot is cleared and a one-month measurement window is available."),
    ("bullet", "Incremental conversion or revenue lift: measure lift versus holdout or historical baseline. Expected direction: positive lift."),
    ("bullet", "Reduced marketing spend: measure lower sends, fewer low-value touches, and better channel mix. Expected direction: lower spend per conversion."),
    ("heading", "MVP Quality Metrics"),
    ("bullet", "Recommendation action alignment on golden suite: target >85%."),
    ("bullet", "Hard rule violation rate: target 0%."),
    ("bullet", "Suppression/service-recovery recall: target >75%."),
    ("bullet", "Auto-approve precision: target >85% once outcome labels exist."),
    ("bullet", "Notification reduction in eligible journeys: target 10-20%."),
    ("heading", "Pilot Readout Questions"),
    ("bullet", "Which users did Pulse suppress that static journeys would have messaged?"),
    ("bullet", "Which high-intent users received a better channel or time recommendation?"),
    ("bullet", "Which users needed service recovery before marketing?"),
    ("bullet", "Which recommendations had high expected value but low confidence?"),
    ("bullet", "Which custom rules were triggered most often?"),
    ("body", "Do not overclaim long-term LTV, unsubscribe reduction, or revenue lift in two weeks unless the pilot has a clean holdout group and enough post-send outcome data."),
]


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def render_lines():
    rendered = []
    for kind, text in CONTENT:
        width = 72 if kind == "title" else 102
        prefix = "- " if kind == "bullet" else ""
        wrapped = textwrap.wrap(prefix + text, width=width)
        for idx, line in enumerate(wrapped or [""]):
            rendered.append((kind if idx == 0 else "body", line))
        rendered.append(("space", ""))
    return rendered


def build_pdf() -> bytes:
    lines = render_lines()
    y = 760
    commands = []
    for kind, line in lines:
        if kind == "space":
            y -= 3
            continue
        if y < 42:
            break
        if kind == "title":
            size = 14
            y -= 18
        elif kind == "heading":
            size = 9.5
            y -= 12
        else:
            size = 7.3
            y -= 9
        commands.append(f"BT /F1 {size} Tf 42 {y} Td ({pdf_escape(line)}) Tj ET")

    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(pdf)


def main() -> None:
    OUTPUT.write_bytes(build_pdf())
    print(OUTPUT)


if __name__ == "__main__":
    main()
