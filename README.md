# SmartParking

## Project Description

SmartParking is an advanced parking monitoring system that utilizes three cameras for real-time image processing. The system enables:

- Automatic vehicle detection at entry and exit points.
- Marking of available and occupied parking spots.
- License plate recognition.
- Collision detection.

![parking1](https://github.com/user-attachments/assets/15b85822-1c64-4880-a236-c050186f58ef)
![parking2](https://github.com/user-attachments/assets/b8594a07-9485-48fa-8626-d00b277eacdb)
![parking3](https://github.com/user-attachments/assets/fd6aeff9-261e-43db-ba28-6b98a0a38331)

## Technologies

SmartParking is built using the following technologies:

- Python + OpenCV for image processing
- MySQL for data storage

## System Requirements

- Python 3.8+
- OpenCV
- MySQL database
- Operating system: Linux / Windows

## Installation
1. Clone the repository:
```
git clone https://github.com/elzyr/SmartParking.git
cd SmartParking
```
2. Create and activate a virtual environment:
```
python -m venv venv
venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
```
3. Install required dependencies:
```
pip install -r requirements.txt
```
4. Configure the database:
- add file config.ini
```
[mysql]
host = localhost
user = root
password = password
database = database_name
port = 3306
```
5. Run main.py
