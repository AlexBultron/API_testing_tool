import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json

def send_request():
    method = method_var.get()
    url = url_entry.get()
    headers = header_text.get("1.0", tk.END).strip()
    body = body_text.get("1.0", tk.END).strip()

    try:
        headers_dict = json.loads(headers) if headers else {}
    except json.JSONDecodeError:
        messagebox.showerror("Invalid Headers", "Headers must be valid JSON.")
        return

    try:
        body_dict = json.loads(body) if body else {}
    except json.JSONDecodeError:
        messagebox.showerror("Invalid Body", "Body must be valid JSON.")
        return

    try:
        response = requests.request(method, url, headers=headers_dict, json=body_dict if method in ["POST", "PUT", "PATCH"] else None)

        result = f"Status Code: {response.status_code}\n"
        result += f"Headers:\n{json.dumps(dict(response.headers), indent=2)}\n\n"

        try:
            response_json = response.json()
            result += "Body:\n" + json.dumps(response_json, indent=2)
        except ValueError:
            result += "Body:\n" + response.text

        response_output.delete("1.0", tk.END)
        response_output.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Request Error", str(e))

# GUI
app = tk.Tk()
app.title("🧪 Python API Testing Tool")
app.geometry("800x700")

# Method & URL
frame_top = ttk.Frame(app)
frame_top.pack(fill="x", padx=10, pady=5)

method_var = tk.StringVar(value="GET")
method_dropdown = ttk.Combobox(frame_top, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"], width=8)
method_dropdown.pack(side="left")

url_entry = ttk.Entry(frame_top, width=80)
url_entry.pack(side="left", padx=5)
url_entry.insert(0, "https://jsonplaceholder.typicode.com/posts/1")

send_button = ttk.Button(frame_top, text="Send", command=send_request)
send_button.pack(side="left", padx=5)

# Headers
ttk.Label(app, text="Headers (JSON format):").pack(anchor="w", padx=10)
header_text = scrolledtext.ScrolledText(app, height=6)
header_text.pack(fill="x", padx=10)

# Body
ttk.Label(app, text="Body (JSON format):").pack(anchor="w", padx=10)
body_text = scrolledtext.ScrolledText(app, height=10)
body_text.pack(fill="x", padx=10)

# Response
ttk.Label(app, text="Response:").pack(anchor="w", padx=10)
response_output = scrolledtext.ScrolledText(app, height=20, bg="#f4f4f4")
response_output.pack(fill="both", expand=True, padx=10, pady=5)

app.mainloop()
