
import time
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

from game_engine import SnakeGame

from config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    BACKGROUND_COLOR,
    GRID_COLOR,
    SNAKE_COLOR,
    FOOD_COLOR,
    BONUS_COLOR,
    OBSTACLE_COLOR
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NEON SNAKE",
    page_icon="🐍",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "game" not in st.session_state:
    st.session_state.game = SnakeGame()

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.monotonic()

game = st.session_state.game

# Ensure pause state exists
if not hasattr(game, "paused"):
    game.paused = False


# --------------------------------------------------
# AUTOMATIC GAME REFRESH
# --------------------------------------------------

st_autorefresh(
    interval=100,
    key="snake_refresh"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #080B16;
    color: white;
}

h1 {
    color: #00FF9C;
    text-align: center;
    letter-spacing: 8px;
}

h3 {
    color: #FF3CAC;
}

.score-card {
    background: #111827;
    border: 1px solid #00FF9C;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown("# NEON SNAKE")

st.markdown(
    "<p style='text-align:center;color:#FF3CAC;'>"
    "ENTER THE GRID"
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# GAME MODE
# --------------------------------------------------

mode = st.selectbox(
    "GAME MODE",
    options=["Classic", "Zen", "Obstacles"],
    index=0
)

if mode != game.mode:

    st.session_state.game = SnakeGame(mode)
    game = st.session_state.game

    game.paused = False
    st.session_state.last_tick = time.monotonic()


# --------------------------------------------------
# GAME LOOP
# --------------------------------------------------

if not game.game_over and not game.paused:

    current_time = time.monotonic()

    # Convert game speed into movement interval
    movement_interval = 1 / max(game.speed, 1)

    if current_time - st.session_state.last_tick >= movement_interval:

        game.move()

        st.session_state.last_tick = current_time


# --------------------------------------------------
# SCOREBOARD
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("SCORE", game.score)

with col2:
    st.metric("LEVEL", game.level)

with col3:
    st.metric("SNAKE LENGTH", len(game.snake))

st.divider()


# --------------------------------------------------
# GAME BOARD
# --------------------------------------------------

def render_game(game):

    grid = [
        ["" for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]

    # Draw obstacles
    for x, y in game.obstacles:

        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            grid[y][x] = "🟪"

    # Draw regular food
    if game.food:

        x, y = game.food

        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            grid[y][x] = "❤️"

    # Draw bonus food
    if game.bonus_food:

        x, y = game.bonus_food

        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            grid[y][x] = "⭐"

    # Draw snake
    for index, (x, y) in enumerate(game.snake):

        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:

            if index == 0:
                grid[y][x] = "🟢"
            else:
                grid[y][x] = "🟩"

    return grid


grid = render_game(game)


# --------------------------------------------------
# HTML BOARD RENDERING
# --------------------------------------------------

board_html = f"""
<style>

.neon-board {{

    display: grid;

    grid-template-columns:
        repeat({GRID_WIDTH}, minmax(0, 1fr));

    grid-template-rows:
        repeat({GRID_HEIGHT}, minmax(0, 1fr));

    width: min(90vw, 600px);

    aspect-ratio: 1;

    margin: auto;

    background: {BACKGROUND_COLOR};

    border: 2px solid {SNAKE_COLOR};

    box-shadow: 0 0 25px #00FF9C55;

}}

.neon-cell {{

    display: flex;

    align-items: center;

    justify-content: center;

    border: 1px solid {GRID_COLOR};

    font-size: clamp(7px, 2vw, 17px);

    overflow: hidden;

}}

</style>

<div class="neon-board">
"""

for row in grid:

    for cell in row:

        board_html += (
            f'<div class="neon-cell">'
            f'{cell if cell else "&nbsp;"}'
            f'</div>'
        )

board_html += "</div>"

components.html(
    board_html,
    height=620,
    scrolling=False
)


# --------------------------------------------------
# CONTROLS
# --------------------------------------------------

st.divider()

st.subheader("CONTROLS")

st.caption("Use the buttons to change direction. The snake moves automatically.")


# Direction controls

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("⬅ LEFT", use_container_width=True):
        game.change_direction((-1, 0))

with col2:

    if st.button("⬆ UP", use_container_width=True):
        game.change_direction((0, -1))

with col3:

    if st.button("➡ RIGHT", use_container_width=True):
        game.change_direction((1, 0))


col1, col2, col3 = st.columns(3)

with col2:

    if st.button("⬇ DOWN", use_container_width=True):
        game.change_direction((0, 1))


# Game controls

col1, col2 = st.columns(2)

with col1:

    pause_label = "RESUME" if game.paused else "PAUSE"

    if st.button(pause_label, use_container_width=True):

        game.paused = not game.paused

        st.session_state.last_tick = time.monotonic()

with col2:

    if st.button("RESTART", use_container_width=True):

        game.restart()

        game.paused = False

        st.session_state.last_tick = time.monotonic()


# --------------------------------------------------
# GAME STATUS
# --------------------------------------------------

if game.game_over:

    st.error("GAME OVER! Press RESTART to play again.")

elif game.paused:

    st.warning("GAME PAUSED")

else:

    st.success("GAME RUNNING")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption("NEON SNAKE | BUILT BY SIDDHARTH")
