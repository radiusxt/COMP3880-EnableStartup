# [ES - Internship] Face Recognition

## Table of Contents
- [Overview](#overview)
- [Requirement](#Requirement)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Overview

The faceless attendance application uses OpenCV and face_recognition libraries to detect and identify faces.

# Project Directory Structure

```plaintext
Project/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   └── modules/
│       ├── face_detector.py
│       └── face_identifier.py
└── data/

```

## Requirement
| Requirement ID | Category       | Description                                                                                                                                                                  |
|-----------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **FR-01**      | Software       | 1. **Face Recognition** - The system must recognize faces in real-time using a camera attached to a Raspberry Pi. <br> 2. **Face Data Management** - Manage face information (add, delete, update). <br> 3. **Image Processing** - Detect face regions and preprocess data (normalize, denoise). <br> 4. **User Interaction** - Interface to display face recognition results. |
| **FR-02**      | Hardware       | 1. **Device Setup** <br> - Raspberry Pi 4. <br> - Camera (Raspberry Pi compatible). <br> - Small-sized screen.                                                             |
| **FR-03**      | AI             | 1. **Face Detection** - Ability to detect faces quickly (< 1 second). <br> 2. **Face Identification** - Achieve an accuracy of approximately >75%.                          |
| **FR-02**      | Non-Functional | 1. **Performance** - Processing time per frame ≤ 1 second; continuous operation ≥ 3 hours. <br> 2. **Deployment Capability** - Application runs stably on Raspberry Pi.      |

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher.
- Required Python libraries:
  - `tk`
  - `face-recognition`

## Installation
1. Create python virtual environment (recommend)
    - Refer: https://docs.python.org/3/library/venv.html


2. **Install required libraries**: You can install the necessary libraries using pip. Run the following command:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. **Run the application**: Execute the script using Python:
   ```bash
   python main.py
   ```
