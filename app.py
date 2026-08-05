import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials

def get_sheet():
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    return client.open("Music Rankings Data").sheet1

def load_data():
    sheet = get_sheet()
    chunks = sheet.col_values(1)
    if chunks:
        return json.loads("".join(chunks))
    return {}

def save_data(data):
    sheet = get_sheet()
    json_str = json.dumps(data)
    chunks = [[chunk] for chunk in [json_str[i:i+40000] for i in range(0, len(json_str), 40000)]]
    sheet.clear()
    sheet.update(values=chunks, range_name="A1")
    st.session_state.rankings_data = data

if "rankings_data" not in st.session_state:
    st.session_state.rankings_data = load_data()

rankings_data = st.session_state.rankings_data

# --- Page Setup ---
st.set_page_config(page_title="Music Rankings", layout="wide")

# --- Cyberpunk Style ---
def apply_cyberpunk_style():
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Iceland&family=Stalinist+One&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown('<script src="https://unpkg.com/lucide@latest"></script>', unsafe_allow_html=True)
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Iceland&family=Stalinist+One&display=swap');
        .stApp { background-color: #0a0a0f; }
        h1 {
            color: #00fff9;
            text-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9;
            font-family: "Stalinist One", sans-serif;
            text-align: center;
        }
        h2, h3 {
            color: #ff2079;
            text-shadow: 0 0 8px #ff2079;
            font-family: "Iceland", sans-serif;
        }
        p, div, label { color: #c0c0c0; font-family: "Iceland", sans-serif; font-size: 20px !important; text-shadow:0 0 8px #ff0090;}
        div.stButton > button {
            background-color: #0a0a0f;
            color: #00fff9;
            border: 2px solid #ff0080;
            box-shadow: 0 0 12px #ff0090cc !important;
            font-family: "Iceland", sans-serif;
            border-radius: 8px;
            padding: 40px 20px;
            font-size: 24px !important;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: #0a0a0f;
        }
        .category-card {
            background-color: #1e1e2e;
            border: 1px solid #444;
            border-radius: 12px;
            padding: 30px 20px;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }

        /* Neon icons */
        .neon-icon {
            display: inline-block;
            vertical-align: middle;
            filter: drop-shadow(0 0 6px #00fff9) drop-shadow(0 0 12px #00fff9);
            color: #00fff9;
            stroke: #00fff9;
        }
        .neon-icon-pink {
            display: inline-block;
            vertical-align: middle;
            filter: drop-shadow(0 0 6px #ff2079) drop-shadow(0 0 12px #ff2079);
            color: #ff2079;
            stroke: #ff2079;
        }
        </style>
    """, unsafe_allow_html=True)

def cyber_title(text, icon=None):
    icon_html = f'<span style="filter: drop-shadow(0 0 8px #00fff9); vertical-align: middle; margin-right: 10px;">{icon}</span>' if icon else ""
    st.markdown(f'<h1 style="font-family: \'Stalinist One\', sans-serif; text-align: center; color: #00fff9; text-shadow: 0 0 10px #00fff9;">{icon_html}{ text}</h1>', unsafe_allow_html=True)

# --- Icons ---
icon_music = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>'
icon_calendar = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
icon_chart = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 13H7"/><path d="M19 9h-4"/><path d="M3 3v16a2 2 0 0 0 2 2h16"/><rect x="15" y="5" width="4" height="12" rx="1"/><rect x="7" y="8" width="4" height="9" rx="1"/></svg>'
icon_mic = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m11 7.601-5.994 8.19a1 1 0 0 0 .1 1.298l.817.818a1 1 0 0 0 1.314.087L15.09 12"/><path d="M16.5 21.174C15.5 20.5 14.372 20 13 20c-2.058 0-3.928 2.356-6 2-2.072-.356-2.775-3.369-1.5-4.5"/><circle cx="16" cy="7" r="5"/></svg>'
icon_plus = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>'
icon_star = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff2079" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #ff2079); vertical-align: middle;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
icon_clock = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #00fff9); vertical-align: middle;"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg>'
icon_home = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #00fff9); vertical-align: middle;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
icon_back = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #00fff9); vertical-align: middle;"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>'
icon_gold = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFD700" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #FFD700); vertical-align: middle;"><circle cx="12" cy="8" r="6"/><path d="M8 14l-3 7h14l-3-7"/></svg>'
icon_silver = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C0C0C0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #C0C0C0); vertical-align: middle;"><circle cx="12" cy="8" r="6"/><path d="M8 14l-3 7h14l-3-7"/></svg>'
icon_bronze = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #CD7F32); vertical-align: middle;"><circle cx="12" cy="8" r="6"/><path d="M8 14l-3 7h14l-3-7"/></svg>'
icon_metric_clock = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #00fff9); vertical-align: middle;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
icon_metric_mic = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #ff2079); vertical-align: middle;"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>'
icon_metric_music = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff0090" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px #00fff9); vertical-align: middle;"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>'

# --- Session State ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_year" not in st.session_state:
    st.session_state.selected_year = None
if "selected_month" not in st.session_state:
    st.session_state.selected_month = None
if "selected_week" not in st.session_state:
    st.session_state.selected_week = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
# --- Add form state ---
if "form_year" not in st.session_state:
    st.session_state.form_year = "2024"
if "form_month" not in st.session_state:
    st.session_state.form_month = "January"
if "form_week" not in st.session_state:
    st.session_state.form_week = "Week 1"
if "form_total_minutes" not in st.session_state:
    st.session_state.form_total_minutes = 0
if "form_total_artists" not in st.session_state:
    st.session_state.form_total_artists = 0
if "form_total_songs" not in st.session_state:
    st.session_state.form_total_songs = 0
for i in range(5):
    if f"form_artist_name_{i}" not in st.session_state:
        st.session_state[f"form_artist_name_{i}"] = ""
    if f"form_artist_url_{i}" not in st.session_state:
        st.session_state[f"form_artist_url_{i}"] = ""
    if f"form_artist_img_{i}" not in st.session_state:
        st.session_state[f"form_artist_img_{i}"] = ""
    if f"form_song_name_{i}" not in st.session_state:
        st.session_state[f"form_song_name_{i}"] = ""
    if f"form_song_url_{i}" not in st.session_state:
        st.session_state[f"form_song_url_{i}"] = ""
    if f"form_song_plays_{i}" not in st.session_state:
        st.session_state[f"form_song_plays_{i}"] = 0
    if f"form_song_dur_{i}" not in st.session_state:
        st.session_state[f"form_song_dur_{i}"] = 0.0
    if f"form_song_img_{i}" not in st.session_state:
        st.session_state[f"form_song_img_{i}"] = ""

# --- Data ---
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]
weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]

# --- HOME PAGE ---
def show_home():
    cyber_title('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00fff9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px #00fff9); vertical-align: middle;"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg> Music Rankings')
    st.write(" ")

    st.markdown("""
        <style>
        .nav-button-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("◈ Year Summary", use_container_width=True):
        st.session_state.page = "summary"
        st.rerun()

    st.write(" ")

    if st.button("◈ Add Week Data", use_container_width=True):
        st.session_state.page = "add_data"
        st.rerun()

    st.write("---")
    st.write("Select a year:")

    for year in rankings_data.keys():
        if st.button(f"◈ {year}", key=f"year_{year}", use_container_width=True):
            st.session_state.selected_year = year
            st.session_state.page = "year"
            st.rerun()

# --- YEAR PAGE ---
def show_year():
    year = st.session_state.selected_year
    cyber_title(f"{year}", icon=icon_calendar)
    st.write("Select a month:")
    st.write("---")

    cols = st.columns(4)
    year_data = rankings_data.get(year, {})

    for i, month in enumerate(months):
        with cols[i % 4]:
            has_data = month in year_data
            label = month if has_data else f"{month} (no data)"
            if st.button(label, key=f"month_{month}", use_container_width=True):
                if has_data:
                    st.session_state.selected_month = month
                    st.session_state.page = "month"
                    st.rerun()

    st.write("---")
    if st.button("⌂ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- MONTH PAGE ---
def show_month():
    year = st.session_state.selected_year
    month = st.session_state.selected_month
    cyber_title(f"{month} {year}", icon=icon_calendar)
    st.write("---")

    month_data = rankings_data[year][month]

    # --- MONTHLY SUMMARY ---
    st.markdown(f"<h3>{icon_chart} Monthly Totals</h3>", unsafe_allow_html=True)
    total_minutes = sum(w["totals"]["minutes"] for w in month_data.values())
    total_artists = sum(w["totals"]["artists"] for w in month_data.values())
    total_songs = sum(w["totals"]["songs"] for w in month_data.values())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"{icon_metric_clock} **Total Minutes**", unsafe_allow_html=True)
        st.markdown(f"### {total_minutes}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"{icon_metric_mic} **Artists Listened**", unsafe_allow_html=True)
        st.markdown(f"### {total_artists}", unsafe_allow_html=True)
    with col3:
        st.markdown(f"{icon_metric_music} **Songs Listened**", unsafe_allow_html=True)
        st.markdown(f"### {total_songs}", unsafe_allow_html=True)

    st.write("---")
    st.write("Select a week:")

    cols = st.columns(4)
    for i, week in enumerate(weeks):
        with cols[i]:
            if week in month_data:
                if st.button(week, key=f"week_{week}", use_container_width=True):
                    st.session_state.selected_week = week
                    st.session_state.page = "week"
                    st.rerun()

    st.write("---")

    # --- MONTHLY RANKINGS ---
    st.markdown(f"<h3>{icon_mic} Monthly Artist Rankings</h3>", unsafe_allow_html=True)
    artist_points = {}
    for week_data in month_data.values():
        for artist in week_data["artists"]:
            name = artist["name"]
            if name not in artist_points:
                artist_points[name] = {"points": 0, "image": artist["image"]}
            artist_points[name]["points"] += artist["points"]

    sorted_artists = sorted(artist_points.items(), key=lambda x: x[1]["points"], reverse=True)
    medals = [icon_gold, icon_silver, icon_bronze]

    top3_cols = st.columns(3)
    for i in range(min(3, len(sorted_artists))):
        name, data = sorted_artists[i]
        with top3_cols[i]:
            st.image(data["image"], width=200)
            st.markdown(f"### {medals[i]} {name}", unsafe_allow_html=True)
            st.markdown(f"{icon_star} **{data['points']} points**", unsafe_allow_html=True)

    st.write(" ")
    for i in range(3, min(len(sorted_artists), 10)):
        name, data = sorted_artists[i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(data["image"], width=100)
            st.markdown(f"**{name}**")
        with col3:
            st.markdown(f"{icon_star} {data['points']} points", unsafe_allow_html=True)
        st.write("---")

    st.write("---")
    st.markdown(f"<h3>{icon_music} Monthly Song Rankings</h3>", unsafe_allow_html=True)
    song_totals = {}
    for week_data in month_data.values():
        for song in week_data["songs"]:
            name = song["name"]
            if name not in song_totals:
                song_totals[name] = {"minutes": 0, "image": song["image"]}
            song_totals[name]["minutes"] += round(song["times_played"] * song["duration"], 1)

    sorted_songs = sorted(song_totals.items(), key=lambda x: x[1]["minutes"], reverse=True)

    top3_cols = st.columns(3)
    for i in range(min(3, len(sorted_songs))):
        name, data = sorted_songs[i]
        with top3_cols[i]:
            st.image(data["image"], width=200)
            st.markdown(f"### {medals[i]} {name}", unsafe_allow_html=True)
            st.markdown(f"{icon_clock} **{data['minutes']} min**", unsafe_allow_html=True)

    st.write(" ")
    for i in range(3, min(len(sorted_songs), 10)):
        name, data = sorted_songs[i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(data["image"], width=100)
            st.markdown(f"**{name}**")
        with col3:
            st.markdown(f"{icon_clock} {data['minutes']} min", unsafe_allow_html=True)
        st.write("---")

    st.write("---")
    if st.button("← Back to Year"):
        st.session_state.page = "year"
        st.rerun()

# --- WEEK PAGE ---
def show_week():
    year = st.session_state.selected_year
    month = st.session_state.selected_month
    week = st.session_state.selected_week
    cyber_title(f"{week} — {month} {year}", icon=icon_calendar)
    st.write("---")

    week_data = rankings_data[year][month][week]
    medals = [icon_gold, icon_silver, icon_bronze]

    # Totals
    st.markdown(f"<h3>{icon_chart} Week Totals</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"{icon_metric_clock} **Minutes**", unsafe_allow_html=True)
        st.markdown(f"### {week_data['totals']['minutes']}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"{icon_metric_mic} **Artists**", unsafe_allow_html=True)
        st.markdown(f"### {week_data['totals']['artists']}", unsafe_allow_html=True)
    with col3:
        st.markdown(f"{icon_metric_music} **Songs**", unsafe_allow_html=True)
        st.markdown(f"### {week_data['totals']['songs']}", unsafe_allow_html=True)

    st.write("---")

    # Artists
    st.markdown(f"<h3>{icon_mic} Top Artists</h3>", unsafe_allow_html=True)
    top3_cols = st.columns(3)
    for i in range(3):
        artist = week_data["artists"][i]
        with top3_cols[i]:
            st.image(artist["image"], width=200)
            st.markdown(f"### {medals[i]} {artist['name']}", unsafe_allow_html=True)
            st.markdown(f"{icon_star} **{artist['points']} points**", unsafe_allow_html=True )

    st.write(" ")
    for i in range(3, 5):
        artist = week_data["artists"][i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(artist["image"], width=100)
            st.markdown(f"**{artist['name']}**")
        with col3:
            st.markdown(f"{icon_star} {artist['points']} points", unsafe_allow_html=True)
        st.write("---")

    st.write("---")

    # Songs
    st.markdown(f"<h3>{icon_music} Top Songs</h3>", unsafe_allow_html=True)
    top3_cols = st.columns(3)
    for i in range(3):
        song = week_data["songs"][i]
        total_mins = round(song["times_played"] * song["duration"], 1)
        with top3_cols[i]:
            st.image(song["image"], width=200)
            st.markdown(f"### {medals[i]} {song['name']}", unsafe_allow_html=True)
            st.markdown(f"{icon_clock} **{total_mins} min**", unsafe_allow_html=True)
            st.markdown(f"{icon_music} {song['times_played']} plays", unsafe_allow_html=True)

    st.write(" ")
    for i in range(3, 5):
        song = week_data["songs"][i]
        total_mins = round(song["times_played"] * song["duration"], 1)
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(song["image"], width=100)
            st.markdown(f"**{song['name']}**")
        with col3:
            st.markdown(f"{icon_clock} {total_mins} min", unsafe_allow_html=True)
            st.markdown(f"{icon_music} {song['times_played']} plays", unsafe_allow_html=True)
        st.write("---")

    st.write("---")
    if st.button("✎ Edit This Week", use_container_width=True):
        st.session_state.page = "edit_data"
        st.rerun()
    if st.button("← Back to Month"):
        st.session_state.page = "month"
        st.rerun()

# --- SUMMARY PAGE ---
def show_summary():
    cyber_title("Year Summary", icon=icon_chart)
    st.write("Your top music across all months combined.")
    st.write("---")

    all_artist_points = {}
    all_song_totals = {}
    total_minutes = 0
    total_artists = 0
    total_songs = 0

    for year, year_data in rankings_data.items():
        for month, month_data in year_data.items():
            for week, week_data in month_data.items():
                total_minutes += week_data["totals"]["minutes"]
                total_artists += week_data["totals"]["artists"]
                total_songs += week_data["totals"]["songs"]

                for artist in week_data["artists"]:
                    name = artist["name"]
                    if name not in all_artist_points:
                        all_artist_points[name] = {"points": 0, "image": artist["image"]}
                    all_artist_points[name]["points"] += artist["points"]

                for song in week_data["songs"]:
                    name = song["name"]
                    if name not in all_song_totals:
                        all_song_totals[name] = {"minutes": 0, "image": song["image"]}
                    all_song_totals[name]["minutes"] += round(song["times_played"] * song["duration"], 1)

    # Overall totals
    st.markdown(f"<h3>{icon_chart} Overall Totals</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"{icon_metric_clock} **Total Minutes**", unsafe_allow_html=True)
        st.markdown(f"### {total_minutes}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"{icon_metric_mic} **Artists Listened**", unsafe_allow_html=True)
        st.markdown(f"### {total_artists}", unsafe_allow_html=True)
    with col3:
        st.markdown(f"{icon_metric_music} **Songs**", unsafe_allow_html=True)
        st.markdown(f"### {total_songs}", unsafe_allow_html=True)

    st.write("---")
    medals = [icon_gold, icon_silver, icon_bronze]

    # Top Artists
    st.markdown(f"<h3>{icon_mic} Top Artists</h3>", unsafe_allow_html=True)
    sorted_artists = sorted(all_artist_points.items(), key=lambda x: x[1]["points"], reverse=True)[:10]
    top3_cols = st.columns(3)
    for i in range(3):
        name, data = sorted_artists[i]
        with top3_cols[i]:
            st.image(data["image"], width=200)
            st.markdown(f"### {medals[i]} {name}", unsafe_allow_html=True)
            st.markdown(f"{icon_star} **{data['points']} points**", unsafe_allow_html=True)

    st.write(" ")
    for i in range(3, len(sorted_artists)):
        name, data = sorted_artists[i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(data["image"], width=100)
            st.markdown(f"**{name}**")
        with col3:
            st.markdown(f"{icon_star} {data['points']} points", unsafe_allow_html=True)
        st.write("---")

    st.write("---")

    # Top Songs
    st.markdown(f"<h3>{icon_music} Top Songs</h3>", unsafe_allow_html=True)
    sorted_songs = sorted(all_song_totals.items(), key=lambda x: x[1]["minutes"], reverse=True)[:10]
    top3_cols = st.columns(3)
    for i in range(3):
        name, data = sorted_songs[i]
        with top3_cols[i]:
            st.image(data["image"], width=200)
            st.markdown(f"### {medals[i]} {name}", unsafe_allow_html=True)
            st.markdown(f"{icon_clock} **{data['minutes']} min**", unsafe_allow_html=True)

    st.write(" ")
    for i in range(3, len(sorted_songs)):
        name, data = sorted_songs[i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(data["image"], width=100)
            st.markdown(f"**{name}**")
        with col3:
            st.markdown(f"{icon_clock} {data['minutes']} min", unsafe_allow_html=True)
        st.write("---")

    if st.button("⌂ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- ADD DATA PAGE ---
def show_add_data():
    cyber_title("Add Week Data", icon=icon_plus)
    form_v = st.session_state.get("form_version", 0)
    st.write("Fill in your weekly Spotify data.")
    st.write("---")

    year = st.selectbox("Year", ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"], key="form_year")
    month = st.selectbox("Month", months, key="form_month")
    week = st.selectbox("Week", weeks, key="form_week")

    st.write("---")
    st.markdown(f"<h3>{icon_chart} Totals</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        total_minutes = st.number_input("Total Minutes Listened", min_value=0, key="form_total_minutes")
    with col2:
        total_artists = st.number_input("Total Artists Listened", min_value=0, key="form_total_artists")
    with col3:
        total_songs = st.number_input("Total Songs Listened", min_value=0, key="form_total_songs")

    st.write("---")
    st.markdown(f"<h3>{icon_mic} Top 5 Artists</h3>", unsafe_allow_html=True)
    st.write("Points are auto-calculated: 1st=5pts, 2nd=4pts, 3rd=3pts, 4th=2pts, 5th=1pt")
    points_map = [5, 4, 3, 2, 1]
    artists = []
    for i in range(5):
        col1, col2 = st.columns([3, 2])
        with col1:
            name = st.text_input(f"Artist #{i+1}", key=f"form_artist_name_{i}")
        with col2:
            url = st.text_input(f"Artist #{i+1} image URL", key=f"form_artist_url_{i}")
            uploaded = st.file_uploader(f"Or upload image", type=["png", "jpg", "jpeg"], key=f"form_artist_img_{i}")
        image = url if url else f"https://picsum.photos/seed/na{i}/100/100"
        artists.append({"name": name, "points": points_map[i], "image": image, "uploaded": uploaded})

    st.write("---")
    st.markdown(f"<h3>{icon_music} Top 5 Songs</h3>", unsafe_allow_html=True)
    songs = []
    for i in range(5):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            name = st.text_input(f"Song #{i+1}", key=f"form_song_name_{i}")
        with col2:
            times_played = st.number_input(f"Times played", min_value=0, key=f"form_song_plays_{i}")
        with col3:
            duration = st.number_input(f"Duration (min)", min_value=0.0, step=0.1, key=f"form_song_dur_{i}")
        col1, col2 = st.columns([3, 2])
        with col1:
            url = st.text_input(f"Song #{i+1} image URL", key=f"form_song_url_{i}")
        with col2:
            uploaded = st.file_uploader(f"Or upload image", type=["png", "jpg", "jpeg"], key=f"form_song_img_{i}")
        image = url if url else f"https://picsum.photos/seed/ns{i}/100/100"
        songs.append({"name": name, "times_played": times_played, "duration": duration, "image": image, "uploaded": uploaded})

    st.write("---")
    if st.button("◈ Submit", use_container_width=True):
        import base64
        for item in artists:
            if item["uploaded"] is not None:
                img_bytes = item["uploaded"].read()
                item["image"] = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
            del item["uploaded"]

        for item in songs:
            if item["uploaded"] is not None:
                img_bytes = item["uploaded"].read()
                item["image"] = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
            del item["uploaded"]

        # Reload fresh data from the file before saving
        current_data = load_data()
        
        if year not in current_data:
            current_data[year] = {}
        if month not in current_data[year]:
            current_data[year][month] = {}

        current_data[year][month][week] = {
            "totals": {
                "minutes": total_minutes,
                "artists": total_artists,
                "songs": total_songs
            },
            "artists": artists,
            "songs": songs
        }
        save_data(current_data)
        st.session_state.rankings_data = current_data

        # Clear form after successful submit
        if "form_version" not in st.session_state:
            st.session_state.form_version = 0
        st.session_state.form_version += 1
        
        st.success(f"◈ {week} of {month} {year} saved successfully!")

    st.write("---")
    if st.button("⌂ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---EDIT DATA PAGE ---
def show_edit_data():
    year = st.session_state.selected_year
    month = st.session_state.selected_month
    week = st.session_state.selected_week
    cyber_title("✎ Edit Week Data")
    st.write(f"Editing **{week} — {month} {year}**")
    st.write("---")

    # Load existing data
    existing = rankings_data[year][month][week]

    # Totals
    st.markdown(f'<h3>{icon_chart} Totals</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        total_minutes = st.number_input("Total Minutes Listened", min_value=0, value=existing["totals"]["minutes"], key="edit_total_minutes")
    with col2:
        total_artists = st.number_input("Total Artists Listened", min_value=0, value=existing["totals"]["artists"], key="edit_total_artists")
    with col3:
        total_songs = st.number_input("Total Songs Listened", min_value=0, value=existing["totals"]["songs"], key="edit_total_songs")

    st.write("---")

    # Artists
    st.markdown(f'<h3>{icon_mic} Top 5 Artists</h3>', unsafe_allow_html=True)
    points_map = [5, 4, 3, 2, 1]
    artists = []
    for i in range(5):
        col1, col2 = st.columns([3, 2])
        with col1:
            name = st.text_input(f"Artist #{i+1}", value=existing["artists"][i]["name"], key=f"edit_artist_name_{i}")
        with col2:
            url = st.text_input(f"Artist #{i+1} image URL", key=f"edit_artist_url_{i}")
            uploaded = st.file_uploader(f"Or upload image", type=["png", "jpg", "jpeg"], key=f"edit_artist_img_{i}")
        image = url if url else existing["artists"][i]["image"]
        artists.append({"name": name, "points": points_map[i], "image": image, "uploaded": uploaded})

    st.write("---")

    # Songs
    st.markdown(f'<h3>{icon_music} Top 5 Songs</h3>', unsafe_allow_html=True)
    songs = []
    for i in range(5):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            name = st.text_input(f"Song #{i+1}", value=existing["songs"][i]["name"], key=f"edit_song_name_{i}")
        with col2:
            times_played = st.number_input(f"Times played", min_value=0, value=existing["songs"][i]["times_played"], key=f"edit_song_plays_{i}")
        with col3:
            duration = st.number_input(f"Duration (min)", min_value=0.0, step=0.1, value=existing["songs"][i]["duration"], key=f"edit_song_dur_{i}")
        col1, col2 = st.columns([3, 2])
        with col1:
            url = st.text_input(f"Song #{i+1} image URL", key=f"edit_song_url_{i}")
        with col2:
            uploaded = st.file_uploader(f"Or upload image", type=["png", "jpg", "jpeg"], key=f"edit_song_img_{i}")
        image = url if url else existing["songs"][i]["image"]
        songs.append({"name": name, "times_played": times_played, "duration": duration, "image": image, "uploaded": uploaded})

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("◈ Save Changes", use_container_width=True):
            import base64
            for item in artists:
                if item["uploaded"] is not None:
                    img_bytes = item["uploaded"].read()
                    item["image"] = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
                del item["uploaded"]

            for item in songs:
                if item["uploaded"] is not None:
                    img_bytes = item["uploaded"].read()
                    item["image"] = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
                del item["uploaded"]

            rankings_data[year][month][week] = {
                "totals": {
                    "minutes": total_minutes,
                    "artists": total_artists,
                    "songs": total_songs
                },
                "artists": artists,
                "songs": songs
            }
            save_data(rankings_data)
            st.success(f"✅ {week} of {month} {year} updated successfully!")

    with col2:
        if st.button("← Cancel", use_container_width=True):
            st.session_state.page = "week"
            st.rerun()

    st.write("---")
    if st.button("← Back to Week", use_container_width=True):
        st.session_state.page = "week"
        st.rerun()

# --- ROUTER ---
apply_cyberpunk_style()

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "year":
    show_year()
elif st.session_state.page == "month":
    show_month()
elif st.session_state.page == "week":
    show_week()
elif st.session_state.page == "summary":
    show_summary()
elif st.session_state.page == "add_data":
    show_add_data()
elif st.session_state.page == "edit_data":
    show_edit_data()
