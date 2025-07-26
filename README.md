Tiketo is a lightweight, Tkinter-based ticket management system designed for local use. It allows users to create, list,and delete tickets while sending
email notifications automatically through Outlook or Gmail, depending on the config.py file. 

🔧 How It Works
Tickets are saved in JSON locally and sent to the recipients/admins email
Each ticket has a UUID, title, description, and status (open).

🗂️ File Structure
project/
├── ticket.pyw         # Main application
├── email_sender.py    # Contains send_outlook_email() logic
├── tickets.json       # Stores ticket data
├── email_log.txt      # Records email status



<img width="366" height="491" alt="image" src="https://github.com/user-attachments/assets/4199638c-7f50-4dae-b5e5-0f1b5ed11892" />


