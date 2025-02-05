import io
import cv2
import json
import base64
import requests

detection_boxes = []
detection_scores = []

# Construct API parameters and URL. The API endpoint URL is https://object- detection6.p.rapidapi.com/objectdetect
# Replace SIGN-UP-FOR-KEY below with your RapidAPI API-key which is obtained after subscription  
url = "https://object-detection6.p.rapidapi.com/objectdetect"
headers = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "object-detection6.p.rapidapi.com", 
        "X-RapidAPI-Key": "SIGN-UP-FOR-KEY"
}
# Start webcam to record video using OpenCV
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        ret, frame = cap.read()
        while not ret:
            ret, frame = cap.read()

    height = frame.shape[0]
    width = frame.shape[1]
    

    file = 'live.png'
    cv2.imwrite( file,frame)
    with io.open("live.png", 'rb') as image_file:
        content = image_file.read()
    
    # Encode an image file from the video into Base64 format
    encoded_string = base64.b64encode(content).decode('utf-8')

    payload = { "b64image": encoded_string}
    
    # Upload image to TenaxisAI API endpoint for analysis
    http_response = requests.request("POST", url, json=payload, headers=headers)
    response = http_response.json()

    # Parse JSON response from TenaxisAI API
    objectAnnotations = response['response'][0]
    Annotations = objectAnnotations['objectAnnotations']

    # Window name in which image is displayed
    window_name = "Object Detection"
    index = 0
    for anno_index in Annotations:
        vertices = Annotations[index]['vertices']
        
        # Starting coordinate
        # represents the bottom left corner of rectangle
        xmin = int(float(vertices['xmin'])*width)
        ymin = int(float(vertices['ymin'])*height)        
        start_point = (xmin, ymin)

  
        # Ending coordinate
        # represents the top right corner of rectangle
        xmax = int(float(vertices['xmax'])*width)
        ymax = int(float(vertices['ymax'])*height)    
        end_point = (xmax, ymax)
  
        # Blue color in BGR
        blue = (255, 0, 0)

        # Red color in BGR
        red = (0, 0, 255)
  
        # Line thickness of 1 px
        thickness = 1

        # Get detected object label 
        label = Annotations[index]['label']

        # Get how score of the detected object
        rating = Annotations[index]['probability']

        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 1 px
        # Add text showing object name and probability
        frame = cv2.rectangle(frame, start_point, end_point, red, thickness)
        cv2.putText(frame, label+" "+rating, (xmin, ymin+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, blue, 2)
        index = index + 1

    # Displaying the image 
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
