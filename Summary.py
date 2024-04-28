import streamlit as st
import gzip
import pickle
import pandas as pd
from datetime import datetime, date
# from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import cleantext
# from googletrans import Translator
from googleapiclient.discovery import build
# import pyrebase
from ExcelReport import convert_to_df
import os
os.chdir("C:\\Users\\Mahadevan Periasamy\\Desktop\\FinalYearProject_ML\\Streamlit\\Final_Project")

# emotion = pipeline("sentiment-analysis", model="j-hartmann/emotion-english-distilroberta-base")

# Loading the saved model
# emotion = pickle.load(open('trained_emotion_model.pkl', 'rb'))
# emotion = pickle.load(open('trained_multilingual_emotion_model.pkl', 'rb'))

with gzip.open('trained_multilingual_emotion_model.pkl.gz', 'rb') as f:
    emotion = pickle.load(f)

# Set up YouTube Data API credentials
API_KEYS = ["AIzaSyCBtHdk65CyZP39arZo1qcDghRFtrzKqUM", "AIzaSyAd-2FR0xlWjCITRtm4Q__t7ja6zb95h_s", "AIzaSyD5dSk_A4D-JM5n4VVQcZFPlT4kysgV7ro", "AIzaSyAglY6VSV8I7HnHGpSJb69oOakFKMcBBOg"]

def build_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

# @st.cache_data
# def load_csv_data(csv_data):
#     return pd.read_csv(StringIO(csv_data))



# def convert_date_to_RFC_3339(start_date, end_date):
#     start_date_RFC_3339 = datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%SZ")
#     end_dateRFC_3339 = datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%SZ")
#     return start_date_RFC_3339, end_dateRFC_3339


def get_youtube_comments(youtube_service, brand_name, start_date, end_date, max_results=20):
    channel_names = []
    video_links = []
    comments = []
    like_counts = []
    followers_counts = []
    channel_links = []
    comment_dates = []  # List to store comment dates

    # Convert start and end dates to RFC 3339 format
    start_date_rfc3339 = datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    end_date_rfc3339 = datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%SZ")

    try:
        # Search for videos related to the brand name
        search_response = youtube_service.search().list(
            q=brand_name,
            part='id,snippet',
            type='video',
            maxResults=max_results,
            publishedAfter=start_date_rfc3339,
            publishedBefore=end_date_rfc3339
        ).execute()

        # Check if search results are empty
        if 'items' not in search_response:
            print(f"No videos found for brand name: {brand_name}")
            return channel_names, video_links, comments, like_counts, followers_counts, channel_links, comment_dates

        # Retrieve comments, channel statistics, and channel links from selected videos
        for item in search_response['items']:
            video_id = item['id']['videoId']
            channel_name = item['snippet']['channelTitle']
            channel_id = item['snippet']['channelId']
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            channel_link = f"https://www.youtube.com/channel/{channel_id}"

            channel_names.append(channel_name)
            video_links.append(video_link)
            channel_links.append(channel_link)

            try:
                # Fetch channel statistics
                channel_response = youtube_service.channels().list(
                    part='statistics',
                    id=channel_id
                ).execute()

                if 'items' in channel_response:
                    statistics = channel_response['items'][0]['statistics']
                    followers_count = statistics.get('subscriberCount')

                    if followers_count is not None:
                        followers_counts.append(followers_count)
                    else:
                        # If follower count information is not available, append None
                        followers_counts.append(None)

                else:
                    # If statistics are not available, append None
                    followers_counts.append(None)

                response = youtube_service.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=15
                ).execute()

                # Check if comments are disabled for the video
                if 'items' not in response:
                    print(f"Comments are disabled for video with ID: {video_id}")
                    comments.append([])
                    like_counts.append([])
                    continue

                video_comments = []
                video_like_counts = []
                video_comment_dates = []  # List to store comment dates for the current video
                for comment in response['items']:
                    text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
                    comment_date = comment['snippet']['topLevelComment']['snippet']['publishedAt']
                    video_comments.append(text)
                    video_like_counts.append(like_count)
                    video_comment_dates.append(comment_date)

                comments.append(video_comments)
                like_counts.append(video_like_counts)
                comment_dates.append(video_comment_dates)

            except Exception as e:
                print(f"Unable to fetch data for video ID: {video_id}. Reason: {e}")
                comments.append([])
                like_counts.append([])
                followers_counts.append(0)

    except Exception as e:
        print(f"An error occurred while searching for videos. Reason: {e}")

    return channel_names, video_links, comments, like_counts, followers_counts, channel_links, comment_dates



