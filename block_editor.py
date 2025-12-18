import streamlit as st
import json
from typing import Dict, List

# ページ設定
st.set_page_config(
    page_title="TUIプログラミング言語ブロックエディター",
    page_icon="🧩",
    layout="wide"
)

# セッション状態の初期化
if 'blocks' not in st.session_state:
    st.session_state.blocks = {
        'if': {
            'label': 'If',
            'color': '#FF6B6B',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#FFFFFF',
            'category': '制御構造'
        },
        'loop': {
            'label': 'Loop',
            'color': '#4ECDC4',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#FFFFFF',
            'category': '制御構造'
        },
        'turn_right': {
            'label': 'Turn Right',
            'color': '#95E1D3',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#2C3E50',
            'category': '動作'
        },
        'turn_left': {
            'label': 'Turn Left',
            'color': '#F38181',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#2C3E50',
            'category': '動作'
        },
        'move_forward': {
            'label': 'Move Forward',
            'color': '#FFE66D',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#2C3E50',
            'category': '動作'
        },
        'while': {
            'label': 'While',
            'color': '#A8E6CF',
            'border_style': 'solid',
            'border_width': 2,
            'padding': 10,
            'font_size': 14,
            'text_color': '#2C3E50',
            'category': '制御構造'
        }
    }

if 'selected_block' not in st.session_state:
    st.session_state.selected_block = 'if'

# タイトル
st.title("🧩 TUIプログラミング言語ブロックエディター")
st.markdown("教育向けプログラミング言語のブロックをカスタマイズできます")

# メインレイアウト
col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("⚙️ ブロック設定")

    # ブロック選択
    block_names = list(st.session_state.blocks.keys())
    selected_index = block_names.index(st.session_state.selected_block) if st.session_state.selected_block in block_names else 0

    selected_block = st.selectbox(
        "編集するブロックを選択",
        block_names,
        index=selected_index,
        format_func=lambda x: f"{st.session_state.blocks[x]['label']} ({st.session_state.blocks[x]['category']})"
    )
    st.session_state.selected_block = selected_block

    # 新しいブロックを追加
    with st.expander("➕ 新しいブロックを追加"):
        new_block_id = st.text_input("ブロックID (例: print)", key="new_block_id")
        new_block_label = st.text_input("ブロック表示名 (例: Print)", key="new_block_label")
        new_block_category = st.selectbox("カテゴリ", ["制御構造", "動作", "演算", "変数", "その他"], key="new_category")

        if st.button("ブロックを追加"):
            if new_block_id and new_block_label:
                if new_block_id not in st.session_state.blocks:
                    st.session_state.blocks[new_block_id] = {
                        'label': new_block_label,
                        'color': '#3498DB',
                        'border_style': 'solid',
                        'border_width': 2,
                        'padding': 10,
                        'font_size': 14,
                        'text_color': '#FFFFFF',
                        'category': new_block_category
                    }
                    st.session_state.selected_block = new_block_id
                    st.success(f"ブロック '{new_block_label}' を追加しました！")
                    st.rerun()
                else:
                    st.error("このIDは既に使用されています")
            else:
                st.error("IDと表示名を入力してください")

    st.markdown("---")

    # 現在のブロック設定
    current_block = st.session_state.blocks[selected_block]

    # テキスト設定
    st.subheader("📝 テキスト設定")
    label = st.text_input("表示テキスト", current_block['label'], key=f"label_{selected_block}")
    category = st.selectbox("カテゴリ", ["制御構造", "動作", "演算", "変数", "その他"],
                           index=["制御構造", "動作", "演算", "変数", "その他"].index(current_block.get('category', 'その他')),
                           key=f"category_{selected_block}")

    # 色設定
    st.subheader("🎨 色設定")
    col_color1, col_color2 = st.columns(2)
    with col_color1:
        color = st.color_picker("背景色", current_block['color'], key=f"color_{selected_block}")
    with col_color2:
        text_color = st.color_picker("文字色", current_block['text_color'], key=f"text_color_{selected_block}")

    # スタイル設定
    st.subheader("🖌️ スタイル設定")
    border_style = st.selectbox(
        "枠線スタイル",
        ["solid", "dashed", "dotted", "double", "groove"],
        index=["solid", "dashed", "dotted", "double", "groove"].index(current_block['border_style']),
        key=f"border_style_{selected_block}"
    )

    col_style1, col_style2 = st.columns(2)
    with col_style1:
        border_width = st.slider("枠線の太さ (px)", 0, 10, current_block['border_width'], key=f"border_width_{selected_block}")
        padding = st.slider("内側の余白 (px)", 5, 30, current_block['padding'], key=f"padding_{selected_block}")
    with col_style2:
        font_size = st.slider("文字サイズ (px)", 10, 24, current_block['font_size'], key=f"font_size_{selected_block}")

    # 設定を保存
    st.session_state.blocks[selected_block].update({
        'label': label,
        'color': color,
        'border_style': border_style,
        'border_width': border_width,
        'padding': padding,
        'font_size': font_size,
        'text_color': text_color,
        'category': category
    })

    # ブロックを削除
    if len(st.session_state.blocks) > 1:
        if st.button(f"🗑️ '{label}' ブロックを削除", type="secondary"):
            del st.session_state.blocks[selected_block]
            st.session_state.selected_block = list(st.session_state.blocks.keys())[0]
            st.rerun()

