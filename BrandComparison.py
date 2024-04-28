import streamlit as st
import pandas as pd
from datetime import date
from Summary import analyze_sentiment, API_KEYS, build_youtube_service, get_youtube_comments



def data_from_youtube(channel_names, comments_data, like_counts_data):
    all_comments = [comment for sublist in comments_data for comment in sublist]
    all_like_counts = [count for sublist in like_counts_data for count in sublist]
    # Compare influencers count (unique channel names)
    inflencers = len(set(channel_names))

    return inflencers, all_comments, all_like_counts

def get_highest_count_label(sentiment_counts):
    # Sort the sentiment counts dictionary by count values in descending order
    sorted_counts = sorted(sentiment_counts.items(), key=lambda x: x[1], reverse=True)
    # Get the label with the highest count (first item in the sorted list)
    highest_count_label = sorted_counts[0][0] if sorted_counts else None
    return highest_count_label

def fetch_counts(df):
    # Get the sentiment value counts
    sentiment_counts = df['Sentiment'].value_counts()
    # Highest sentiment's count
    highest_count_label = get_highest_count_label(sentiment_counts)
    # Extract the counts for each sentiment category
    total_comments_count = len(df)
    positive_comments_count = sentiment_counts.get('positive', 0)
    neutral_comments_count = sentiment_counts.get('neutral', 0)
    negative_comments_count = sentiment_counts.get('negative', 0)

    return sentiment_counts, highest_count_label, total_comments_count, positive_comments_count, neutral_comments_count, negative_comments_count


def display(brand_name, highest_count_label, inflencers, total_comments_count, positive_comments_count, neutral_comments_count, negative_comments_count):
    st.write(f'''           
                - :label: :orange[**Brand**]: [{brand_name}](https://en.wikipedia.org/wiki/{brand_name.replace(" ", "_")})
                - :floppy_disk: :orange[**Data from**]: YouTube
                - :bar_chart: :orange[**Status**]: {brand_name} has {highest_count_label} feedback!
                - :bust_in_silhouette: :orange[**Inflencers Count**]: {inflencers}
                - :1234: :orange[**Total Comments**]: {total_comments_count}
                - :relaxed: :orange[**Positive Comments**]: {positive_comments_count}
                - :neutral_face: :orange[**Neutral Comments**]: {neutral_comments_count}
                - :white_frowning_face: :orange[**Negative Comments**]: {negative_comments_count}
                            ''')

def comparison_winner(brand_name_1, brand_name_2, total_comments_count_1, total_comments_count_2, positive_comments_count_1, positive_comments_count_2, inflencers_1, inflencers_2):
    # Compare total comments count
    if total_comments_count_1 > total_comments_count_2:
        total_comments_winner = brand_name_1
    else:
        total_comments_winner = brand_name_2

    # Compare positive comments count
    if positive_comments_count_1 > positive_comments_count_2:
        positive_comments_winner = brand_name_1
    else:
        positive_comments_winner = brand_name_2

    if inflencers_1 > inflencers_2:
        influencers_winner = brand_name_1
    elif inflencers_2 > inflencers_1:
        influencers_winner = brand_name_2
    else:
        influencers_winner = "Same"

    return total_comments_winner, positive_comments_winner, influencers_winner



def compare_brands():

    brand_1, brand_2 = st.columns((6, 6), gap='small')

    with brand_1:
        # Brand name input 1
        brand_name_1 = st.text_input(":first_place_medal: Enter brand name 1:")
    with brand_2:
        # Brand name input 2
        brand_name_2 = st.text_input(":second_place_medal: Enter brand name 2:")


    if st.button("Compare"):

        if not brand_name_1 or not brand_name_2:
            st.info("Please! Enter both Brand Names to Continue...")
        elif brand_name_1==brand_name_2:
            st.info("Please! Enter different Brand Names to Continue...")
        else:
            result_1, result_2 = st.columns((6, 6), gap='medium')

            # start_date = st.session_state['start_date']
            # end_date = st.session_state['end_date']
            start_date = date(2000, 1, 1)
            end_date = date.today()

            with (result_1):
                # Retrieving Data from YT and Analyzing it
                for api_key in API_KEYS:
                    youtube_service = build_youtube_service(api_key)
                    try:
                        channel_names_1, video_links_1, comments_data_1, like_counts_data_1, followers_counts_1, channel_links_1, comment_dates_1 = get_youtube_comments(
                            youtube_service,
                            brand_name_1, start_date=start_date, end_date=end_date)
                        inflencers_1, all_comments_1, all_like_counts_1 = data_from_youtube(channel_names_1,
                                                                                            comments_data_1,
                                                                                            like_counts_data_1)
                        st.write(f"Fetched {len(all_comments_1)} comments.")
                        break  # Exit the loop if comments are successfully fetched
                    except Exception as e:
                        st.write(f"Failed to fetch comments: {e}")

                sentiments = analyze_sentiment(all_comments_1)
                df_1 = pd.DataFrame({'Comment': all_comments_1, 'Sentiment': sentiments,
                                     'Like Count': all_like_counts_1})
                sentiment_counts_1, highest_count_label_1, total_comments_count_1, positive_comments_count_1, neutral_comments_count_1, negative_comments_count_1 = fetch_counts(
                    df_1)
                display(brand_name_1, highest_count_label_1, inflencers_1, total_comments_count_1,
                        positive_comments_count_1, neutral_comments_count_1, negative_comments_count_1)

            with result_2:
                # Retrieving Data from YT and Analyzing it
                for api_key in API_KEYS:
                    youtube_service = build_youtube_service(api_key)
                    try:
                        channel_names_2, video_links_2, comments_data_2, like_counts_data_2, followers_counts_2, channel_links_2, comment_dates_2 = get_youtube_comments(
                            youtube_service,
                            brand_name_2, start_date=start_date, end_date=end_date)
                        inflencers_2, all_comments_2, all_like_counts_2 = data_from_youtube(channel_names_2,
                                                                                            comments_data_2,
                                                                                            like_counts_data_2)
                        st.write(f"Fetched {len(all_comments_2)} comments.")
                        break  # Exit the loop if comments are successfully fetched
                    except Exception as e:
                        st.write(f"Failed to fetch comments: {e}")

                sentiments = analyze_sentiment(all_comments_2)
                df_2 = pd.DataFrame({'Comment': all_comments_2, 'Sentiment': sentiments,
                                     'Like Count': all_like_counts_2})
                sentiment_counts_2, highest_count_label_2, total_comments_count_2, positive_comments_count_2, neutral_comments_count_2, negative_comments_count_2 = fetch_counts(
                    df_2)
                display(brand_name_2, highest_count_label_2, inflencers_2, total_comments_count_2,
                        positive_comments_count_2, neutral_comments_count_2, negative_comments_count_2)

            winner_1, winner_2, winner_3 = st.columns((6, 6, 6), gap='small')

            with winner_2:
                total_comments_winner, positive_comments_winner, influencers_winner = comparison_winner(brand_name_1,
                                                                                                        brand_name_2,
                                                                                                        total_comments_count_1,
                                                                                                        total_comments_count_2,
                                                                                                        positive_comments_count_1,
                                                                                                        positive_comments_count_2,
                                                                                                        inflencers_1,
                                                                                                        inflencers_2)

                # Highlight the highest of these 3 parameters
                st.write(f'''
                                :trophy: **Winners in Comparison**:
                                - :1234: **Total Comments Count**: {total_comments_winner}
                                - :relaxed: **Positive Comments Count**: {positive_comments_winner}
                                - :busts_in_silhouette: **Influencers (Unique Channels)**: {influencers_winner}
                            ''')
