# NAOHand 🤖✋
**Real-time Hand Gesture Recognition on the NAO Humanoid Robot using MediaPipe and OpenCV**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NAOqi](https://img.shields.io/badge/NAOqi-SDK-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-red)

---

# 🧩 Overview

This project enables the **NAO humanoid robot** to recognize **hand gestures in real time** using **MediaPipe** for hand landmark detection and **OpenCV** for visualization.

Unlike traditional approaches that rely on **data gloves or physical markers**, this method is **purely vision-based**, requiring only the robot’s built-in camera.

The system can detect:

- Open hand ✋  
- One to four raised fingers ☝️✌️🤟✋  
- No gesture detected ❌  

The robot can optionally **speak the recognized gesture** using its built-in **Text-to-Speech (TTS)** engine.

---

# 🚀 Features

- Real-time video capture from NAO’s camera (RGB, 640×480)
- Hand landmark detection with **Google MediaPipe**
- Automatic gesture classification based on finger position
- Optional speech feedback (**ALTextToSpeech**)
- Modular Python implementation with **NAOqi SDK integration**

---

# 📦 Requirements

## Hardware

- NAO humanoid robot (tested on **NAO V5**)
- Network connection between **NAO and your PC**

## Software

Make sure you have the following installed:

```bash
pip install qi mediapipe opencv-python numpy
````

💡 The `qi` module is part of the **NAOqi SDK**. Ensure it is available in your Python environment.

---

# ⚙️ Setup

## Clone the repository

```bash
git clone https://github.com/vitor-souza-ime/naohand.git
cd naohand
```

## Configure the robot IP

Edit the IP address of your NAO robot in `main.py`:

```python
NAO_IP = "172.15.4.178"   # Replace with your robot’s IP
```

## Run the program

```bash
python main.py
```

Press **q** to quit.

---

# 🧠 How It Works

### 1️⃣ Camera Streaming

The NAO’s RGB camera feed is obtained via **ALVideoDevice**.

### 2️⃣ Hand Detection

MediaPipe processes the frames to extract **21 hand landmarks**.

### 3️⃣ Gesture Classification

The code compares **finger tip and base positions** to count the number of raised fingers.

### 4️⃣ Speech Output (Optional)

The NAO can announce the detected gesture using **ALTextToSpeech**.

### 5️⃣ Visualization

Landmarks and gesture labels are overlaid using **OpenCV**.

---

# 🗂️ Project Structure

```
naohand/
│
├── main.py           # Main application script
├── README.md         # Project documentation
└── requirements.txt  # Dependency list
```

---

# 📊 Example Output

```
Conectado ao NAO!
Open Hand t=0.089s
2 Finger t=0.133s
No Gesture
```

A live video window will display the camera feed with landmarks and recognized gestures.

---

# 🧪 Notes

* For faster detection, ensure **good lighting** and a **clear view of the hand**.
* The system currently detects **up to 4 raised fingers and an open hand**.
* The robot’s stiffness is disabled:

```python
setStiffnesses("Body", 0.0)
```

This prevents unwanted motion during vision tasks.

---

# 🧑‍💻 Author

**Vitor Souza**
Intelligent Systems and Robotics Research

GitHub:
[https://github.com/vitor-souza-ime](https://github.com/vitor-souza-ime)

---

# 📝 License

This project is released under the **MIT License**.

See the `LICENSE` file for details.
