import os
import re
import numpy as np
import matplotlib.pyplot as plt
def clean_and_convert_equation(
    eq_str
):
    if not eq_str:
        return None
    eq_str = eq_str.replace(
        "^",
        "**"
    )
    eq_str = re.sub(
        r'\bX\b',
        'x',
        eq_str
    )
    eq_str = re.sub(
        r'(\d+(?:\.\d+)?)\s*([xX])',
        r'\1*\2',
        eq_str
    )
    eq_str = re.sub(
        r'(\d+(?:\.\d+)?)\s*\(',
        r'\1*(',
        eq_str
    )
    eq_str = re.sub(
        r'([xX])\s*\(',
        r'\1*(',
        eq_str
    )
    eq_str = re.sub(
        r'\)\s*([xX\d\(])',
        r')*\1',
        eq_str
    )
    eq_str = eq_str.replace(
        " ",
        ""
    )
    words = re.findall(
        r'[a-zA-Z]+',
        eq_str
    )
    for word in words:
        if word.lower() not in (
            'x',
            'np'
        ):
            return None
    return eq_str
def extract_equation(
    question
):
    patterns = [
        r"y\s*=\s*((?:[^\n,\.]|\.\d)+)",
        r"f\(x\)\s*=\s*((?:[^\n,\.]|\.\d)+)"
    ]
    for pattern in patterns:
        match = re.search(
            pattern,
            question
        )
        if match:
            raw_equation = (
                match.group(1)
            )
            converted_equation = (
                clean_and_convert_equation(
                    raw_equation
                )
            )
            if converted_equation:
                return converted_equation
    return None
def detect_polynomial_type(
    equation
):
    if "x**3" in equation:
        return "cubic"
    elif "x**2" in equation:
        return "quadratic"
    elif "x" in equation:
        return "linear"
    return "unknown"
def generate_graph(
    question,
    graph_id
):
    equation = extract_equation(
        question
    )
    if equation is None:
        return None
    polynomial_type = (
        detect_polynomial_type(
            equation
        )
    )
    if polynomial_type == "linear":
        x = np.linspace(
            -10,
            10,
            500
        )
    elif polynomial_type == "quadratic":
        x = np.linspace(
            -10,
            10,
            1000
        )
    elif polynomial_type == "cubic":
        x = np.linspace(
            -6,
            6,
            1500
        )
    else:
        x = np.linspace(
            -10,
            10,
            1000
        )
    safe_dict = {
        "x": x,
        "np": np
    }
    try:
        y = eval(
            equation,
            {"__builtins__": {}},
            safe_dict
        )
    except Exception as e:
        print(
            "Graph Generation Error:",
            e
        )
        return None
    os.makedirs(
        "outputs/graphs",
        exist_ok=True
    )
    graph_path = (
        f"outputs/graphs/graph_{graph_id}.png"
    )
    plt.figure(
        figsize=(6, 4)
    )
    plt.plot(
        x,
        y,
        linewidth=2
    )
    plt.axhline(
        0,
        linewidth=1
    )
    plt.axvline(
        0,
        linewidth=1
    )
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(
        f"Graph of y = {equation.replace('**', '^')}"
    )
    plt.tight_layout()
    plt.savefig(
        graph_path,
        bbox_inches="tight"
    )
    plt.close()
    return graph_path