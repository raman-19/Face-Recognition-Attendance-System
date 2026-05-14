import cv2
from datetime import datetime

# Load Haar Cascade Face Detector
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Start Webcam
cap = cv2.VideoCapture(0)

# Attendance Function
def markAttendance():
    with open('Attendance.csv', 'a') as f:
        now = datetime.now()

        time = now.strftime('%H:%M:%S')
        date = now.strftime('%d/%m/%Y')

        f.write(f'Present,{time},{date}\n')

attendanceMarked = False

while True:

    # Read webcam frame
    success, img = cap.read()

    if not success:
        print("Failed to capture image from webcam")
        break

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw rectangle around detected face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            img,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Mark attendance only once
        if not attendanceMarked:

            markAttendance()
            attendanceMarked = True

            print("Attendance Stored Successfully")

            # Show window briefly before closing
            cv2.imshow("Attendance System", img)
            cv2.waitKey(2000)

            # Close camera
            cap.release()
            cv2.destroyAllWindows()

            # Stop loop
            exit()

    # Show webcam window
    cv2.imshow("Attendance System", img)

    # Press q to quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera properly
cap.release()
cv2.destroyAllWindows()