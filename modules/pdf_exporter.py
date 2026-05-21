from fpdf import FPDF
import os
import re
class PDF(FPDF):
    def header(self):
        self.set_font(
            "Arial",
            "B",
            14
        )
        self.cell(
            0,
            10,
            self.title,
            ln=True,
            align="C"
        )
        self.ln(5)
def create_pdf(
    content,
    output_path,
    title
):
    pdf = PDF()
    pdf.title = title
    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )
    pdf.add_page()
    pdf.set_font(
        "Arial",
        size=11
    )
    question_blocks = re.split(
        r"(Q\d+\.)",
        content
    )
    merged_questions = []
    i = 1
    while i < len(question_blocks):
        question_number = (
            question_blocks[i]
        )
        question_text = (
            question_blocks[i + 1]
        )
        merged_questions.append(
            question_number + question_text
        )
        i += 2
    for idx, question in enumerate(
        merged_questions
    ):
        cleaned_question = (
            question.encode(
                "latin-1",
                "replace"
            )
            .decode("latin-1")
        )
        pdf.multi_cell(
            0,
            8,
            cleaned_question
        )
        pdf.ln(3)
        graph_path = (
            f"outputs/graphs/graph_{idx}.png"
        )
        if os.path.exists(
            graph_path
        ):
            try:
                pdf.image(
                    graph_path,
                    w=120
                )
                pdf.ln(5)
            except Exception as e:
                print(
                    "Graph Error:",
                    e
                )
        pdf.ln(4)
    os.makedirs(
        os.path.dirname(
            output_path
        ),
        exist_ok=True
    )
    pdf.output(
        output_path
    )