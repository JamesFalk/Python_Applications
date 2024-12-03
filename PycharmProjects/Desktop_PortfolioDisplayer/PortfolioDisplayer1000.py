from tkinter import Tk, Frame, Label, ttk, Button, Entry, StringVar
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf  # For Retrieving Data from Yahoo Finance

# Creating the Main Window
master = Tk(); master.title("Portfolio Displayer")
master.geometry("800x525+200+100")

# Generating the master_grid
mstr_grid = Frame(master, width=800, height=525); mstr_grid.grid()
for i in range(15):  # Create 15 rows
    mstr_grid.grid_rowconfigure(i, weight=1, minsize=35)
for i in range(9):  # Create 9 columns
    mstr_grid.grid_columnconfigure(i, weight=1, minsize=80)
mstr_grid.grid_propagate(False)

# Create the container box_grid
box_grid = Frame(mstr_grid, width=750, height=450)
box_grid.grid_propagate(False)
box_grid.grid(row=0, column=0, columnspan=8, rowspan=13, sticky='nw')

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
            else: stock_data.append(None)
        except Exception: stock_data.append(None); pass

    figure, ax = plt.subplots(1, 1)

    for h in range(8):
        if stock_data[h] is not None:  # Skip None elements
            ax.plot(stock_data[h].index, stock_data[h]['Close'], label=stock_entries[h].get())

    current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    # Labeling the plot
    ax.set_xlabel(f'Date-({current_datetime})')
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_form[slctr]))
    ax.set_ylabel('Closing Price ($)')
    ax.set_title('Stock Prices Over Time')
    ax.legend()  # Display legend

    canvas = FigureCanvasTkAgg(figure, box_grid)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(sticky='news')
    box_grid.rowconfigure(0, weight=1)
    box_grid.columnconfigure(0, weight=1)

# Adding Button to the Form that plots the portfolio when pressed
btn_pltport = Button(mstr_grid, text="D I S P L A Y   S T O C K S")
btn_pltport.grid(row=13, column=3, columnspan=3, sticky='news')
btn_pltport.bind("<Button-1>", plot_portfolio)

master.mainloop()
