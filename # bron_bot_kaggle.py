import pandas as pd

# Load the MVP and DPOY datasets
mvp_df = pd.read_csv("mvp_1982_to_now.csv")
dpoy_df = pd.read_csv("dpoy_1982_to_now.csv")

# Load the player career stats dataset
player_stats_df = pd.read_csv("all_seasons.csv")  # or .csv if you used CSV

def bron_bot():
    print("🏀 Welcome to The Bron Bot!")
    player_name = input("Enter a player's full name (e.g., LeBron James): ").strip().lower()

    # Find player in all datasets
    player_data = player_stats_df[player_stats_df['player_name'].str.lower().str.contains(player_name)]
    mvp_data = mvp_df[mvp_df['Player'].str.lower().str.contains(player_name)]
    dpoy_data = dpoy_df[dpoy_df['Player'].str.lower().str.contains(player_name)]

    print(f"\n🔍 Searching for: {player_name}")
    print(f"🧾 Found {len(player_data)} matching rows in the player database.")

    if not player_data.empty:
        player_display_name = player_data.iloc[0]['player_name']

        # MVP Status and Count
        if not mvp_data.empty:
            num_mvp_wins = len(mvp_data)
            print(f"\n🏆 MVP Winner: YES - {player_display_name} has won MVP {num_mvp_wins} time(s)!")
        else:
            print(f"\n🏆 MVP Winner: NO - {player_display_name} has never won MVP (since 1982).")

        # DPOY Status and Count
        if not dpoy_data.empty:
            num_dpoy_wins = len(dpoy_data)
            print(f"🛡️ DPOY Winner: YES - {player_display_name} has won DPOY {num_dpoy_wins} time(s)!")
        else:
            print(f"🛡️ DPOY Winner: NO - {player_display_name} has never won DPOY (since 1982).")

        # Career stats weighted by games played
        total_games = player_data['gp'].sum()
        total_points = (player_data['pts'] * player_data['gp']).sum()
        total_rebounds = (player_data['reb'] * player_data['gp']).sum()
        total_assists = (player_data['ast'] * player_data['gp']).sum()

        career_ppg = total_points / total_games
        career_rpg = total_rebounds / total_games
        career_apg = total_assists / total_games

        print(f"\n📊 Career Averages for {player_display_name}:")
        print(f"  - Points Per Game (PPG): {career_ppg:.1f}")
        print(f"  - Rebounds Per Game (RPG): {career_rpg:.1f}")
        print(f"  - Assists Per Game (APG): {career_apg:.1f}")

        # YouTube highlights
        print("\n🎥 Suggested Highlights:")
        print(f"  - https://www.youtube.com/results?search_query=" + '+'.join(player_display_name.split()) + "+highlights")

    else:
        print("\n❌ Player not found in the main player database.")

# Run the bot
if __name__ == "__main__":
    bron_bot()
