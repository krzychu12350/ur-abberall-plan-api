# from fastapi import FastAPI, __version__, HTTPException, UploadFile
# from fastapi.responses import JSONResponse
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from collections import defaultdict
# from datetime import datetime
# from typing import List, Dict, Any
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
# import os
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# import json
# from datetime import datetime
# import openpyxl
# import re
# import openpyxl
# import re
# from datetime import datetime
# # Lo
# # ad environment variables from .env file
# load_dotenv()
#
# # Initialize Cloudinary
# cloudinary.config(
#     cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )
#
# import openpyxl
# import re
# from datetime import datetime
#
# # Precompile the regular expression for date extraction
# pattern = re.compile(r'\b\w+\s(\d{1,2})\.(\d{1,2})\.(\d{4})\b')
#
#
# def split_time_range(time_range):
#     if ' - ' in time_range:
#         return time_range.split(' - ')
#     elif '- ' in time_range:
#         return time_range.split('- ')
#     else:
#         return None, None  # In case the format is unexpected
#
# # Optimize the word removal by using a set for faster lookup
# def remove_words_from_string(input_string, words_to_remove):
#     words_to_remove_set = set(words_to_remove)
#     return ' '.join(word for word in input_string.split() if word not in words_to_remove_set)
#
#
# def find_nearest_godzina(sheet, col, start_row):
#     """Find the nearest cell with value 'GODZINA' above the specified row in the given column."""
#     for row in range(start_row - 1, 0, -1):  # Go upwards from start_row
#         cell_value = sheet.cell(row=row, column=col).value
#         if isinstance(cell_value, str) and cell_value.strip() == 'GODZINA':
#             return row
#     return None
#
#
# def extract_date(text):
#     """Extract and format the date from text using a precompiled regex."""
#     match = pattern.search(text)
#     if match:
#         day, month, year = match.groups()
#         return f"{int(day):02d}.{int(month):02d}.{year}"
#     return "No date found"
#
#
# def parse_time(time_str: str) -> datetime:
#     """Parses a time string into a datetime object. Handles time ranges by returning the start time."""
#     if '-' in time_str:
#         time_str = time_str.split('-')[0].strip()  # Take the first part as the start time
#     return datetime.strptime(time_str.strip(), '%H:%M')
#
#
# def extract_data():
#     # Load the Excel workbook and sheet only once
#     workbook = openpyxl.load_workbook('./plan3.xlsx')
#     sheet = workbook['Arkusz1']  # Replace 'Arkusz1' with your actual sheet name
#
#     data_list = []
#     words_to_remove = ["PONIEDZIAŁEK", "WTOREK", "ŚRODA", "CZWARTEK", "PIĄTEK"]
#
#     # Iterate through merged cell ranges
#     for merged_range in sheet.merged_cells.ranges:
#
#         # Skip rows 1 to 3 and rows 947 till the end
#         if merged_range.bounds[1] <= 3 or merged_range.bounds[1] >= 947:
#             continue
#
#         # Get the number of cells in the merged range
#         min_row, min_col, max_row, max_col = merged_range.bounds
#
#         num_cells = (max_row - min_row + 1) * (max_col - min_col + 1)
#         # print(merged_range.bounds)
#
#         # Access the second and fourth elements
#         second_element = merged_range.bounds[1]  # Index 1 for the second element
#         fourth_element = merged_range.bounds[3]  # Index 3 for the fourth element
#         number_of_rows = fourth_element - second_element
#
#         if number_of_rows < 1:
#             continue
#
#         # Access the value of the top-left cell of the merged range
#         min_value_cell_data = sheet.cell(row=merged_range.bounds[1], column=merged_range.bounds[0]).value
#
#         # Check if the cell data is a string
#         if isinstance(min_value_cell_data, str):
#             # Remove excessive whitespace using regex
#             cleaned_text = re.sub(r'\s+', ' ', min_value_cell_data).strip()
#         else:
#             cleaned_text = str(min_value_cell_data)
#
#             # Assign time ranges from column A for each row in the merged range
#         time_ranges = []
#         for row in range(second_element, fourth_element + 1):
#             time_range = sheet.cell(row=row, column=1).value  # Assuming column A is the first column
#             time_ranges.append(time_range)
#
#         if time_ranges[0].split(' - ')[0] == 'GODZINA':
#             continue
#         else:
#             # print(time_ranges)
#             # start_time = time_ranges[0].split(' - ')[0]
#             # end_time = time_ranges[-1].split(' - ')[1]
#             # Handling start_time and end_time based on input ranges
#             start_range = time_ranges[0]
#             end_range = time_ranges[-1]
#
#             # Splitting start_time and end_time based on the delimiter found
#             start_time, _ = split_time_range(start_range)  # Only need the start part
#             _, end_time = split_time_range(end_range)  # Only need the end part
#             # Splitting the first and last elements
#             # start_time = re.split(r' - |- ', time_ranges[0])[0]
#             # end_time = re.split(r' - |- ', time_ranges[-1])[-1]
#             # print(time_ranges[0].split(' - ')[0])
#             # print(time_ranges[-1].split(' - ')[1])
#
#         nearest_godzina_row = find_nearest_godzina(sheet, 1, merged_range.bounds[1])
#
#         # column
#         # print(merged_range.bounds[0])
#
#         # row
#         # print(nearest_godzina_row)
#         # if merged_range.bounds[0] > 2 and merged_range.bounds[0] <= 6:
#         #     date_column = 3
#         # elif merged_range.bounds[0] >= 7 and merged_range.bounds[0] <= 10:
#         #     date_column = 7
#         # elif merged_range.bounds[0] >= 11 and merged_range.bounds[0] <= 14:
#         #     date_column = 11
#         # elif merged_range.bounds[0] >= 15 and merged_range.bounds[0] <= 18:
#         #     date_column = 15
#         # elif merged_range.bounds[0] >= 19 and merged_range.bounds[0] <= 22:
#         #     date_column = 19
#
#         date_column = 0
#         if 2 < merged_range.bounds[0] <= 22:
#             date_column = 3 + 4 * ((merged_range.bounds[0] - 3) // 4)
#
#         date = sheet.cell(row=nearest_godzina_row, column=date_column).value
#
#         words_to_remove = ["PONIEDZIAŁEK", "WTOREK", "ŚRODA", "CZWARTEK", "PIĄTEK"]
#
#         fromated_date = remove_words_from_string(date, words_to_remove)
#
#         # print(extract_date(date))  # Output: 06.12.2024
#
#         # print(f'Merged Range: {merged_range}, Number of Rows: { number_of_rows}, Min Value Cell Data: {cleaned_text}, Start time: {start_time}, End_time: {end_time}')
#
#         data = {
#             'text': cleaned_text,
#             'date': fromated_date,
#             'start_time': start_time,
#             'end_time': end_time,
#             # 'nearest_godzina_row': nearest_godzina_row,
#             # 'nearest_godzina_column': merged_range.bounds[0],
#             # 'lesson_block_cells_range': merged_range.bounds,
#
#         }
#         # Append each data object to the list
#         data_list.append(data)
#         # print('----------------------------')
#
#     # Convert the list of dictionaries to a JSON array of objects
#     # json_data = json.dumps(data_list, indent=4, ensure_ascii=False)
#
#     # Print the resulting JSON array
#     # print(json_data)
#
#     # Sort the data list by start_time in ascending order
#     data_list.sort(key=lambda x: parse_time(x['start_time']))
#     return data_list
#
#
# origins = ["*"]
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # app.include_router(system.router, prefix="/system")
#
#
# @app.get("/statuss")
# def status():
#     return {"ok": True, "version": __version__}
#
#
# @app.get("/")
# def status():
#     return {"ok": True, 'page': 'home'}
#
#
# @app.get("/api/schedules", response_model=Dict[str, List[Dict[str, Any]]])
# async def get_schedules():
#     data = extract_data()
#
#     # Group schedules by date
#     grouped_schedules = defaultdict(list)
#
#     for schedule in data:
#         grouped_schedules[schedule['date']].append(schedule)
#
#     # Sort the grouped schedules by date
#     sorted_grouped_schedules = dict(
#         sorted(grouped_schedules.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y')))
#
#     return sorted_grouped_schedules
#
#
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         # Upload file to Cloudinary
#         response = cloudinary.uploader.upload(file.file)
#         return JSONResponse(content={"url": response['url'], "public_id": response['public_id']})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @app.get("/file/{public_id}")
# async def get_file(public_id: str):
#     try:
#         # Fetch file details from Cloudinary
#         response = cloudinary.api.resource(public_id)
#         return JSONResponse(content={"url": response['url'], "public_id": response['public_id'], "format": response['format']})
#     except cloudinary.exceptions.NotFound:
#         raise HTTPException(status_code=404, detail="File not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

from app.main import app
