import streamlit as st
import dataLoder as dl
import matplotlib.pyplot as plt
import numpy as np

semester=st.sidebar.selectbox("semester", ["sem-1","sem-2"])


data = dl.DataLoader()

st.title("📈 Overview Dashboard")
st.markdown("---")

st.header("📊 Overall Statistics")

col1, col2, col3 = st.columns(3)





with col1:
    total_students = data.data[semester].shape[0]
    st.metric("Total Students", total_students)
with col2:
    branches = data.uniqueCategory(semester, data.data[semester][:,2])[0]
    st.metric("Total Branches", len(branches))
with col3:
    batch = data.uniqueCategory(semester, data.data[semester][:,5])[0]
    st.metric("Total Batch", len(batch))

branchs , counts = data.uniqueCategory(semester, data.data[semester][:,2])

plt.figure(figsize=(10, 6))
plt.gcf().set_facecolor("#0e1117")

# Colors
colors = plt.cm.viridis(np.linspace(0.8, 0.2, len(branchs)))

# Bar plot
plt.bar(branchs, counts, color=colors, edgecolor="white")

# Labels and title
plt.title("Student Count by Branch", color="white", fontsize=14, fontweight="bold")
plt.xlabel("Branch", color="white", fontsize=12)
plt.ylabel("Number of Students", color="white", fontsize=12)

# Axes styling
plt.gca().set_facecolor("#1e1e2e")
plt.xticks(rotation=45, ha="right", color="white")
plt.yticks(color="white")



st.pyplot(plt.gcf())

st.markdown("---")

st.header("📊 Average Performance by Branch")

avgMarkByBranch = []

for i in branchs:
    
    indexes = data.filterByBranchIndex(semester, i)
    avgMark = data.averageMark(indexes, semester)
    avgMarkByBranch.append(avgMark)

BranchAndAvgMark = list(zip(branchs, avgMarkByBranch))
BranchAndAvgMark = sorted(BranchAndAvgMark, key=lambda x: x[1])
branchs, avgMarkByBranch = zip(*BranchAndAvgMark)


plt.figure(figsize=(10, 6))
plt.gcf().set_facecolor("#0e1117")

# Colors
colors = plt.cm.RdYlGn(np.linspace(1,0.1 , len(branchs)))

# Bar plot
plt.barh(branchs, avgMarkByBranch, color=colors, edgecolor="white")



# Labels and title
plt.title("Average Performance by Branch", color="white", fontsize=14, fontweight="bold")
plt.xlabel("Average Total Marks", color="white", fontsize=12)
plt.ylabel("Branch", color="white", fontsize=12)

# Axes styling
plt.gca().set_facecolor("#1e1e2e")
plt.xticks(rotation=0, ha="right", color="white")
plt.yticks(color="white")



st.pyplot(plt.gcf())

st.markdown("---")

st.header("🎓 Distribution of Students by Marks")

sublist = data.subjects[semester][:]
subjects = st.multiselect("Select Subjects for Marks Distribution", sublist, default=sublist)   


chart_data= data.Mark_distribution(data.TotalMarksBysub[semester],subjects)


fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f172a')
ax.set_facecolor('#1e293b')

# Plot lines
colors = ['#4ade80', '#22d3ee', '#3b82f6', '#8b5cf6', '#ec4899']
for idx, subject in enumerate(subjects):
    ax.plot(chart_data["Marks"], chart_data[subject], 
            label=subject, linewidth=2, color=colors[idx % len(colors)])

# Add vertical lines for mean and SD
for subject in subjects:
    marks = data.TotalMarksBysub[semester][subject]
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

table_data = []

for subject in subjects:
    marks = data.TotalMarksBysub[semester][subject]  # Adjust based on your data structure
    
    table_data.append({
        "Subject": subject,
        "Average": f"{np.mean(marks):.2f}",
        "Highest": f"{np.max(marks):.2f}",
        "Lowest": f"{np.min(marks):.2f}",
        "Std Dev": f"{np.std(marks):.2f}"
    })



# Display as table
st.dataframe(
    table_data,
    width='stretch',
    hide_index=True
)