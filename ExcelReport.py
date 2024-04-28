import streamlit as st

# Save the Classified CSV
@st.cache_data
def convert_to_df(df):
    # IMPORTANT : Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def download_csv(csv, brand_name):
    st.download_button(
            label=":white_check_mark: Generate EXCEL Report",
            data=csv,
            file_name=f'{brand_name}_comments.csv',
            mime="text/csv"
    )

def excel_report_gen():

    brand_name = st.session_state.get('brand_name')
    analyzed_data = st.session_state.get('analyzed_data')

    if analyzed_data is not None:
        # Prepare the HTML table with bold and centered column names
        html_table = "<table><tr style='text-align: center; font-weight: bold;'>"
        html_table += "".join([f"<th>{col}</th>" for col in analyzed_data.columns])
        html_table += "</tr>"

        # Add table rows with data
        for index, row in analyzed_data.head(21).iterrows():
            html_table += "<tr>"
            html_table += "".join([f"<td>{value}</td>" for value in row])
            html_table += "</tr>"

        html_table += "</table>"

        # Display the HTML table
        st.write(html_table, unsafe_allow_html=True)

        # Prepare the CSV for download
        csv = convert_to_df(analyzed_data)
        st.markdown('')
        st.markdown('')
        download_csv(csv, brand_name)

    else:
        st.write("No analyzed data found. Please! first analyze data in the 'Summary' page.")