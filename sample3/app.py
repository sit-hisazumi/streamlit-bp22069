import streamlit as st

st.set_page_config(
    page_title="絵文字キャンバス",
    page_icon="🎨",
    layout="wide",
)

st.title("🎨 絵文字キャンバス")

# 絵文字パレット
EMOJI_PALETTES = {
    "自然": ["🌲", "🌳", "🌴", "🌵", "🌸", "🌺", "🌻", "🌷", "🍀", "🍁", "🍂", "🌾"],
    "動物": ["🐶", "🐱", "🐭", "🐰", "🦊", "🐻", "🐼", "🐨", "🐸", "🐵", "🐔", "🐧"],
    "食べ物": ["🍎", "🍊", "🍋", "🍇", "🍓", "🍔", "🍕", "🍣", "🍩", "🍰", "🍦", "🧁"],
    "天気": ["☀️", "🌙", "⭐", "🌈", "☁️", "🌧️", "⛈️", "❄️", "💧", "🔥", "💨", "🌊"],
    "顔": ["😀", "😊", "😎", "🥰", "😴", "🤔", "😱", "😭", "🤣", "😡", "👻", "💀"],
    "乗り物": ["🚗", "🚕", "🚌", "🚂", "✈️", "🚀", "🛸", "⛵", "🚲", "🏍️", "🚁", "🎠"],
    "建物": ["🏠", "🏢", "🏭", "🏥", "🏫", "⛪", "🏰", "🗼", "🗽", "⛩️", "🎪", "⛺"],
    "記号": ["❤️", "💛", "💚", "💙", "💜", "⬛", "⬜", "🟥", "🟧", "🟨", "🟩", "🟦"],
}

# セッション状態の初期化
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 16
if "canvas" not in st.session_state:
    st.session_state.canvas = [
        ["⬜" for _ in range(st.session_state.grid_size)]
        for _ in range(st.session_state.grid_size)
    ]
if "selected_emoji" not in st.session_state:
    st.session_state.selected_emoji = "🌲"
if "history" not in st.session_state:
    st.session_state.history = []


def resize_canvas(new_size: int):
    """キャンバスサイズを変更"""
    old_canvas = st.session_state.canvas
    old_size = len(old_canvas)
    new_canvas = [["⬜" for _ in range(new_size)] for _ in range(new_size)]

    # 既存の内容をコピー
    for i in range(min(old_size, new_size)):
        for j in range(min(old_size, new_size)):
            new_canvas[i][j] = old_canvas[i][j]

    st.session_state.canvas = new_canvas
    st.session_state.grid_size = new_size


def clear_canvas():
    """キャンバスをクリア"""
    save_history()
    st.session_state.canvas = [
        ["⬜" for _ in range(st.session_state.grid_size)]
        for _ in range(st.session_state.grid_size)
    ]


def save_history():
    """履歴を保存"""
    import copy
    st.session_state.history.append(copy.deepcopy(st.session_state.canvas))
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)


def undo():
    """元に戻す"""
    if st.session_state.history:
        st.session_state.canvas = st.session_state.history.pop()


def fill_canvas(emoji: str):
    """キャンバスを塗りつぶし"""
    save_history()
    st.session_state.canvas = [
        [emoji for _ in range(st.session_state.grid_size)]
        for _ in range(st.session_state.grid_size)
    ]


# サイドバー
st.sidebar.header("設定")

# キャンバスサイズ
new_size = st.sidebar.select_slider(
    "キャンバスサイズ",
    options=[8, 12, 16, 20, 24],
    value=st.session_state.grid_size,
)
if new_size != st.session_state.grid_size:
    resize_canvas(new_size)

st.sidebar.markdown("---")

# パレット選択
st.sidebar.header("パレット")
selected_palette = st.sidebar.selectbox(
    "カテゴリ",
    options=list(EMOJI_PALETTES.keys()),
)

# 絵文字選択
st.sidebar.markdown("絵文字を選択:")
palette_emojis = EMOJI_PALETTES[selected_palette]
cols = st.sidebar.columns(4)
for i, emoji in enumerate(palette_emojis):
    with cols[i % 4]:
        if st.button(
            emoji,
            key=f"palette_{emoji}",
            use_container_width=True,
            type="primary" if emoji == st.session_state.selected_emoji else "secondary",
        ):
            st.session_state.selected_emoji = emoji

st.sidebar.markdown("---")

# 操作ボタン
st.sidebar.header("操作")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("クリア", use_container_width=True):
        clear_canvas()
        st.rerun()
with col2:
    if st.button("元に戻す", use_container_width=True, disabled=len(st.session_state.history) == 0):
        undo()
        st.rerun()

if st.sidebar.button("選択中の絵文字で塗りつぶし", use_container_width=True):
    fill_canvas(st.session_state.selected_emoji)
    st.rerun()

# メインエリア
st.markdown(f"### 選択中: {st.session_state.selected_emoji}")

# キャンバス表示
grid_size = st.session_state.grid_size
button_size = max(30, 400 // grid_size)

# CSSでボタンサイズを調整
st.markdown(
    f"""
    <style>
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 0 0 auto !important;
    }}
    div.canvas-btn button {{
        width: {button_size}px !important;
        height: {button_size}px !important;
        padding: 0 !important;
        font-size: {button_size * 0.6}px !important;
        min-height: 0 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# キャンバスグリッド
for i in range(grid_size):
    cols = st.columns(grid_size)
    for j in range(grid_size):
        with cols[j]:
            st.markdown('<div class="canvas-btn">', unsafe_allow_html=True)
            if st.button(
                st.session_state.canvas[i][j],
                key=f"cell_{i}_{j}",
                use_container_width=True,
            ):
                save_history()
                st.session_state.canvas[i][j] = st.session_state.selected_emoji
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# エクスポート機能
st.markdown("---")
st.markdown("### エクスポート")

# テキスト形式で出力
canvas_text = "\n".join(["".join(row) for row in st.session_state.canvas])

col1, col2 = st.columns(2)
with col1:
    st.text_area("テキスト形式", value=canvas_text, height=200)
with col2:
    st.markdown("**プレビュー:**")
    st.markdown(
        f'<div style="font-size: 16px; line-height: 1.2; font-family: monospace;">{canvas_text.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )
