from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


@dataclass
class MCQQuestion:
    qno: int
    prompt: str
    options: list[str]


@dataclass
class OutputQuestion:
    qno: int
    code: str


@dataclass
class RefactorQuestion:
    qno: int
    prompt: str
    bad_code: str
    tasks: list[str]


class LinedAnswerArea(Flowable):
    def __init__(self, line_count: int, line_gap: float = 8.0) -> None:
        super().__init__()
        self.line_count = max(1, line_count)
        self.line_gap = line_gap
        self.width = 0
        self.height = self.line_count * self.line_gap + 5

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = avail_width
        self.height = self.line_count * self.line_gap + 5
        return self.width, self.height

    def draw(self) -> None:
        self.canv.setStrokeColor(colors.HexColor("#909090"))
        self.canv.setLineWidth(0.45)
        y = self.height - self.line_gap
        for _ in range(self.line_count):
            self.canv.line(0, y, self.width, y)
            y -= self.line_gap


class CodeWriteArea(Flowable):
    def __init__(self, height: float = 120, line_gap: float = 10.0) -> None:
        super().__init__()
        self.fixed_height = height
        self.line_gap = line_gap
        self.width = 0
        self.height = height

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = avail_width
        self.height = self.fixed_height
        return self.width, self.height

    def draw(self) -> None:
        self.canv.setStrokeColor(colors.HexColor("#808080"))
        self.canv.setLineWidth(0.7)
        self.canv.rect(0, 0, self.width, self.height)
        self.canv.setStrokeColor(colors.HexColor("#C0C0C0"))
        self.canv.setLineWidth(0.35)
        y = self.height - self.line_gap
        while y > 6:
            self.canv.line(6, y, self.width - 6, y)
            y -= self.line_gap


def parse_questions(markdown_text: str) -> tuple[list[MCQQuestion], list[OutputQuestion], list[RefactorQuestion]]:
    parts = re.split(r"(?m)^### Q(\d+)\s*$", markdown_text)
    mcqs: list[MCQQuestion] = []
    outputs: list[OutputQuestion] = []
    refactors: list[RefactorQuestion] = []

    for i in range(1, len(parts), 2):
        qno = int(parts[i])
        block = parts[i + 1].strip()

        if 1 <= qno <= 40:
            lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
            prompt = ""
            options: list[str] = []
            for line in lines:
                mcq_match = re.match(r"^- \*\*([A-D])\.\*\* (.+)$", line)
                if mcq_match:
                    letter, text = mcq_match.groups()
                    options.append(f"{letter}. {text}")
                elif not prompt and not line.startswith("```"):
                    prompt = line
            mcqs.append(MCQQuestion(qno=qno, prompt=prompt, options=options))
            continue

        if 41 <= qno <= 95:
            code_match = re.search(r"```python\s*(.*?)```", block, flags=re.S)
            code = code_match.group(1).strip() if code_match else ""
            outputs.append(OutputQuestion(qno=qno, code=code))
            continue

        if 96 <= qno <= 100:
            prompt = ""
            lines = [ln.rstrip() for ln in block.splitlines()]
            for ln in lines:
                if ln.strip():
                    prompt = ln.strip()
                    break

            code_matches = re.findall(
                r'<code class="language-python">(.*?)</code>',
                block,
                flags=re.S,
            )
            bad_code = code_matches[0].strip() if code_matches else ""
            tasks = re.findall(r"(?m)^- (.+)$", block)
            refactors.append(RefactorQuestion(qno=qno, prompt=prompt, bad_code=bad_code, tasks=tasks))

    mcqs.sort(key=lambda q: q.qno)
    outputs.sort(key=lambda q: q.qno)
    refactors.sort(key=lambda q: q.qno)
    return mcqs, outputs, refactors


