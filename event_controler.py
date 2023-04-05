from tkinter import *
import smtplib
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import atexit

# --Instance plánovače--
scheduler = BackgroundScheduler()

# --Seznam událostí--
events = []

# --Barvy--
black = "#000000"

# --Okno--
window = Tk()
window.title("události")
window.minsize(150, 150)
window.resizable(False, False)
window.config(bg=black)

# --Funkce--
def add_event():
    date_str = input_date.get()
    time_str = input_time.get()
    event_str = input_event.get()

    # --Kontrola formátů--
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        error_label.config(text="Chybny format data!")
        return

    try:
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        error_label.config(text="Chybny format casu!")
        return

    # --Přidání nové události do seznamu--
    event = {'date': date_obj,
             'time': time_obj,
             'event': event_str
             }
    events.append(event)
    error_label.config(text="Udalost pridana")

    check_events()

@scheduler.scheduled_job('interval', minutes=1)
def check_events():
    # --Získání aktuálního času--
    time_now = datetime.now()
    for event in events:
        event_datetime = datetime.combine(event['date'], event['time'])
        if event_datetime - time_now <= timedelta(days=1):
            send_mail(event)

def send_mail(event):
    # --Nastavení Mailu--
    sending_mail = "vojtechfink.business@gmail.com"
    password = "jilwivesofrxegio"
    recieving_mail = "vojtechfink@gmail.com"
    subject = f"Upomínka na událost: {event['event']}"
    text = f"Událost {event['event']} se koná zítra v {event['date'].strftime('%d.%m.%Y')} v {event['time'].strftime('%H:%M')}."
    message = f"Subject: {subject}\n\n{text}"

    # --Odesílání Mailu--
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=sending_mail, password=password)
        connection.sendmail(from_addr=sending_mail,
                            to_addrs=recieving_mail,
                            msg=message.encode("utf-8")
                            )

def start_scheduler():
    threading.Thread(target=scheduler.start).start()

def on_closing():
    if scheduler.running:
        scheduler.shutdown(wait=False)
    window.destroy()

# --Inputy--
input_date = Entry(width=10, font=("Times New Roman", 12), justify=CENTER)
input_date.insert(0, "")
input_date.grid(row=1, column=0, padx=10, pady=(10, 0))
input_time = Entry(width=10, font=("Times New Roman", 12), justify=CENTER)
input_time.insert(0, "")
input_time.grid(row=1, column=1, padx=10, pady=(10, 0))
input_event = Entry(width=10, font=("Times New Roman", 12), justify=CENTER)
input_event.insert(0, "")
input_event.grid(row=3, column=0, padx=10, pady=(10, 0))

# --Tlačítko--
add_button = Button(text="Přidat", font=("Times New Roman", 12), command=add_event)
add_button.grid(row=3, column=1, padx=10, pady=(10, 0))

# --Labely--
date_label = Label(text="Datum", bg=black, fg="white", font=("Times New Roman", 12))
date_label.grid(row=0, column=0, padx=10, pady=(10, 0))

time_label = Label(text="Time", bg=black, fg="white", font=("Times New Roman", 12))
time_label.grid(row=0, column=1, padx=10, pady=(10, 0))

event_label = Label(text="Událost", bg=black, fg="white", font=("Times New Roman", 12))
event_label.grid(row=2, column=0, padx=10, pady=(10, 0))

error_label = Label(text="", bg=black, fg="white", font=("Times New Roman", 12))
error_label.grid(row=4, column=0, padx=10, pady=(10, 0))

# --Hlavní cyklus--

window.protocol("WM_DELETE_WINDOW", on_closing)
scheduler.add_job(check_events, 'interval', minutes=1, id='check_events')
start_scheduler()
window.mainloop()


