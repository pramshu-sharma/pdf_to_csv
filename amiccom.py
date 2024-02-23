from verify_pdf import verify_directory_and_pdfs

import pdfplumber
import pandas as pd
import os


def process_table_1_and_3(table, table_index, output_path, file):
    """
    Process tables 1 and 3 data and save it to a CSV file.
    Headers and rows are assumed to be arranged correctly and do not need processing.
    """
    table_headers = table[0]
    table_list = []

    for index_row in range(1, len(table)):
        dict_append = {}
        for headers, rows in zip(table_headers, table[index_row]):
            dict_append[headers] = rows
        table_list.append(dict_append)

    df = pd.DataFrame(table_list)
    file_name = os.path.basename(file).split('.')[0]
    df.to_csv(f'{output_path}/{file_name}_table_{table_index + 1}.csv', index=False)


def process_table_2(table, table_index, output_path, file):
    """
    Process table 2 data and save it to a CSV file.
    Headers are processed by concatenating values in the header row.
    'None' values are omitted from rows.
    """

    header_row = table[0]

    clean_headers = []
    for index, header in enumerate(header_row):
        if header == 'F' and header_row[index + 1] == 'D[7:0]':
            clean_headers.append((header + header_row[index + 1]))
            header_row.pop(index)

        if header != '' and header != 'F':
            clean_headers.append(header)

    clean_rows = []
    for row_index in range(1, len(table)):
        clean_row = []
        for attribute_index in range(len(table[row_index])):
            if table[row_index][attribute_index] is not None:
                clean_row.append(table[row_index][attribute_index])
        clean_rows.append(clean_row)

    table_data = []
    for list_rows in clean_rows:
        row_dict = {}
        for header, row in zip(clean_headers, list_rows):
            row_dict[header] = row
        table_data.append(row_dict)

    df = pd.DataFrame(table_data)
    file_name = os.path.basename(file).split('.')[0]
    df.to_csv(f'{output_path}/{file_name}_table_{table_index + 1}.csv', index=False)


def process_table_4(table, table_index, output_path, file):
    """
    Process table 4 data and save it to a CSV file.
    Headers are corrected by removing '' values from rows.
    'None' values are omitted from rows.
    """
    headers = table[0]
    filtered_headers = []
    for header in headers:
        if header != '':
            filtered_headers.append(header)

    table_data = []

    for index_row in range(1, len(table)):
        dict_append = {}
        clean_row = []

        for unfiltered_rows in table[index_row]:
            if unfiltered_rows is not None:
                clean_row.append(unfiltered_rows)

        for headers, clean_rows in zip(filtered_headers, clean_row):
            dict_append[headers] = clean_rows
        table_data.append(dict_append)

    df = pd.DataFrame(table_data)
    file_name = os.path.basename(file).split('.')[0]
    df.to_csv(f'{output_path}/{file_name}_table_{table_index + 1}.csv', index=False)


def process_table_5(table, table_index, output_path, file):
    """
    Process table 5 data and save it to a CSV file.
    Headers are corrected by concatenating values from two separate rows.
    'None' values are omitted from rows.
    """
    header_row1 = table[0]
    header_row2 = table[1]
    clean_headers = []
    for row1, row2 in zip(header_row1, header_row2):
        if row1 is not None and row1 != '' and row2 is None:
            clean_headers.append(row1)
        elif row1 is not None and row2 != '' and row2 is not None:
            clean_headers.append(f'{row1}\n{row2}')

    clean_rows = []
    for row_index in range(2, len(table)):
        clean_row = []
        for attribute_index in range(len(table[row_index])):
            if table[row_index][attribute_index] is not None:
                clean_row.append(table[row_index][attribute_index])
        clean_rows.append(clean_row)

    table_data = []
    for list_rows in clean_rows:
        row_dict = {}
        for header, row in zip(clean_headers, list_rows):
            row_dict[header] = row
        table_data.append(row_dict)

    df = pd.DataFrame(table_data)
    file_name = os.path.basename(file).split('.')[0]
    df.to_csv(f'{output_path}/{file_name}_table_{table_index + 1}.csv', index=False)


def extract_tables_and_generate_csv(pdf_path, output_path, password=None):
    """
    Loops through the tables in the PDF and extracts data using functions and table index.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with pdfplumber.open(pdf_path, password=password) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

        for table_index, table in enumerate(tables):
            if table_index == 0 or table_index == 2:
                process_table_1_and_3(table, table_index, output_path, pdf_path)
            if table_index == 1:
                process_table_2(table, table_index, output_path, pdf_path)
            if table_index == 3:
                process_table_4(table, table_index, output_path, pdf_path)
            if table_index == 4:
                process_table_5(table, table_index, output_path, pdf_path)
        pdf.close()
        print('CSV files generated.')


if __name__ == '__main__':
    pdf_files, output_path, pdf_password = verify_directory_and_pdfs()
    for file in pdf_files:
        extract_tables_and_generate_csv(file, output_path, pdf_password)
