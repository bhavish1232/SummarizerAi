import tkinter as tk
import random
import time


score = 0
level = 1
correct_answer = 0
start_time = 0
time_limit = 5
timer_running = True


def generate_question():
    global correct_answer, time_limit, level, current_operator

    
    if level < 3:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
    elif level < 6:
        num1 = random.randint(10, 100)
        num2 = random.randint(10, 100)
    else:
        num1 = random.randint(100, 999)
        num2 = random.randint(10, 99)

    operators = ['+', '-', '*']
    current_operator = random.choice(operators)

    if current_operator == '+':
        correct_answer = num1 + num2
    elif current_operator == '-':
        correct_answer = num1 - num2
    elif current_operator == '*':
        correct_answer = num1 * num2

    
    if current_operator == '*':
        time_limit = 10
    else:
        time_limit = max(3, 6 - level // 2)

    return f"{num1} {current_operator} {num2}"

def next_question():
    global start_time, timer_running
    entry.delete(0, tk.END)
    result_label.config(text="")
    question = generate_question()
    question_label.config(text=question)
    start_time = time.time()
    timer_running = True
    update_timer()

def check_answer():
    global score, level, timer_running
    elapsed_time = time.time() - start_time
    user_input = entry.get()
    timer_running = False

    try:
        if int(user_input) == correct_answer and elapsed_time <= time_limit:
            score += 1
            level = score // 3 + 1
            result_label.config(text="✅ Correct!", fg="green")
        else:
            result_label.config(text=f"❌ Wrong! Ans: {correct_answer}", fg="red")
    except:
        result_label.config(text=f"⚠️ Invalid! Ans: {correct_answer}", fg="orange")

    score_label.config(text=f"Score: {score} | Level: {level}")
    root.after(1500, next_question)

def update_timer():
    if not timer_running:
        return

    elapsed = time.time() - start_time
    remaining = max(0, int(time_limit - elapsed))
    timer_label.config(text=f"Time Left: {remaining}s")

    if remaining <= 0:
        check_answer()
    else:
        root.after(500, update_timer)


root = tk.Tk()
root.title("Focusmania")
root.iconbitmap("logo.ico")
root.geometry("420x360")
root.configure(bg='#0f172a')
root.resizable(False, False)

title_label = tk.Label(root, text="🧠 Speed Math Challenge", font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#333")
title_label.pack(pady=10)

question_label = tk.Label(root, text="", font=("Arial", 22), bg="#f0f4f8", fg="#005577")
question_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 18), justify='center')
entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", font=("Arial", 14), bg="#4CAF50", fg="white", command=check_answer)
submit_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#0f172a")
result_label.pack(pady=5)

score_label = tk.Label(root, text="Score: 0  |  Level: 1", font=("Arial", 12), bg="#0f172a",fg='#FFFFFF')
score_label.pack(pady=5)

timer_label = tk.Label(root, text="Time Left: 5s", font=("Arial", 12, "bold"), fg="red", bg="#0f172a")
timer_label.pack()

root.bind("<Return>", lambda event: check_answer())

next_question()
root.mainloop()
