import streamlit as st

Overview = st.Page("Overview.py", title="Overview",icon="🏠")

Student_Analysis = st.Page("Student_Analysis.py", title="Student Analysis",icon="📊")

Subjects_Analysis = st.Page("Subject_Analysis.py", title="Subjects Analysis",icon="📚")

Test_Comparison = st.Page("Test_Comparison.py", title="Test Comparison",icon="🧪")

Rankings = st.Page("Rankings.py", title="Rankings",icon="🏆"  )


pg = st.navigation([Overview,Student_Analysis, Subjects_Analysis, Test_Comparison, Rankings],)

pg.run()