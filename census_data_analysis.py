import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(page_title="Census Data Analysis", layout="wide")

st.title("📊 Census Data Analysis Dashboard By Revanth Gutha")
st.write("Upload your Census CSV file and explore various insights interactively.")

# --- File uploader ---
uploaded_file = st.file_uploader("📂 Upload your census.csv file", type=["csv"])

# --- Initialize toggle state for all sections ---
sections = [
    "senior", "voters", "employable_females", "orphans", "pension",
    "gender_pci", "per_capita", "tax", "income_gender", "sex_ratio",
    "edu_employment", "edu_gender", "widow", "parent", "age_60",
    "employable_all", "non_citizens_work", "non_citizens_money",
    "doctorate", "citizens_no_employment"
]

for key in sections:
    if key not in st.session_state:
        st.session_state[key] = False


def toggle(section):
    st.session_state[section] = not st.session_state[section]


# --- Main App Logic ---
if uploaded_file is not None:
    census = pd.read_csv(uploaded_file)
    st.success("✅ Dataset loaded successfully!")
    st.dataframe(census.head())

    # Sidebar controls
    st.sidebar.header("⚙️ Settings")
    X = st.sidebar.number_input("Enter number of years (for projections)", min_value=1, max_value=50, value=5)

    st.divider()
    st.subheader("🔍 Click buttons to open or close sections:")

    # 1️⃣ Senior Citizens to be added in next X years
    if st.button("1️⃣ Senior Citizens to be added in next X years"):
        toggle("senior")
    if st.session_state.senior:
        senior_voters = census[(census['Age'] < 60) & ((census['Age'] + X) >= 60)]
        st.info(f"Number of Senior Citizens to be added in next {X} years: **{len(senior_voters)}**")

    # 2️⃣ Voters to be added in next X years
    if st.button("2️⃣ Voters to be added in next X years"):
        toggle("voters")
    if st.session_state.voters:
        new_voters = census[(census['Age'] < 18) & ((census['Age'] + X) >= 18)]
        st.info(f"Number of voters to be added in next {X} years: **{len(new_voters)}**")

    # 3️⃣ Employable Female Citizens (Widowed / Divorced)
    if st.button("3️⃣ Employable Female Citizens (Widowed / Divorced)"):
        toggle("employable_females")
    if st.session_state.employable_females:
        employable_females = census[
            (census['Gender'] == 'Female') &
            (census['Marital Status'].isin(['Widowed', 'Divorced'])) &
            (census['Weeks Worked'] != 0)
        ]
        st.success(f"Number of Employable Female Citizens: **{len(employable_females)}**")
        st.dataframe(employable_females[['Age', 'Gender', 'Marital Status', 'Weeks Worked']].head())

    # 4️⃣ Orphans for each category
    if st.button("4️⃣ Orphans for each category (Parents Present)"):
        toggle("orphans")
    if st.session_state.orphans:
        st.bar_chart(census['Parents Status'].value_counts())

    # 5️⃣ Pension Additions after X years
    if st.button("5️⃣ Pension Additions after X years"):
        toggle("pension")
    if st.session_state.pension:
        pension_add = census.loc[(census['Age'] < 60) & (census['Age'] + X >= 60)].shape[0]
        st.write(f"Pensioners to be added in {X} years: **{pension_add}**")

    # 6️⃣ Gender-wise Per Capita Income
    if st.button("6️⃣ Gender-wise Per Capita Income"):
        toggle("gender_pci")
    if st.session_state.gender_pci:
        gender_pci = census.groupby('Gender')['Income'].sum() / census['Gender'].value_counts()
        st.dataframe(gender_pci)

    # 7️⃣ Overall Per Capita Income
    if st.button("7️⃣ Overall Per Capita Income"):
        toggle("per_capita")
    if st.session_state.per_capita:
        st.write(f"Per Capita Income: **{census['Income'].mean():,.2f}**")

    # 8️⃣ Total Tax to be Collected (10%)
    if st.button("8️⃣ Total Tax to be Collected (10%)"):
        toggle("tax")
    if st.session_state.tax:
        tax_collected = (census['Income'] * 0.1).sum()
        st.write(f"Total Tax: **{tax_collected:,.2f}**")

    # 9️⃣ Gender-wise Total Income
    if st.button("9️⃣ Gender-wise Total Income"):
        toggle("income_gender")
    if st.session_state.income_gender:
        st.bar_chart(census.groupby('Gender')['Income'].sum())

    # 🔟 Sex Ratio (Male : Female)
    if st.button("🔟 Sex Ratio (Male : Female)"):
        toggle("sex_ratio")
    if st.session_state.sex_ratio:
        gender_count = census['Gender'].value_counts()
        if 'Male' in gender_count and 'Female' in gender_count:
            sex_ratio = gender_count['Male'] / gender_count['Female']
            st.write(f"Sex Ratio = **{sex_ratio:.2f} : 1**")
        else:
            st.warning("Not enough gender data to calculate ratio.")

    # 1️⃣1️⃣ Education vs Employment
    if st.button("1️⃣1️⃣ Education vs Employment"):
        toggle("edu_employment")
    if st.session_state.edu_employment:
        edu_employment = census.groupby(['Education', 'Weeks Worked']).size().reset_index(name='Count')
        st.dataframe(edu_employment)

    # 1️⃣2️⃣ Education & Gender-wise Count
    if st.button("1️⃣2️⃣ Education & Gender-wise Count"):
        toggle("edu_gender")
    if st.session_state.edu_gender:
        education_gender = census.groupby(['Education', 'Gender']).size().reset_index(name='Count')
        st.dataframe(education_gender)

    # 1️⃣3️⃣ Widow Female Count
    if st.button("1️⃣3️⃣ Widow Female Count"):
        toggle("widow")
    if st.session_state.widow:
        widow_female = census[(census['Gender'] == 'Female') & (census['Marital Status'] == 'Widowed')]
        st.write(f"No. of Widow Females: **{len(widow_female)}**")

    # 1️⃣4️⃣ Parents Status & Gender-wise Count
    if st.button("1️⃣4️⃣ Parents Status & Gender-wise Count"):
        toggle("parent")
    if st.session_state.parent:
        parent = census.groupby(['Parents Status', 'Gender']).size().reset_index(name='Count')
        st.dataframe(parent)

    # 1️⃣5️⃣ Citizens aged above 60 (by Citizenship)
    if st.button("1️⃣5️⃣ Citizens aged above 60 (by Citizenship)"):
        toggle("age_60")
    if st.session_state.age_60:
        age_60 = census[census['Age'] > 60].groupby('Citizen Ship').size().reset_index(name='Count')
        st.dataframe(age_60)

    # 1️⃣6️⃣ Employable Widows & Divorced (All Genders)
    if st.button("1️⃣6️⃣ Employable Widows & Divorced (All Genders)"):
        toggle("employable_all")
    if st.session_state.employable_all:
        employable = census[
            (census['Marital Status'].isin(['Widowed', 'Divorced'])) &
            (census['Weeks Worked'] != 0)
        ]
        st.write(f"Total Employable Widows/Divorced: **{len(employable)}**")

    # 1️⃣7️⃣ Non-citizens Working Percentage
    if st.button("1️⃣7️⃣ Non-citizens Working Percentage"):
        toggle("non_citizens_work")
    if st.session_state.non_citizens_work:
        non_citizens = census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
        percent_working = (non_citizens['Weeks Worked'] > 0).mean() * 100
        st.write(f"Working Non-citizens: **{percent_working:.2f}%**")

    # 1️⃣8️⃣ Money Generated by Non-citizens
    if st.button("1️⃣8️⃣ Money Generated by Non-citizens"):
        toggle("non_citizens_money")
    if st.session_state.non_citizens_money:
        non_citizens = census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
        money_generated = non_citizens['Income'].sum()
        st.write(f"Total Income of Non-citizens: **{money_generated:,.2f}**")

    # 1️⃣9️⃣ Doctorate Holders (already in dataset)
    if st.button("1️⃣9️⃣ Citizens above 23 with No Employment (Doctorate Holders)"):
        toggle("doctorate")
    if st.session_state.doctorate:
        filtered = census[
            (census['Age'] > 23) &
            (census['Weeks Worked'] == 0) &
            (census['Education'] == 'Doctoratedegree(PhDEdD)')
        ][['Age', 'Weeks Worked', 'Education']]
        st.dataframe(filtered)

    # 2️⃣0️⃣ Citizens above 23 having No Employment and Highest Education
    if st.button("2️⃣0️⃣ Citizens age above 23 having no employment and highest education (Doctorate Holders)"):
        toggle("citizens_no_employment")
    if st.session_state.citizens_no_employment:
        filtered = census[
            (census['Age'] > 23) &
            (census['Weeks Worked'] == 0) &
            (census['Education'] == 'Doctoratedegree(PhDEdD)')
        ][['Age', 'Weeks Worked', 'Education']]
        st.dataframe(filtered)
        st.success(f"Total Count: **{len(filtered)}**")

else:
    st.warning("👆 Please upload a CSV file to begin.")
