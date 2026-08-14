# 🚨 AI Fall Detection System

An AI-based computer vision system designed to detect when a person falls using **YOLOv8 Pose Estimation, ByteTrack, OpenCV, and Python**.

The system analyzes a person's body pose, body angle, and movement speed to identify possible falls and trigger an alarm.

## ✨ Features

* 👤 Human detection
* 🦴 Pose estimation
* 🎯 Multi-person tracking
* 🆔 Person ID tracking using ByteTrack
* 📐 Body angle calculation
* 🏃 Movement speed tracking
* 🚨 Fall detection
* ⏱️ Ground-time monitoring
* 🟢 Green bounding box for normal activity
* 🔴 Red bounding box for detected falls
* ⚠️ `FALL DETECTED` alert
* 🔊 Alarm using Pygame
* 📊 Displays Person ID, Angle, and Speed

## 🧠 How It Works

The system processes the video frame-by-frame.

### 1. Person Detection

YOLOv8 Pose detects people in the video and extracts their body keypoints.

### 2. Pose Estimation

The system uses shoulder and hip positions to calculate the person's body angle.

### 3. Person Tracking

ByteTrack tracks people between frames and assigns a unique ID.

Example:

```text
ID:2
ID:8
```

### 4. Speed Tracking

The system calculates movement speed using changes in the person's hip position.

Example:

```text
ID:2  Angle:93.6  Speed:29.0
```

### 5. Fall Detection

The system combines body angle and movement speed to determine whether a person may have fallen.

When a fall is detected:

* The bounding box becomes red.
* `FALL DETECTED` is displayed.
* An alarm can be triggered.
* Ground time can be monitored.

## 🛠️ Technologies

* Python
* YOLOv8 Pose
* Ultralytics
* OpenCV
* ByteTrack
* PyTorch
* Pygame

## 📁 Project Structure

```text
Fall_Detection_Project/
│
├── main.py
│
├── detectors/
│   ├── pose_detector.py
│   └── fall_detector.py
│
├── trackers/
│   └── tracker.py
│
├── utils/
│   ├── geometry.py
│   └── speed.py
│
├── videos/
│   └── fall_test.mp4
│
├── alarm/
│   └── alarm.wav
│
├── yolov8n-pose.pt
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ashishrahar/Fall_Detection_Project.git
cd Fall_Detection_Project
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on Linux:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run

Make sure your test video is available at:

```text
videos/fall_test.mp4
```

Run the project:

```bash
python main.py
```

Press **Q** to close the video window.

## 📊 Example Output

Terminal output:

```text
ID:2  Angle:93.6  Speed:29.0
Fall Status: False
```

When a fall is detected:

```text
******** FALL DETECTED ********
```

The video window displays the person's bounding box and detection information.

## ⚠️ Current Limitations

This project is currently under development.

Detection performance may be affected by:

* Camera angle
* Lighting conditions
* Occlusion
* Multiple people
* Tracking ID changes
* Pose estimation errors
* Falls onto sofas or beds
* Slow or unusual falls

The system is currently being tested with recorded videos.

## 🚀 Future Improvements

* Improve person ID stability
* Improve fall detection accuracy
* Reduce false positives
* Improve sofa and bed fall detection
* Add real-time webcam support
* Add SMS/mobile notifications
* Add emergency alerts
* Add fall event logging
* Support multiple cameras
* Improve alarm management

## 📌 Project Status

**🚧 Work in Progress**

The project currently includes:

* Person detection
* Pose estimation
* Multi-person tracking
* Body angle calculation
* Speed tracking
* Fall detection
* Ground-time monitoring
* Alarm functionality

Further testing and tuning are being performed to improve reliability in real-world situations.

## 👨‍💻 Author

**Ashish**

AI & Computer Vision Project
