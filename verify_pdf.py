import os
import pdfplumber


def verify_directory_and_pdfs():
    """
    Takes user input for pdf files directory, output path for csv and password for encrypted PDF files.
    """
    while True:
        pdf_path = str(
            input('Please provide the directory for the PDF file(s). e.g. C:/pdf_files (Type quit to Exit)\n'))
        if pdf_path == 'quit':
            break
        output_path = str(input('Please input the CSV output directory.\n'))
        pdf_password = str(input('Please input the password for the file(s). (Leave blank for no password)\n'))

        # Check if path exists.
        if not os.path.exists(pdf_path):

            print('The provided path does not exist, please enter a valid path.\n')
        else:
            # Creates a list of pdf files for extraction, if no PDF files are found returns an error message.
            pdf_files = [f'{pdf_path}/' + file for file in os.listdir(pdf_path) if file.endswith('.pdf')]

            if len(pdf_files) == 0:
                print('No PDF files found, please check your directory.\n')
            else:
                break
    try:
        for file in pdf_files:
            try:
                with pdfplumber.open(file, password=pdf_password) as pdf:
                    # Checks the provided password with encrypted PDF files.
                    pass
                    pdf.close()
            except Exception as e:
                print(f'Incorrect password for file: {file}, please re-try.\n')
    except NameError:
        pass
    # If all checks are okay, returns the objects below.
    return pdf_files, output_path, pdf_password
