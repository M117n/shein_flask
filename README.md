# Player Points Processing and Management System

This project implements a web application built with Flask that manages and processes player points, providing functionalities to store, update, and generate reports. It also includes a system for backing up and restoring previous states, along with detailed activity logs.

## Features
- **Point Processing**: Accepts point lists in text format and calculates points based on custom rules.
- **Data Management**: Updates and saves player results in CSV files.
- **History Tracking**: Allows undoing the last changes made and restoring previous states.
- **Report Generation**: Exports results to Excel files with applied formatting and styles.
- **Result Viewing and Downloading**: Recent results can be viewed and downloaded at any time.
- **Event Logging**: Logs all processing activities and updates.

## Requirements
- Python 3.x
- Flask
- Pandas
- Openpyxl

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/repository-name.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

 ##  Usage
1. Process Points: Enter the list of player points in the correct format and click "Execute".
2. Undo Changes: If an incorrect update is made, you can undo the last action.
3. Download Results: Updated results can be downloaded in Excel format.
4. Logs and Statistics: The system keeps a history of all performed actions for review.
