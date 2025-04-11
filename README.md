📦 Pharma Data Tool
The Pharma Data Tool is a secure command-line application built with Python. It automates the process of downloading pharmaceutical trial data from an FTP server, validates the data for consistency, and stores it into a local SQLite database. Designed with security, reliability, and real-world constraints in mind, it follows professional software engineering practices including the use of design patterns, containerization, and Git-based version control.

🔍 Project Overview
This tool was created for securely handling pharmaceutical trial data submissions. Trial data is typically submitted via FTP in CSV format. This tool:

Connects to an FTP server to download CSV data.

Validates each record for required fields and duplicate Batch IDs.

Uses a Singleton database connection to store clean, valid data.

Can be run via CLI for full automation.

⚙️ Setup Instructions
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/pharma_data_tool.git
cd pharma_data_tool
2. Install dependencies (Python 3.9+ recommended)
bash
Copy
Edit
pip install -r requirements.txt
3. Run the application
bash
Copy
Edit
# Local file mode
python pharma_data_tool.py --file sample.csv

# FTP download and process
python pharma_data_tool.py --ftp --file sample.csv
🧪 Usage Guidelines
Make sure the CSV file contains the following headers: BatchID, TrialDate, PatientID

Ensure all BatchIDs are unique and that no required fields are left blank

Place sample.csv in the working directory, or store it on a reachable FTP server

🔐 FTP Server Configuration (For Testing)
Use FileZilla Server or any local FTP server to host test files

Update credentials inside pharma_data_tool.py:

python
Copy
Edit
FTP_HOST = "127.0.0.1"
FTP_USER = "your_user"
FTP_PASS = "your_password"
🧱 API Endpoints
N/A – This is a command-line application and does not expose API endpoints.

🤝 Contribution Guide
Fork this repo

Create your feature branch: git checkout -b feature/my-feature

Commit your changes: git commit -m 'feat: Add my feature'

Push to the branch: git push origin feature/my-feature

Open a pull request

📄 License
MIT License. Free to use for educational or professional purposes.

🧠 Author
David – IT student and developer on a mission to deliver clean, secure, and scalable tools for the real world 🚀

For questions, reach out to: davidibitayo123@gmail.com