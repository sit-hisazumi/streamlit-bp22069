from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="製造ライン稼働状況ダッシュボード",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 製造ライン稼働状況ダッシュボード")

# データファイルのパス
DATA_DIR = Path(__file__).parent / "data"
EQUIPMENT_FILE = DATA_DIR / "equipment.csv"
HISTORY_FILE = DATA_DIR / "history.csv"


def load_equipment_data() -> list[dict]:
    """設備データを読み込む（CSVがあれば使用、なければサンプルデータ）"""
    if EQUIPMENT_FILE.exists():
        df = pd.read_csv(EQUIPMENT_FILE)
        return df.to_dict("records")
    else:
        return [
            {"name": "プレス機A", "utilization": 92},
            {"name": "組立ラインB", "utilization": 65},
            {"name": "検査機C", "utilization": 35},
        ]


def load_history_data() -> pd.DataFrame:
    """履歴データを読み込む（CSVがあれば使用、なければサンプルデータ）"""
    if HISTORY_FILE.exists():
        df = pd.read_csv(HISTORY_FILE, parse_dates=["時刻"])
        return df
    else:
        return pd.DataFrame({
            "時刻": pd.date_range(end=pd.Timestamp.now(), periods=24, freq="h"),
            "プレス機A": [
                85, 88, 90, 87, 92, 95, 93, 91, 89, 88, 90, 92,
                94, 91, 88, 85, 87, 90, 93, 95, 94, 92, 91, 92,
            ],
            "組立ラインB": [
                70, 72, 68, 65, 60, 58, 62, 65, 68, 70, 72, 75,
                73, 70, 68, 65, 62, 60, 63, 65, 67, 68, 66, 65,
            ],
            "検査機C": [
                80, 75, 70, 65, 55, 50, 45, 40, 38, 35, 33, 30,
                32, 35, 38, 40, 42, 40, 38, 36, 35, 34, 35, 35,
            ],
        })


def get_status_and_color(utilization: int) -> tuple[str, str]:
    """稼働率に応じた状態と色を返す"""
    if utilization >= 80:
        return "稼働中", "#28a745"  # 緑
    elif utilization >= 50:
        return "注意", "#ffc107"  # 黄
    else:
        return "停止", "#dc3545"  # 赤


# グラフ用の固定色（設備ごと）- 状態色（緑/黄/赤）と被らない色
LINE_COLORS = {
    "プレス機A": "#1f77b4",  # 青
    "組立ラインB": "#9467bd",  # 紫
    "検査機C": "#17becf",  # シアン
}


def render_equipment_card(name: str, utilization: int):
    """設備カードを描画"""
    status, status_color = get_status_and_color(utilization)
    line_color = LINE_COLORS.get(name, "#666666")

    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            border-left: 5px solid {status_color};
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="
                    display: inline-block;
                    width: 16px;
                    height: 16px;
                    background-color: {line_color};
                    border-radius: 3px;
                    margin-right: 10px;
                "></span>
                <h3 style="margin: 0; color: #333;">{name}</h3>
            </div>
            <p style="margin: 5px 0; font-size: 16px;">
                <strong>稼働率:</strong> {utilization}%
            </p>
            <p style="margin: 5px 0; font-size: 16px;">
                <strong>状態:</strong>
                <span style="
                    background-color: {status_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 4px;
                    font-weight: bold;
                ">{status}</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# データ読み込み
equipment_data = load_equipment_data()
history_data = load_history_data()

# データソースの表示
if EQUIPMENT_FILE.exists() or HISTORY_FILE.exists():
    st.caption("📂 データソース: CSVファイル")
else:
    st.caption("📂 データソース: サンプルデータ（data/フォルダにCSVを配置すると実データを表示）")

# 3カラムで設備カードを表示
cols = st.columns(len(equipment_data))

for i, equipment in enumerate(equipment_data):
    with cols[i]:
        render_equipment_card(equipment["name"], equipment["utilization"])

# 稼働率推移グラフ
st.markdown("---")
st.markdown("### 📈 稼働率推移（過去24時間）")

# 長形式に変換
chart_df = history_data.melt(id_vars=["時刻"], var_name="設備", value_name="稼働率")

# Altairチャートを作成（固定色を使用）
chart = (
    alt.Chart(chart_df)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("時刻:T", title="時刻"),
        y=alt.Y("稼働率:Q", title="稼働率 (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color(
            "設備:N",
            scale=alt.Scale(
                domain=list(LINE_COLORS.keys()),
                range=list(LINE_COLORS.values()),
            ),
            legend=alt.Legend(title="設備"),
        ),
    )
    .properties(height=400)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

# 凡例
st.markdown("---")
st.markdown("### 状態の凡例")
legend_cols = st.columns(3)
with legend_cols[0]:
    st.markdown("🟢 **稼働中**: 稼働率 80% 以上")
with legend_cols[1]:
    st.markdown("🟡 **注意**: 稼働率 50-79%")
with legend_cols[2]:
    st.markdown("🔴 **停止**: 稼働率 50% 未満")
