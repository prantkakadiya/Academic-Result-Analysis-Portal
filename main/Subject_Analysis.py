import streamlit as st
import dataLoder as dl
import matplotlib.pyplot as plt
import numpy as np

data = dl.DataLoader()

st.title("📚 Subject Analysis")
st.markdown("---")


semester=st.sidebar.selectbox("semester", ["sem-1","sem-2"])
sublist = data.subjects[semester][:]
subject = st.sidebar.selectbox("Select Subjects for Marks Distribution", sublist)   

marks = data.TotalMarksBysub[semester][subject] 

st.header(f"📊 {subject} Analysis")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Mean", f"{np.mean(marks):.2f}")
with col2:
    st.metric("🏆 Maximum", f"{np.max(marks):.2f}")
with col3:
    st.metric("📉 Minimum", f"{np.min(marks):.2f}" )
with col4:
    st.metric("📈 Std Dev", f"{np.std(marks):.2f}" )

st.markdown("---")

st.header("📋 Test-wise Statistics")

table_data = []
for Test_n in ["Test-1", "Test-2", "Test-3", "Test-4"]:
    testMarks = data.DataSplitBySubject[semester][subject][Test_n]
    table_data.append({
        "Test": Test_n,
        "Average": f"{np.mean(testMarks):.2f}",
        "Highest": f"{np.max(testMarks):.2f}",
        "Lowest": f"{np.min(testMarks):.2f}",
        "Std Dev": f"{np.std(testMarks):.2f}",
    })

st.dataframe(
    table_data,
    column_config={
        "Test": st.column_config.TextColumn("🧪 Test"),
        "Average": st.column_config.TextColumn("📊 Average"),
        "Highest": st.column_config.TextColumn("🏆 Highest"),
        "Lowest": st.column_config.TextColumn("📉 Lowest"),
        "Std Dev": st.column_config.TextColumn("📈 Std Dev"),
    },
    hide_index=True,
    width='stretch'
)

st.markdown("---")


marks_by_test={}



for m in data.DataSplitBySubject[semester][subject]:
    

    marks_by_test[m]=data.DataSplitBySubject[semester][subject][m]


st.subheader("📊 Score Distribution ")

tests = st.multiselect("Tests" ,["Test-1","Test-2","Test-3","Test-4"],default=["Test-1","Test-2","Test-3","Test-4"])

chart_data= data.Mark_distribution(marks_by_test,tests,end=25,step=0.5)


fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f172a')
ax.set_facecolor('#1e293b')

# Plot lines
colors = ['#4ade80', '#22d3ee', '#3b82f6', '#8b5cf6', '#ec4899']


for idx, subject in enumerate(tests):
    ax.plot(chart_data["Marks"], chart_data[subject], 
            label=subject, linewidth=2, color=colors[idx % len(colors)])

for test in tests:
    marks = marks_by_test[test]
    mean = np.mean(marks)
    std = np.std(marks)
    
    # Mean line
    ax.axvline(mean, color='#ef4444', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(mean, ax.get_ylim()[1] * 0.95, f'μ={mean:.1f}', 
            color='#ef4444', ha='center', fontsize=10)
    
    # Mean - SD line
    ax.axvline(mean - std, color='#fb923c', linestyle=':', linewidth=1.5, alpha=0.6)
    ax.text(mean - std, ax.get_ylim()[1] * 0.85, '-σ', 
            color='#fb923c', ha='center', fontsize=9)
    
    # Mean + SD line
    ax.axvline(mean + std, color='#fb923c', linestyle=':', linewidth=1.5, alpha=0.6)
    ax.text(mean + std, ax.get_ylim()[1] * 0.85, '+σ', 
            color='#fb923c', ha='center', fontsize=9)

ax.set_xlabel('Marks', fontsize=12, color='white')
ax.set_ylabel('Count', fontsize=12, color='white')
ax.set_title('Marks Distribution', fontsize=16, color='white', pad=20)
ax.grid(True, alpha=0.2, color='#334155')
ax.legend(facecolor='#1e293b', edgecolor='#334155', framealpha=0.9)

st.pyplot(fig)

