from gs_utils import *
from data_utils import *

df = get_data()
df = rename_columns(df)
df = compute_right_selected_players(df=df)
df = assign_points(df=df)
df_ranking = make_ranking(df=df)
markdown_table = df_ranking.to_markdown(index=False)

# Read existing Markdown page
with open("docs/Classifica.md", "r", encoding="utf-8") as f:
    content = f.read()

# Decide where to insert: for example, after a heading
insert_after = "# Vedi qua la classifica aggiornata"  # heading that already exists

parts = content.split(insert_after)
if len(parts) == 2:
    new_content = parts[0] + insert_after + "\n\n" + markdown_table + "\n" + parts[1]
else:
    # fallback: append at the end
    new_content = content + "\n\n## Player Scores\n\n" + markdown_table

# Save back
with open("docs/Classifica.md", "w", encoding="utf-8") as f:
    f.write(new_content)

df_ranking.to_csv("docs/data/ranking.csv")