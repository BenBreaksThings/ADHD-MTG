import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

class PNGManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG Metadata & Rename Tool")
        self.root.geometry("1000x800")
        
        self.current_dir = ""
        self.selected_file = ""
        self.tags = ["[Lan]", "[Ins]", "[Cre]", "[Art]", "[Enc]", "[Pla]", "[Bat]", "[Sor]", "[Tok]", "[Leg]"]

        # --- UI Layout ---
        
        # Top Controls
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=5)
        btn_open = tk.Button(top_frame, text="Open Folder", command=self.load_directory)
        btn_open.pack(side=tk.LEFT, padx=10)

        # Paned Window (Split screen)
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left: Listbox
        self.file_listbox = tk.Listbox(self.paned)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select)
        self.paned.add(self.file_listbox)

        # Right: Image Preview
        self.img_label = tk.Label(self.paned, text="Select an image", bg="gray")
        self.paned.add(self.img_label)

        # Bottom Input Area
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        self.name_entry = tk.Entry(bottom_frame, font=("Arial", 12))
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_minus = tk.Button(bottom_frame, text="-", width=5, command=self.minus_logic)
        btn_minus.pack(side=tk.LEFT, padx=2)

        btn_save = tk.Button(bottom_frame, text="Save", width=10, bg="green", fg="white", command=self.save_filename)
        btn_save.pack(side=tk.LEFT, padx=2)

        # Tag Buttons Row
        tag_frame = tk.Frame(self.root)
        tag_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        for tag in self.tags:
            btn = tk.Button(tag_frame, text=tag, command=lambda t=tag: self.add_tag(t))
            btn.pack(side=tk.LEFT, padx=2)

    def load_directory(self):
        self.current_dir = filedialog.askdirectory()
        if not self.current_dir:
            return
        
        self.file_listbox.delete(0, tk.END)
        files = [f for f in os.listdir(self.current_dir) if f.lower().endswith('.png')]
        for f in files:
            self.file_listbox.insert(tk.END, f)

    def on_select(self, event):
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        filename = self.file_listbox.get(selection[0])
        self.selected_file = filename
        filepath = os.path.join(self.current_dir, filename)

        # Update Textbox (name without extension)
        base_name = os.path.splitext(filename)[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, base_name)

        # Display Image & Check Dimensions
        try:
            with Image.open(filepath) as img:
                w, h = img.size
                
                # Logic: Change background to red if dimensions mismatch
                if w == 2187 and h == 2975:
                    self.root.config(bg="SystemButtonFace") # Default
                else:
                    self.root.config(bg="red")

                # Resize for preview (keep aspect ratio)
                img.thumbnail((500, 600))
                photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=photo, text="")
                self.img_label.image = photo # Keep reference
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    def minus_logic(self):
        current = self.name_entry.get().strip()
        if not current:
            return
        
        parts = current.split(' ')
        if len(parts) > 1:
            new_val = " ".join(parts[:-1])
        else:
            new_val = "" # or keep as is if only one word
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, new_val)

    def add_tag(self, tag):
        current = self.name_entry.get().strip()
        
        # Split into base name and existing tags
        parts = current.split(' ')
        
        # Identify which parts are already recognized tags
        current_tags = [p for p in parts if p in self.tags]
        base_parts = [p for p in parts if p not in self.tags]
        
        if tag not in current_tags:
            current_tags.append(tag)

        # Rule: [Leg] must be first among tags
        if "[Leg]" in current_tags:
            current_tags.remove("[Leg]")
            current_tags.insert(0, "[Leg]")

        new_string = " ".join(base_parts + current_tags)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, new_string)

    def save_filename(self):
        if not self.selected_file or not self.current_dir:
            return
            
        new_base = self.name_entry.get().strip()
        new_name = new_base + ".png"
        
        old_path = os.path.join(self.current_dir, self.selected_file)
        new_path = os.path.join(self.current_dir, new_name)

        try:
            os.rename(old_path, new_path)
            # Update listbox selection
            idx = self.file_listbox.curselection()[0]
            self.file_listbox.delete(idx)
            self.file_listbox.insert(idx, new_name)
            self.file_listbox.selection_set(idx)
            self.selected_file = new_name
        except Exception as e:
            messagebox.showerror("Rename Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PNGManagerApp(root)
    root.mainloop()