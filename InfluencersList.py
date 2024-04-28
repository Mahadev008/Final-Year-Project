import streamlit as st
import pandas as pd
from ExcelReport import convert_to_df
import re

def download_csv(csv, brand_name):
    st.download_button(
            label=":white_check_mark: Download Influencers List",
            data=csv,
            file_name=f'{brand_name}\'s_influencers.csv',
            mime="text/csv"
    )

def extract_link(html):
    match = re.search(r'href="(.*?)"', html)
    if match:
        return match.group(1)
    else:
        return ''

def gen_influencers_list():

    brand_name = st.session_state.get('brand_name')
    channel_names = st.session_state.get('channel_names')
    influencers_count = st.session_state.get('influencers_count')
    channel_links = st.session_state.get('channel_links')
    followers_counts = st.session_state.get('followers_counts')

    # Remove duplicates while preserving the order
    unique_channels = []
    unique_followers = []
    seen = set()
    for channel, followers in zip(channel_names, followers_counts):
        if channel not in seen:
            unique_channels.append(channel)
            unique_followers.append(followers)
            seen.add(channel)

    # Update the channel names and followers counts
    channel_names = unique_channels
    followers_counts = unique_followers

    st.markdown(f':1234: Influencers Count: {len(channel_names)}')

    # Convert list of unique channel names to DataFrame
    df = pd.DataFrame({'Profile Name': channel_names, 'Followers': followers_counts})

    # Set index starting from 1
    df.index += 1

    # Create a new column for the redirect links
    df['Redirect Link'] = ''

    # Interchange positions of columns 2 and 3
    df = df[['Profile Name', 'Redirect Link', 'Followers']]

    # Create clickable buttons for channel links and store redirect links in the DataFrame
    for idx, link in enumerate(channel_links):
        try:
            button_label = f"Visit {channel_names[idx]}'s Channel"
            redirect_link = f'<a href="{link}" target="_blank">{button_label}</a>'
            df.at[idx+1, 'Redirect Link'] = redirect_link
        except IndexError:
            pass  # Skip if the index is out of range

    # Render DataFrame to HTML
    html = df.to_html(escape=False)

    # Center align column titles using CSS styling
    html = html.replace('<th>', '<th style="text-align:center;">')

    # Display HTML-rendered DataFrame
    st.write(html, unsafe_allow_html=True)

    # Add clickable links to "Redirect Link" column
    df['Redirect Link'] = df['Redirect Link'].apply(extract_link)

    csv = convert_to_df(df)
    st.markdown('')
    st.markdown('')
    download_csv(csv, brand_name)



