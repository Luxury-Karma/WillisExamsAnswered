import tkinter as tk
import WillisAnswered as w

def process_input():
    input_word = entry.get()

    # Process the input word and update the output label
    output_label.config(text="Processed: " + input_word)


t = w.DataHandle()


# Create the main window
window = tk.Tk()
window.title("Willis Answer Student Database")

# Create input label and entry widget
input_label = tk.Label(window, text="Enter the searched words")
input_label.pack()
entry = tk.Entry(window)
entry.pack()

# Create a button to process the input
process_button = tk.Button(window, text="Send", command=process_input)
process_button.pack()

# Create an output label
output_label = tk.Label(window, text="")
output_label.pack()

# Start the main event loop
window.mainloop()
