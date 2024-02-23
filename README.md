PDF to CSV converter

Steps to setup:

1. Open 'cmd' or terminal to create python virtual environment. 'virtualenv venv'
2. Activate virtual environment. 'venv/scripts/Activate'
3. Clone repository. 'git clone https://github.com/pramshu-sharma/pdf_to_csv'
4. Navigate to project directory. 'cd pdf_to_csv'
5. Install requirements.txt. 'pip install -r requirements.txt'

To use the application please see 'example_use.mp4'.

Application Details:

- Parsers are named according to the type of PDF. e.g. original PDF filename: pd2.pdf has been renamed to amicomm.pdf
  (as seen in the PDF file.) therefore, the parser = amiccom.py
  
- Folders should contain identical PDFs to be parsed into CSV.
  
- verify_pdf.py is used to verify: pdf files directory and password for PDF files.

Application Limitations:

- Due to time constraints a parser for pdf3.pdf i.e. diesel_engines was not made, as was for pdf1.pdf which i assume fell   
  under the corrupt PDF file category.

- Extracting data from PDFs is something that i am not much familiar with therefore,
  the algorithms used to extract data might not be the most efficient.

- Only parses documents with similar structures, error handling is limited.

Suggestions:

- The library's (pdfplumber) table_settings feature could have been used for efficient extraction but
  the learning curve was steep for the allocated time.

- Use of Regular expressions.
