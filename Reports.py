import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64
import os
# os.chdir("P:\PyCharm Selenium Practice\pythonProject\Sentiment Analysis\example app\TestingApp")

# Function to generate PDF report
def generate_pdf_report(analyzed_data, count_plot_image, pie_chart_image, include_countplot,
        include_piechart, include_meta_data, include_top_comments, highest_count_label, brand_name,  brand_category,
                        channel_names, video_links, top_positive_comments, top_negative_comments, top_neutral_comments,
                            total_comments_count, positive_comments_count, negative_comments_count, neutral_comments_count):
    # Create a new PDF canvas
    pdf_filename = f"{brand_name}_analysis_report.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    width, _ = letter
    pdfmetrics.registerFont(TTFont('tahoma-bold', 'tahoma-bold.ttf'))
    pdfmetrics.registerFont(TTFont('Segoe UI Emoji', 'seguiemj.ttf'))

    # Add title and data description on Page 1
    # pdf.drawString(150, 750, f"Sentiment Analysis Report for {brand_name}")
    # pdf.setFont("Helvetica", 12)
    # pdf.drawString(50, 700, "Data Description:")
    # text = analyzed_data.head().to_string()
    # y = 680
    # for line in text.split('\n'):
    #     pdf.drawString(50, y, line)
    #     y -= 12
    # pdf.showPage()

    # Load image and get its dimensions
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

    # Page 1: Sentiment Analysis Report with Brand Name centered
    pdf.setFont("Helvetica", 25)
    title_width = pdf.stringWidth("Sentiment Analysis Report")
    center_x = width / 2 - title_width / 2
    pdf.drawString(center_x, 700, "Sentiment Analysis Report")

    pdf.setFont("tahoma-bold", 40)
    brand_name_width = pdf.stringWidth(brand_name)
    center_x = width / 2 - brand_name_width / 2
    pdf.drawString(center_x, 450, brand_name)

    pdf.setFont("Helvetica", 18)

    category_text_width = pdf.stringWidth(f"Brand Category: {brand_category}")
    center_x = width / 2 - category_text_width / 2
    pdf.drawString(center_x, 200, f"Brand Category: {brand_category}")

    from_text_width = pdf.stringWidth("Data from: YouTube")
    center_x = width / 2 - from_text_width / 2
    pdf.drawString(center_x, 150, "Data from: YouTube")

    status_text_width = pdf.stringWidth(f"Status: {brand_name} has {highest_count_label} side as you see!")
    center_x = width / 2 - status_text_width / 2
    pdf.drawString(center_x, 100, f"Status: {brand_name} has {highest_count_label} side as you see!")

    pdf.showPage()


    # Page 2: List of Channel Names and Video Links
    if include_meta_data:
        pdf.setFont("Helvetica", 20)
        pdf.drawString(50, 700, "List of Channel Names and Video Links")
        y_position = 650
        # for channel_name, video_link in zip(channel_names, video_links):
        for idx, (channel_name, video_link) in enumerate(zip(channel_names, video_links), 1):
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, y_position, f"{idx}. Channel Name: {channel_name}") # - https: // www.youtube.com / @ {channel_name[:channel_name.index(' ')]}
            pdf.drawString(50, y_position - 20, f"       Video Link: {video_link}")
            y_position -= 50
            if y_position < 50:
                pdf.showPage()
                y_position = 750
        pdf.showPage()

    # Function to draw comments with proper alignment
    def draw_comments(comments, title, start_y):
        pdf.setFont("Segoe UI Emoji", 18)
        pdf.drawString(50, start_y, title)
        y_position = start_y - 30  # Start position below the title
        for idx, comment in enumerate(comments, 1):
            comment_text = comment['Comment']
            like_count = comment['Like Count']
            pdf.setFont("Segoe UI Emoji", 8)
            pdf.drawString(50, y_position, f"{idx}. {comment_text} (Likes: {like_count})")
            y_position -= 20  # Vertical spacing between comments


    # Page 3: Top Comments
    if include_top_comments:
        pdf.setFont("Helvetica", 20)
        pdf.drawString(220, 750, "TOP COMMENTS")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 700, f"Total comments Count - {total_comments_count}")
        pdf.drawString(50, 660, f"Positive Comments Count - {positive_comments_count}")
        pdf.drawString(50, 620, f"Negative Comments Count - {negative_comments_count}")
        pdf.drawString(50, 580, f"Neutral Comments Count - {neutral_comments_count}")

        start_y = 520  # Starting Y position for the first section
        draw_comments(top_positive_comments, "Top Positive Comments:", start_y)

        start_y -= len(top_positive_comments) * 20 + 50  # Adjust Y position for next section
        draw_comments(top_negative_comments, "Top Negative Comments:", start_y)

        start_y -= len(top_negative_comments) * 20 + 50  # Adjust Y position for next section
        draw_comments(top_neutral_comments, "Top Neutral Comments:", start_y)

        pdf.showPage()


    # Page 4: Countplot
    if include_countplot:
        # Add count-plot with title on Page 2
        pdf.setFont("Helvetica", 16)
        pdf.drawString(250, 700, "COUNT-PLOT")
        # Calculate center coordinates for the image
        x_center = (pdf._pagesize[0] - 500) / 2
        y_center = (pdf._pagesize[1] - 300) / 2
        pdf.drawImage(count_plot_image, x_center, y_center, width=500, height=300)
        pdf.showPage()

    # Page 5: Pie-Chart
    if include_piechart:
        # Add pie-chart with title on Page 3
        pdf.setFont("Helvetica", 16)
        pdf.drawString(250, 700, "PIE-CHART")
        # Calculate center coordinates for the image
        x_center = (pdf._pagesize[0] - 500) / 2
        y_center = (pdf._pagesize[1] - 300) / 2
        pdf.drawImage(pie_chart_image, x_center, y_center, width=500, height=300)
        pdf.showPage()

    # Add status on the last page
    # pdf.drawString(150, 750, f"Status : {brand_name} has {highest_count_label} side as you see!")
    # pdf.setFont("Helvetica", 12)

    # Save the PDF file
    pdf.save()
    return pdf_filename