# @st.cache_data
def data_processing(text):
    if not text or text.isspace():
        return text
    else:
        text = cleantext.clean(text, clean_all=False, extra_spaces=True, stopwords=True,
                               lowercase=True, numbers=True, punct=True, stemming=True, )
    return text

# @st.cache_data
# def translate_to_english(input_text, translator):
#     translation = str(translator.translate(text=input_text, src='auto', dest='en').text)
#     return translation


# @st.cache_data
def get_emotion_label(text):
    return emotion(text)[0]['label']


# Function to perform sentiment analysis
def analyze_sentiment(all_video_comments):
    sentiments = []
    # translator = Translator()
    for comment in all_video_comments:
        # Clean the comment text
        cleaned_comment = data_processing(comment)
        # Translate Text to English
        # translated_text = translate_to_english(cleaned_comment, translator)
        # Perform sentiment analysis on cleaned text
        sentiment = get_emotion_label(cleaned_comment)
        sentiments.append(sentiment)
    return sentiments


# Changing Emotion Label for Food Category
def food_category(label):
    if label == "positive":
        return "Delicious"
    elif label == "neutral":
        return "Not Bad"
    elif label == "negative":
        return "Waste of Money"


# Changing Emotion Label for Clothing Category
def clothing_category(label):
    if label == "positive":
        return "Happy with the product"
    elif label == "neutral":
        return "Just fine"
    elif label == "negative":
        return "Not worth it"

# Changing Emotion Label for FootWear Category
def footwear_category(label):
    if label == "positive":
        return "Comfortable"
    elif label == "neutral":
        return "Ordinary"
    elif label == "negative":
        return "Uncomfortable"

# Changing Emotion Label for Cosmetics
def cosmetics_category(label):
    if label == "positive":
        return "Natural-looking"
    elif label == "neutral":
        return "Acceptable"
    elif label == "negative":
        return "Un-Natural"

# Changing Emotion Label for Beverages
def beverages_category(label):
    if label == "positive":
        return "High-quality"
    elif label == "neutral":
        return "Average"
    elif label == "negative":
        return "Flat"

# Changing Emotion Label for Accessories
def accessories_category(label):
    if label == "positive":
        return "Functional"
    elif label == "neutral":
        return "Flimsy"
    elif label == "negative":
        return "Just Basic"

# @st.cache_data
def gen_countplot(df):
    plt.figure(figsize=(5, 4), dpi=300)
    sns.countplot(data=df, y="Sentiment", hue="Sentiment", palette="Set1").set_title("Emotion Distribution")
    # Save the plot as PNG file
    count_plot_image = "countplot.png"
    plt.savefig(count_plot_image, format="png", bbox_inches="tight")
    plt.close()
    st.session_state['count_plot_image'] = count_plot_image
    # st.pyplot(fig)
    return count_plot_image


# @st.cache_data
def gen_piechart(df):
    # visualizing the distribution of data using piechart
    emotion_counts = df['Sentiment'].value_counts()
    # Plotting
    fig, ax = plt.subplots()
    # explode = (0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03)
    wedges, _, _ = ax.pie(emotion_counts, autopct='', textprops=dict(color="w"))

    # Draw legend with same labels and percentages
    legend_labels = [f"{label} ({percentage:.1f}%)"
                     for label, percentage in zip(emotion_counts.index,
                                                  100. * emotion_counts / emotion_counts.sum())]
    ax.legend(wedges, legend_labels, title="Opinion", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Distribution of Sentiments')
    # Save the plot as PNG file
    pie_chart_image = "piechart.png"
    plt.savefig(pie_chart_image, format="png", bbox_inches="tight", dpi=300)
    plt.close()
    st.session_state['pie_chart_image'] = pie_chart_image
    return pie_chart_image

def gen_linechart(df, brand_category):
    # Define mapping of sentiment labels based on brand category
    sentiment_labels_mapping = {
        "Food Category": {"positive": "Delicious", "negative": "Waste of Money", "neutral": "Not Bad"},
        "Clothing Category": {"positive": "Happy with the product", "negative": "Not worth it", "neutral": "Just fine"},
        "FootWear Category": {"positive": "Comfortable", "negative": "Uncomfortable", "neutral": "Ordinary"},
        "Cosmetics": {"positive": "Natural-looking", "negative": "Un-Natural", "neutral": "Acceptable"},
        "Beverages": {"positive": "High-quality", "negative": "Flat", "neutral": "Average"},
        "Accessories": {"positive": "Functional", "negative": "Just Basic", "neutral": "Flimsy"}
    }

    # Get the sentiment labels based on the brand category
    sentiment_labels = sentiment_labels_mapping.get(brand_category, {})

    # Replace sentiment labels in the DataFrame
    df['Sentiment'] = df['Sentiment'].replace(sentiment_labels)

    # Assuming df contains the DataFrame with columns 'Date', 'Sentiment', and 'Comment'
    # You may need to preprocess your data to count the occurrences of each sentiment for each date
    # Convert 'Date' column to datetime type if it's not already
    df['Date'] = pd.to_datetime(df['Date'])
    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    # Resample the DataFrame by month and count the occurrences of each sentiment
    sentiment_counts_by_month = df.groupby([pd.Grouper(freq='M'), 'Sentiment']).size().unstack(fill_value=0)
    # Plotting the line graph
    plt.figure(figsize=(10, 6))
    for sentiment_label in sentiment_labels.values():
        plt.plot(sentiment_counts_by_month.index, sentiment_counts_by_month[sentiment_label], label=sentiment_label, marker='o')
    # Adding labels and title
    plt.xlabel('Date (Month)')
    plt.ylabel('Count of Comments')
    plt.title('Sentiment Distribution Over Time (Monthly Interval)')
    plt.legend()
    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45)
    # Save the plot as PNG file
    linechart_image = "linechart.png"
    plt.savefig(linechart_image, format="png", bbox_inches="tight")
    plt.close()
    st.session_state['linechart_image'] = linechart_image
    return linechart_image



