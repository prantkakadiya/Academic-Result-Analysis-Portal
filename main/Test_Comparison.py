import streamlit as st
import dataLoder as dl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = dl.DataLoader()

st.title("🧪 Test Comparison")
st.markdown("---")

semester=st.sidebar.selectbox("semester", ["sem-1","sem-2"])

subjects = data.subjects[semester]
tests = ["Test-1", "Test-2", "Test-3", "Test-4"]

# ============================================================
# 1. Test Performance Trend
# ============================================================

st.header("📈 Test Performance Trend")

sublist = ["Overall"] + subjects[:]
selectedSubs = st.multiselect("Select Subjects", sublist, default=sublist)

chart_data = {}
chart_data["Test"] = tests

for selected in selectedSubs:
    avgMarks = []
    if selected == "Overall":
        for Test_n in tests:
            total = np.zeros(data.data[semester].shape[0])
            for sub in subjects:
                total = total + data.DataSplitBySubject[semester][sub][Test_n]
            avgMarks.append(np.mean(total) / len(subjects))
    else:
        for Test_n in tests:
            marks = data.DataSplitBySubject[semester][selected][Test_n]
            avgMarks.append(np.mean(marks))
    chart_data[selected] = avgMarks

chartDf = pd.DataFrame(chart_data)
chartDf = chartDf.set_index("Test")

st.line_chart(chartDf)

st.markdown("---")

# ============================================================
# 6. Head-to-Head Test Comparison
# ============================================================

st.header("🆚 Head-to-Head Test Comparison")

h2hSub = st.selectbox("Select Subject", ["Overall"] + subjects)

col1, col2 = st.columns(2)
with col1:
    testX = st.selectbox("X-Axis Test", tests, index=0)
with col2:
    testY = st.selectbox("Y-Axis Test", tests, index=3)

if h2hSub == "Overall":
    xMarks = np.zeros(data.data[semester].shape[0])
    yMarks = np.zeros(data.data[semester].shape[0])
    for sub in subjects:
        xMarks = xMarks + data.DataSplitBySubject[semester][sub][testX]
        yMarks = yMarks + data.DataSplitBySubject[semester][sub][testY]
else:
    xMarks = data.DataSplitBySubject[semester][h2hSub][testX]
    yMarks = data.DataSplitBySubject[semester][h2hSub][testY]

fig, ax = plt.subplots(figsize=(10, 8))
fig.set_facecolor('#0e1117')
ax.set_facecolor('#1e1e2e')

ax.scatter(xMarks, yMarks, alpha=0.5, color='#667eea', edgecolor='white', linewidth=0.5, s=50)

maxMark = max(np.max(xMarks), np.max(yMarks)) + 2
ax.plot([0, maxMark], [0, maxMark], '--', color='#ef4444', linewidth=1.5, alpha=0.7, label='Equal Line')

ax.set_xlabel(f'{testX} Marks', color='white', fontsize=12)
ax.set_ylabel(f'{testY} Marks', color='white', fontsize=12)
ax.set_title(f'{h2hSub}: {testX} vs {testY}', color='white', fontsize=14, fontweight='bold')
ax.legend(facecolor='#1e293b', edgecolor='#334155', framealpha=0.9)
plt.xticks(color='white')
plt.yticks(color='white')

st.pyplot(fig)

above = np.sum(yMarks > xMarks)
below = np.sum(yMarks < xMarks)
equal = np.sum(yMarks == xMarks)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"Improved ({testX} → {testY})", above)
with col2:
    st.metric(f"Declined ({testX} → {testY})", below)
with col3:
    st.metric("Same Score", equal)