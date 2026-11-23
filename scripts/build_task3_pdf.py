from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "TASK3_REPORT.md"
OUTPUT = ROOT / "reports" / "TASK3_REPORT.pdf"


def main() -> None:
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="TASK 3 - DataOps Pipeline and Multimodal Fusion Study",
    )
    story = []
    sections = SOURCE.read_text(encoding="utf-8").split("\n## ")
    for index, section in enumerate(sections):
        text = section if index == 0 else "## " + section
        for block in text.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("#"):
                level = 1 if block.startswith("# ") and not block.startswith("## ") else 2
                title = block.lstrip("# ").strip()
                style = styles["Title"] if level == 1 else styles["Heading1"]
                story.append(Paragraph(title, style))
            else:
                escaped = (
                    block.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br/>")
                )
                story.append(Paragraph(escaped, styles["BodyText"]))
        if index < len(sections) - 1:
            story.append(PageBreak())
    document.build(story)
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    main()
