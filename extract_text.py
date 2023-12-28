# importing required modules
from PyPDF2 import PdfReader

if __name__ == '__main__':
    # creating a pdf reader object
    reader = PdfReader('/Users/xhs/Downloads/add_project.pdf')

    # printing number of pages in pdf file
    print(len(reader.pages))

    # getting a specific page from the pdf file
    page = reader.pages[0]

    # extracting text from page
    text = page.extract_text()
    print(text)
