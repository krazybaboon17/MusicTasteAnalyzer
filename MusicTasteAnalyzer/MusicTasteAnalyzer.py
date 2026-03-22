import spotipy
from spotipy.oauth2 import SpotifyOAuth
import reflex as rx

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="2a59e0328a074720a0902ac2e69a8ca9",
        client_secret="57df342acbbf4a16a87bf60694b03ae5",
        redirect_uri="http://127.0.0.1:3000/callback",
        scope="user-top-read user-read-recently-played user-read-private",
    )
)

results = sp.current_user_top_tracks(limit=5, time_range="medium_term")

artist = sp.current_user_top_artists(limit=5, time_range="medium_term")

artists_data = []
for a in artist["items"]:
    name = a["name"]
    if a["images"]:
        image_url = a["images"][0]["url"]
    else:
        image_url = ""
    artists_data.append({"name": name, "image": image_url})

tracks_data = []   
duration = []
for track in results["items"]:
    name = track["name"]
    short_name = name if len(name) <= 15 else name[:15] + "..."
    image_url = track["album"]["images"][0]["url"]
    tracks_data.append({"name": name, "short_name": short_name, "image": image_url})
    length_sec = track["duration_ms"] // 1000
    duration.append(str(length_sec) + "s")
    tracks_data[-1]["duration"] = length_sec



class State(rx.State):
    tracks: list[dict[str, str]] = tracks_data
    artists: list[dict[str, str]] = artists_data
    duration: list[str] = duration


def getTrack(track: dict):
    return rx.hstack(
        rx.image(src=track["image"], width="60px", height="60px", border_radius="5px"),
        rx.text(track["name"], font_family="Poppins", font_weight="bold", text_align="left"),
        align="center",
        justify="start",
        gap="20px",
        padding_left="50px",
        width="100%"
    )


def getArtist(artist: dict):
    return rx.hstack(
        rx.image(src=artist["image"], width="60px", height="60px", border_radius="5px"),
        rx.text(artist["name"], font_family="Poppins", font_weight="bold", text_align="left"),
        align="center",
        justify="start",
        gap="20px",
        padding_left="50px",
        width="100%"
    )
def getLength():
    return rx.hstack(
        rx.foreach(State.duration, lambda length: rx.text(length, font_family="Poppins", font_weight="bold", font_size="24px")),
        gap="30px"
    )


def navbar():
    return rx.box(
        rx.hstack(
            rx.heading(
                "Music Taste Analyzer",
                font_family="Poppins",
                font_weight="bold",
                font_size="30px",
                color="#1DB954",
                text_align="center",
            ),
            bg="#0A0A0A",
            width="100%",
            height="15vh",
            justify="center",
            align="center",
            padding="20px",
        ),
        width="100%",
    )
def durGraph():
    return rx.box(
        rx.heading("Track Duration (Seconds)", color="#1DB954", font_family="Poppins", padding_bottom="20px"),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="duration",
                fill="#1DB954",
            ),
            rx.recharts.x_axis(
                data_key="short_name",
                stroke="#1DB954",
            ),
            rx.recharts.y_axis(
                stroke="#1DB954",
            ),
            rx.recharts.graphing_tooltip(),
            data=State.tracks,
            width="100%",
            height=300,
        ),
        width="800px",
        bg="#1F1F1F",
        padding="30px",
        border_radius="10px",
        margin_top="70px",
        margin_bottom="50px"
    )
def index():
    return rx.vstack(
        navbar(),
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Top Tracks",
                    font_family="Poppins",
                    font_weight="bold",
                    font_size="30px",
                    color="#1DB954",
                    text_align="center",
                    padding_bottom="30px",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(State.tracks, getTrack),
                        align="center",
                        style={"gap": "5vh"},
                    ),
                    bg="#1F1F1F",
                    padding_top="30px",
                    padding_bottom="30px",
                    margin_left="50px",
                    margin_right="50px",
                    border_radius="8px",
                    width="650px",
                    text_align="center",
                    _hover={"bg": "#282828"},
                ),
                width="100%",
                align="center",
            ),
            rx.vstack(
                rx.heading(
                    "Top Artists",
                    font_family="Poppins",
                    font_weight="bold",
                    font_size="30px",
                    color="#1DB954",
                    text_align="center",
                    padding_bottom="30px",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(State.artists, getArtist),
                        align="center",
                        style={"gap": "5vh"},
                    ),
                    bg="#1F1F1F",
                    padding_top="30px",
                    padding_bottom="30px",
                    margin_left="50px",
                    margin_right="50px",
                    border_radius="8px",
                    width="650px",
                    text_align="center",
                    _hover={"bg": "#282828"},
                ),
                width="100%",
                align="center",
            ),
            width="100%",
            color="#1DB954",
            justify="center",
            style={"gap": "1vw"},
            padding_top="50px",
        ),
        durGraph(),
        align_items = "center",
        
        background_color="#121212",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap",
    ],
)
app.add_page(index)
