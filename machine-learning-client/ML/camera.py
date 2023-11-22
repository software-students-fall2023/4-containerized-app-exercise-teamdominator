import cv2
import os
import time

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set the directory for saving images (current directory in this case)
save_path = './camera_data/'
if not os.path.exists(save_path):
    os.makedirs(save_path)


frame_count = 0
start_time = time.time()
last_saved_time = start_time

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()

        # Display the frame
        cv2.imshow('Frame', frame)

        # Save an image every 3 seconds
        if current_time - last_saved_time > 3:
            frame_filename = os.path.join(save_path, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
            last_saved_time = current_time

        # Break the loop and shut down the camera after 10 seconds
        if current_time - start_time > 10:
            break

        # Press 'q' to quit early (optional)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
