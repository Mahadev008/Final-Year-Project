import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64
import os
# os.chdir("C:\\Users\\Mahadevan Periasamy\\Desktop\\FinalYearProject_ML\\Streamlit\\Final_Project")

# Function to generate PDF report
def generate_pdf_report(analyzed_data, count_plot_image, linechart_image, pie_chart_image, include_countplot, include_linechart,
            include_piechart, include_sample_links, include_influencers_list, include_top_comments,
            highest_count_label, brand_name,  brand_category, channel_names,video_links,
            top_positive_comments, top_negative_comments, top_neutral_comments, influencers_count,
            total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count):

    # Create a new PDF canvas
    pdf_filename = f"{brand_name}_analysis_report.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    width, _ = letter
    pdfmetrics.registerFont(TTFont('tahoma-bold', 'tahoma-bold.ttf'))
    pdfmetrics.registerFont(TTFont('Segoe UI Emoji', 'seguiemj.ttf'))

    # Load image and get its dimensions
    def bg_image():
        image_path = "services_social_3.jpg"  # Path to your image
        image = ImageReader(image_path)
        image_width, image_height = image.getSize()
        # Calculate scaling factor to fit the image to the page
        scale_factor = letter[0] / image_width
        # Draw image with transparency
        pdf.saveState()
        pdf.setFillColorRGB(1, 1, 1, 0.2)  # Adjust alpha value (0 to 1) for transparency
        pdf.drawImage(image, 0, 0, width=letter[0], height=image_height * scale_factor)
        pdf.restoreState()

    def center_format(font, fontsize, text, y_axis_count):
        pdf.setFont(f"{font}", fontsize)
        title_width = pdf.stringWidth(f"{text}")
        center_x = width / 2 - title_width / 2
        pdf.drawString(center_x, y_axis_count, f"{text}")

    # Page 1: Sentiment Analysis Report with Brand Name centered
    bg_image()
    center_format("Helvetica", 25, "Sentiment Analysis Report", 700)
    center_format("tahoma-bold", 40, brand_name, 450)
    center_format("Helvetica", 18, f"Brand Category: {brand_category}", 200)
    center_format("Helvetica", 18, "Data from: YouTube", 150)
    center_format("Helvetica", 18, f"Status: {brand_name} has {highest_count_label} feedback!", 100)
    pdf.showPage()


    # Page 2: List of Channel Names and Video Links
    if include_sample_links:
        center_format("Helvetica", 25,"List of Channel Names and Video Links", 700)
        y_position = 630

        # Limit the loop to only the first 5 comments and video links
        for idx in range(min(7, len(channel_names))):
            channel_name = channel_names[idx]
            video_link = video_links[idx]

            pdf.setFont("Helvetica", 15)
            pdf.drawString(70, y_position, f"{idx + 1}. Channel Name: {channel_name}")
            pdf.drawString(70, y_position - 20, f"       Video Link: {video_link}")

            y_position -= 70
            if y_position < 50:
                pdf.showPage()
                y_position = 750

        pdf.showPage()

    # Page 3: List of Influencers
    if include_influencers_list:

        center_format("Segoe UI Emoji", 25,"INFLUENCERS DETAILS", 700)

        # Influencers Count
        pdf.setFont("Segoe UI Emoji", 18)
        pdf.drawString(70, 630, f"Influencers Count: {influencers_count}")

        # Preprocess influencers list: sort by text length and remove duplicates
        sorted_unique_influencers = sorted(set(channel_names), key=len)

        # List of Influencers in two columns
        pdf.drawString(70, 580, f"Influencers List:")
        pdf.setFont("Segoe UI Emoji", 15)
        bullet = u'\u2022 '  # Bullet point
        num_influencers = len(sorted_unique_influencers)
        middle_idx = num_influencers // 2  # Index to split the influencers into two columns

        # First column
        y_position = 540
        for channel_name in sorted_unique_influencers[:middle_idx]:
            pdf.drawString(100, y_position, f"{bullet}{channel_name}")
            y_position -= 30  # Vertical spacing between influencers

        # Second column
        y_position = 540
        for channel_name in sorted_unique_influencers[middle_idx:]:
            pdf.drawString(300, y_position, f"{bullet}{channel_name}")
            y_position -= 30  # Vertical spacing between influencers

        pdf.showPage()

    # Function to draw comments with proper alignment
    def draw_comments(comments, title, start_y):
        pdf.setFont("Segoe UI Emoji", 18)
        pdf.drawString(70, start_y, title)
        y_position = start_y - 30  # Start position below the title
        for idx, comment in enumerate(comments, 1):
            comment_text = comment['Comment']
            like_count = comment['Like Count']
            pdf.setFont("Segoe UI Emoji", 10)
            pdf.drawString(70, y_position, f"{idx}. {comment_text} (Likes: {like_count})")
            y_position -= 20  # Vertical spacing between comments

    # Page 4: Top Comments
    if include_top_comments:
        center_format("Helvetica", 25,"TOP COMMENTS", 700)
        pdf.setFont("Helvetica", 15)
        pdf.drawString(70, 650, f"Total comments Count - {total_comments_count}")
        pdf.drawString(70, 620, f"Positive Comments Count - {positive_comments_count}")
        pdf.drawString(70, 590, f"Negative Comments Count - {negative_comments_count}")
        pdf.drawString(70, 560, f"Neutral Comments Count - {neutral_comments_count}")

        start_y = 500  # Starting Y position for the first section
        draw_comments(top_positive_comments, "Top Positive Comments:", start_y)

        start_y -= len(top_positive_comments) * 20 + 50  # Adjust Y position for next section
        draw_comments(top_negative_comments, "Top Negative Comments:", start_y)

        start_y -= len(top_negative_comments) * 20 + 50  # Adjust Y position for next section
        draw_comments(top_neutral_comments, "Top Neutral Comments:", start_y)

        pdf.showPage()


    # Page 5: Countplot
    if include_countplot:
        # Add count-plot with title on Page 5
        center_format("Helvetica", 25,"COUNT-PLOT", 700)
        # Calculate center coordinates for the image
        x_center = (pdf._pagesize[0] - 500) / 2
        y_center = (pdf._pagesize[1] - 300) / 2
        pdf.drawImage(count_plot_image, x_center, y_center, width=500, height=300)
        pdf.showPage()

    # Page 6: LineChart
    if include_linechart:
        # Add line-chart with title on Page 6
        center_format("Helvetica", 25, "LINE CHART", 700)
        # Calculate center coordinates for the image
        x_center = (pdf._pagesize[0] - 500) / 2
        y_center = (pdf._pagesize[1] - 300) / 2
        pdf.drawImage(linechart_image, x_center, y_center, width=500, height=300)
        pdf.showPage()

    # Page 7: Pie-Chart
    if include_piechart:
        # Add pie-chart with title on Page 7
        center_format("Helvetica", 25, "PIE-CHART", 700)
        # Calculate center coordinates for the image
        x_center = (pdf._pagesize[0] - 500) / 2
        y_center = (pdf._pagesize[1] - 300) / 2
        pdf.drawImage(pie_chart_image, x_center, y_center, width=500, height=300)
        pdf.showPage()

    # Last Page
    bg_image()

    center_format("tahoma-bold", 40,"Thank You", 440)
    center_format("Segoe UI Emoji", 15, "🙌 We hope your experience was excellent and We can’t wait to see you again soon 😉", 400)
    # center_format("Segoe UI Emoji", 15, "🙌 We can’t wait to see you again soon 😉", 380)

    # Save the PDF file
    pdf.save()
    return pdf_filename

