from tkinter import Tk, Frame, Label, ttk, Button, Entry, StringVar
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf  # For Retrieving Data from Yahoo Finance
import numpy as np

# Creating the Main Window
master = Tk(); master.title("Portfolio Displayer")
master.geometry("800x800+200+100")  # Increased height to accommodate two plots

# Generating the master_grid
mstr_grid = Frame(master, width=1000, height=1250); mstr_grid.grid()
for i in range(25):  # Increased number of rows
    mstr_grid.grid_rowconfigure(i, weight=1, minsize=35)
for i in range(9):  # Create 9 columns
    mstr_grid.grid_columnconfigure(i, weight=1, minsize=80)
mstr_grid.grid_propagate(False)

# Create the container box_grid
box_grid = Frame(mstr_grid, width=750, height=1000)  # Increased height
box_grid.grid_propagate(False)
box_grid.grid(row=1, column=0, columnspan=8, rowspan=10, sticky='nw')

# Secondary plot grid for full-width original chart
full_width_grid = Frame(mstr_grid, width=1000, height=2000)
full_width_grid.grid(row=15, column=1, columnspan=9, rowspan=20, sticky='ew')
full_width_grid.grid_propagate(False)

# TimePeriod_Label
lbl_time_prd = Label(mstr_grid, text="Time Period")
lbl_time_prd.grid(row=0, column=8, sticky='s')
# TimePeriod_Selector
prd_select = StringVar()
period_ddbox = ttk.Combobox(mstr_grid, width=15, textvariable=prd_select)
period_ddbox['values'] = ('1WK', '1MO', '3MO', '6MO', '1YR', '5YR')
period_ddbox.grid(row=1, column=8, sticky='nw'); period_ddbox.current(3)

# Portfolio_Label
lbl_portfolio = Label(mstr_grid, text="Portfolio")
lbl_portfolio.grid(row=2, column=8, sticky='s')
# Portfolio_InputBoxes
stock_entries = []
for f in range(3, 11):
    entry = Entry(mstr_grid)
    entry.grid(row=f, column=8, sticky='nw')
    stock_entries.append(entry)

# Portfolio Plotter Function
def plot_portfolio(ding):

    date_form = ['%m-%d, ', '%m-%d', '%m-%d', '%m-%d', '%m-%Y', '%m-%Y']
    tm_prd = ['1wk', '1mo', '3mo', '6mo', '1yr', '5yr']
    tm_intrvl = ['1d', '1d', '5d', '1wk', '1mo', '3mo']

    slctr = period_ddbox.current()

    stock_data = []  # Store stock data
    for g in range(8):
        ticker = stock_entries[g].get()
        try:
            info = yf.Ticker(ticker).info
            if 'symbol' in info and info['symbol'] == ticker:
                data = yf.download(ticker, period=tm_prd[slctr], interval=tm_intrvl[slctr])
                stock_data.append(data)
            else: 
                stock_data.append(None)
        except Exception: 
            stock_data.append(None)
            pass

    # Clear any existing plots in both grids
    for widget in box_grid.winfo_children():
        widget.destroy()
    for widget in full_width_grid.winfo_children():
        widget.destroy()

    # Original Closing Price Plot (full width)
    full_figure, full_ax = plt.subplots(figsize=(15, 4))
    
    for h in range(8):
        if stock_data[h] is not None and not stock_data[h].empty:
            full_ax.plot(stock_data[h].index, stock_data[h]['Close'], label=stock_entries[h].get())

    current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    # Labeling the original price plot
    full_ax.set_xlabel(f'Date-({current_datetime})')
    full_ax.xaxis.set_major_formatter(mdates.DateFormatter(date_form[slctr]))
    full_ax.set_ylabel('Closing Price ($)')
    full_ax.set_title('Stock Prices Over Time')
    full_ax.legend()
    full_ax.grid(True, linestyle='--', alpha=0.7)

    # Percentage Plot (in original location)
    figure, ax2 = plt.subplots(figsize=(10, 5))

    for h in range(8):
        if stock_data[h] is not None and not stock_data[h].empty:
            # Calculate percentage relative to mean
            close_prices = stock_data[h]['Close']
            mean_price = close_prices.mean()
            percentage_prices = (close_prices / mean_price - 1) * 100

            ax2.plot(stock_data[h].index, percentage_prices, label=f'{stock_entries[h].get()} (% of Avg)')

    # Labeling the percentage plot
    ax2.set_xlabel(f'Date-({current_datetime})')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter(date_form[slctr]))
    ax2.set_ylabel('Percentage of Average Price (%)')
    ax2.set_title('Stock Prices Relative to Average')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5)

    # Add full-width closing price plot to full_width_grid
    full_canvas = FigureCanvasTkAgg(full_figure, full_width_grid)
    full_canvas.draw()
    full_canvas_widget = full_canvas.get_tk_widget()
    full_canvas_widget.pack(fill='both', expand=True)

    # Add percentage plot to original box_grid
    canvas = FigureCanvasTkAgg(figure, box_grid)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(sticky='news')
    box_grid.rowconfigure(0, weight=1)
    box_grid.columnconfigure(0, weight=1)

# Adding Button to the Form that plots the portfolio when pressed
btn_pltport = Button(mstr_grid, text="D I S P L A Y   S T O C K S", font=('Helvetica', 8))
btn_pltport.grid(row=12, column=1, rowspan=2, columnspan=8, sticky='news')
btn_pltport.bind("<Button-1>", plot_portfolio)

master.mainloop()
