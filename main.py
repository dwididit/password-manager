# Welcome to Password Manager. Created by Dwi Didit Prasetiyo

from tkinter import *
from typing import TextIO

from data import alphabet, symbols, numbers
import random
from tkinter import messagebox
import pyperclip
import json

# Generate Password
def generate_password():
    password = []
    for i in range(0, 5):
        password.append(random.choice(alphabet))
        password.append(random.choice(alphabet).lower())
        password.append(random.choice(symbols))
        password.append(random.choice(numbers))
    password = "".join(password)
    password_entry.insert(index=0, string=password)


# Search Password
def search():
    try:
        # search key in json file and return the value
        with open("password.json", mode="r") as file:
            #access json data
            data = json.load(file)
            #access website data
            website = data[website_entry.get()]
            #access email data
            email = website["email"]
            #access password data
            password = website["password"]
    except KeyError:
        messagebox.showwarning(title="Error", message="No Data File Found")
    else:
        messagebox.showinfo(title=f"{website_entry.get()}", message=f"Email: {email}\nPassword: {password}")




# Save Password

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    # Message box
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="oppss", message="Please make sure you haven't left any fields empty!")
    else:
        messagebox.showinfo(title="Success", message="Your password has been saved successfully!")
        pyperclip.copy(password)
        pyperclip.paste()
        messagebox.showinfo(title="Success", message="Your password has been copied to clipboard!")
        # Write to txt file
        with open("password.txt", mode="a") as file:
            file.write(f"{website} | {email} | {password}\n")

        # Convert to json
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }
        # Write to json file
        try:
            with open("password.json", mode="r") as file:
                # Read old data
                data = json.load(file)
        except FileNotFoundError:
            with open("password.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Update old data with new data
            data.update(new_data)
            with open("password.json", mode="w") as file:
                # Save updated data
                json.dump(data, file, indent=4)
        finally:
            # Clear entry
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# UI setup using Tkinter
# Create a window
window = Tk()
window.title("Password Manager. Created by Dwi Didit Prasetiyo")
window.config(padx=20, pady=20)

# Create a canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Create a label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

# Create a entry
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
# Placeholders
website_entry.insert(index=0, string="google.com")



email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
# Create a entry
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(index=0, string="name@domain.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
# Create a entry
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

# Create a button
generate_button = Button(text="Generate", command=generate_password)
generate_button.grid(row=3, column=2)

# Create a button
copy_button = Button(text="Save", width=33, command=save)
copy_button.grid(row=4, column=1, columnspan=2)

# Create a button
search_button = Button(text="Search", width=7, command=search)
search_button.grid(row=1, column=2)

window.mainloop()