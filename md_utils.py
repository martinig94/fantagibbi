from datetime import datetime
import re

def update_table_in_file(file_path, markdown_table, suffix:str):
    # Read existing Markdown page
    with open(f"{file_path}", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace section between markers
    new_content = re.sub(
        rf"(<!-- START_TABLE {suffix} -->)(.*?)(<!-- END_TABLE {suffix} -->)",
        f"\\1\n{markdown_table}\n\\3",
        content,
        flags=re.DOTALL
    )

    # Optionally update a timestamp too
    new_content = new_content.replace(
        "{{ date }}", datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    # Save back
    with open(f"{file_path}", "w", encoding="utf-8") as f:
        f.write(new_content)