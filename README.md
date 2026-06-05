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

  **Email Alert Preview:**
  ![Automated Email Alert](https://github.com/eapinedo/PythonAutomations/blob/main/E-mail%20alert%20(Spanish).png?raw=true)

  **Generated Excel Attachment:**
  ![Excel report.png](https://github.com/eapinedo/Sales-Inventory-Automation/blob/main/Excel%20report.png?raw=true)

* **Modular & Scalable Architecture:** Organized with clear separation of concerns (configuration, extraction, database connection, file management, and logging).

## 🧠 Implementation Highlights

To ensure high data integrity and minimal manual intervention, both pipelines utilize dynamic Python capabilities and intelligent error handling.

### 1. Intelligent Data Cleaning (`etl_engine.py`)

The ETL engine automatically standardizes decimals and intercepts inconsistent date formats before they reach SQL Server:

```python
# Cleans comma separators, rounds to 4 decimals, and enforces YYYY-MM-DD
df[col] = df[col].str.replace(',', '.', regex=False)
df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).round(4)
df[col] = pd.to_datetime(
    df[col],
    errors='coerce',
    dayfirst=True
).dt.strftime('%Y-%m-%d')
```

### 2. Smart File Routing (`main.py`)

The orchestrator differentiates between critical database failures and simple syntax errors to prevent data loss:

```python
# Detects DB crashes vs. syntax errors and routes files accordingly
if any(palabra in mensaje_error for palabra in errores_db):
    logger.warning("   ├─ [!] Critical Database Error detected.")
    logger.warning(
        f"   └─ Moving file to error folder: {carpeta_errores}"
    )
    mover_archivo(archivo_input, carpeta_errores)
```

### 3. Dynamic Email Generation & Secure Dispatch (`app.py` & `sendmail.py`)

The alerting bot dynamically converts SQL query results into styled HTML tables. It then attaches generated Excel reports and securely dispatches them via SMTP using TLS encryption:

```python
# Convert SQL query results into an HTML table
df = pd.read_sql_query(query, con=conn)
contenido_html += df.to_html(index=False, classes='table')

# Attach Excel report and send via secure SMTP
message.attach(MIMEText(contenido_html, 'html'))
message.attach(
    MIMEApplication(
        fil.read(),
        Name=basename(filename)
    )
)

with smtplib.SMTP(smtp, port) as server:
    server.starttls()
    server.login(sender_email, pwd)
    server.sendmail(
        sender_email,
        toaddrs,
        message.as_string()
    )
```

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

## 📈 Business Impact

* **Efficiency:** Eradicated manual ETL processing, reclaiming 15+ hours/week for the analytics team.
* **Visibility:** Automated daily email triggers give stakeholders immediate confirmation of data warehouse health and distributor status.
* **Reliability:** Built-in rollback mechanisms, transaction safety (ACID compliance), and intelligent file archiving prevent data corruption and accidental duplication.