# @st.cache_data
def about(brand_name, brand_category, sentiment_counts, influencers_count, total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count):
    highest_count_label = sentiment_counts.idxmax()
    st.session_state['highest_count_label'] = highest_count_label
    st.session_state['total_comments_count'] = total_comments_count
    st.session_state['positive_comments_count'] = positive_comments_count
    st.session_state['negative_comments_count'] = negative_comments_count
    st.session_state['neutral_comments_count'] = neutral_comments_count
    st.session_state['influencers_count'] = influencers_count

    # Display the about section with sentiment counts
    with st.expander(':shamrock: About', expanded=True):
        st.write(f'''           
                - :label: :orange[**Brand**]: [{brand_name}](https://en.wikipedia.org/wiki/{brand_name.replace(" ", "_")}).
                - :bookmark: :orange[**Category**]: {brand_category}
                - :floppy_disk: :orange[**Data from**]: YouTube
                - :bar_chart: :orange[**Status**]: {brand_name} has {highest_count_label} feedback!
                - :bust_in_silhouette: :orange[**Inflencers Count**]: {influencers_count}
                - :1234: :orange[**Total Comments**]: {total_comments_count}
                - :relaxed: :orange[**Positive Comments**]: {positive_comments_count}
                - :neutral_face: :orange[**Neutral Comments**]: {neutral_comments_count}
                - :white_frowning_face: :orange[**Negative Comments**]: {negative_comments_count}
            ''')



# @st.cache_data(experimental_allow_widgets=True)
# def download_csv(csv, brand_name):
#     st.download_button(
#             label=":white_check_mark: Generate EXCEL Report",
#             data=csv,
#             file_name=f'{brand_name}_comments.csv',
#             mime="text/csv"
#     )