def build_pdf(input_md: Path, output_pdf: Path) -> None:
    text = input_md.read_text(encoding="utf-8")
    mcqs, outputs, refactors = parse_questions(text)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=17,
        alignment=1,
        spaceAfter=4,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=11.2,
        leading=13,
        spaceBefore=4,
        spaceAfter=2,
    )
    q_style = ParagraphStyle(
        "Q",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=11.8,
        spaceAfter=1.5,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=10.8,
        spaceAfter=1.2,
    )
    opt_style = ParagraphStyle(
        "Option",
        parent=body_style,
        fontName="Helvetica",
        fontSize=9.1,
        leading=10.4,
        leftIndent=8,
        spaceAfter=0.6,
    )
    code_style = ParagraphStyle(
        "Code",
        fontName="Courier-Bold",
        fontSize=9.6,
        leading=11.2,
        textColor=colors.black,
    )
    small_style = ParagraphStyle(
        "Small",
        parent=body_style,
        fontName="Helvetica",
        fontSize=8.6,
        leading=10.0,
    )

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        leftMargin=6 * mm,
        rightMargin=6 * mm,
        topMargin=6 * mm,
        bottomMargin=6 * mm,
        title="Python Week 4 Test",
    )

    def add_footer(canvas_obj, doc_obj) -> None:
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.HexColor("#666666"))
        canvas_obj.drawRightString(A4[0] - 10 * mm, 6 * mm, f"Page {doc_obj.page}")

    story = []
    story.append(Paragraph("PYTHON WEEK 4 TEST: OOP", title_style))
    story.append(
        Paragraph(
            "Sections: MCQ (40), Predict Output (55), Quick Refactor (5).",
            body_style,
        )
    )
    story.append(Spacer(1, 1))

    story.append(Paragraph("Section A: MCQ (1-40)", h1_style))
    for q in mcqs:
        block = [Paragraph(f"Q{q.qno}. {q.prompt}", q_style)]
        for opt in q.options:
            block.append(Paragraph(opt, opt_style))
        block.append(Spacer(1, 0.4))
        story.extend(block)

    story.append(Paragraph("Section B: Predict the Output (41-95)", h1_style))
    for q in outputs:
        block = [Paragraph(f"Q{q.qno}. Predict the output:", q_style)]
        code_table = Table([[Preformatted(q.code, code_style)]], colWidths=["100%"])
        code_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#7a7a7a")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        block.append(code_table)
        block.append(Spacer(1, 0.6))
        block.append(Paragraph("Answer:", small_style))
        block.append(LinedAnswerArea(line_count=1))
        block.append(Spacer(1, 0.4))
        story.extend(block)

    story.append(Paragraph("Section C: Quick Refactor (96-100)", h1_style))
    for q in refactors:
        story.append(Paragraph(f"Q{q.qno}. {q.prompt}", q_style))
        story.append(Paragraph("Refactor in the right-half area.", small_style))
        story.append(Spacer(1, 1))

        left_col = [
            Paragraph("<b>BAD Code</b>", small_style),
            Spacer(1, 1),
            Table(
                [[Preformatted(q.bad_code, code_style)]],
                colWidths=["100%"],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff3f3")),
                        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cc6d6d")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ]
                ),
            ),
        ]

        right_col = [
            Paragraph("<b>Refactor Here</b>", small_style),
            Spacer(1, 1),
            CodeWriteArea(height=120),
        ]

        two_col = Table(
            [[left_col, right_col]],
            colWidths=["50%", "50%"],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#808080")),
                    ("LINEBEFORE", (1, 0), (1, 0), 0.7, colors.HexColor("#9a9a9a")),
                ]
            ),
        )
        story.append(two_col)
        story.append(Spacer(1, 0.3))
        if q.tasks:
            task_line = " | ".join(q.tasks)
            story.append(Paragraph(f"<b>Task:</b> {task_line}", small_style))
        story.append(Spacer(1, 0.5))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)


def main() -> None:
    input_md = Path("python/assignment/test/python-week-4-oops.md")
    output_pdf = Path("python/assignment/test/python-week-4-oops.pdf")
    build_pdf(input_md=input_md, output_pdf=output_pdf)
    print(f"Generated: {output_pdf}")
    try:
        from pypdf import PdfReader

        page_count = len(PdfReader(str(output_pdf)).pages)
        print(f"Pages: {page_count}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
