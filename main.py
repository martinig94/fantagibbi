from gs_utils import *
from data_utils import *

df = get_data()
df = rename_columns(df)
df = compute_right_selected_players(df=df)
df = assign_points(df=df)