@st.cache_data
def analysis():

    if st.session_state['brand_name'] is not None:
        brand_name = st.session_state['brand_name']

        # start_date = st.date_input("Start Date")
        # end_date = st.date_input("End Date")
        # converted_start_date, converted_end_date = convert_date_to_RFC_3339(start_date, end_date)

        # start_date = st.session_state['start_date']
        # end_date = st.session_state['end_date']

        start_date = date(2000, 1, 1)
        end_date = date.today()
        # st.session_state['start_date'] = start_date
        # st.session_state['end_date'] = end_date

        # Retrieving Data from YT and Analyzing it
        for api_key in API_KEYS:
            youtube_service = build_youtube_service(api_key)
            try:
                channel_names, video_links, comments_data, like_counts_data, followers_counts, channel_links, comment_dates = get_youtube_comments(youtube_service, brand_name, start_date=start_date, end_date=end_date)
                # comments = get_youtube_comments(youtube_service, brand_name)
                all_comments = [comment for sublist in comments_data for comment in sublist]
                all_like_counts = [count for sublist in like_counts_data for count in sublist]
                influencers_count = len(set(channel_names))
                all_comment_dates = [date for sublist in comment_dates for date in sublist]  # Flatten the list of lists

                st.write(f":1234: Fetched {len(all_comments)} comments.")
                break  # Exit the loop if comments are successfully fetched
            except Exception as e:
                st.write(f":white_frowning_face: Failed to fetch comments: {e}")

        sentiments = analyze_sentiment(all_comments)
        # Create DataFrame with comments, sentiment, like count, and comment dates
        df = pd.DataFrame({'Date': all_comment_dates,
                           'Comment': all_comments,
                           'Sentiment': sentiments,
                           'Like Count': all_like_counts})

        # Filter comments based on sentiment
        positive_comments = df[df['Sentiment'] == 'positive'].sort_values(by='Like Count', ascending=False).head(5)
        negative_comments = df[df['Sentiment'] == 'negative'].sort_values(by='Like Count', ascending=False).head(5)
        neutral_comments = df[df['Sentiment'] == 'neutral'].sort_values(by='Like Count', ascending=False).head(5)
        # Convert filtered DataFrames to dictionaries
        top_positive_comments = positive_comments[['Comment', 'Like Count']].to_dict(orient='records')
        top_negative_comments = negative_comments[['Comment', 'Like Count']].to_dict(orient='records')
        top_neutral_comments = neutral_comments[['Comment', 'Like Count']].to_dict(orient='records')

        # Get the sentiment value counts
        sentiment_counts = df['Sentiment'].value_counts()
        # Extract the counts for each sentiment category
        total_comments_count = len(df)
        positive_comments_count = sentiment_counts.get('positive', 0)
        negative_comments_count = sentiment_counts.get('negative', 0)
        neutral_comments_count = sentiment_counts.get('neutral', 0)

        # Changing Emotion Labels Based on Brand Category
        brand_category = st.session_state['brand_category']
        if brand_category == "Food Category":
            df['Sentiment'] = df['Sentiment'].apply(food_category)
        elif brand_category == "Clothing Category":
            df['Sentiment'] = df['Sentiment'].apply(clothing_category)
        elif brand_category == "FootWear Category":
            df['Sentiment'] = df['Sentiment'].apply(footwear_category)
        elif brand_category == "Cosmetics":
            df['Sentiment'] = df['Sentiment'].apply(cosmetics_category)
        elif brand_category == "Beverages":
            df['Sentiment'] = df['Sentiment'].apply(beverages_category)
        elif brand_category == "Accessories":
            df['Sentiment'] = df['Sentiment'].apply(accessories_category)

        # Dashboard Main Panel
        col1, col2 = st.columns((6, 5), gap='medium')

        with col1:
            cp_img = gen_countplot(df)
            st.image(cp_img)

        with col2:
            pc_img = gen_piechart(df)
            st.image(pc_img)

        col3, col4 = st.columns((6, 4), gap='medium')

        with col3:
            line_img = gen_linechart(df, brand_category)
            st.image(line_img)

        with col4:
            about(brand_name, brand_category, sentiment_counts, influencers_count,
                total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count)

        # Store analyzed data, video links and channel names in session state
        st.session_state['analyzed_data'] = df
        st.session_state['video_links'] = video_links
        st.session_state['channel_names'] = channel_names

        st.session_state['followers_counts'] = followers_counts
        st.session_state['channel_links'] = channel_links

        st.session_state['top_positive_comments'] = top_positive_comments
        st.session_state['top_negative_comments'] = top_negative_comments
        st.session_state['top_neutral_comments'] = top_neutral_comments

        # csv = convert_to_df(df)
        # download_csv(csv, brand_name)
        #
        # st.write(followers_counts)


        # for idx, (channel_name, video_link, video_comments) in enumerate(zip(channel_names, video_links, comments), 1):
        #     st.write(f"{idx}. {channel_name}")
        #     st.write(f"   {video_link}")
        #     if video_comments:
        #         st.write("   Comments:")
        #         for comment in video_comments:
        #             st.write(f"      - {comment}")
        #     else:
        #         st.write("   No comments available.")
        #     st.write("---")

        # for idx, comment_data in enumerate(sorted_all_comments[:5], 1):
        #     text = comment_data['text']
        #     like_count = comment_data['like_count']
        #     st.write(f"{idx}. {text} (Likes: {like_count})")
        #     st.write("---")

        # # Display top 5 comments for each sentiment
        # st.write("Top 5 Positive Comments:")
        # st.write(top_positive_comments)
        #
        # st.write("Top 5 Negative Comments:")
        # st.write(top_negative_comments)
        #
        # st.write("Top 5 Neutral Comments:")
        # st.write(top_neutral_comments)

# if __name__ == "__main__":
#     analysis()