def pdf_report_gen():
    st.write(":balloon: Choose Report Content:")
    analyzed_data = st.session_state.get('analyzed_data')
    count_plot_image = st.session_state.get('count_plot_image')
    pie_chart_image = st.session_state.get('pie_chart_image')
    linechart_image = st.session_state.get('linechart_image')
    highest_count_label = st.session_state.get('highest_count_label')
    brand_name = st.session_state.get('brand_name')
    brand_category = st.session_state.get('brand_category')
    channel_names = st.session_state.get('channel_names')
    video_links = st.session_state.get('video_links')
    top_positive_comments = st.session_state.get('top_positive_comments')
    top_negative_comments = st.session_state.get('top_negative_comments')
    top_neutral_comments = st.session_state.get('top_neutral_comments')

    influencers_count = st.session_state.get('influencers_count')
    total_comments_count = st.session_state.get('total_comments_count')
    positive_comments_count = st.session_state.get('positive_comments_count')
    negative_comments_count = st.session_state.get('negative_comments_count')
    neutral_comments_count = st.session_state.get('neutral_comments_count')

    include_sample_links = st.checkbox("Include Sample Video Links")
    include_influencers_list = st.checkbox("Include Influencers List")
    include_top_comments = st.checkbox("Include Top Comments")
    include_countplot = st.checkbox("Include Count Plot")
    include_linechart = st.checkbox("Include Line Chart")
    include_piechart = st.checkbox("Include Pie Chart")
    if analyzed_data is not None:
        if st.button(":white_check_mark: Generate Report"):
            pdf_output_path = generate_pdf_report(analyzed_data, count_plot_image, linechart_image, pie_chart_image, include_countplot, include_linechart,
                        include_piechart, include_sample_links, include_influencers_list, include_top_comments, highest_count_label, brand_name,  brand_category, channel_names,
                            video_links, top_positive_comments, top_negative_comments, top_neutral_comments, influencers_count,
                                total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count)

            with open(pdf_output_path, "rb") as f:
                pdf_bytes = f.read()
            # Download the PDF file
            b64 = base64.b64encode(pdf_bytes).decode()
            pdf_filename = f"{brand_name}_analysis_report.pdf"
            href = f'<a href="data:application/octet-stream;base64,{b64}" download={pdf_filename}>Download PDF report</a>'
            st.markdown(href, unsafe_allow_html=True)
            # Delete the PDF file after downloading
            os.remove(pdf_output_path)
    else:
        st.write("No analyzed data found. Please analyze data first in the 'Summary' page.")
