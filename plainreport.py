from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# PDF report generation function
def create_pdf_report(user_name, test_name, schematic_folder, current_measurement_folder, image_folder, equip_images_folder, file_name="Test_Report.pdf"):
    # Define the folder where reports will be saved
    report_folder = "C:/Reportfiles"
    
    # Check if the folder exists; if not, create it
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    
    # Construct the full file path
    file_path = os.path.join(report_folder, file_name)

    # Create the PDF
    pdf = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Title Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2.0, height - 50, "Test Report")
    
    # Date Section
    pdf.setFont("Helvetica", 10)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.drawRightString(width - 50, height - 70, f"Date: {current_date}")
    
    # User Name
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 100, "User Name:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 100, user_name)
    
    # Test Name
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 120, "Test Name:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 120, test_name)
    
    # Function to handle image placement (horizontal layout)
    def add_images(pdf, folder_path, title, width, height, y_position, add_name_below=False, additional_space=0, limit=0):
        x_position = 50  # Starting x-position for images
        image_width = 250  # Adjust to fit 2 images per row
        image_height = 150  # Adjust for proper image height
        max_images_per_row = 2  # Limit to 2 images per row
        max_rows_per_page = 4  # Maximum 4 rows per page
        image_count = 0  # Image counter for current row
        row_count = 0  # Track the number of rows added

        # Add additional space if needed (to move the section title down)
        y_position -= additional_space

        # Title for the image section
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, title)
        y_position -= 20  # Move down after title

        # Loop through the images in the folder and add them to the report
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_path = os.path.join(folder_path, file_name)

                    # Check if limit is set and image_count exceeds the limit
                    if limit > 0 and image_count >= limit:
                        break

                    # Check if the row is full (i.e., 2 images)
                    if image_count == max_images_per_row:
                        y_position -= image_height + 40  # Move down to the next row (with space for text if required)
                        x_position = 50  # Reset x-position for the next row
                        image_count = 0  # Reset image counter for the new row
                        row_count += 1  # Increment row counter

                    # If the page is full (4 rows), start a new page
                    if row_count == max_rows_per_page:
                        pdf.showPage()
                        y_position = height - 50  # Reset y-position for the new page
                        row_count = 0  # Reset row counter for the new page
                        x_position = 50  # Reset x-position
                        image_count = 0  # Reset image count
                        
                        # Add the section title again
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(50, y_position, title)
                        y_position -= 20

                    # Add image to the PDF
                    pdf.drawImage(image_path, x_position, y_position - image_height, width=image_width, height=image_height)

                    # Add equipment name below the image if flag is true
                    if add_name_below:
                        equipment_name = os.path.splitext(file_name)[0]  # Get the name without the extension
                        pdf.setFont("Helvetica", 10)
                        pdf.drawCentredString(x_position + (image_width / 2), y_position - image_height - 10, equipment_name)

                    # Update x_position and increment image counter
                    x_position += image_width + 20
                    image_count += 1

            # Adjust final y_position after processing all images
            return y_position - image_height - 20

        return y_position

    # Add schematic images on the first page
    y_position = height - 150  # Position after test name
    y_position = add_images(pdf, schematic_folder, "Schematic Images:", width, height, y_position, add_name_below=False)

    # Move to the next page to add equipment images first
    pdf.showPage()

    # Add equipment images on the second page, with names below them
    y_position = height - 50  # Reset y-position for the new page
    y_position = add_images(pdf, equip_images_folder, "Equipment Images:", width, height, y_position, add_name_below=True)

    # Add Supply Current Graph from the current measurement folder
    # Limit the number of images to 1
    additional_space_between_sections1 = 3 
    y_position = add_images(pdf, current_measurement_folder, "Supply Current Graph:", width, height, y_position, limit=1,additional_space=additional_space_between_sections1)

    # Add some extra space between equipment and waveform sections
    additional_space_between_sections = 50  # Adjust this value to control the space between equipment images and waveform section

    # If no more space is left, move to a new page for waveform images
    if y_position < 50:  # Check if a new page is needed
        pdf.showPage()
        y_position = height - 50  # Reset y-position

    # Add waveform images after equipment images, with added space between sections
    add_images(pdf, image_folder, "Waveform Snapshots:", width, height, y_position, additional_space=additional_space_between_sections)

    # Save the PDF
    pdf.save()
    print(f"Report saved in '{file_path}' successfully!")

# Function to run the script
def main():
    # Sample user input
    user_name = "MRUNALI DALVI"
    test_name = "Supply Current Measurement Test"
    
    # Folder paths (update these paths based on your system)
    schematic_folder = "C:/Schematic_images"  # Update this to the correct path
    equip_images_folder = "C:/Equip_images"  # Update this to the correct path
    current_measurement_folder = "C:\Mesurement_Results\Current_Measurement"  # Folder for current measurement graph
    waveform_folder = "C:/Mesurement_Results/Waveforms"  # Update this to the correct path

    # Generate PDF report
    create_pdf_report(user_name, test_name, schematic_folder, current_measurement_folder, waveform_folder, equip_images_folder)

if __name__ == "__main__":
    main()
