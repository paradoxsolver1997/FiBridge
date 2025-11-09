# FiBridge 🚀

<p align="left">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/flask-%3E=2.0-lightgrey.svg" alt="Flask">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-informational.svg" alt="Platform">
  <img src="https://img.shields.io/badge/SSL-self--signed-blue.svg" alt="Self-signed SSL">
</p>

FiBridge is a local web application for secure and convenient file and data sharing between PC and mobile devices. 🔗📱💻

## Features ✨

FiBridge can transfer text, (drawing) images, and files between your PC and mobile device in a fast and convenient way. The main features include:

### Text transfer via QR code scanning 📄➡️📱

- **QR Code Generator:** Generate QR codes for text, URLs, or files to share with mobile devices. 🔳
- **Remote Scan:** Use your phone to scan QR codes and send the result back to your PC. 📲

### Image transfer via drawing or signing on mobile device 🎨✍️

- **Draw & Sign:** Draw or sign on your device and transfer the image to your PC. 🖼️

### File transfer between PC and mobile device 📁🔄

- **File Share:** Transfer files from your PC to your mobile device via browser. 📤
- **File Fetch:** Transfer files from your mobile device to your PC. 📥

## Installation ⚙️

### Requirements 📋

- Windows, Linux, or macOS 🖥️
- Python 3.7 or higher (recommended: Python 3.10+) 🐍
- pip (Python package manager) 📦

### Clone & Install ⬇️

Clone the repository and install all dependencies:

```bash
git clone https://github.com/paradoxsolver1997/FiBridge.git
cd FiBridge
pip install -r requirements.txt
```

### Run the Application ▶️

Start the desktop app:

```bash
python main.py
```

- By default, the local web server is closed. Configrue it in "Server Setup" and click "Start Server". 🖱️
- Check [help](static/html/help.html) for how to use the app. ℹ️

### SSL keys Setup 🔐

To enable HTTPS (recommended for security):

1. Generate a self-signed certificate using the provided script:
   - On Windows:
     ```bat
     scripts\generate_cert.bat
     ```
   - On Linux/macOS:
     ```bash
     bash scripts/generate_cert.sh
     ```
2. The generated `key.pem` and `cert.pem` will be placed in the `configs/` directory. 📁
3. Update your Flask app configuration to use these certificate files for SSL. 🔒

## File Structure 🗂️

```
FiBridge/
├── main.py                # Main entry, starts the Flask server
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # Open source license
├── configs/               # Configuration files (e.g., SSL certificates)
├── output/                # Uploaded/shared files storage
├── static/                # Frontend static resources
│   ├── index.html         # Main entry page (dashboard/portal)
│   ├── help.html          # User help and documentation
│   ├── scan.html          # Remote scan page (scan QR codes, send result to PC)
│   ├── share.html         # File share page (PC to mobile file download)
│   ├── fetch.html         # File fetch page (mobile to PC file upload)
│   ├── text.html          # Direct text sending page
│   ├── js/                # JavaScript files for each page
│   │   ├── scan.js        # Logic for scan.html
│   │   ├── share.js       # Logic for share.html
│   │   ├── fetch.js       # Logic for fetch.html
│   │   ├── text.js        # Logic for text.html
│   │   └── ...
│   ├── css/
│   │   └── style.css      # Global styles
│   └── ...                # Other static assets (images, etc.)
├── scripts/               # Utility scripts (e.g., certificate generation)
│   ├── generate_cert.bat  # Windows: generate self-signed SSL cert
│   ├── generate_cert.sh   # Linux/Mac: generate self-signed SSL cert
│   └── detect_cjk.py      # Detect CJK characters in codebase
└── src/                   # Backend core code
    ├── app.py             # Main application window (Tkinter)
    ├── tabs/              # Tab logic for each feature (QR, scan, share, fetch, about, etc.)
    ├── frames/            # UI frame components (title, server, tool, etc.)
    └── utils/             # Utility modules (logger, server_manager, etc.)
```

### File/Directory Explanations 📝

- **main.py**: Entry point for the backend server and desktop app. 🏁
- **requirements.txt**: Lists all Python dependencies. 📦
- **configs/**: Stores configuration files and SSL certificates (key.pem, cert.pem). 🔑
- **output/**: Stores files uploaded or shared via the app. 📂
- **static/**: Contains all frontend resources:
  - **index.html**: Main dashboard/portal for navigation. 🗺️
  - **help.html**: In-app help and usage guide. 🆘
  - **scan.html / scan.js**: Scan QR codes with mobile, send result to PC. 🔍
  - **share.html / share.js**: Download files from PC to mobile. 📤
  - **fetch.html / fetch.js**: Upload files from mobile to PC. 📥
  - **text.html / text.js**: Directly send/paste text between devices. 📝
  - **css/style.css**: Global styles for all pages. 🎨
- **scripts/**: Utility scripts for development and deployment. 🛠️
- **src/**: All backend and desktop app logic:
  - **app.py**: Main Tkinter application window and logic. 🖼️
  - **tabs/**: Each feature tab (QR, scan, share, fetch, about, etc.). 🗂️
  - **frames/**: UI frame components for modular design. 🧩
  - **utils/**: Helper modules (logging, server management, etc.). 🧰

This structure ensures clear separation of backend, frontend, configuration, and utility scripts, making the project easy to maintain and extend. 🧑‍💻


## License 📝

MIT License

## Credits 🙏

- **Developed by:** [Paradoxsolver](https://github.com/paradoxsolver1997/) 👨‍💻
- **License:** MIT 🪪
- **Powered by:**
  - [Flask](https://flask.palletsprojects.com/) ⚗️
  - [html5-qrcode](https://github.com/mebjas/html5-qrcode) 📷
  - And more open source libraries 🌐
- **Project Home:** [https://github.com/paradoxsolver1997/FiBridge](https://github.com/paradoxsolver1997/FiBridge) 🏠

---

For questions, suggestions, or contributions, feel free to open an issue or contact the author! 💬