# **PROMPT ANSWERS**

---
## **Formula:**

#### For Query Based Confidence Score:
    retrieval_score=(Top 3 retrievals)\*weights(0.5,0.3,0.2)

    normalized=(retrieval_score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE)

where,

    MIN_SCORE=0.35
    MAX_SCORE=0.75



Here, MIN and MAX SCORE were chosen based on observed scores for various chunks and queries.

---

## 1) What is this document about?



### Answer:
    This document is about a take-home evaluation project that tests a candidate's ability to think, research, structure, and ship a project, specifically a "Smart Document Q\&A and Summarizer Tool". The project involves building a backend application that accepts a document, splits it into chunks, answers user questions about the document using a Large Language Model (LLM), and provides a summary of the document. The document outlines the objectives, tasks, and phases of the project, including setup, implementation, testing, and documentation.

    Confidence Score(Based on Retrieval)(in %)=75.87541043758395


---


## 2\) What rules must the interns follow?

### Answer:
    The interns must follow these ground rules: ● Work independently ● They can use AI tools to help with coding and research ● Ask clarifying questions anytime ● If they get stuck, document what they tried and why it didn't work.
    
    
    
    Confidence Score(Based on Retrieval)(in %)=66.33271425962447

---

## 3) What are some tools used to make this Project?

### Answer:
    The tools used for this project include:

       Flutter
       Python
       OpenCV
       TensorFlow
       C++
       HTML
       Firebase

    These are the software tools mentioned in the context. Additionally, the document mentions hardware tools, but they are not specified on the provided pages.

    Confidence Score(Based on Retrieval)(in %)= 65.53979516029356

Note: This answer is partially correct. It missed most Hardware Tools

---

## 4\) List some software and hardware tools used in this Project.

### Answer:
    The software tools used in this project include:

       Flutter: an open-source UI software development toolkit for building cross-platform applications.

       Python: a high-level, interpreted computer programming language for tasks like building websites, artificial intelligence, and data analysis.
    
       OpenCV: an open-source library for computer vision, machine learning, and image processing.
    
       TensorFlow: an open-source machine learning and deep learning framework.
    
       C++: a powerful, high-performance programming language.
    
    
    
    The hardware tools used in this project include:

       ESP32-CAM: a compact and low-cost camera module with Wi-Fi, Bluetooth, and a dual-core processor.
    
       ESP32-Lolin: a development board based on the ESP32 microcontroller for IoT and embedded systems applications.
    
    Confidence Score(Based on Retrieval)(in %)=70.36638706922533

---

## 5\) How does the system actually work?

### Answer:

    The system works by introducing an AI-based waste segregation capability that automatically classifies incoming waste into five distinct categories: organic, plastic, paper, metal, and unknown. Here's a step-by-step explanation: 
    
       The user places the waste into the mechanical flap of the smart bin.
    
       An ultrasonic sensor detects the user's hand and sends a signal to the ESP32-CAM module, which captures an image of the waste.
    
       The image is sent to the Waste Detection Model for classification into one of the five categories.
    
       The classified waste type is sent back to the ESP32 Lolin microcontroller, which determines the appropriate action for waste disposal.
    
       The microcontroller controls the servo motors to rotate and tilt the mechanical flap, directing the waste into the correct compartment.
    
       The system also monitors the waste level in each compartment using ultrasonic sensors and sends real-time updates to the user through the TrashGold mobile application or the TrashNet website.
    
       If a compartment is 90% full, the system sends an alert to the user to empty the bin.
    
    The system integrates automation, IoT, and user interaction to create a cleaner and more organized environment, and it also encourages sustainable habits among users by rewarding them with points for proper waste segregation.
    
    Confidence Score(Based on Retrieval)(in %)=60.0641131401062

---

## 6\) For a .pdf with image of Flowchart only: Question=What are the steps in :FLOWCHART OF WASTE DISPOSAL PROCESS

### Chunks sent:
    Image to Text Parse:================================================================================
    
    Introduction
    
    1
    
    1
    
    Heading: Introduction
    
    
    
    Page Number:1
    
    
    
    text:Capture frame from
    
    camera
    
    Verify waste type
    
    Dispose into "Bio-
    
    degradable”
    
    compartment
    
    Dispose into “Plastic” Is waste
    
    compartment plastic?
    
    Dispose into "Paper"
    
    compartment
    
    Is waste paper? Is waste metal?
    
    Dispose into "Other" Thspose into "Metal"
    
    compartment compartment
    
    eal time waste level
    
    statis
    
    Send notification


### Answer:
    Answer: The steps in the waste disposal process are:
    
    
    
    &#x20;   Capture frame from camera
    
    &#x20;   Verify waste type
    
    &#x20;   Dispose into respective compartments based on the type:
    
    &#x20;       "Bio-degradable"
    
    &#x20;       "Plastic" (if waste is plastic)
    
    &#x20;       "Paper" (if waste is paper)
    
    &#x20;       "Metal" (if waste is metal)
    
    &#x20;       "Other"
    
    &#x20;   Send notification and track real-time waste level statistics.
    
Note: This is actually the correct answer


---


## 7) Summary for above image:

### Answer:
    The system captures a frame from a camera to verify the type of waste and dispose of it into the corresponding compartment, such as biodegradable, plastic, paper, metal, or other, and sends notifications based on real-time waste level statistics.

---

## 8\) Use Case Diagram only summary:

### Answer:
    The TrashNet system allows users to manage waste disposal by monitoring waste levels, classifying waste types, and sending notifications when compartments are full. It also generates and displays QR codes, updates points and leaderboards, and enables authorities to view bin locations.

---

## 9\) For same use case diagram, Q: Explain how user interacts with TrashNet.

### Chunks Sent:

    Image to Text Parser:================================================================================
    
    Introduction
    
    1
    
    1
    
    Heading: Introduction
    
    
    
    Page Number:1
    
    
    
    text:User
    
    TrashNet
    
    Dispose Waste
    
    View waste level
    
    Check notifications
    
    Scan OR code
    
    View points
    
    View leaderboard
    
    <<extend>>
    
    >| Monitor waste level
    
    Classify waste type
    
    Dispose waste to the
    
    proper compartment
    
    Send notification if
    
    compartment 1s full
    
    Genetate and display
    
    QR code
    
    Update points and
    
    leaderboard
    
    Monitor bin levels
    
    View bin locations
    
    TrashNet authority



### Answer:
    The user interacts with TrashNet by performing the following actions:
    
    
    
       Dispose Waste
    
       View waste level
    
       Check notifications
    
       Scan QR code
    
       View points
    
       View leaderboard.

(Once again the answer is correct)

---

## 10\) Explain the content of Data Flow Diagram(From HYBRID DEEP LEARNING FRAMEWORK FOR LOW LIGHT IMAGE ENHANCEMENT AND SUPERRESOLUTION.pdf)


### Answer:
`The contents of the data flow diagram are not explicitly explained in the provided context, but according to the table of contents, it is mentioned in Chapter 5: System Design, specifically in sections 5.2 (Data Flow Diagrams) with DFD Level 0 and DFD Level 1, and corresponding figures (Figure 5.2 and Figure 5.3).`

