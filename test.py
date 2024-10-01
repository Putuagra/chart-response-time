import pandas as pd
import win32com.client as win32
from PIL import Image
import os

def convert_csv(csv_name, excel_name):
    df_csv = pd.read_csv(csv_name, sep="|", header=0)
    percentage_df = df_csv.copy()
    for col_num in range(1, len(df_csv.columns) - 1): 
        percentage_df[df_csv.columns[col_num]] = (df_csv[df_csv.columns[col_num]] / df_csv["total_requests"]) * 100
    with pd.ExcelWriter(excel_name, engine="xlsxwriter") as writer:
        percentage_df.to_excel(writer, index=False, sheet_name="Sheet1", startrow=0)
        workbook = writer.book
        worksheet_chart = workbook.add_worksheet("Sheet2")
        # worksheet = writer.sheets["Sheet1"]
        # df_csv = percentage_df.copy()
        chart = workbook.add_chart({"type": "column", "subtype": "stacked"})
        
        # Configure the series of the chart from the DataFrame data
        for col_num in range(1, len(percentage_df.columns) - 1):
            color = ""
            if percentage_df.columns[col_num] in ["2s-3s", "3s-4s"]:
                color = "#32CD32"
            elif percentage_df.columns[col_num] == "4s-5s":
                color = "#FF4500"
            elif percentage_df.columns[col_num] in ["5s-6s", "6s-7s", "7s-8s"]:
                color = "#FFD700"
            elif percentage_df.columns[col_num] in ["8s-9s", "9s-10s", ">10s"]:
                color = "red"
            
            chart.add_series(
                {
                    "name": ["Sheet1", 0, col_num],
                    # 'categories': ['Sheet1', 1, 0, len(df)-1, 0],
                    # 'values':     ['Sheet1', 1, col_num, len(df)-1, col_num],
                    "categories": ["Sheet1", 1, 0, 20, 0],
                    "values": ["Sheet1", 1, col_num, 20, col_num],
                    "gap": 5,
                    "fill": {"color": color},
                }
            )

        # Configure the chart axes
        chart.set_y_axis(
            {
                "major_gridlines": {"visible": False},
                "format": "#.0%",
                'min': 0, 
                'max': 100,
            }
        )

        chart.set_size({"width": 1000, "height": 400})

        # Insert the chart into the worksheet
        # worksheet.insert_chart("M2", chart)
        worksheet_chart.insert_chart("A1", chart)
        
def convert_pdf():
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False

    workbook = excel.Workbooks.Open(r"E:\Metrodata\BNI\Backend-resptime\backend.xlsx")
    
    # Activate Sheet2
    sheet2 = workbook.Sheets("Sheet2")
    
    chart_object = sheet2.ChartObjects(1)  # Assuming the first chart on the sheet
    chart_image_path = r"E:\Metrodata\BNI\Backend-resptime\chart_image.png"
    chart_object.Chart.Export(chart_image_path, "PNG")
    
    # Close the workbook
    workbook.Close(False)
    
    # Step 3: Rotate the image using PIL
    img = Image.open(chart_image_path)
    img_rotated = img.rotate(0, expand=True)  # Rotate 90 degrees to the right
    rotated_image_path = r"E:\Metrodata\BNI\Backend-resptime\rotated_chart_image.png"
    img_rotated.save(rotated_image_path)

    # Step 4: Save the rotated image as a PDF
    pdf_path = r"E:\Metrodata\BNI\Backend-resptime\chart.pdf"
    img_rotated.save(pdf_path, "PDF", resolution=100.0)

    # Clean up: Remove the temporary image file if needed
    if os.path.exists(chart_image_path):
        os.remove(chart_image_path)
    
    # Quit Excel
    excel.Quit()


def main():
    convert_csv("backend_resp_time_v2.csv", "backend.xlsx")
    convert_pdf()

if __name__ == "__main__":
    print("Running.....")
    main()