with col_right:
    st.header("👁️ プレビュー")

    # 単一ブロックのプレビュー
    st.subheader(f"現在のブロック: {current_block['label']}")

    def render_block(block_data, block_label=None):
        """ブロックをHTMLでレンダリング"""
        if block_label is None:
            block_label = block_data['label']

        html = f"""
        <div style="
            background-color: {block_data['color']};
            color: {block_data['text_color']};
            border: {block_data['border_width']}px {block_data['border_style']} {block_data['color']};
            border-radius: 8px;
            padding: {block_data['padding']}px;
            font-size: {block_data['font_size']}px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            display: inline-block;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            {block_label}
        </div>
        """
        return html

    st.markdown(render_block(current_block), unsafe_allow_html=True)

    st.markdown("---")

    # すべてのブロックのプレビュー
    st.subheader("📚 すべてのブロック")

    # カテゴリごとにグループ化
    categories = {}
    for block_id, block_data in st.session_state.blocks.items():
        cat = block_data.get('category', 'その他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((block_id, block_data))

    for category_name, blocks in categories.items():
        st.markdown(f"**{category_name}**")
        blocks_html = ""
        for block_id, block_data in blocks:
            blocks_html += render_block(block_data)
        st.markdown(blocks_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # サンプルプログラムのプレビュー
    st.subheader("💻 サンプルプログラム")

    sample_program_html = """
    <div style="background-color: #2C3E50; padding: 20px; border-radius: 10px; margin: 10px 0;">
    """

    # サンプルプログラムの構造
    sample_blocks = ['loop', 'move_forward', 'if', 'turn_right', 'turn_left']
    indent_level = 0

    for i, block_id in enumerate(sample_blocks):
        if block_id in st.session_state.blocks:
            block_data = st.session_state.blocks[block_id]

            # インデント処理
            if block_id in ['if', 'loop', 'while']:
                margin_left = indent_level * 30
                indent_level += 1
            else:
                margin_left = indent_level * 30

            sample_program_html += f"""
            <div style="margin-left: {margin_left}px; margin-top: 5px;">
                {render_block(block_data)}
            </div>
            """

    sample_program_html += "</div>"
    st.markdown(sample_program_html, unsafe_allow_html=True)

# エクスポート/インポート機能
st.markdown("---")
st.header("💾 設定の保存・読み込み")

col_export, col_import = st.columns(2)

with col_export:
    st.subheader("エクスポート")
    config_json = json.dumps(st.session_state.blocks, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 設定をJSONファイルでダウンロード",
        data=config_json,
        file_name="block_config.json",
        mime="application/json"
    )

    with st.expander("JSON設定を表示"):
        st.code(config_json, language="json")

with col_import:
    st.subheader("インポート")
    uploaded_file = st.file_uploader("設定ファイルをアップロード", type=['json'])

    if uploaded_file is not None:
        try:
            imported_config = json.load(uploaded_file)
            if st.button("📤 設定を適用"):
                st.session_state.blocks = imported_config
                st.success("設定を読み込みました！")
                st.rerun()
        except Exception as e:
            st.error(f"エラー: {str(e)}")

# フッター
st.markdown("---")
st.markdown("**ヒント**: 左側でブロックの設定を変更すると、右側のプレビューがリアルタイムで更新されます。")
