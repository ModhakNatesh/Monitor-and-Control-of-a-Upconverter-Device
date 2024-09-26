# Monitoring and Control of a Device

This project is designed to monitor and control a device (such as an upconverter) over TCP/IP. It provides a user interface for real-time monitoring of device parameters and allows authorized users to modify the device's settings.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Monitoring](#monitoring)
- [Alerts](#alerts)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Real-time monitoring of device parameters such as frequency, gain, mute, etc.
- Separate controls for modifying each parameter.
- User authentication (Admin and regular users) with different access rights.
- Continuous monitoring of device status with alerts for anomalies.
- Logging of all parameter changes, including failed attempts.
- Multi-threaded monitoring for efficient device status checking.

---

## Requirements

- Python 3.8+
- Django 4.0+
- Redis (for caching alerts)
- OpenCV (if required for visual components)
- TCP/IP connection to the device
- PostgreSQL/MySQL/SQLite (for database support)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/monitoring-control-device.git
   cd monitoring-control-device
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the Django server:

   ```bash
   python manage.py runserver
   ```

6. Start Redis (if applicable):

   ```bash
   redis-server
   ```

---

## Usage

1. Open the web application in your browser at `http://127.0.0.1:8000`.
2. Log in using the credentials created in the `createsuperuser` step.
3. Navigate to the status page to view current device parameters in real-time.
4. Use the provided controls to modify parameters like frequency, gain, mute, etc.
5. Alerts will be displayed if temperature exceeds thresholds or other anomalies are detected.

### Parameter Edit Process

- Each parameter (Frequency, Gain, Mute, Frequency Step) has a separate edit page.
- Only updated values will be sent to the device to minimize unnecessary communication.
- All changes are logged in the `DeviceLog` table.

---

## API Endpoints

### 1. **GET** `/api/device/status/`
- Fetch current device parameters.
  
### 2. **POST** `/api/device/edit/`
- Edit a specific device parameter.
  
### 3. **GET** `/api/device/alerts/`
- Fetch current alerts related to device anomalies.

---

## Monitoring

- The project uses multi-threading to continuously monitor the device every second.
- The device parameters are fetched via TCP/IP commands, and the latest status is updated in the database.
  
---

## Alerts

- Alerts are generated if any abnormal behavior is detected, such as:
  - Temperature exceeding 35°C.
  - Device response delays or failures.
  
- Alerts are cached using Redis and displayed to users on the dashboard.

---

## Logging

- All device interactions, including successful and failed edit attempts, are logged in the `DeviceLog` table.
- Logs can be viewed by admin users in the admin panel.

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

### Additional Files

- **`.gitignore`**: Ensures sensitive files like `settings.py` and `db.sqlite3` are not pushed to GitHub.
- **`requirements.txt`**: Contains all the necessary Python packages.
- **`LICENSE`**: Describes the license under which this project is distributed.
- **`CONTRIBUTING.md`**: Provides guidelines for contributing to the project.

---
