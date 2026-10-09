import streamlit as st
import dataLoder as dl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = dl.DataLoader()


st.title("🏆 Rankings")
st.markdown("---")

st.sidebar.header("🔧 Options")
    
ranking_type = st.sidebar.radio(
    "Ranking Type",
    ["Overall Rankings", "Branch-wise Rankings", "Subject Toppers"]
)

semester=st.sidebar.selectbox("semester", ["sem-1","sem-2"])
if ranking_type == "Overall Rankings":
        st.header("🏆 Overall Top Performers")

        top_performers = data.data[semester][:10]
        
        st.subheader("🥇🥈🥉 Top 3")
        col1, col2, col3 = st.columns(3)
            
        medals = ['🥇', '🥈', '🥉']
        medal_colors = ['#FFD700', '#C0C0C0', '#CD7F32']
         
        for i, (col, medal, color) in enumerate(zip([col1, col2, col3], medals, medal_colors)):
            with col:
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}40, {color}20); 
                            padding: 1.5rem; border-radius: 15px; text-align: center;
                            border: 2px solid {color};">
                    <h1 style="margin: 0;">{medal}</h1>
                    <h3 style="margin: 0.5rem 0;">{top_performers[i][6]}</h3>
                    <p><b>Total:</b> {data.TotalMark(semester)[i]:.2f}</p>
                    <p><b>Branch:</b> {top_performers[i][2]}</p>
                    <p><b>Enrollment:</b> {top_performers[i][4]}</p>
                </div>
                """, unsafe_allow_html=True)

        leaderboard_data =  pd.DataFrame(top_performers)

        leaderboard_data = leaderboard_data.drop(columns=[1,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

        leaderboard_data["Total Marks"]=data.TotalMark(semester)[0:10]

        leaderboard_data = leaderboard_data.rename(columns={
            6: "Name",
            4: "Enrollment",
            2: "Branch",
            5: "Section",
            3: "Roll No",
            0 :"Rank"
        })

        st.markdown("---")
        st.subheader("📋 Top 10 Students")
        leaderboard_data=leaderboard_data[["Rank","Name","Enrollment","Branch","Section","Roll No","Total Marks"]]
        st.dataframe(
                leaderboard_data,
                column_config={
                    "Rank": st.column_config.TextColumn("🏅 Rank"),
                    "Name": st.column_config.TextColumn("👤 Student Name", width="large"),
                    "Enrollment": st.column_config.TextColumn("🆔 Enrollment ID", width="medium"),
                    "Branch": st.column_config.TextColumn("🏛️ Branch"),
                    "Section": st.column_config.TextColumn("📑 Section"),
                    "Marks": st.column_config.NumberColumn("📊 Marks",  format="%.1f"),
                },
                hide_index=True,
                width='stretch',
                height=400
            )
        st.markdown("---")

        st.subheader("📊 Top Performers Visualization")

        names = [top_performers[i][6][:15] + '...' if len(str(top_performers[i][6])) > 15 else top_performers[i][6] for i in range(10)]
        marks = [data.TotalMark(semester)[i] for i in range(10)]

        fig, ax = plt.subplots(figsize=(14, 6))

        colors = plt.cm.cool(np.linspace(0.3, 0.9, len(names)))
        bars = ax.bar(names, marks, color=colors, edgecolor='white', linewidth=0.7)

        ax.set_xlabel('Student Name', color='white', fontsize=12)
        ax.set_ylabel('Total Marks', color='white', fontsize=12)
        ax.set_title('Top Performers by Total Marks', color='white', fontsize=14, fontweight='bold')

        ax.set_facecolor('#1e1e2e')
        fig.set_facecolor('#0e1117')
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(color='white')

        for bar, val in zip(bars, marks):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=10)

        st.pyplot(fig)

elif ranking_type == "Branch-wise Rankings":
        st.header("🏫 Branch-wise Top Performers")

        branchs = data.uniqueCategory(semester, data.data[semester][:,2])[0]
        selected_branch = st.selectbox("Select Branch", branchs)

        indexes = data.filterByBranchIndex(semester, selected_branch)
        totalMarks = data.TotalMark(semester)
        sortedIndexes = indexes[np.argsort(totalMarks[indexes])[::-1]]

        top_n = min(10, len(sortedIndexes))
        top_performers = data.data[semester][sortedIndexes[:top_n]]
        topMarks = totalMarks[sortedIndexes[:top_n]]

        st.subheader("🥇🥈🥉 Top 3")
        col1, col2, col3 = st.columns(3)

        medals = ['🥇', '🥈', '🥉']
        medal_colors = ['#FFD700', '#C0C0C0', '#CD7F32']

        for i, (col, medal, color) in enumerate(zip([col1, col2, col3], medals, medal_colors)):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}40, {color}20); 
                            padding: 1.5rem; border-radius: 15px; text-align: center;
                            border: 2px solid {color};">
                    <h1 style="margin: 0;">{medal}</h1>
                    <h3 style="margin: 0.5rem 0;">{top_performers[i][6]}</h3>
                    <p><b>Total:</b> {topMarks[i]:.2f}</p>
                    <p><b>Division:</b> {top_performers[i][1]}</p>
                </div>
                """, unsafe_allow_html=True)

        leaderboard_data = pd.DataFrame(top_performers)
        leaderboard_data = leaderboard_data.drop(columns=[1,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
        leaderboard_data["Total Marks"] = topMarks
        leaderboard_data[0] = range(1, top_n + 1)

        leaderboard_data = leaderboard_data.rename(columns={
            6: "Name",
            4: "Enrollment",
            2: "Branch",
            5: "Section",
            3: "Roll No",
            0: "Rank"
        })

        st.markdown("---")
        st.subheader(f"📋 Top {top_n} in {selected_branch}")
        leaderboard_data=leaderboard_data[["Rank","Name","Enrollment","Branch","Section","Roll No","Total Marks"]]
        st.dataframe(
                leaderboard_data,
                column_config={
                    "Rank": st.column_config.TextColumn("🏅 Rank"),
                    "Name": st.column_config.TextColumn("👤 Student Name", width="large"),
                    "Enrollment": st.column_config.TextColumn("🆔 Enrollment ID", width="medium"),
                    "Branch": st.column_config.TextColumn("🏛️ Branch"),
                    "Section": st.column_config.TextColumn("📑 Section"),
                },
                hide_index=True,
                width='stretch',
                height=400
            )
        st.markdown("---")

        st.subheader("📊 Top Performers Visualization")

        names = [top_performers[i][6][:15] + '...' if len(str(top_performers[i][6])) > 15 else top_performers[i][6] for i in range(top_n)]
        marks = list(topMarks[:top_n])

        fig, ax = plt.subplots(figsize=(14, 6))

        colors = plt.cm.cool(np.linspace(0.3, 0.9, len(names)))
        bars = ax.bar(names, marks, color=colors, edgecolor='white', linewidth=0.7)

        ax.set_xlabel('Student Name', color='white', fontsize=12)
        ax.set_ylabel('Total Marks', color='white', fontsize=12)
        ax.set_title(f'Top Performers in {selected_branch}', color='white', fontsize=14, fontweight='bold')

        ax.set_facecolor('#1e1e2e')
        fig.set_facecolor('#0e1117')
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(color='white')

        for bar, val in zip(bars, marks):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=10)

        st.pyplot(fig)

elif ranking_type == "Subject Toppers":
        st.header("📚 Subject Toppers")

        selected_subject = st.selectbox("Select Subject", data.subjects[semester])

        subjectMarks = data.TotalMarksBysub[semester][selected_subject].astype('f')
        sortedIndexes = np.argsort(subjectMarks)[::-1]

        top_n = min(10, len(sortedIndexes))
        top_performers = data.data[semester][sortedIndexes[:top_n]]
        topMarks = subjectMarks[sortedIndexes[:top_n]]

        st.subheader("🥇🥈🥉 Top 3")
        col1, col2, col3 = st.columns(3)

        medals = ['🥇', '🥈', '🥉']
        medal_colors = ['#FFD700', '#C0C0C0', '#CD7F32']

        for i, (col, medal, color) in enumerate(zip([col1, col2, col3], medals, medal_colors)):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}40, {color}20); 
                            padding: 1.5rem; border-radius: 15px; text-align: center;
                            border: 2px solid {color};">
                    <h1 style="margin: 0;">{medal}</h1>
                    <h3 style="margin: 0.5rem 0;">{top_performers[i][6]}</h3>
                    <p><b>Score:</b> {topMarks[i]:.2f}</p>
                    <p><b>Branch:</b> {top_performers[i][2]}</p>
                </div>
                """, unsafe_allow_html=True)

        leaderboard_data = pd.DataFrame(top_performers)
        leaderboard_data = leaderboard_data.drop(columns=[1,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
        leaderboard_data["Score"] = topMarks
        leaderboard_data[0] = range(1, top_n + 1)

        leaderboard_data = leaderboard_data.rename(columns={
            6: "Name",
            4: "Enrollment",
            2: "Branch",
            5: "Section",
            3: "Roll No",
            0: "Rank"
        })

        st.markdown("---")
        st.subheader(f"📋 Top {top_n} in {selected_subject}")
        leaderboard_data=leaderboard_data[["Rank","Name","Enrollment","Branch","Section","Roll No","Score"]]
        st.dataframe(
                leaderboard_data,
                column_config={
                    "Rank": st.column_config.TextColumn("🏅 Rank"),
                    "Name": st.column_config.TextColumn("👤 Student Name", width="large"),
                    "Enrollment": st.column_config.TextColumn("🆔 Enrollment ID", width="medium"),
                    "Branch": st.column_config.TextColumn("🏛️ Branch"),
                    "Section": st.column_config.TextColumn("📑 Section"),
                },
                hide_index=True,
                width='stretch',
                height=400
            )
        st.markdown("---")

        st.subheader("📊 Top Performers Visualization")

        names = [top_performers[i][6][:15] + '...' if len(str(top_performers[i][6])) > 15 else top_performers[i][6] for i in range(top_n)]
        marks = list(topMarks[:top_n])

        fig, ax = plt.subplots(figsize=(14, 6))

        colors = plt.cm.cool(np.linspace(0.3, 0.9, len(names)))
        bars = ax.bar(names, marks, color=colors, edgecolor='white', linewidth=0.7)

        ax.set_xlabel('Student Name', color='white', fontsize=12)
        ax.set_ylabel('Marks', color='white', fontsize=12)
        ax.set_title(f'Top Performers in {selected_subject}', color='white', fontsize=14, fontweight='bold')

        ax.set_facecolor('#1e1e2e')
        fig.set_facecolor('#0e1117')
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(color='white')

        for bar, val in zip(bars, marks):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=10)

        st.pyplot(fig)

        st.markdown("---")
        st.subheader("🏅 All Subject Toppers")

        subjects = data.subjects[semester]
        table_data = []
        for subj in subjects:
            subMarks = data.TotalMarksBysub[semester][subj].astype('f')
            topInds = np.argsort(subMarks)[::-1][:3]

            table_data.append({
                "Subject": subj,
                "🥇 1st": f"{data.data[semester][topInds[0]][6]} ({subMarks[topInds[0]]:.1f})",
                "🥈 2nd": f"{data.data[semester][topInds[1]][6]} ({subMarks[topInds[1]]:.1f})",
                "🥉 3rd": f"{data.data[semester][topInds[2]][6]} ({subMarks[topInds[2]]:.1f})",
            })

        st.dataframe(
                table_data,
                column_config={
                    "Subject": st.column_config.TextColumn("📚 Subject"),
                    "🥇 1st": st.column_config.TextColumn("🥇 1st", width="large"),
                    "🥈 2nd": st.column_config.TextColumn("🥈 2nd", width="large"),
                    "🥉 3rd": st.column_config.TextColumn("🥉 3rd", width="large"),
                },
                hide_index=True,
                width='stretch'
            )