import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ========================
# 📊 圖表字型設定
# ========================
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# ========================
# 🎨 網頁設定
# ========================
st.set_page_config(
    page_title="段考分析系統",
    page_icon="📚",
    layout="wide"
)

st.title("📚 段考分析機器人")
st.write("輸入你的成績與PR值，系統會自動分析！")

# ========================
# 👤 使用者名稱
# ========================
name = st.text_input("請輸入你的名字")

if name:

    st.success(f"你好，{name}！")

    scores = {}
    prs = {}
    weights = {}

    # ========================
    # 📖 主科
    # ========================
    st.header("📖 主科成績")

    col1, col2, col3 = st.columns(3)

    with col1:
        scores["國文"] = st.number_input("國文成績", 0.0, 100.0, 0.0)
        prs["國文"] = st.number_input("國文PR", 0.0, 100.0, 0.0)

    with col2:
        scores["英文"] = st.number_input("英文成績", 0.0, 100.0, 0.0)
        prs["英文"] = st.number_input("英文PR", 0.0, 100.0, 0.0)

    with col3:
        scores["數學"] = st.number_input("數學成績", 0.0, 100.0, 0.0)
        prs["數學"] = st.number_input("數學PR", 0.0, 100.0, 0.0)

    weights["國文"] = 4
    weights["英文"] = 4
    weights["數學"] = 4

    # ========================
    # 🧪 模式
    # ========================
    st.header("🧪 自然組選擇")

    mode = st.selectbox("請選擇模式", ["化學+生物", "物理+芒果"])

    if mode == "化學+生物":
        subjects = ["化學", "生物"]
    else:
        subjects = ["物理", "芒果"]

    st.header("🔬 選修")

    cols = st.columns(2)

    for i, sub in enumerate(subjects):
        with cols[i]:
            scores[sub] = st.number_input(f"{sub}成績", 0.0, 100.0, 0.0)
            prs[sub] = st.number_input(f"{sub}PR", 0.0, 100.0, 0.0)
        weights[sub] = 2

    # ========================
    # 🌍 社會
    # ========================
    st.header("🌍 社會科")

    social_cols = st.columns(3)

    for i, sub in enumerate(["歷史", "地理", "公民"]):
        with social_cols[i]:
            scores[sub] = st.number_input(f"{sub}成績", 0.0, 100.0, 0.0)
            prs[sub] = st.number_input(f"{sub}PR", 0.0, 100.0, 0.0)
        weights[sub] = 2

    # ========================
    # 📈 PR模式
    # ========================
    st.header("📈 校排PR")

    pr_mode = st.radio("PR輸入方式", ["手動輸入", "自動計算"])

    if pr_mode == "手動輸入":
        pr = st.number_input("請輸入你的PR值", 0.0, 100.0, 50.0)
    else:
        total_students = st.number_input("全年級人數", 1, 10000, 100)
        rank = st.number_input("你的名次", 1, int(total_students), 1)
        pr = (1 - (rank - 1) / total_students) * 100

    # ========================
    # 📌 PR開關
    # ========================
    use_pr = st.checkbox("📊 是否啟用PR分析", value=True)

    # ========================
    # 🚀 開始分析
    # ========================
    if st.button("🚀 開始分析"):

        total = sum(scores.values())
        average = total / len(scores)

        weighted_sum = 0
        total_weight = 0

        for sub in scores:
            weighted_sum += scores[sub] * weights[sub]
            total_weight += weights[sub]

        weighted_avg = weighted_sum / total_weight

        avg_pr = sum(prs.values()) / len(prs)

        max_subject = max(scores, key=scores.get)
        min_subject = min(scores, key=scores.get)

        # ========================
        # 📋 結果
        # ========================
        st.header("📋 分析結果")

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric("總成績", f"{total:.2f}")
        with colB:
            st.metric("平均成績", f"{average:.2f}")
        with colC:
            st.metric("加權平均", f"{weighted_avg:.2f}")

        st.success(f"🥇 最強科目：{max_subject}")
        st.error(f"🥶 最弱科目：{min_subject}")

        # ========================
        # 📈 PR分析
        # ========================
        if use_pr:
            st.header("📈 PR分析")
            st.info(f"你的PR：{pr:.1f}")
            st.info(f"平均PR：{avg_pr:.2f}")

            # 🔥 PR顏色提示（新增）
            if pr >= 90:
                st.success(f"🟢 PR {pr:.1f}（頂尖）")
            elif pr >= 70:
                st.warning(f"🟡 PR {pr:.1f}（中上）")
            else:
                st.error(f"🔴 PR {pr:.1f}（需加油）")

            # 📈 PR即時圖（新增）
            st.subheader("📈 PR即時圖")
            fig_live, ax_live = plt.subplots()
            ax_live.bar(["你的PR", "基準PR"], [pr, 50])
            ax_live.set_ylim(0, 100)
            st.pyplot(fig_live)

            # 🧠 班排預估（新增）
            st.subheader("🧠 班排預估")

            estimated_rank = round((1 - pr / 100) * 100)

            st.info(f"📊 約前 {estimated_rank}%")

            if pr >= 90:
                st.success("🔥 前10%")
            elif pr >= 75:
                st.info("👍 前25%")
            elif pr >= 50:
                st.warning("🙂 中段")
            else:
                st.error("📉 後段")

        # ========================
        # 🧠 建議
        # ========================
        if scores[min_subject] < 60:
            st.warning("👉 建議：先搶救不及格科目！")
        elif weighted_avg >= 85:
            st.success("👉 建議：你已經很強了🔥")
        elif weighted_avg >= 70:
            st.info("👉 建議：加強弱科會進步很多")
        else:
            st.error("👉 建議：需要全面提升📚")

        # ========================
        # 🎭 評價
        # ========================
        if weighted_avg < 60:
            st.error("拉完了💩")
        elif weighted_avg == 67:
            st.warning("6🤷7")
        elif weighted_avg < 70:
            st.warning("NPC🤦")
        elif weighted_avg < 80:
            st.info("人上人😀")
        elif weighted_avg < 90:
            st.success("頂級👍")
        else:
            st.success("夯📈")

        # ========================
        # 📊 排名
        # ========================
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        st.header("🏆 科目排名")

        rank_num = 1
        for subject, score in sorted_scores.items():
            st.write(f"{rank_num}. {subject}：{score}")
            rank_num += 1

        # ========================
        # 📊 成績圖
        # ========================
        st.header("📊 成績分析圖")

        fig1, ax1 = plt.subplots(figsize=(12, 6))

        colors = []
        for score in sorted_scores.values():
            if score < 60:
                colors.append("red")
            elif score >= 90:
                colors.append("gold")
            else:
                colors.append("skyblue")

        ax1.bar(sorted_scores.keys(), sorted_scores.values(), color=colors)

        ax1.axhline(average, linestyle='--')
        ax1.axhline(60, linestyle=':')

        st.pyplot(fig1)

        # ========================
        # 📊 PR圖（可關）
        # ========================
        if use_pr:
            st.header("📊 PR柱狀圖")

            fig2, ax2 = plt.subplots(figsize=(12, 6))
            ax2.bar(prs.keys(), prs.values(), color="orange")
            ax2.axhline(avg_pr, linestyle='--')
            ax2.set_ylim(0, 100)
            st.pyplot(fig2)

        st.success("✅ 分析完成！")