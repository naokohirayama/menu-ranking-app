import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets 認証設定 ---
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open("menu_results").sheet1  # ← スプレッドシート名を合わせてください

# --- メニュー定義 ---
menus = [
    {"id": "[1]", "main": "チーズバーガー", "side": "ポテト", "drink": "ホットコーヒー", "price": "570円"},
    {"id": "[2]", "main": "チーズバーガー", "side": "コールスロー", "drink": "コーラ", "price": "680円"},
    {"id": "[3]", "main": "チーズバーガー", "side": "グリーンサラダ", "drink": "オレンジジュース", "price": "620円"},
    {"id": "[4]", "main": "フィッシュバーガー", "side": "ポテト", "drink": "コーラ", "price": "620円"},
    {"id": "[5]", "main": "フィッシュバーガー", "side": "コールスロー", "drink": "オレンジジュース", "price": "570円"},
    {"id": "[6]", "main": "フィッシュバーガー", "side": "グリーンサラダ", "drink": "ホットコーヒー", "price": "680円"},
    {"id": "[7]", "main": "ホットサンド", "side": "ポテト", "drink": "オレンジジュース", "price": "680円"},
    {"id": "[8]", "main": "ホットサンド", "side": "コールスロー", "drink": "ホットコーヒー", "price": "620円"},
    {"id": "[9]", "main": "ホットサンド", "side": "グリーンサラダ", "drink": "コーラ", "price": "570円"}
]

# --- UI表示 ---
st.title("🍔 メニューランキングアンケート")
name = st.text_input("📝 あなたのお名前を入力してください")

st.write("⬇️ 各メニューに対して 1～9 位の順位を割り当ててください。順位は1度ずつしか使えません。")

columns = st.columns(3)
rankings = {}

rank_options = [str(i) for i in range(1, 10)]

for i, menu in enumerate(menus):
    with columns[i % 3]:
        st.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 10px; margin: 5px; background-color: #f9f9f9;">
                <strong>{menu['id']}</strong><br>
                🍔 {menu['main']}<br>
                🥗 {menu['side']}<br>
                🥤 {menu['drink']}<br>
                💰 {menu['price']}
            </div>
            """, unsafe_allow_html=True
        )
        selected_rank = st.selectbox(f"{menu['id']} の順位", ["--"] + rank_options, key=f"rank_{i}")
        if selected_rank != "--":
            rankings[menu["id"]] = selected_rank

# --- 送信処理 ---
if st.button("📤 送信"):
    if not name:
        st.error("⚠️ 名前を入力してください。")
    elif len(rankings) != 9:
        st.error("⚠️ すべてのメニューに順位を付けてください（重複なし）。")
    elif len(set(rankings.values())) != 9:
        st.error("⚠️ 同じ順位を複数のメニューに割り当てないでください。")
    else:
        # ランキング順にソートして送信
        sorted_menus = sorted(rankings.items(), key=lambda x: int(x[1]))
        menu_ids = [m[0] for m in sorted_menus]
        sheet.append_row([name] + menu_ids)
        st.success("✅ 送信しました。ありがとうございました！")


