# MyHome Household Bills

Clean HTML, CSS, and JavaScript frontend for the Flask backend in `Backend`.

## Run The Backend

```powershell
cd "D:\Home bills S.E\Backend"
python -m pip install -r requirements.txt
python app.py
```

If `python` points to an environment without Flask, use the Python installation where the requirements were installed.

## Run The Frontend

```powershell
cd "D:\Home bills S.E\Frontend"
python -m http.server 8000
```

Open:

```text
http://127.0.0.1:8000/Html/Login.html
```

Use the Sign Up tab to create an account, then use Login for returning users. The frontend verifies the active session through `/api/me`, and bills are stored through the Flask API for the signed-in user.

## Email Reminders

Reminder emails are sent for unpaid bills that are overdue, due today, or due within the configured reminder window. Set these environment variables before starting Flask:

```powershell
$env:MAIL_SERVER="smtp.example.com"
$env:MAIL_PORT="587"
$env:MAIL_USERNAME="tariqiskandar2@gmail.com"
$env:MAIL_PASSWORD="your-password"
$env:MAIL_FROM="tariqiskandar2@gmail.com"
$env:MAIL_USE_TLS="true"
```

If mail settings are missing, the backend safely logs the reminder instead of failing the app.
