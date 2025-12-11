from gs_utils import *
from data_utils import *
from md_utils import *

df = get_data()
df = rename_columns(df)
df = clean_data(df)
df = compute_right_selected_players(df=df)
df = assign_points(df=df)
df = add_points_first_round(df=df)
df = get_cumulative_points(df=df)

df_ranking = make_ranking(df=df)
markdown_table = df_ranking.to_markdown()
update_table_in_file("docs/Classifica.md", markdown_table=markdown_table, suffix="RANKING")
last_pick = df.groupby("Name", as_index=False)["Timestamp"].max()
markdown_table_selected = df.loc[~(df["Name"]=="Coach")&(df["Timestamp"].isin(last_pick["Timestamp"])), ["Name", "Selezionata e convocata", "Selezionata e non convocata"]]
markdown_table_selected = markdown_table_selected.to_markdown()
update_table_in_file("docs/Classifica.md", markdown_table=markdown_table_selected, suffix="CORRECT")
plot_most_selected_coach(df=df, save=True)
plot_most_selected_players(df=df, save=True)
plot_trend_points(df)
df_ranking.to_csv("docs/data/ranking.csv")