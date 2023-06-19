import tkinter as tk
import WillisAnswered as w

def process_input():
    input_word = entry.get()
    max_answer: int = int(entry_max.get())
    answer = t.getQuestionFromPrompt(input_word.lower().split())

    # Process the input word and update the output label
    output_label.config(text=f'Processed: {input_word}\nThe Questions detected : {answer}')

    text_data = ''
    answer_number = 0
    for a in answer:
        text_data += f'question : {a[0]}\n->answer : {t.jsonDictionary[a[0]]}\n'
        answer_number = answer_number + 1
        if answer_number >= max_answer:
            break


    output_label.config(text=text_data)


t = w.DataHandle()


# Create the main window
window = tk.Tk()
window.title("Willis Answer Student Database")

# Create input label and entry widget
input_label = tk.Label(window, text="Enter the searched words")
input_label.pack()
entry = tk.Entry(window)
entry.pack()
input_maximum_answer = tk.Label(window, text='Enter the maximum amount of answer')
input_maximum_answer.pack()
entry_max = tk.Entry(window)
entry_max.pack()

# Create a Button for activating the data search
search_button = tk.Button(window, text='find Data', command=t.global_quiz_data_collecting)
search_button.pack()

# Create a button to process the input
process_button = tk.Button(window, text="Send", command=process_input)
process_button.pack()

# Create an output label
output_label = tk.Label(window, text="")
output_label.pack()

# Start the main event loop
window.mainloop()
