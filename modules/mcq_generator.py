import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)
model = genai.GenerativeModel(
    "gemini-flash-lite-latest"
)
def generate_mcqs(
    chapter_name,
    context
):
    prompt = f"""
Generate a comprehensive MCQ question bank
    from the NCERT Class 10 Mathematics
    chapter Polynomials.

    Instructions:

    - Generate a COMPLETE balanced MCQ question bank
    - Cover the ENTIRE chapter uniformly
    - Cover ALL concepts
    - Cover ALL exercises
    - Cover ALL examples
    - Cover graphs, tables and figures
    - Generate MCQs unit-wise/topic-wise
    - Cover every major topic separately
    - Maintain balanced distribution across all units
    - Generate enough MCQs for each unit
    - Focus more on conceptual and exercise-based questions
    - Keep graph questions limited

    - Include a balanced mix of:
      - Conceptual questions
      - Formula-based questions
      - Graph-based questions
      - Table-based questions
      - Figure-based questions
      - Exercise-based questions
      - Polynomial zeroes questions
      - Factorization questions
      - HOTS questions
      - Application-based questions

    - Generate proper NCERT-style table-based MCQs

    - Include questions based on:
      - x and p(x) value tables
      - observation tables
      - polynomial value tables
      - zero identification tables
      - pattern-based tables

    - Create proper formatted tables inside questions whenever needed

    - Table questions must be generated dynamically

    - Do NOT focus only on graphs
    - Do NOT focus only on tables
    - Do NOT focus only on formulas

    - Maintain balanced distribution across all topics

    - Generate a massive, comprehensive,
      and high-quality MCQ question bank
      covering the entire chapter thoroughly

    - Generate enough MCQs to achieve
      maximum possible chapter coverage

    - Continue generating questions until
      all major concepts, exercises,
      examples, graphs and tables are covered

    - Do not stop generation early

    - Prioritize complete textbook coverage
      over short output

    - Generate as many unique,
      non-repetitive questions as possible
      so that no topic, exercise, example,
      graph, figure, or formula is left out

    - Ensure a balanced distribution across:
      - Conceptual/theory-based MCQs
      - Calculation/formula/exercise-based MCQs
      - Graph, figure, or table interpretation MCQs

    - Number every question consecutively
      starting from Q1

    - Match NCERT standard and rigour

    IMPORTANT RULES FOR GRAPH QUESTIONS:

    - NEVER reference NCERT figure names like
      Fig 2.9 or Fig 2.10

    - NEVER write:
      "Assume a graph"

    - NEVER depend on textbook images

    - Every graph-based question MUST be
      completely self-contained

    - Every graph question must include the
      complete polynomial equation explicitly
      inside the question

    - Generate equations dynamically based on
      chapter concepts

    Example style only:

    "Observe the graph of
    y = x^2 - 5x + 6
    and identify the zeroes."

    Formatting Rules:

    - Do NOT use markdown
    - Do NOT use symbols like ### or **
    - Do NOT use headings
    - Do NOT provide explanations
    - Do NOT provide answers
    - Keep clean professional formatting

    Format:

    Q1. Question

    A. Option
    B. Option
    C. Option
    D. Option

    Q2. Question

    A. Option
    B. Option
    C. Option
    D. Option


Content:
{context}

"""
    

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1024
        }
    )
    return response.text
def generate_explanations(
    mcqs
):
    prompt = f"""

Generate correct answers and brief,
    step-by-step explanations for the
    following MCQs.

    Instructions:

    - Mention the correct option clearly
      Example:
      Correct Answer: B

    - The explanation MUST focus only on
      the solving process

    - Provide explanations in short bullet points
      using only simple dashes '-'

    - Keep explanations short and clean

    - Use simple NCERT-level explanations

    - Maintain proper numbering

    - Do NOT use markdown

    - Do NOT use symbols like ** or ###

    - Do NOT use characters like < or >

    - Keep professional answer-sheet format

    Format:

    Q1. Correct Answer: B

    Explanation:

    - Step 1: State the formula or concept.
    - Step 2: Apply the calculation or logic.
    - Step 3: Final answer.

    Q2. Correct Answer: A

    Explanation:

    - Step 1: State the formula or concept.
    - Step 2: Apply the calculation or logic.
    - Step 3: Final answer.

MCQs:
{mcqs}
"""
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.5,
            "max_output_tokens": 2048
        }
    )
    return response.text