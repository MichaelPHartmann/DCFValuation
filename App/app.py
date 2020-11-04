import tkinter as tk
import dataAq as da

window = tk.Tk()
greeting  = tk.Label(text='Enter a ticker:')

ticker_entry = tk.Entry()

def ticker_request():
    ticker = ticker_entry.get()
    da.create_corporate_book(ticker)
    ticker_entry.delete(0, tk.END)

enter = tk.Button(text='ENTER', command=ticker_request)


greeting.pack()
ticker_entry.pack()
enter.pack()

window.mainloop()
