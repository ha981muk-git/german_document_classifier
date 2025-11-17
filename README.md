Always run in colab
If project is stored in  Google Drive:

from google.colab import drive
drive.mount('/content/drive')


After mounting,  files will be visible in colab at :
/content/drive/MyDrive/your_project_folder/

install in colab ? 
!pip install -r "/content/drive/MyDrive/Projects/german_document_classifier/requirements.txt"

change to the project folder 
%cd /content/drive/MyDrive/Projects/german_document_classifier

run 

!python /content/drive/MyDrive/Projects/german_document_classifier/main.py
