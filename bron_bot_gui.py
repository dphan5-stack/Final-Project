import tkinter as tk                 # built-in library for GUI windows and widgets
from tkinter import messagebox      # pop-up dialogs for messages
from PIL import Image, ImageTk      # for loading and displaying images
import pandas as pd                 # for reading and handling CSV data
import requests                     # to download images from the web
from io import BytesIO              # to turn downloaded bytes into an image
from duckduckgo_search import DDGS  # to search DuckDuckGo for a “funny nba” image
from urllib.parse import quote_plus # to safely build URLs for YouTube searches
import webbrowser                   # to open YouTube links in your default web browser

# 1. Load all of our data files into pandas DataFrames
player_stats_df = pd.read_csv("all_seasons.csv")       # career stats by season
mvp_df          = pd.read_csv("mvp_1982_to_now.csv")   # MVP winners since 1982
dpoy_df         = pd.read_csv("dpoy_1982_to_now.csv")  # DPOY winners since 1982

# 2. Define the core search function BEFORE creating the GUI widgets
def search_player(event=None):
    # get the text the user typed and normalize to lowercase
    name = entry.get().strip().lower()
    if not name:
        return  # if the box is empty, do nothing

    # filter each table for rows that mention the player
    player_data = player_stats_df[player_stats_df['player_name']
        .str.lower().str.contains(name)]
    mvp_data    = mvp_df[mvp_df['Player']
        .str.lower().str.contains(name)]
    dpoy_data   = dpoy_df[dpoy_df['Player']
        .str.lower().str.contains(name)]

    # if we found no stats, show a popup and clear previous outputs
    if player_data.empty:
        messagebox.showinfo("Not Found", "Player not found.")
        stats_var.set("")        # clear stats text
        link_var.set("")         # clear link text
        image_label.config(image="", text="")  # clear image
        return

    # grab the nicely formatted player name
    display_name = player_data.iloc[0]['player_name']

    # count how many times they won MVP or DPOY
    mvp_wins  = len(mvp_data)
    dpoy_wins = len(dpoy_data)

    # calculate career totals weighted by games played (same logic as your original script)
    total_games    = player_data['gp'].sum()
    total_points   = (player_data['pts'] * player_data['gp']).sum()
    total_rebounds = (player_data['reb'] * player_data['gp']).sum()
    total_assists  = (player_data['ast'] * player_data['gp']).sum()

    # turn totals into per-game averages
    career_ppg = total_points   / total_games
    career_rpg = total_rebounds / total_games
    career_apg = total_assists  / total_games

    # update the stats display label
    stats_var.set(
        f"📊 {display_name}'s Career Averages:\n"
        f"PPG: {career_ppg:.1f} | RPG: {career_rpg:.1f} | APG: {career_apg:.1f}\n"
        f"🏆 MVPs: {mvp_wins}   🛡️ DPOYs: {dpoy_wins}"
    )

    # build and display the YouTube highlights search link
    yt_q = quote_plus(f"{display_name} highlights")
    link_var.set(f"https://www.youtube.com/results?search_query={yt_q}")

    # fetch one “funny nba” image via DuckDuckGo
    with DDGS() as ddgs:
        results = ddgs.images(f"{display_name} funny nba", max_results=1)
    if results:
        try:
            img_url = results[0]["image"]
            resp    = requests.get(img_url, timeout=5)
            img     = Image.open(BytesIO(resp.content)).resize((250,250))
            photo   = ImageTk.PhotoImage(img)
            image_label.config(image=photo, text="")  # show the image
            image_label.image = photo                # keep reference so it doesn’t vanish
        except Exception:
            image_label.config(text="Could not load image.", image="")
    else:
        image_label.config(text="No funny image found.", image="")

# 3. Now that our function exists, we build the GUI window and widgets
root = tk.Tk()
root.title("The Bron Bot GUI")  # window title
root.geometry("450x650")        # window size

# 4. Input field for typing the player’s name
tk.Label(root, text="Enter Player Name:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack()
entry.bind("<Return>", search_player)  # pressing Enter runs the search

# 5. Search button (calls the same function)
tk.Button(root, text="Search", command=search_player).pack(pady=10)

# 6. Label to display the stats output
stats_var = tk.StringVar()
tk.Label(root, textvariable=stats_var, justify="center").pack(pady=10)

# 7. Label to display the YouTube highlights link
link_var = tk.StringVar()
link_label = tk.Label(root, textvariable=link_var, fg="blue", cursor="hand2")
link_label.pack()
link_label.bind("<Button-1>", lambda e: webbrowser.open(link_var.get()))

# 8. Label to display the fetched funny image
image_label = tk.Label(root)
image_label.pack(pady=15)

# 9. Start Tkinter’s event loop (opens and keeps the window running)
root.mainloop()
