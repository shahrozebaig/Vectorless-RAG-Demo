import re
import os
import json


def detect_heading_level(line):

    line = line.strip()

    match = re.match(
        r"^(\d+(?:\.\d+)*)\s+(.+)",
        line
    )

    if match:

        numbering = (
            match.group(1)
            .strip()
        )

        title = (
            match.group(2)
            .strip()
        )

        level = (
            numbering.count(".") + 1
        )

        return {
            "number": numbering,
            "title": title,
            "level": level
        }

    return None


def split_into_topics(text):

    lines = text.split("\n")

    tree = {}

    current_node_key = None

    current_content = []

    for line in lines:

        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        heading = detect_heading_level(
            cleaned_line
        )

        if heading:

            if (
                current_node_key
                and current_node_key in tree
            ):

                tree[current_node_key][
                    "content"
                ] = "\n".join(
                    current_content
                )

            node_key = (
                heading["number"]
            )

            tree[node_key] = {

                "title": heading["title"],

                "level": heading["level"],

                "content": "",

                "children": []
            }


            parent_key = ".".join(
                node_key.split(".")[:-1]
            )

            if (
                parent_key
                and parent_key in tree
            ):

                tree[parent_key][
                    "children"
                ].append(node_key)

            current_node_key = (
                node_key
            )

            current_content = []

        else:

            current_content.append(
                cleaned_line
            )


    if (
        current_node_key
        and current_node_key in tree
    ):

        tree[current_node_key][
            "content"
        ] = "\n".join(
            current_content
        )

    return tree


def save_chunks(
    tree,
    output_dir="data/chunks"
):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    for node_id, node_data in tree.items():

        safe_title = re.sub(
            r'[^a-zA-Z0-9]',
            '_',
            node_data["title"]
        )

        filename = (
            f"{node_id}_{safe_title}.txt"
        )

        path = os.path.join(
            output_dir,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                node_data["content"]
            )


def save_json_tree(
    tree,
    chapter_name,
    output_path="data/tree/structure.json"
):

    os.makedirs(
        "data/tree",
        exist_ok=True
    )

    final_tree = {

        "chapter": chapter_name,

        "nodes": tree
    }

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_tree,
            f,
            indent=4,
            ensure_ascii=False
        )


def save_tree_visualization(
    tree,
    chapter_name,
    output_path="data/tree/tree_output.txt"
):

    os.makedirs(
        "data/tree",
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{chapter_name}\n"
        )

        f.write("│\n")

        for node_id, node_data in tree.items():

            level = (
                node_data["level"]
            )

            indent = (
                "│   " * (level - 1)
            )

            connector = "├── "

            f.write(

                f"{indent}"
                f"{connector}"
                f"{node_id} "
                f"{node_data['title']}\n"
            )