import pandas as pd
import matplotlib.pyplot as plt

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
    df_ranking = df.groupby("Name", as_index=True)["point"].sum()
    return df_ranking

def plot_most_selected(df: pd.DataFrame, save:bool=True):
    df = df.loc[df["Name"] == "Coach", :]
    counts = df["Selected_players"].explode().value_counts()
    fix, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index, counts.values)
    plt.title("Numero di Convocazioni")
    plt.xlabel("Giocatrici")
    plt.ylabel("")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("docs/images/most_selected.png", dpi=300)


