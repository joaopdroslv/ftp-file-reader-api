# FTP File Reader API (FastAPI)

This project is a **FastAPI-based** API for interacting with an FTP server. It allows you to list directories, download files (CSV or Excel), and process their contents using Pandas.

## Features

- 📂 **List FTP Directory**: Retrieve the list of files in a specified FTP directory.
- 📑 **Read Files**: Download CSV or Excel files from the FTP server and return their content as JSON.
- 🔍 **Retrieve Specific Column**: Get a unique, non-empty list of values from a specific column in a CSV or Excel file.

## API Endpoints

- GET `/file/list`
Returns a list of files in the FTP directory.

- GET `/file/read?target_file=<file_name>`
Reads a CSV or Excel file and returns its content as JSON.

- GET `/file/column?target_file=<file_name>&target_column=<column_name>`
Extracts unique values from a specific column in a CSV or Excel file.
