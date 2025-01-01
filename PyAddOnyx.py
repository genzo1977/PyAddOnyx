import os
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

def get_chrome_extensions():
    """Retrieve Chrome extensions from default profile directories."""
    extensions = []
    chrome_path = Path.home() / "AppData/Local/Google/Chrome/User Data"
    
    if not chrome_path.exists():
        print("Chrome path not found:", chrome_path)
        return extensions
    
    profiles = [p for p in chrome_path.iterdir() if p.is_dir() and (p.name.startswith("Profile") or p.name == "Default")]
    
    for profile in profiles:
        extensions_dir = profile / "Extensions"
        if extensions_dir.exists():
            for ext in extensions_dir.iterdir():
                for version_dir in ext.iterdir():  # Extensions are versioned subdirectories
                    manifest_file = version_dir / "manifest.json"
                    if manifest_file.exists():
                        try:
                            with open(manifest_file, "r", encoding="utf-8") as f:
                                manifest = json.load(f)
                                name = manifest.get("name", "Unknown")
                                version = manifest.get("version", "Unknown")
                                desc = manifest.get("description", "No description")
                                extensions.append({
                                    "Browser": "Chrome",
                                    "Name": name,
                                    "Version": version,
                                    "Description": desc
                                })
                        except Exception as e:
                            print(f"Error reading {manifest_file}: {e}")
    return extensions

def get_firefox_extensions():
    """Retrieve Firefox extensions from the default profile directory."""
    extensions = []
    firefox_path = Path.home() / "AppData/Roaming/Mozilla/Firefox/Profiles"
    profiles = [p for p in firefox_path.iterdir() if p.is_dir()]
    
    for profile in profiles:
        extensions_file = profile / "extensions.json"
        if extensions_file.exists():
            try:
                with open(extensions_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for addon in data.get("addons", []):
                        name = addon.get("defaultLocale", {}).get("name", "Unknown")
                        version = addon.get("version", "Unknown")
                        desc = addon.get("defaultLocale", {}).get("description", "No description")
                        extensions.append({
                            "Browser": "Firefox",
                            "Name": name,
                            "Version": version,
                            "Description": desc
                        })
            except Exception as e:
                print(f"Error reading extensions.json: {e}")
    return extensions

def fetch_addons():
    """Fetch browser add-ons and display them in the Treeview."""
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    
    # Fetch extensions
    addons = get_chrome_extensions() + get_firefox_extensions()
    for addon in addons:
        tree.insert("", "end", values=(addon["Browser"], addon["Name"], addon["Version"], addon["Description"]))

# Tkinter GUI Setup
root = tk.Tk()
root.title("PyAddOnyx")
root.geometry("800x400")

# Frame for Treeview and Scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Treeview for displaying extensions
columns = ("Browser", "Name", "Version", "Description")
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading("Browser", text="Browser")
tree.heading("Name", text="Name")
tree.heading("Version", text="Version")
tree.heading("Description", text="Description")

# Adjust column widths
tree.column("Browser", width=100)
tree.column("Name", width=200)
tree.column("Version", width=100)
tree.column("Description", width=400)

# Vertical Scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack Treeview and Scrollbar using grid to ensure proper layout
tree.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure row and column weights
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Fetch Add-ons Button
btn_fetch = tk.Button(root, text="Fetch Add-ons", command=fetch_addons)
btn_fetch.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
