import time
import cv2
import os

def detect_cars(video_path, file_counter):
    print(f'Processing file {file_counter}: {video_path}...')
    # Read the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize the background subtraction model
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    # Set a counter to keep track of the number of frames processed
    frame_count = 0

    # Loop through each frame of the video
    counter = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # Check if we have reached the end of the video
        if not ret:
            break

        # Increment the frame counter
        frame_count += 1

        # Skip frames if necessary
        if frame_count % 35 != 0:
            continue

        # Apply background subtraction to the frame
        fg_mask = bg_subtractor.apply(frame)

        # Apply morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        # Find contours in the foreground mask
        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through each contour
        for contour in contours:
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Only consider contours that are larger than a certain size
            if w * h > 5000:
                # Let the frame skip a little to capture the car in the middle of the screen
                skip_frames = 8
                for i in range(skip_frames):
                    _, frame = cap.read()
                    frame_count += 1

                # get the filename form the path
                filename = video_path.split('\\')[-1]

                folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'output_' + filename)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                save_path = os.path.join(folder_path, str(frame_count) + '_car.jpg')
                cv2.imwrite(save_path, frame)
                #print(f'Frame {frame_count} saved to {save_path}...')

                # We only need at most 2 screenshots, so break out of the loop
                counter += 1
                break

    # Release the video capture object and close all windows
    cap.release()


def detect_cars_in_folder(folder_path):
    # Loop through all files and subfolders in the folder
    file_counter = 0
    with open('C:\\Users\\hwa_r\\Downloads\\ELTRAK\\video_processing_times.txt', 'w') as f:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Check if the file is a video file
                if file.endswith('.mp4') or file.endswith('.avi'):
                    # Call the detect_cars function on the video file and measure the elapsed time
                    print(f'Processing file {file_counter}: {file}...')
                    video_path = os.path.join(root, file)
                    start_time = time.time()
                    detect_cars(video_path, file_counter)
                    file_counter += 1
                    elapsed_time = time.time() - start_time
                    print(f'Elapsed time: {elapsed_time:.2f} seconds , filename: {file}')
                    # Write the filename and elapsed time to the text file
                    f.write(f'{file}: {elapsed_time:.2f} seconds\n')

if __name__ == '__main__':
    print('Starting video processing...')
    # Call the detect_cars_in_folder function on the folder containing the videos
    folder_path = 'C:\\Users\\hwa_r\\Downloads\\ELTRAK\\K5'
    print('Processing folder: ' + folder_path)
    try:
        detect_cars_in_folder(folder_path)
    except Exception as e:
        print(e)
    print('Video processing complete!')
