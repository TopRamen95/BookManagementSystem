# 📚 Library Management System (BMS)

A **desktop-based Library Management System** built using **Python, Tkinter, and CustomTkinter** with **Supabase** backend for database management.

This system is designed to streamline library operations and allows for:
- **Admin login** and comprehensive management of the library.
- **Member login** and **self-registration**.
- Management of **book issue, return, and reissue** transactions.
- Efficient **search functionality** for both books and members.

---

## 🛠 Features

- **GUI-based application** using **CustomTkinter** for a modern, clean look.
- **Admin Dashboard** for centralized management of books and members.
- **Member Dashboard** for members to view their currently issued books.
- **Database Management** handled by **Supabase** for robust, cloud-based data storage.
- **QR Code Scanning** for books (optional) using \`OpenCV\` and \`pyzbar\`.
- Enhanced **User Interface** with image and logo support via \`Pillow\`.

---

## 📦 Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.13** | Core programming language. |
| **Tkinter + CustomTkinter** | Building the GUI and custom widgets. |
| **Supabase** | Cloud-based backend for database, authentication, and real-time features. |
| **Pillow** | Image manipulation and handling. |
| **OpenCV + pyzbar** | Optional QR code reading functionality. |
| **Docker** | Containerization for easy deployment and setup. |

---

## ⚡ Getting Started

### Clone the Repository

\`\`\`bash
git clone https://github.com/yourusername/bms.git
cd bms
\`\`\`

### Run the App Locally

1.  **Install Dependencies (Optional, but recommended):**
    \`\`\`bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt
    \`\`\`
2.  **Run the Main Application:**
    \`\`\`bash
    python main.py
    \`\`\`

---

## 🐳 Running with Docker

Docker provides an easy way to run the application without managing local dependencies.

### 1. Build the Docker Image

\`\`\`bash
docker build -t bms .
\`\`\`

### 2. Run the Docker Container

**Option 1: Headless / CLI Mode** (GUI not visible, primarily for testing backend/db connection)
\`\`\`bash
docker run --rm bms
\`\`\`

**Option 2: GUI Mode via VNC / X11**
To view the Tkinter GUI, you need to set up X11 forwarding (Linux/macOS) or connect via VNC (recommended for Windows).
* Instructions and a dedicated \`Dockerfile\` for VNC are included in the \`docker\` folder.

---

## 🔑 Default Admin Credentials

Use these credentials to log in to the system for the first time:

| Field | Value |
| :--- | :--- |
| **Username** | \`admin1\` |
| **Password** | \`admin123\` |

***Note:** More administrator accounts can be created once logged into the admin dashboard.*

---

---

## ⚡ Notes

### Supabase Setup
Make sure to update your **Supabase credentials** (Project URL, Anon/Service Role Key) in the \`database.py\` file before running the application.

## THIS APP NEEDS MANY ADDONS AND UPDATED ACCORDING TO THE LATEST TECH

### GUI on Docker
Sharing GUI applications via Docker can be complex. If you encounter issues viewing the GUI, refer to standard methods like **X11 forwarding** on Linux/macOS or utilizing the **VNC setup** provided in the \`docker\` folder.

---

## 📝 License

This project is **open-source** and free to use under the **MIT License**.
EOF
