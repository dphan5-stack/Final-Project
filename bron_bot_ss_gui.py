# --- Import necessary libraries ---
import tkinter as tk                      # GUI framework
from tkinter import messagebox, ttk       # Extra GUI widgets
from PIL import Image, ImageTk            # For loading and displaying images
import pandas as pd                       # For reading and handling CSV data
import requests                           # For making HTTP requests
from io import BytesIO                    # For handling image byte streams
from duckduckgo_search import DDGS        # For finding images online
from urllib.parse import quote_plus       # For creating YouTube search URLs
import webbrowser                         # To open URLs in the browser

# --- Load CSV data into DataFrames using pandas ---
player_stats_df = pd.read_csv("all_seasons.csv")         # Contains season stats for all players
mvp_df = pd.read_csv("mvp_1982_to_now.csv")              # Contains MVP award data
dpoy_df = pd.read_csv("dpoy_1982_to_now.csv")            # Contains DPOY award data

# --- Create a list of seasons for the dropdown menu ---
seasons = sorted(player_stats_df['season'].unique(), reverse=True)

# --- Set up the main GUI window ---
root = tk.Tk()
root.title("The Bron Bot GUI")           # Window title
root.geometry("450x700")                 # Window size

# --- Input: Player Name Entry ---
tk.Label(root, text="Enter player name:").pack(pady=5)
entry = tk.Entry(root, width=40)         # Text box for player name
entry.pack()

# --- Dropdown: Select Season ---
tk.Label(root, text="Select season:").pack(pady=5)
season_sel = tk.StringVar()              # Variable that stores selected season
season_dropdown = ttk.Combobox(
    root, textvariable=season_sel, values=seasons, state="readonly", width=37
)
season_dropdown.pack()
season_dropdown.current(0)               # Default to the most recent season

# --- Function: Search for funny image using DuckDuckGo ---
def fetch_funny_image(name):
    with DDGS() as ddgs:
        results = ddgs.images(f"{name} funny nba", max_results=1)  # Search for funny image
        if results:
            return results[0]["image"]    # Return image URL
    return None

# --- Text label to display stats ---
stats_var = tk.StringVar()
tk.Label(root, textvariable=stats_var, justify="center", wraplength=450).pack(pady=10)

# --- Clickable link label for YouTube highlights ---
link_var = tk.StringVar()
link_label = tk.Label(root, textvariable=link_var, fg="blue", cursor="hand2")
link_label.pack()
link_label.bind("<Button-1>", lambda e: webbrowser.open(link_var.get()))

# --- Label to display funny image ---
image_label = tk.Label(root)
image_label.pack(pady=15)

# --- Function: Search player and display results ---
def search_player():
    name = entry.get().strip().lower()     # Get typed name and lowercase it
    selected_season = season_sel.get()     # Get selected season from dropdown
    
    if not name:
        return                             # Do nothing if input is empty

    # Filter DataFrame for matching player and selected season
    name_mask = player_stats_df['player_name'].str.lower().str.contains(name)
    df = player_stats_df[name_mask & (player_stats_df['season'] == selected_season)]

    # Also filter MVP and DPOY DataFrames for the player
    mvp = mvp_df[mvp_df['Player'].str.lower().str.contains(name)]
    dpoy = dpoy_df[dpoy_df['Player'].str.lower().str.contains(name)]

    if df.empty:
        messagebox.showinfo("Not Found", "Player not found for that season.")
        return

    display_name = df.iloc[0]['player_name']        # Properly formatted name from data
    total_games = df['gp'].sum()                    # Sum of games played
    total_pts = (df['pts'] * df['gp']).sum()        # Weighted total points
    total_reb = (df['reb'] * df['gp']).sum()        # Weighted total rebounds
    total_ast = (df['ast'] * df['gp']).sum()        # Weighted total assists

    # Calculate career or season averages
    ppg = total_pts / total_games
    rpg = total_reb / total_games
    apg = total_ast / total_games

    # Display the output in the stats label
    stats_var.set(
        f"📊 {display_name} ({selected_season})\n"
        f"PPG: {ppg:.1f} | RPG: {rpg:.1f} | APG: {apg:.1f}\n"
        f"🏆 MVPs: {len(mvp)}   🛡️ DPOYs: {len(dpoy)}"
    )

    # Generate YouTube search link and make it clickable
    q = quote_plus(f"{display_name} highlights")
    link_var.set(f"https://www.youtube.com/results?search_query={q}")

    # Get funny image
    img_url = fetch_funny_image(display_name)
    if img_url:
        try:
            resp = requests.get(img_url, timeout=5)           # Download image
            img = Image.open(BytesIO(resp.content)).resize((250, 250))  # Resize
            photo = ImageTk.PhotoImage(img)                   # Convert for Tkinter
            image_label.config(image=photo, text="")          # Set image
            image_label.image = photo                         # Save reference
        except Exception:
            image_label.config(text="Could not load image.", image="")  # Error fallback
    else:
        image_label.config(text="No funny image found.", image="")      # No result fallback

# --- Button to trigger search ---
tk.Button(root, text="Search", command=search_player).pack(pady=10)

# --- Allow pressing "Enter" key to search ---
entry.bind("<Return>", lambda e: search_player())

# --- Run the GUI app ---
root.mainloop()