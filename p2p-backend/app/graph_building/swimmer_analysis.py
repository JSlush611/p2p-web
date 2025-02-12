# Swimmer Analysis Functions (Non-Plot)
def find_user_position_in_year(df, name, year):
    swimmer_data = df[(df["Name"] == name) & (df["Year"] == year)]
    if swimmer_data.empty:
        return {"error": f"No data found for {name} in {year}"}, 404

    best_time = swimmer_data["Time (min)"].min()
    overall_rank = int((df[df["Year"] == year]["Time (min)"] < best_time).sum() + 1)

    age_group = str(swimmer_data["AgeGroup"].iloc[0])
    gender = swimmer_data["Gender"].iloc[0]
    total_participants_in_age_group_and_gender = int(
        len(
            df[
                (df["Year"] == year)
                & (df["AgeGroup"] == age_group)
                & (df["Gender"] == gender)
            ]
        )
    )

    return {
        "name": name,
        "year": int(year),
        "position": overall_rank,
        "total_participants": int(len(df[df["Year"] == year])),
        "age_group": age_group,
        "total_participants_in_age_group": total_participants_in_age_group_and_gender,
    }

