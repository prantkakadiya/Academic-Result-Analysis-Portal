import streamlit as st
import dataLoder as dl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = dl.DataLoader()

st.title("👨‍🎓 Student Analysis")



semester=st.sidebar.selectbox("semester", ["sem-1","sem-2"])
st.sidebar.header("🔍 Search Options")
    
search_method = st.sidebar.radio(
    "Search by",
    ["Name", "Enrollment Number"]
)

if search_method == "Name":
    all_names = sorted([i for i in data.Names[semester]] )
    name = st.sidebar.selectbox("Select Student", all_names)
    selected_student = data.SearchByName(semester,name)

elif search_method == "Enrollment Number":
    all_enrollments = sorted([i for i in data.EnrNums[semester]])
    Enroll = st.sidebar.selectbox("Select Enrollment", all_enrollments)
    selected_student = data.SearchByEnrNum(semester,Enroll)

st.markdown("---")
st.header(f"📋 {selected_student[6]}")

col1, col2, col3 = st.columns(3)
        
with col1:

    st.markdown("### 📌 Basic Information")
    st.info(f"""
    **Enrollment:** {selected_student[4]}  
    **Roll No:** {selected_student[3]}  
    **Branch:** {selected_student[2]}  
    **Division:** {selected_student[1]}  
    **Batch:** {selected_student[5]}
    """)

with col2:
    st.markdown("### 📊 Performance Summary")
    TotalMarks = data.TotalMark(semester)

    if search_method == "Name":
        TotalMark = TotalMarks[data.Names[semester][name]]
        st.success(f"""
        **Total Marks:** {TotalMark}  
        **Average:** {TotalMark/4}  
        **Rank:** {selected_student[0]}
        """)
        pass
    elif search_method == "Enrollment Number":
        TotalMark = TotalMarks[data.EnrNums[semester][Enroll]]
        st.success(f"""
        **Total Marks:** {TotalMark}  
        **Average:** {TotalMark/4}  
        **Rank:** {selected_student[0]}
        """)
        pass

with col3:
    st.markdown("### 🎓 Additional Info")
    st.warning(f"""
    **Faculty Code:** {selected_student[7]}  
    **Language:** {selected_student[28]}
    """)

st.markdown("---")

st.header("📚 Subject-wise Performance")

if search_method == "Name":
    studentInd = data.Names[semester][name]
elif search_method == "Enrollment Number":
    studentInd = data.EnrNums[semester][Enroll]

subjects = data.subjects[semester]

cols = st.columns(len(subjects))


studen_Data = data.DataSplitBySubject[semester]

for i, subject in enumerate(subjects):
    with cols[i]:
        totalMark = data.TotalMarksBysub[semester][subject][studentInd]
        st.subheader(subject)
        st.metric("Total", f"{float(totalMark):.1f}")
        for Test_n in ["Test-1", "Test-2", "Test-3", "Test-4"]:

            mark = data.DataSplitBySubject[semester][subject][Test_n][studentInd]
            studen_Data[subject][Test_n] = mark
            st.caption(f"{Test_n}: {mark:.1f}")
            
st.dataframe(studen_Data)

fd = pd.DataFrame(studen_Data)

d = fd.to_csv().encode("utf-8")


st.download_button("download ",d,"studen_Data.csv")

st.markdown("---")

st.header("🆚 Comparison with average or other students")

compareMethod = st.radio("Search by", ["Name", "Enrollment Number"], key="compare_method", horizontal=True)

if compareMethod == "Name":
    compareOptions = ["Average"] + sorted([i for i in data.Names[semester]])
    compareWith = st.selectbox("Compare with", compareOptions)
elif compareMethod == "Enrollment Number":
    compareOptions = ["Average"] + sorted([i for i in data.EnrNums[semester]])
    compareWith = st.selectbox("Compare with", compareOptions)

studentMarks = []
compareMarks = []

for subject in subjects:
    studentMarks.append(float(data.TotalMarksBysub[semester][subject][studentInd]))

    if compareWith == "Average":
        compareMarks.append(float(np.mean(data.TotalMarksBysub[semester][subject].astype('f'))))
    else:
        if compareMethod == "Name":
            compareInd = data.Names[semester][compareWith]
        elif compareMethod == "Enrollment Number":
            compareInd = data.EnrNums[semester][compareWith]
        compareMarks.append(float(data.TotalMarksBysub[semester][subject][compareInd]))

fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))

angles = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()

studentMarks_plot = studentMarks + [studentMarks[0]]
compareMarks_plot = compareMarks + [compareMarks[0]]
angles += angles[:1]

ax.plot(angles, studentMarks_plot, 'o-', linewidth=2, color='#667eea', label=selected_student[6])
ax.fill(angles, studentMarks_plot, alpha=0.25, color='#667eea')

ax.plot(angles, compareMarks_plot, 'o-', linewidth=2, color='#FFD700', label=compareWith)
ax.fill(angles, compareMarks_plot, alpha=0.15, color='#FFD700')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(subjects, color='white', fontsize=10)
ax.set_yticklabels([])

ax.set_facecolor('#1e1e2e')
fig.set_facecolor('#0e1117')
ax.spines['polar'].set_color('white')
ax.tick_params(colors='white')
ax.legend(facecolor='#1e293b', edgecolor='#334155', framealpha=0.9)

st.pyplot(fig)

st.markdown("---")

st.header("💡 Performance Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💪 Strengths")
    strengths = []
    for i, subject in enumerate(subjects):
        if studentMarks[i] > compareMarks[i]:
            diff = studentMarks[i] - compareMarks[i]
            strengths.append((subject, studentMarks[i], diff))

    if strengths:
        for subject, mark, diff in sorted(strengths, key=lambda x: x[2], reverse=True):
            st.success(f"**{subject}**: {mark:.1f} (+{diff:.1f} above {compareWith})")
    else:
        st.info(f"Performance is below or at {compareWith} in all subjects")

with col2:
    st.markdown("### 📚 Areas for Improvement")
    improvements = []
    for i, subject in enumerate(subjects):
        if studentMarks[i] < compareMarks[i]:
            diff = compareMarks[i] - studentMarks[i]
            improvements.append((subject, studentMarks[i], diff))

    if improvements:
        for subject, mark, diff in sorted(improvements, key=lambda x: x[2], reverse=True):
            st.warning(f"**{subject}**: {mark:.1f} ({diff:.1f} below {compareWith})")
    else:
        st.info(f"Performance is above {compareWith} in all subjects!")
