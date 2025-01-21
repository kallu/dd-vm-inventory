# dd-vm-inventory
Sample project to pull VM info from DataDog

NOTE: .cursorrules is modified from https://cursor.directory/

## Prerequisites

- Python 3.10 or higher installed on your system
- DataDog API and Application keys
- pip (Python package installer)

## Installation

1. Clone this repository

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your DataDog API credentials as environment variables:
   ```bash
   export DD_API_KEY='your_api_key'
   export DD_APP_KEY='your_application_key'
   ```
4. Run the script:
   ```bash
   python dd-vm-inventory.py
   ```

This script will output the VM inventory data in CSV format.
