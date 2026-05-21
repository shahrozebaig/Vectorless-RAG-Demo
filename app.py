import streamlit as st
import os
import time
import re
from modules.pdf_extractor import (
    extract_text_from_pdf
)
from modules.tree_chunker import (
    split_into_topics,
    save_chunks,
    save_json_tree,
    save_tree_visualization
)
from modules.mcq_generator import (
    generate_mcqs,
    generate_explanations
)
from modules.graph_generator import (
    generate_graph
)
from modules.pdf_exporter import (
    create_pdf
)
st.set_page_config(
    page_title="Vectorless MCQ Generator"
)
st.title(
    "Vectorless MCQ Generator"
)
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
if uploaded_file:
    os.makedirs(
        "data/uploads",
        exist_ok=True
    )
    pdf_path = os.path.join(
        "data/uploads",
        uploaded_file.name
    )
    with open(
        pdf_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )
    st.success(
        "PDF Uploaded Successfully"
    )
    if st.button(
        "Generate MCQs"
    ):
        with st.spinner(
            "Extracting Text..."
        ):
            text = extract_text_from_pdf(
                pdf_path
            )
        with st.spinner(
            "Creating Tree Structure..."
        ):
            chunks = split_into_topics(
                text
            )
            chapter_name = (
                uploaded_file.name
                .replace(".pdf", "")
            )
            save_chunks(
                chunks
            )
            save_json_tree(
                chunks,
                chapter_name
            )
            save_tree_visualization(
                chunks,
                chapter_name
            )
        with st.spinner(
            "Generating Questions..."
        ):
            all_questions = ""
            global_question_counter = 1
            graph_paths = {}
            for topic_id, node_data in chunks.items():
                content = (
                    node_data["content"]
                )
                if not content.strip():
                    continue
                limited_content = (
                    content[:800]
                )
                topic_questions = (
                    generate_mcqs(
                        node_data["title"],
                        limited_content
                    )
                )
                split_questions = re.split(
                    r"Q\d+\.",
                    topic_questions
                )
                for question in split_questions:
                    cleaned_question = (
                        question.strip()
                    )
                    if not cleaned_question:
                        continue
                    formatted_question = (
                        f"Q{global_question_counter}. "
                        f"{cleaned_question}\n\n"
                    )
                    all_questions += (
                        formatted_question
                    )
                    if (
                        "y =" in cleaned_question
                        or "f(x)" in cleaned_question
                    ):
                        graph_path = (
                            generate_graph(
                                cleaned_question,
                                global_question_counter
                            )
                        )
                        if graph_path:
                            graph_paths[
                                global_question_counter
                            ] = graph_path
                    global_question_counter += 1
                all_questions += (
                    "\n\n"
                )
                time.sleep(5)
        with st.spinner(
            "Generating Answers..."
        ):
            answers = (
                generate_explanations(
                    all_questions
                )
            )
        with st.spinner(
            "Generating PDFs..."
        ):
            os.makedirs(
                "outputs",
                exist_ok=True
            )
            create_pdf(
                all_questions,
                "outputs/question_bank.pdf",
                "Question Bank"
            )
            create_pdf(
                answers,
                "outputs/answers_explanations.pdf",
                "Answers and Explanations"
            )
        st.success(
            "All Files Generated Successfully"
        )
        st.success(
            f"{len(graph_paths)} Graphs Generated"
        )
if os.path.exists(
    "outputs/question_bank.pdf"
):
    with open(
        "outputs/question_bank.pdf",
        "rb"
    ) as f:
        st.download_button(
            "Download Question Bank",
            f,
            file_name="question_bank.pdf"
        )
if os.path.exists(
    "outputs/answers_explanations.pdf"
):
    with open(
        "outputs/answers_explanations.pdf",
        "rb"
    ) as f:
        st.download_button(
            "Download Answers PDF",
            f,
            file_name="answers_explanations.pdf"
        )