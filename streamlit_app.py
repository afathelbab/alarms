import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

# Function to load the mapping file from GitHub
def load_mapping_file():
    url = "https://github.com/afathelbab/alarms/blob/main/saa.csv"
    return pd.read_csv(url, on_bad_lines='skip')

# Function to handle file uploads and analysis
def analyze_data():
    if ph_files is not None:
        mapping_file = load_mapping_file()

        # Combine PH files into a single DataFrame
        combined_df = pd.concat([pd.read_csv(file) for file in ph_files])

        # Filter by priority and alarm state
        filtered_df = combined_df[
            (combined_df["Priority"].isin([1, 2, 3]))
            & (combined_df["AlarmState"] == "UNACK_ALM")
        ]

        # Extract compound from tagname
        filtered_df["Compound"] = filtered_df["TagName"].str.split(".").str[0]

        # Use mapping file to assign alarms to consoles
        stations = mapping_file[["Station"]].unique()
        df_compounds = {k: v for (k,v) in filtered_df.groupby('Compound')}
        mapping = mapping_file[['Station','Compound']]
        mapping_consoles = {k: v for (k,v) in mapping.groupby('Station')}
        for k,v in mapping_consoles.items():
            mapping_consoles[k] = v.drop(columns=['Station'])
            mapping_consoles[k] = v['Compound'].values.tolist()
            
        #Consoles Manpower
        owc_mp = {'OPC101': 2,
                  'OPC104': 2,
                  'OPC129': 2,
                  'OPC132': 1,
                  'OPC115': 2,
                  'OPC140': 1,
                  'OPC107': 1,
                  'OPC110': 1,
                  'OPC135': 1}
        
        combined_dict = {k:{u:t for (u,t) in df_compounds.items() if u in v} for (k,v) in mapping_consoles.items() if k in owc_mp}

      

        # Calculate KPIs for each console, including Tier 3.6
        results_df = {}
        for console in combined_dict.keys():
            owc_df = pd.concat(combined_dict[console].values(), ignore_index=True)
            owc_startdate = owc_df['EventStamp'].min()
            owc_enddate = owc_df['EventStamp'].max()
            owc_duration = owc_enddate - owc_startdate
            owc_durationinhours = round(owc_duration / np.timedelta64(1, 'h'))
            owc_sorted = pd.pivot_table(owc_df, values='EventStamp', index='TagName', aggfunc='count')
            owc_top10 = owc_sorted.sort_values(by=['EventStamp'], ascending=False).head(10)
            owc_top10count = owc_top10['EventStamp'].sum()
            owc_alarmscount = len(owc_df)
            owc_tier36 = owc_alarmscount/owc_durationinhours/owc_mp[console]
            owc_top10percent = round(owc_top10count*100/owc_alarmscount)

            results_df[console] = {'Start Date': [owc_startdate],
                                'End Date': [owc_enddate],
                                'Alarms Count': [owc_alarmscount],
                                'Tier 3.6': [owc_tier36],
                                'Top 10 Alarms Count': [owc_top10count],
                                'Top 10 Alarms Percent': [owc_top10percent],
                                'Top 10 Alarms': [owc_top10]}
            
        # Identify Top 10 alarms for each console with counts and percentages
        # ... (your code to create the desired output DataFrame)

        # Create Excel output with results
        create_excel_output(results_df)

