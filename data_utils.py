import pandas as pd

def rename_columns(df):
    df.rename(columns={'Chi sei': 'Name', "Seleziona le tue 10 convocate": "Selected_players", "Giornata":"Date"}, inplace=True)
    return df


def to_player_list(x):
    if isinstance(x, str):
        return [p.strip() for p in x.split(",")]
    elif isinstance(x, list):
        return x
    else:
        return []

def compute_right_selected_players(df: pd.DataFrame):
    df["Selected_players"] = df["Selected_players"].apply(to_player_list)

    # 1. Build coach_map
    coach_map = (
        df[df["Name"] == "Coach"]
        .set_index("Date")["Selected_players"]
        .apply(set)
        .to_dict()
    )

    # 2. Compute same_as_coach
    df["same_as_coach"] = df.apply(
        lambda row: len(set(row["Selected_players"]) & coach_map.get(row["Date"], set())),
        axis=1
    )

    return df

def assign_points(df: pd.DataFrame):
    df["point"]=df.apply(lambda row: 150 if row["same_as_coach"]==10 else 10*row["same_as_coach"], axis=1)
    return df

def make_ranking(df: pd.DataFrame):
    df = df.loc[df["Name"] != "Coach", :]
    df_ranking = df.groupby("Name")["point"].sum()
    return df_ranking