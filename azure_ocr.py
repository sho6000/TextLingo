#from dotenv import load_dotenv
import os
import time
import streamlit as st

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

global cv_client

# Get Configuration Settings
#load_dotenv()
cog_endpoint ='https://visionnew3000.cognitiveservices.azure.com/'
cog_key ='95f135cd76d141e595f2ffe607558453'

#To fix this error, you need to modify the GetTextRead function to accept the binary data of the image directly,
#  instead of a file path. Then, you can use the image_data directly in the function, without the need for the open() function.

#Here's how you can modify the GetTextRead function:

credential = CognitiveServicesCredentials(cog_key) 
cv_client = ComputerVisionClient(cog_endpoint, credential)
#image_file = os.path.join('images','temp_image.jpg')
    
def GetTextRead(image_file):
    print('Reading text in {}\n'.format(image_file))
    #print('Reading text in the uploaded image...\n')
    # Use Read API to read text in image
    with open(image_file, mode="rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)

    # Get the async operation ID so we can check for the results
    operation_location = read_op.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the asynchronous operation to complete
    while True:
        read_results = cv_client.get_read_result(operation_id)
        if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    # If the operation was successfully, process the text line by line
    if read_results.status == OperationStatusCodes.succeeded:
        extracted_text = ""
        for page in read_results.analyze_result.read_results:
            for line in page.lines:
                extracted_text += line.text + "\n"

        return extracted_text
                #return line.text
                # Uncomment the following line if you'd like to see the bounding box 
                #print(line.bounding_box)
    else:
        print(f"Text extraction failed with status code: {read_results.status}")
        return None