def report_gen():
    st.write("Generate PDF Report:")
    analyzed_data = st.session_state.get('analyzed_data')
    count_plot_image = st.session_state.get('count_plot_image')
    pie_chart_image = st.session_state.get('pie_chart_image')
    highest_count_label = st.session_state.get('highest_count_label')
    brand_name = st.session_state.get('brand_name')
    brand_category = st.session_state.get('brand_category')
    channel_names = st.session_state.get('channel_names')
    video_links = st.session_state.get('video_links')
    top_positive_comments = st.session_state.get('top_positive_comments')
    top_negative_comments = st.session_state.get('top_negative_comments')
    top_neutral_comments = st.session_state.get('top_neutral_comments')

    total_comments_count = st.session_state.get('total_comments_count')
    positive_comments_count = st.session_state.get('positive_comments_count')
    negative_comments_count = st.session_state.get('negative_comments_count')
    neutral_comments_count = st.session_state.get('neutral_comments_count')

    include_meta_data = st.checkbox("Include Meta Data")
    include_top_comments = st.checkbox("Include Top Comments")
    include_countplot = st.checkbox("Include Count Plot")
    include_piechart = st.checkbox("Include Pie Chart")
    if analyzed_data is not None:
        if st.button(":white_check_mark: Generate Report"):
            pdf_output_path = generate_pdf_report(analyzed_data, count_plot_image, pie_chart_image, include_countplot,
                        include_piechart, include_meta_data, include_top_comments, highest_count_label, brand_name,  brand_category, channel_names,
                            video_links, top_positive_comments, top_negative_comments, top_neutral_comments,
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
