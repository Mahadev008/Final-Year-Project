import streamlit as st
import gzip
import pickle
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import cleantext
# from googletrans import Translator
from googleapiclient.discovery import build
# import pyrebase
import os

# os.chdir("P:\PyCharm Selenium Practice\pythonProject\Sentiment Analysis\example app\TestingApp")

# emotion = pipeline("sentiment-analysis", model="j-hartmann/emotion-english-distilroberta-base")

# Loading the saved model
# emotion = pickle.load(open('trained_emotion_model.pkl', 'rb'))
# mini_emotion = pickle.load(open('trained_multilingual_emotion_model.pkl', 'rb'))


# Load the compressed model
with gzip.open('trained_multilingual_emotion_model.pkl.gz', 'rb') as f:
    mini_emotion = pickle.load(f)


# Set up YouTube Data API credentials
# api_key = "AIzaSyAglY6VSV8I7HnHGpSJb69oOakFKMcBBOg"
# youtube = build('youtube', 'v3', developerKey=api_key)
API_KEYS = ["AIzaSyCeUEng4Rltl1TBGd_xFXrTD__ibiZSIg0", "AIzaSyAd-2FR0xlWjCITRtm4Q__t7ja6zb95h_s", "AIzaSyD5dSk_A4D-JM5n4VVQcZFPlT4kysgV7ro", "AIzaSyAglY6VSV8I7HnHGpSJb69oOakFKMcBBOg"]

def build_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

# @st.cache_data
# def load_csv_data(csv_data):
#     return pd.read_csv(StringIO(csv_data))


# Function to retrieve comments from YouTube
def get_youtube_comments(youtube_service, brand_name, max_results=7):
    channel_names = []
    video_links = []
    comments = []
    like_counts = []

    try:
        # Search for videos related to the brand name
        search_response = youtube_service.search().list(
            q=brand_name,
            part='id,snippet',
            type='video',
            maxResults=max_results
        ).execute()

        # Check if search results are empty
        if 'items' not in search_response:
            print(f"No videos found for brand name: {brand_name}")
            return channel_names, video_links, comments, like_counts

        # Retrieve comments from selected videos
        for item in search_response['items']:
            video_id = item['id']['videoId']
            channel_name = item['snippet']['channelTitle']
            video_link = f"https://www.youtube.com/watch?v={video_id}"

            channel_names.append(channel_name)
            video_links.append(video_link)

            try:
                response = youtube_service.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=30
                ).execute()

                # Check if comments are disabled for the video
                if 'items' not in response:
                    print(f"Comments are disabled for video with ID: {video_id}")
                    comments.append([])
                    continue

                video_comments = []
                video_like_counts = []
                for comment in response['items']:
                    text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
                    video_comments.append(text)
                    video_like_counts.append(like_count)

                comments.append(video_comments)
                like_counts.append(video_like_counts)

            except Exception as e:
                print(f"Unable to fetch comments for video ID: {video_id}. Reason: {e}")
                comments.append([])
                like_counts.append([])

    except Exception as e:
        print(f"An error occurred while searching for videos. Reason: {e}")

    return channel_names, video_links, comments, like_counts



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
    return mini_emotion(text)[0]['label']


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
        return "Basic"

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

# @st.cache_data
def about(df, brand_name, brand_category, sentiment_counts, total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count):
    highest_count_label = sentiment_counts.idxmax()
    st.session_state['highest_count_label'] = highest_count_label
    st.session_state['total_comments_count'] = total_comments_count
    st.session_state['positive_comments_count'] = positive_comments_count
    st.session_state['negative_comments_count'] = negative_comments_count
    st.session_state['neutral_comments_count'] = neutral_comments_count

    # Display the about section with sentiment counts
    with st.expander('About', expanded=True):
        st.write(f'''           
                - :label: :orange[**Brand**]: [{brand_name}](https://en.wikipedia.org/wiki/{brand_name.replace(" ", "_")}).
                - :bookmark: :orange[**Category**]: {brand_category}
                - :floppy_disk: :orange[**Data from**]: YouTube
                - :bar_chart: :orange[**Status**]: {brand_name} has {highest_count_label} side as you see! 
                - :1234: :orange[**Total Comments**]: {total_comments_count}
                - :relaxed: :orange[**Positive Comments**]: {positive_comments_count}
                - :neutral_face: :orange[**Neutral Comments**]: {neutral_comments_count}
                - :white_frowning_face: :orange[**Negative Comments**]: {negative_comments_count}
            ''')

@st.cache_data(experimental_allow_widgets=True)
def download_csv(csv, brand_name):
    st.download_button(
            label=":white_check_mark: Download Analysed data as CSV",
            data=csv,
            file_name=f'{brand_name}_comments.csv',
            mime="text/csv"
    )




@st.cache_data
def analysis():

    if st.session_state['brand_name'] is not None:
        brand_name = st.session_state['brand_name']

        # Retrieving Data from YT and Analyzing it
        for api_key in API_KEYS:
            youtube_service = build_youtube_service(api_key)
            try:
                channel_names, video_links, comments_data, like_counts_data = get_youtube_comments(youtube_service, brand_name)
                # comments = get_youtube_comments(youtube_service, brand_name)
                all_comments = [comment for sublist in comments_data for comment in sublist]
                all_like_counts = [count for sublist in like_counts_data for count in sublist]
                st.write(f"Fetched {len(all_comments)} comments.")
                break  # Exit the loop if comments are successfully fetched
            except Exception as e:
                st.write(f"Failed to fetch comments: {e}")

        sentiments = analyze_sentiment(all_comments)
        df = pd.DataFrame({'Comment': all_comments, 'Sentiment': sentiments,
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

        col3, col4 = st.columns((6, 3), gap='medium')

        with col3:
            st.write(df.head(20))

        with col4:
            about(df, brand_name, brand_category, sentiment_counts, total_comments_count,
                  positive_comments_count, negative_comments_count, neutral_comments_count)

        # Store analyzed data, video links and channel names in session state
        st.session_state['analyzed_data'] = df
        st.session_state['video_links'] = video_links
        st.session_state['channel_names'] = channel_names

        st.session_state['top_positive_comments'] = top_positive_comments
        st.session_state['top_negative_comments'] = top_negative_comments
        st.session_state['top_neutral_comments'] = top_neutral_comments

        # Save the Classified CSV
        @st.cache_data
        def convert_to_df(df):
            # IMPORTANT : Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_to_df(df)
        download_csv(csv, brand_name)

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
