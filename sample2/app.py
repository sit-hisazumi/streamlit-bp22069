import time
from datetime import datetime, timedelta
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="センサーモニタリング",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ センサーモニタリングダッシュボード")

# データファイルのパス
DATA_DIR = Path(__file__).parent / "data"
SENSOR_FILE = DATA_DIR / "sensor_data.csv"

# センサーの閾値設定
THRESHOLDS = {
    "温度": {"min": 18, "max": 28, "unit": "°C"},
    "湿度": {"min": 40, "max": 70, "unit": "%"},
    "CO2濃度": {"min": 0, "max": 1000, "unit": "ppm"},
}

# センサーごとの色
SENSOR_COLORS = {
    "温度": "#e74c3c",
    "湿度": "#3498db",
    "CO2濃度": "#9b59b6",
}


def generate_sample_data() -> pd.DataFrame:
    """サンプルデータを生成"""
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i * 5) for i in range(144)][::-1]

    np.random.seed(42)
    temp_base = 23 + np.sin(np.linspace(0, 4 * np.pi, 144)) * 3
    humidity_base = 55 + np.sin(np.linspace(0, 3 * np.pi, 144)) * 10
    co2_base = 600 + np.sin(np.linspace(0, 5 * np.pi, 144)) * 200

    return pd.DataFrame({
        "時刻": timestamps,
        "温度": temp_base + np.random.normal(0, 0.5, 144),
        "湿度": humidity_base + np.random.normal(0, 2, 144),
        "CO2濃度": co2_base + np.random.normal(0, 30, 144),
    })


def load_sensor_data() -> pd.DataFrame:
    """センサーデータを読み込む"""
    if SENSOR_FILE.exists():
        return pd.read_csv(SENSOR_FILE, parse_dates=["時刻"])
    else:
        return generate_sample_data()


def get_status(value: float, sensor_type: str) -> tuple[str, str]:
    """値に応じたステータスと色を返す"""
    threshold = THRESHOLDS[sensor_type]
    if threshold["min"] <= value <= threshold["max"]:
        return "正常", "#28a745"
    else:
        return "警告", "#dc3545"


def render_sensor_card(name: str, value: float, unit: str, color: str):
    """センサーカードを描画"""
    status, status_color = get_status(value, name)
    threshold = THRESHOLDS[name]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-top: 4px solid {color};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <p style="margin: 0; color: #666; font-size: 14px;">{name}</p>
            <p style="margin: 10px 0; font-size: 36px; font-weight: bold; color: #333;">
                {value:.1f}<span style="font-size: 18px;">{unit}</span>
            </p>
            <p style="margin: 5px 0;">
                <span style="
                    background-color: {status_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                ">{status}</span>
            </p>
            <p style="margin: 10px 0 0 0; color: #888; font-size: 12px;">
                適正範囲: {threshold["min"]} - {threshold["max"]}{unit}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# サイドバー設定
st.sidebar.header("設定")
auto_refresh = st.sidebar.checkbox("自動更新（5秒ごと）", value=False)
selected_sensors = st.sidebar.multiselect(
    "表示するセンサー",
    options=list(THRESHOLDS.keys()),
    default=list(THRESHOLDS.keys()),
)

# データ読み込み
sensor_data = load_sensor_data()

# データソースの表示
if SENSOR_FILE.exists():
    st.caption("📂 データソース: CSVファイル")
else:
    st.caption("📂 データソース: サンプルデータ")

# 最新データの取得
latest = sensor_data.iloc[-1]

# 現在値カード
st.markdown("### 📊 現在のセンサー値")
cols = st.columns(len(selected_sensors))

for i, sensor in enumerate(selected_sensors):
    with cols[i]:
        render_sensor_card(
            sensor,
            latest[sensor],
            THRESHOLDS[sensor]["unit"],
            SENSOR_COLORS[sensor],
        )

# グラフ表示
st.markdown("---")
st.markdown("### 📈 センサー推移（過去12時間）")

# 表示期間の選択
time_range = st.selectbox(
    "表示期間",
    options=["1時間", "3時間", "6時間", "12時間"],
    index=3,
)

# 期間に応じたデータのフィルタリング
hours_map = {"1時間": 12, "3時間": 36, "6時間": 72, "12時間": 144}
display_data = sensor_data.tail(hours_map[time_range])

# タブで各センサーのグラフを表示
tabs = st.tabs(selected_sensors)

for tab, sensor in zip(tabs, selected_sensors):
    with tab:
        threshold = THRESHOLDS[sensor]

        # ベースチャート
        base = alt.Chart(display_data).encode(
            x=alt.X("時刻:T", title="時刻"),
        )

        # 適正範囲の背景
        area = (
            alt.Chart(pd.DataFrame({"y": [threshold["min"]], "y2": [threshold["max"]]}))
            .mark_rect(opacity=0.2, color="#28a745")
            .encode(
                y=alt.datum(threshold["min"]),
                y2=alt.datum(threshold["max"]),
            )
        )

        # 折れ線グラフ
        line = base.mark_line(
            strokeWidth=2,
            color=SENSOR_COLORS[sensor],
        ).encode(
            y=alt.Y(
                f"{sensor}:Q",
                title=f"{sensor} ({threshold['unit']})",
            ),
        )

        # ポイント
        points = base.mark_circle(
            size=30,
            color=SENSOR_COLORS[sensor],
        ).encode(
            y=alt.Y(f"{sensor}:Q"),
            tooltip=[
                alt.Tooltip("時刻:T", title="時刻", format="%H:%M"),
                alt.Tooltip(f"{sensor}:Q", title=sensor, format=".1f"),
            ],
        )

        chart = (area + line + points).properties(height=300).interactive()
        st.altair_chart(chart, use_container_width=True)

        # 統計情報
        stat_cols = st.columns(4)
        with stat_cols[0]:
            st.metric("最新値", f"{latest[sensor]:.1f}{threshold['unit']}")
        with stat_cols[1]:
            st.metric("最高値", f"{display_data[sensor].max():.1f}{threshold['unit']}")
        with stat_cols[2]:
            st.metric("最低値", f"{display_data[sensor].min():.1f}{threshold['unit']}")
        with stat_cols[3]:
            st.metric("平均値", f"{display_data[sensor].mean():.1f}{threshold['unit']}")

# 凡例
st.markdown("---")
st.markdown("### 状態の凡例")
legend_cols = st.columns(2)
with legend_cols[0]:
    st.markdown("🟢 **正常**: 適正範囲内")
with legend_cols[1]:
    st.markdown("🔴 **警告**: 適正範囲外")

# 自動更新
if auto_refresh:
    time.sleep(5)
    st.rerun()
