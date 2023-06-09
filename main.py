import requests
from tkinter import *

# --Barvy--
main_color = "#14085f"

# --Okno--
window = Tk()
window.title("Převod měn v2.0")
window.minsize(300, 120)
window.resizable(False, False)
window.config(bg=main_color)
window.iconbitmap("img/icon.ico")

# --Funkce--
def count():
    try:
        currency_from = drop_down_from.get()
        currency_to = drop_down_to.get()
        amount = float(u_input.get())

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency_to}&from={currency_from}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "UVUS8YM1zStOAYdqfwQPVFtq4frfGT2x"
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        response.raise_for_status()
        data_result = response.json()
        result_label.config(text=data_result["result"])
        kurz_label.config(text=data_result["info"]["rate"])
        notif_label.config(text="")
    except:
        notif_label.config(text="Zadejte částku")
        result_label.config(text="0")
        kurz_label.config(text="kurz")

# --Uživatelský vstup--
u_input = Entry(width=10, font=("Times New Roman", 12), justify=CENTER)
u_input.insert(0, "0")
u_input.grid(row=0, column=0, padx=10, pady=(10, 0))

# --Roletky--
drop_down_from = StringVar(window)
drop_down_from.set("CZK")
drop_down_from_option = OptionMenu(window, drop_down_from, "CZK", "EUR", "USD", "AUD", "CAD", "CHF", "JPY", "NZD", "GBP", "SEK", "DKK", "NOK", "SGD", "HKD", "MXN", "PLN", "RUB", "TRY", "ZAR", "CNH")
drop_down_from_option.grid(row=0, column=1, padx=10, pady=(10, 0))

drop_down_to = StringVar(window)
drop_down_to.set("EUR")
drop_down_to_optiton = OptionMenu(window, drop_down_to, "CZK", "EUR", "USD", "AUD", "CAD", "CHF", "JPY", "NZD", "GBP", "SEK", "DKK", "NOK", "SGD", "HKD", "MXN", "PLN", "RUB", "TRY", "ZAR", "CNH")
drop_down_to_optiton.grid(row=1, column=1, padx=10, pady=(10, 0))

# --Tlačítka--
count_button = Button(text="Převést", font=("Times New Roman", 12), command=count)
count_button.grid(row=0, column=2, padx=10, pady=(10, 0))

# --Labely--
result_label = Label(text="0", bg=main_color, fg="white", font=("Times New Roman", 12))
result_label.grid(row=1, column=0, padx=10, pady=(10, 0))

notif_label = Label(bg=main_color, fg="white", font=("Times New Roman", 12))
notif_label.grid(row=2, column=0, padx=10, pady=(10, 0))

kurz_label = Label(text="kurz", bg=main_color, fg="white", font=("Times New Roman", 12))
kurz_label.grid(row=1, column=2, padx=10, pady=(10, 0))

# --Hlavní cyklus--
window.mainloop()