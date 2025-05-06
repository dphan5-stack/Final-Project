import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
from duckduckgo_search import DDGS
from urllib.parse import quote_plus
import webbrowser

# Load data
player_stats_df = pd.read_csv("all_seasons.csv")
mvp_df = pd.read_csv("mvp_1982_to_now.csv")
dpoy_df = pd.read_csv("dpoy_1982_to_now.csv")

# GUI app
root = tk.Tk()
root.title("The Bron Bot GUI")
root.geometry("450x650")

tk.Label(root, text="Enter Player Name:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack()
entry.bind("<Return>", lambda e: search_player())

tk.Button(root, text="Search", command=lambda: search_player()).pack(pady=10)

stats_var = tk.StringVar()
tk.Label(root, textvariable=stats_var, justify="center").pack(pady=10)

link_var = tk.StringVar()
link_label = tk.Label(root, textvariable=link_var, fg="blue", cursor="hand2")
link_label.pack()
link_label.bind("<Button-1>", lambda e: webbrowser.open(link_var.get()))

image_label = tk.Label(root)
image_label.pack(pady=15)

def fetch_funny_image(name):
    with DDGS() as ddgs:
        results = ddgs.images(f"{name} funny nba", max_results=1)
        if results:
            return results[0]["image"]
    return None

def search_player():
    name = entry.get().strip().lower()
    if not name:
        return

    df = player_stats_df[player_stats_df['player_name'].str.lower().str.contains(name)]
    mvp = mvp_df[mvp_df['Player'].str.lower().str.contains(name)]
    dpoy = dpoy_df[dpoy_df['Player'].str.lower().str.contains(name)]

    if df.empty:
        messagebox.showinfo("Not Found", "Player not found.")
        return

    display_name = df.iloc[0]['player_name']
    total_games = df['gp'].sum()
    total_pts = (df['pts'] * df['gp']).sum()
    total_reb = (df['reb'] * df['gp']).sum()
    total_ast = (df['ast'] * df['gp']).sum()

    ppg = total_pts / total_games
    rpg = total_reb / total_games
    apg = total_ast / total_games

    stats_var.set(
        f"📊 {display_name}\n"
        f"PPG: {ppg:.1f} | RPG: {rpg:.1f} | APG: {apg:.1f}\n"
        f"🏆 MVPs: {len(mvp)}   🛡️ DPOYs: {len(dpoy)}"
    )

    # YouTube link
    q = quote_plus(f"{display_name} highlights")
    link_var.set(f"https://www.youtube.com/results?search_query={q}")

    # Funny image
    img_url = fetch_funny_image(display_name)
    if img_url:
        try:
            resp = requests.get(img_url, timeout=5)
            img = Image.open(BytesIO(resp.content)).resize((250, 250))
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo
        except Exception:
            image_label.config(text="Could not load image.")
    else:
        image_label.config(text="No funny image found.")

root.mainloop()
