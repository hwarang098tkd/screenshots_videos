import argparse
import os
import time
import cv2

def detect_objects(video_path, file_counter, skip_frames, mode):
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

        # Apply background subtraction to the frame
        fg_mask = bg_subtractor.apply(frame)

        # Apply morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        # Find contours in the foreground mask or detect objects using HOG descriptor
        if mode == 'mode1':
            contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        elif mode == 'mode2':
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            # Detect people in the frame using HOG descriptor
            rects, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.05)

        # Loop through each contour or detected object
        if mode == 'mode1':
            for contour in contours:
                # Get the bounding box of the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Only consider contours that are larger than a certain size
                if w * h < 20000:
                    continue

                # Let the frame skip a little to capture the object in the middle of the screen
                for i in range(skip_frames):
                    _, frame = cap.read()
                    frame_count += 1

                # Draw a red rectangle around the object
                thickness = 1
                color = (0, 0, 250)  # red color in BGR format
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

                # Save the frame as an image file
                filename = video_path.split('\\')[-1]
                folder_path = os.path.join(os.path.expanduser('~'), 'output_' + filename)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                save_path = os.path.join(folder_path, f'frame_{frame_count}_{mode}.jpg')
                cv2.imwrite(save_path, frame)
                print("Saved.." + save_path)

                # We only need at most 2 screenshots, so break out of the loop
                counter += 1
                if counter == 2:
                    break


        elif mode == 'mode2':

            hog = cv2.HOGDescriptor()

            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

            #car_cascade = cv2.CascadeClassifier('cars.xml')
            car_cascade = cv2.CascadeClassifier('C:\\Users\\hwa_r\\Downloads\\cars.xml')

            # Detect people in the frame using HOG descriptor

            rects_people, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.05)

            # Detect cars in the frame using Haar Cascade Classifier

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects_cars = car_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(10, 10))

            # Loop through each detected person and draw a bounding box and label

            # for (x, y, w, h) in rects_people:
            #
            #     # Only consider people that are larger than a certain size
            #
            #     if w * h < 5000:
            #         continue
            #
            #     # Let the frame skip a little to capture the object in the middle of the screen
            #
            #     for i in range(skip_frames):
            #         _, frame = cap.read()
            #
            #         frame_count += 1
            #
            #     # Draw a red rectangle around the person
            #
            #     thickness = 2
            #
            #     color = (0, 0, 200)  # red color in BGR format
            #
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
            #
            #     # Add label with the name of the detected object
            #
            #     cv2.putText(frame, 'Person', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)
            #
            #     # Save the frame as an image file
            #
            #     filename = video_path.split('\\')[-1]
            #
            #     folder_path = os.path.join(os.path.expanduser('~'), 'output_' + filename)
            #
            #     if not os.path.exists(folder_path):
            #         os.makedirs(folder_path)
            #
            #     save_path = os.path.join(folder_path, f'frame_{frame_count}_{mode}.jpg')
            #
            #     cv2.imwrite(save_path, frame)
            #
            #     # Continue to the next iteration of the loop to detect all objects in the frame
            #
            #     counter += 1
            #
            #     if counter == 2:
            #         break

            for (x, y, w, h) in rects_cars:
                # Only consider cars that are larger than a certain size
                # if w * h < 25000:
                #     continue

                # Let the frame skip a little to capture the object in the middle of the screen
                for i in range(skip_frames):
                    _, frame = cap.read()
                    frame_count += 1

                # Draw a green rectangle around the car
                thickness = 2
                color = (0, 255, 0)  # green color in BGR format
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
                # Add label with the name of the detected object
                cv2.putText(frame, 'Car', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)

                # Save the frame as an image file
                filename = video_path.split('\\')[-1]
                folder_path = os.path.join(os.path.expanduser('~'), 'output_' + filename)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                save_path = os.path.join(folder_path, f'frame_{frame_count}_{mode}.jpg')
                cv2.imwrite(save_path, frame)
                # Continue to the next iteration of the loop to detect all objects in the frame
                counter += 1
                if counter == 2:
                    break

            # for (x, y, w, h) in rects:
            #     # Only consider people that are larger than a certain size
            #     if w * h < 5000:
            #         continue
            #
            #     # Let the frame skip a little to capture the object in the middle of the screen
            #     for i in range(skip_frames):
            #         _, frame = cap.read()
            #         frame_count += 1
            #
            #     # Draw a red rectangle around the person
            #     thickness = 2
            #     color = (0, 0, 200)  # red color in BGR format
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
            #     # Add label with the name of the detected object
            #     cv2.putText(frame, 'Person', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)
            #
            #     # Save the frame as an image file
            #     filename = video_path.split('\\')[-1]
            #     folder_path = os.path.join(os.path.expanduser('~'), 'output_' + filename)
            #
            #     if not os.path.exists(folder_path):
            #         os.makedirs(folder_path)
            #
            #     save_path = os.path.join(folder_path, f'frame_{frame_count}_{mode}.jpg')
            #     cv2.imwrite(save_path, frame)
            #     # Continue to the next iteration of the loop to detect all objects in the frame
            #     counter += 1
            #     if counter == 2:
            #         break

    cap.release()

def detect_cars_in_folder(folder_path, skip_frames, mode):
    # Loop through all files and subfolders in the folder
    file_counter = 0
    with open(os.path.join(os.getcwd(), 'video_processing_times.txt'), 'w') as f:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Check if the file is a video file
                if file.endswith('.mp4') or file.endswith('.avi') or file.endswith('.dav'):
                    # Call the detect_cars function on the video file and measure the elapsed time
                    print(f'Processing file {file_counter}: {file}...')
                    video_path = os.path.join(root, file)
                    start_time = time.time()
                    detect_objects(video_path, file_counter, skip_frames, mode)
                    file_counter += 1
                    elapsed_time = time.time() - start_time
                    print(f'Elapsed time: {elapsed_time:.2f} seconds, filename: {file}')
                    # Write the filename and elapsed time to the text file
                    f.write(f'{file}: {elapsed_time:.2f} seconds\n')
                else:
                    print('File is not a video file or not supported(yet): ' + file)


if __name__ == '__main__':
    print('Starting video processing...')
    # Create argument parser
    parser = argparse.ArgumentParser(description='Detect cars in videos and capture screenshots.')
    parser.add_argument('--folder_path', '-fpath', type=str, default='E:\Κάμερα Θριάσειο - Λαφαζάνης (8-5 ως 14-5)',
                        help='Path to the folder containing the videos.')
    parser.add_argument('--skip_frames', '-sf', type=int, default=4,
                        help='Number of frames to skip before checking for cars.')

    parser.add_argument('--mode', '-m', type=str, default='mode1',
                        help='Mode to use for detecting objects. mode1: contours, mode2: HOG descriptor')
    args = parser.parse_args()

    # Prompt user to enter folder path if not provided
    if not args.folder_path:
        folder_path = input('Enter the path to the folder containing the videos: ')
    else:
        folder_path = args.folder_path

    # Call the detect_cars_in_folder function on the folder containing the videos
    print(f'Processing folder: {folder_path}')

    # print the selected mode
    print(f'Using mode: {args.mode}')
    detect_cars_in_folder(folder_path, args.skip_frames, args.mode)

    print('Video processing complete!')
