from verify_pdf import verify_directory_and_pdfs

import pdfplumber
import pandas as pd
import os


def get_start_index(table):
    """
    Returns the starting row index for non-header cell values in the extracted table.
    """
    for row_index, rows in enumerate(table):
        if rows[0] != '' and rows[0] is not None:
            start_index = row_index
            break
    return start_index


def get_clean_rows(table, start_index):
    """
    Takes the starting index from the previous function and returns cell values != None for rows.
    """
    clean_rows = []

    for row_index in range(start_index, len(table)):
        clean_row = []
        for attribute_index in range(len(table[row_index])):
            if table[row_index][attribute_index] is not None:
                clean_row.append(table[row_index][attribute_index])
        clean_rows.append(clean_row)
    return clean_rows


def get_filtered_headers(table, start_index):
    """
    Returns clean headers from rows (lists from pdfplumber's extract_tables() method).
    It uses the starting index to identify rows before cell values, i.e., header values.
    """
    headers_list = []

    for row_index in range(1, start_index):
        for attribute_index, attribute_value in enumerate(table[row_index]):
            if attribute_value is not None and attribute_value != '':
                headers_list.append([attribute_index, attribute_value])

    sorted_headers = sorted(headers_list, key=lambda header: header[0])

    merged_headers = {}
    for sorted_header in sorted_headers:
        if sorted_header[0] not in merged_headers:
            merged_headers[sorted_header[0]] = '' + sorted_header[1]
        else:
            merged_headers[sorted_header[0]] += f' {sorted_header[1]}'

    filtered_headers = list(merged_headers.values())

    return filtered_headers


def extract_tables_and_generate_csv(pdf_path, output_path, password=None):
    """
    Utilizes all three previous functions to generate a CSV file for the extracted table.
    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with pdfplumber.open(pdf_path, password=password) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables_in_page = page.extract_tables()
            all_tables.extend(tables_in_page)
        pdf.close()

    for idx, table in enumerate(all_tables):
        start_index = get_start_index(table)
        clean_rows = get_clean_rows(table, start_index)
        headers = get_filtered_headers(table, start_index)

        table_data = []
        for clean_row in clean_rows:
            row_dict = {}
            for header, cell_value in zip(headers, clean_row):
                row_dict[header] = cell_value
            table_data.append(row_dict)

        df = pd.DataFrame(table_data)
        file_name = os.path.basename(pdf_path).split('.')[0]
        df.to_csv(f'{output_path}/{file_name}_table_{idx + 1}.csv', index=False)
        print('CSV files generated.')


if __name__ == '__main__':
    pdf_files, output_path, pdf_password = verify_directory_and_pdfs()
    for file in pdf_files:
        extract_tables_and_generate_csv(file, output_path, pdf_password)
