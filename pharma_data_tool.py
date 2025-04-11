# pharma_data_tool.py
import csv
import os
import sqlite3
import argparse
from ftplib import FTP_TLS
from datetime import datetime

DB_PATH = "pharma_trials.db"
FTP_HOST = "127.0.0.1"  # Replace with real FTP
FTP_USER = "14148"
FTP_PASS = "0612"

# -------------------- Singleton DB Connection --------------------
class Database:
    _instance = None

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.conn = sqlite3.connect(DB_PATH)
            self.create_table()
            Database._instance = self

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database()
        return Database._instance

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trials (
                BatchID TEXT PRIMARY KEY,
                TrialDate TEXT,
                PatientID TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, batch_id, trial_date, patient_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO trials (BatchID, TrialDate, PatientID) VALUES (?, ?, ?)",
                           (batch_id, trial_date, patient_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

# -------------------- FTP Download --------------------
def download_csv_from_ftp(filename):
    print(f"Connecting securely to FTP: {FTP_HOST}")
    ftps = FTP_TLS(FTP_HOST)
    ftps.login(FTP_USER, FTP_PASS)
    ftps.prot_p()  # Protect the data connection
    with open(filename, 'wb') as f:
        ftps.retrbinary(f"RETR " + filename, f.write)
    ftps.quit()
    print(f"Downloaded {filename} from FTP securely")

# -------------------- CSV Validation --------------------
def validate_csv(file_path):
    errors = []
    batch_ids = set()
    valid_data = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        if 'BatchID' not in reader.fieldnames or 'TrialDate' not in reader.fieldnames or 'PatientID' not in reader.fieldnames:
            return False, ["Missing required headers"]

        for row_num, row in enumerate(reader, start=2):
            batch_id = row.get('BatchID')
            trial_date = row.get('TrialDate')
            patient_id = row.get('PatientID')

            if not batch_id:
                errors.append(f"Missing BatchID at row {row_num}")
            elif batch_id in batch_ids:
                errors.append(f"Duplicate BatchID '{batch_id}' at row {row_num}")
            else:
                batch_ids.add(batch_id)

            if not trial_date:
                errors.append(f"Missing TrialDate at row {row_num}")

            if not patient_id:
                errors.append(f"Missing PatientID at row {row_num}")

            if batch_id and trial_date and patient_id:
                valid_data.append((batch_id, trial_date, patient_id))

    return len(errors) == 0, errors if errors else valid_data

# -------------------- Main CLI Application --------------------
def main():
    parser = argparse.ArgumentParser(description="Pharmaceutical Trial Data Processor")
    parser.add_argument('--file', type=str, help='CSV filename to process')
    parser.add_argument('--ftp', action='store_true', help='Download file from FTP')
    args = parser.parse_args()

    filename = args.file

    if args.ftp:
        if not filename:
            print("Filename must be provided when using FTP mode.")
            return
        download_csv_from_ftp(filename)

    if not filename or not os.path.exists(filename):
        print("CSV file not found.")
        return

    print(f"Validating {filename}...")
    is_valid, result = validate_csv(filename)
    if not is_valid:
        print("Validation failed with the following errors:")
        for err in result:
            print(f" - {err}")
        return

    print("CSV is valid. Inserting into database...")
    db = Database.get_instance()
    inserted_count = 0
    for row in result:
        success = db.insert_data(*row)
        if success:
            inserted_count += 1

    print(f"Inserted {inserted_count} new records into the database.")

if __name__ == '__main__':
    main()
