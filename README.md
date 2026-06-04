# Python & SQL Automation Solutions for Sales & Inventory Data

## 📖 Project Overview
This repository contains a robust, dual-purpose automation suite designed to streamline data operations for Modern Trade sales. Built with Python and SQL, the project consists of two core modules: an **Automated ETL Pipeline** for daily sales records and an **Automated Alerting System** for data warehouse tracking. 

By eliminating manual data entry, this solution saves over 15 hours of manual work weekly, minimizes error rates, and ensures 100% data integrity for executive reporting.

## ✨ Key Features

* **High-Performance ETL Pipeline:**
  * Parses and loads daily sales/inventory records from various formats (CSV, Excel).
  * Automatically handles data cleaning, decimal rounding, and intelligent date formatting.
  * Utilizes native Bulk Insert capabilities (via `PyODBC` and `SQLAlchemy`) for maximum database ingestion speed.
* **Automated Data Reporting & Alerts:**
  * Queries SQL databases to track daily data warehouse updates.
  * Automatically generates and formats Excel reports using `pandas` and `xlsxwriter`.
  * Sends responsive HTML email alerts to stakeholders detailing processed dates, total sales, and pipeline health.
  
  ![Automated Email Alert](https://github.com/eapinedo/PythonAutomations/blob/main/E-mail%20alert%20(Spanish).png?raw=true)

* **Modular & Scalable Architecture:** Organized with clear separation of concerns (configuration, extraction, database connection, file management, and logging).

## 📂 Repository Structure

* `config/`: Contains `config.json` for database credentials, target schemas, and file routing logic.
* `input/`: Target directory for raw daily sales files (Excel, CSV).
* `output/`: Auto-generated directories (`procesados/`, `errores/`, `logs/`) for post-processing file management.
* `src/`: Core logic and Python modules.
  * `main.py`: The main orchestrator for the ETL process.
  * `etl_engine.py`: Pandas-driven data transformation, cleaning, and dynamic column generation.
  * `db_connection.py`: Secure SQL Server connections, transaction management, and ultra-fast bulk insertions.
  * `file_manager.py`: Automated file routing and directory cleanup.
  * `logger_setup.py`: Standardized execution tracking and log formatting.
  * `app.py`: The reporting bot that queries the database, generates Excel attachments, and dispatches HTML emails.
* `envio-alertas.bat`: Batch script for scheduling and executing the email alert bot.
* `requirements.txt`: Project dependencies.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Manipulation:** Pandas, Openpyxl, Xlsxwriter
* **Database:** SQL Server, SQLAlchemy, PyODBC
* **Automation:** Windows Batch Scripting, Smtplib

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/Sales-Inventory-Automation.git](https://github.com/YourUsername/Sales-Inventory-Automation.git)
   cd Sales-Inventory-Automation