# Function to create a new Excel file with results
def create_excel_output(results_df):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write results to the Excel sheet (adjust as needed based on your results_df structure)
    # Writing to Excel File
    # Gas Trains 1 & 2
    sheet_obj['C5'] = results['OPC101']['Start Date'][0]
    sheet_obj['C6'] = results['OPC101']['End Date'][0]
    sheet_obj['C7'] = owc_mp['OPC101']
    sheet_obj['C8'] = results['OPC101']['Alarms Count'][0]
    sheet_obj['C9'] = results['OPC101']['Tier 3.6'][0]
    sheet_obj['C10'] = results['OPC101']['Top 10 Alarms Count'][0]
    sheet_obj['C11'] = results['OPC101']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_101=results['OPC101']['Top 10 Alarms'][0].index
    top10_alarms_values_101=results['OPC101']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'B{14+i}'] = top10_alarms_index_101[i]
        sheet_obj[f'C{14+i}'] = top10_alarms_values_101[i][0]

    # Gas Trains 3 & 4
    sheet_obj['F5'] = results['OPC104']['Start Date'][0]
    sheet_obj['F6'] = results['OPC104']['End Date'][0]
    sheet_obj['F7'] = owc_mp['OPC104']
    sheet_obj['F8'] = results['OPC104']['Alarms Count'][0]
    sheet_obj['F9'] = results['OPC104']['Tier 3.6'][0]
    sheet_obj['F10'] = results['OPC104']['Top 10 Alarms Count'][0]
    sheet_obj['F11'] = results['OPC104']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_104=results['OPC104']['Top 10 Alarms'][0].index
    top10_alarms_values_104=results['OPC104']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'E{14+i}'] = top10_alarms_index_104[i]
        sheet_obj[f'F{14+i}'] = top10_alarms_values_104[i][0]

    # Gas Trains 5 & 6
    sheet_obj['I5'] = results['OPC129']['Start Date'][0]
    sheet_obj['I6'] = results['OPC129']['End Date'][0]
    sheet_obj['I7'] = owc_mp['OPC129']
    sheet_obj['I8'] = results['OPC129']['Alarms Count'][0]
    sheet_obj['I9'] = results['OPC129']['Tier 3.6'][0]
    sheet_obj['I10'] = results['OPC129']['Top 10 Alarms Count'][0]
    sheet_obj['I11'] = results['OPC129']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_129=results['OPC129']['Top 10 Alarms'][0].index
    top10_alarms_values_129=results['OPC129']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'H{14+i}'] = top10_alarms_index_129[i]
        sheet_obj[f'I{14+i}'] = top10_alarms_values_129[i][0]

    # Gas Train 7
    sheet_obj['C28'] = results['OPC132']['Start Date'][0]
    sheet_obj['C29'] = results['OPC132']['End Date'][0]
    sheet_obj['C30'] = owc_mp['OPC132']
    sheet_obj['C31'] = results['OPC132']['Alarms Count'][0]
    sheet_obj['C32'] = results['OPC132']['Tier 3.6'][0]
    sheet_obj['C33'] = results['OPC132']['Top 10 Alarms Count'][0]
    sheet_obj['C34'] = results['OPC132']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_132=results['OPC132']['Top 10 Alarms'][0].index
    top10_alarms_values_132=results['OPC132']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'B{37+i}'] = top10_alarms_index_132[i]
        sheet_obj[f'C{37+i}'] = top10_alarms_values_132[i][0]

    # SRUs 1 & 2
    sheet_obj['F28'] = results['OPC115']['Start Date'][0]
    sheet_obj['F29'] = results['OPC115']['End Date'][0]
    sheet_obj['F30'] = owc_mp['OPC115']
    sheet_obj['F31'] = results['OPC115']['Alarms Count'][0]
    sheet_obj['F32'] = results['OPC115']['Tier 3.6'][0]
    sheet_obj['F33'] = results['OPC115']['Top 10 Alarms Count'][0]
    sheet_obj['F34'] = results['OPC115']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_115=results['OPC115']['Top 10 Alarms'][0].index
    top10_alarms_values_115=results['OPC115']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'E{37+i}'] = top10_alarms_index_115[i]
        sheet_obj[f'F{37+i}'] = top10_alarms_values_115[i][0]

    # SRUs 3 & 4
    sheet_obj['I28'] = results['OPC140']['Start Date'][0]
    sheet_obj['I29'] = results['OPC140']['End Date'][0]
    sheet_obj['I30'] = owc_mp['OPC140']
    sheet_obj['I31'] = results['OPC140']['Alarms Count'][0]
    sheet_obj['I32'] = results['OPC140']['Tier 3.6'][0]
    sheet_obj['I33'] = results['OPC140']['Top 10 Alarms Count'][0]
    sheet_obj['I34'] = results['OPC140']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_140=results['OPC140']['Top 10 Alarms'][0].index
    top10_alarms_values_140=results['OPC140']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'H{37+i}'] = top10_alarms_index_140[i]
        sheet_obj[f'I{37+i}'] = top10_alarms_values_140[i][0]

    # Liquid Trains 1 & 2 - MRUs 1 & 2
    sheet_obj['C51'] = results['OPC107']['Start Date'][0]
    sheet_obj['C52'] = results['OPC107']['End Date'][0]
    sheet_obj['C53'] = owc_mp['OPC107']
    sheet_obj['C54'] = results['OPC107']['Alarms Count'][0]
    sheet_obj['C55'] = results['OPC107']['Tier 3.6'][0]
    sheet_obj['C56'] = results['OPC107']['Top 10 Alarms Count'][0]
    sheet_obj['C57'] = results['OPC107']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_107=results['OPC107']['Top 10 Alarms'][0].index
    top10_alarms_values_107=results['OPC107']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'B{60+i}'] = top10_alarms_index_107[i]
        sheet_obj[f'C{60+i}'] = top10_alarms_values_107[i][0]

    # Utilities Phase 1
    sheet_obj['F51'] = results['OPC110']['Start Date'][0]
    sheet_obj['F52'] = results['OPC110']['End Date'][0]
    sheet_obj['F53'] = owc_mp['OPC110']
    sheet_obj['F54'] = results['OPC110']['Alarms Count'][0]
    sheet_obj['F55'] = results['OPC110']['Tier 3.6'][0]
    sheet_obj['F56'] = results['OPC110']['Top 10 Alarms Count'][0]
    sheet_obj['F57'] = results['OPC110']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_110=results['OPC110']['Top 10 Alarms'][0].index
    top10_alarms_values_110=results['OPC110']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'E{60+i}'] = top10_alarms_index_110[i]
        sheet_obj[f'F{60+i}'] = top10_alarms_values_110[i][0]

    # Utilities Phase 2 - Liquid Train 3
    sheet_obj['I51'] = results['OPC135']['Start Date'][0]
    sheet_obj['I52'] = results['OPC135']['End Date'][0]
    sheet_obj['I53'] = owc_mp['OPC135']
    sheet_obj['I54'] = results['OPC135']['Alarms Count'][0]
    sheet_obj['I55'] = results['OPC135']['Tier 3.6'][0]
    sheet_obj['I56'] = results['OPC135']['Top 10 Alarms Count'][0]
    sheet_obj['I57'] = results['OPC135']['Top 10 Alarms Percent'][0]/100

    top10_alarms_index_135=results['OPC135']['Top 10 Alarms'][0].index
    top10_alarms_values_135=results['OPC135']['Top 10 Alarms'][0].values

    for i in range(10):
        sheet_obj[f'H{60+i}'] = top10_alarms_index_135[i]
        sheet_obj[f'I{60+i}'] = top10_alarms_values_135[i][0]



    # Offer download option
    st.download_button(label="Download Results Report", data=workbook, file_name="Analysis Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Main app structure

st.title("Alarm Analyzer App")
ph_files = st.file_uploader("Upload alarms log files (CSV format)", type="csv", accept_multiple_files=True)

if st.button("Analyze"):
    analyze_data()
