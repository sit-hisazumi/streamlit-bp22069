import colorsys
import random

import streamlit as st

st.set_page_config(
    page_title="カラーパレット生成器",
    page_icon="🎨",
    layout="wide",
)

st.title("🎨 カラーパレット生成器")


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """HEXをRGBに変換"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGBをHEXに変換"""
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """RGBをHSLに変換"""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return h * 360, s * 100, l * 100


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """HSLをRGBに変換"""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)


def get_contrast_color(hex_color: str) -> str:
    """背景色に対するコントラスト色を返す"""
    r, g, b = hex_to_rgb(hex_color)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.5 else "#ffffff"


def generate_random_palette(count: int = 5) -> list[str]:
    """ランダムなパレットを生成"""
    return [rgb_to_hex(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(count)]


def generate_analogous(base_hex: str, count: int = 5) -> list[str]:
    """類似色パレットを生成"""
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    colors = []
    spread = 30
    start_h = h - spread * (count // 2)

    for i in range(count):
        new_h = (start_h + spread * i) % 360
        new_rgb = hsl_to_rgb(new_h, s, l)
        colors.append(rgb_to_hex(*new_rgb))

    return colors


def generate_complementary(base_hex: str, count: int = 5) -> list[str]:
    """補色パレットを生成"""
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    comp_h = (h + 180) % 360

    colors = []
    for i in range(count):
        if i < count // 2:
            new_h = h
            new_l = max(20, min(80, l - 15 * (count // 2 - i - 1)))
        elif i == count // 2:
            new_h = comp_h
            new_l = l
        else:
            new_h = comp_h
            new_l = max(20, min(80, l + 15 * (i - count // 2)))

        new_rgb = hsl_to_rgb(new_h, s, new_l)
        colors.append(rgb_to_hex(*new_rgb))

    return colors


def generate_triadic(base_hex: str, count: int = 5) -> list[str]:
    """トライアド配色を生成"""
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    # 3つの基本色相（120度ずつ）
    base_hues = [h, (h + 120) % 360, (h + 240) % 360]

    # 各色相グループに何色ずつ割り当てるか計算
    per_hue = count // 3
    remainder = count % 3

    colors = []
    for hue_idx, hue in enumerate(base_hues):
        # この色相グループの色数
        group_count = per_hue + (1 if hue_idx < remainder else 0)
        for j in range(group_count):
            # グループ内で明度にバリエーション
            if group_count == 1:
                new_l = l
            else:
                new_l = l - 15 + (30 / (group_count - 1)) * j
            new_l = max(20, min(80, new_l))
            new_rgb = hsl_to_rgb(hue, s, new_l)
            colors.append(rgb_to_hex(*new_rgb))

    return colors


def generate_monochromatic(base_hex: str, count: int = 5) -> list[str]:
    """モノクロマティック配色を生成"""
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    colors = []
    for i in range(count):
        new_l = 20 + (60 / (count - 1)) * i if count > 1 else l
        new_rgb = hsl_to_rgb(h, s, new_l)
        colors.append(rgb_to_hex(*new_rgb))

    return colors


def generate_split_complementary(base_hex: str, count: int = 5) -> list[str]:
    """分裂補色配色を生成"""
    r, g, b = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    # 3つの基本色相（ベース色と補色の両隣）
    base_hues = [h, (h + 150) % 360, (h + 210) % 360]

    # 各色相グループに何色ずつ割り当てるか計算
    per_hue = count // 3
    remainder = count % 3

    colors = []
    for hue_idx, hue in enumerate(base_hues):
        # この色相グループの色数
        group_count = per_hue + (1 if hue_idx < remainder else 0)
        for j in range(group_count):
            # グループ内で明度にバリエーション
            if group_count == 1:
                new_l = l
            else:
                new_l = l - 15 + (30 / (group_count - 1)) * j
            new_l = max(20, min(80, new_l))
            new_rgb = hsl_to_rgb(hue, s, new_l)
            colors.append(rgb_to_hex(*new_rgb))

    return colors


def render_color_card(hex_color: str, index: int):
    """カラーカードを描画"""
    text_color = get_contrast_color(hex_color)
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(r, g, b)

    st.markdown(
        f"""
        <div style="
            background-color: {hex_color};
            border-radius: 10px;
            padding: 30px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            min-height: 180px;
        ">
            <p style="color: {text_color}; font-size: 24px; font-weight: bold; margin: 0 0 15px 0;">
                {hex_color.upper()}
            </p>
            <p style="color: {text_color}; font-size: 12px; margin: 5px 0; opacity: 0.9;">
                RGB({r}, {g}, {b})
            </p>
            <p style="color: {text_color}; font-size: 12px; margin: 5px 0; opacity: 0.9;">
                HSL({h:.0f}°, {s:.0f}%, {l:.0f}%)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# セッション状態の初期化
if "palette" not in st.session_state:
    st.session_state.palette = generate_random_palette(5)

# サイドバー
st.sidebar.header("パレット設定")

# ベースカラー選択
base_color = st.sidebar.color_picker("ベースカラー", "#3498db")

# 配色タイプ
harmony_type = st.sidebar.selectbox(
    "配色タイプ",
    options=[
        "ランダム",
        "類似色 (Analogous)",
        "補色 (Complementary)",
        "トライアド (Triadic)",
        "モノクロマティック",
        "分裂補色 (Split-complementary)",
    ],
)

# 色数
color_count = st.sidebar.slider("色数", min_value=3, max_value=8, value=5)

# 生成ボタン
if st.sidebar.button("パレット生成", type="primary", use_container_width=True):
    if harmony_type == "ランダム":
        st.session_state.palette = generate_random_palette(color_count)
    elif harmony_type == "類似色 (Analogous)":
        st.session_state.palette = generate_analogous(base_color, color_count)
    elif harmony_type == "補色 (Complementary)":
        st.session_state.palette = generate_complementary(base_color, color_count)
    elif harmony_type == "トライアド (Triadic)":
        st.session_state.palette = generate_triadic(base_color, color_count)
    elif harmony_type == "モノクロマティック":
        st.session_state.palette = generate_monochromatic(base_color, color_count)
    elif harmony_type == "分裂補色 (Split-complementary)":
        st.session_state.palette = generate_split_complementary(base_color, color_count)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### 配色タイプについて
    - **類似色**: 色相環で隣り合う色
    - **補色**: 色相環で反対の色
    - **トライアド**: 色相環で等間隔の3色
    - **モノクロマティック**: 同じ色相で明度違い
    - **分裂補色**: 補色の両隣の色を使用
    """
)

# メインエリア
st.markdown("### 生成されたパレット")

# パレット表示
cols = st.columns(len(st.session_state.palette))
for i, color in enumerate(st.session_state.palette):
    with cols[i]:
        render_color_card(color, i)

# プレビューエリア
st.markdown("---")
st.markdown("### プレビュー")

preview_tabs = st.tabs(["グラデーション", "UI サンプル", "テキスト"])

with preview_tabs[0]:
    gradient_colors = ", ".join(st.session_state.palette)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, {gradient_colors});
            height: 100px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        "></div>
        """,
        unsafe_allow_html=True,
    )

with preview_tabs[1]:
    if len(st.session_state.palette) >= 3:
        primary = st.session_state.palette[0]
        secondary = st.session_state.palette[len(st.session_state.palette) // 2]
        accent = st.session_state.palette[-1]

        st.markdown(
            f"""
            <div style="
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <div style="
                    background-color: {primary};
                    color: {get_contrast_color(primary)};
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 15px;
                ">
                    <h3 style="margin: 0;">ヘッダー</h3>
                </div>
                <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <button style="
                        background-color: {secondary};
                        color: {get_contrast_color(secondary)};
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">ボタン1</button>
                    <button style="
                        background-color: {accent};
                        color: {get_contrast_color(accent)};
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">ボタン2</button>
                </div>
                <div style="
                    border-left: 4px solid {primary};
                    padding-left: 15px;
                    color: #333;
                ">
                    <p style="margin: 0;">サンプルテキストがここに表示されます。</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with preview_tabs[2]:
    st.markdown("各色でのテキスト表示:")
    for color in st.session_state.palette:
        st.markdown(
            f'<span style="color: {color}; font-size: 18px; font-weight: bold; margin-right: 20px;">Sample Text {color.upper()}</span>',
            unsafe_allow_html=True,
        )

# エクスポート
st.markdown("---")
st.markdown("### エクスポート")

export_cols = st.columns(3)

with export_cols[0]:
    st.markdown("**HEX**")
    hex_codes = "\n".join(st.session_state.palette)
    st.code(hex_codes, language=None)

with export_cols[1]:
    st.markdown("**CSS変数**")
    css_vars = ":root {\n"
    for i, color in enumerate(st.session_state.palette):
        css_vars += f"  --color-{i + 1}: {color};\n"
    css_vars += "}"
    st.code(css_vars, language="css")

with export_cols[2]:
    st.markdown("**Tailwind**")
    tailwind_config = "colors: {\n"
    names = ["primary", "secondary", "accent", "highlight", "muted", "dark", "light", "extra"]
    for i, color in enumerate(st.session_state.palette):
        name = names[i] if i < len(names) else f"color{i + 1}"
        tailwind_config += f"  '{name}': '{color}',\n"
    tailwind_config += "}"
    st.code(tailwind_config, language="javascript")
