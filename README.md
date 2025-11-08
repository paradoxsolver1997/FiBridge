# FiBridge

<p align="left">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/flask-%3E=2.0-lightgrey.svg" alt="Flask">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-informational.svg" alt="Platform">
  <img src="https://img.shields.io/badge/SSL-self--signed-blue.svg" alt="Self-signed SSL">
</p>

FiBridge is a local web application for secure and convenient file and data sharing between PC and mobile devices.

## Features

- **QR Code File Sharing/Receiving**: Transfer files across devices by scanning QR codes.
- **File Upload & Download**: Supports multi-file selection, preview, upload, and download.
- **Page Separation**: Sending (fetch.html) and receiving (share.html) are separated for a clean interface.
- **Local Security**: All data is transmitted only within the local network, ensuring privacy and security.
- **Mobile/Desktop Responsive**: UI adapts to both mobile and PC for smooth operation.
- **Refresh & Navigation**: One-click refresh and easy navigation to home.

## Main Pages

- `scan.html`: Scan QR codes to get sharing links or data.
- `fetch.html`: Select and upload files to the local server.
- `share.html`: Browse, select, and download shared files.

## Usage

1. Start the service:
   ```bash
   python main.py
   ```
2. Access the local address in your PC browser (e.g., http://localhost:5000) and follow the instructions.
3. Scan the QR code on the PC page with your mobile device to transfer files between devices.

## Requirements

- Python 3.7+
- Flask

Install dependencies:
```bash
pip install -r requirements.txt
```

## Directory Structure

- `main.py`: Main entry, starts the Flask service.
- `src/`: Backend core code.
- `static/`: Frontend static resources (HTML/JS/CSS).
- `configs/`: Configuration files.
- `output/`: File storage output directory.

## License

MIT License

---

For questions or suggestions, feel free to contact!