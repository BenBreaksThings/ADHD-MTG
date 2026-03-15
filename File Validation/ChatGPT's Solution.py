import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

REQUIRED_WIDTH = 2187
REQUIRED_HEIGHT = 2975
TAG_ORDER = ["[Leg]", "[Lan]", "[Ins]", "[Cre]", "[Art]", "[Enc]", "[Pla]", "[Bat]", "[Sor]", "[Tok]"]
TAG_SET = set(TAG_ORDER)
PREVIEW_MAX_SIZE = (700, 700)


class PngRenamerApp:
	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("PNG Filename Tagger")
		self.root.geometry("1200x800")

		self.default_bg = self.root.cget("bg")
		self.current_folder = ""
		self.current_file_path = None
		self.current_photo = None
		self.png_files = []

		self._build_ui()

	def _build_ui(self):
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		main_frame = tk.Frame(self.root)
		main_frame.grid(row=0, column=0, sticky="nsew")
		main_frame.rowconfigure(1, weight=1)
		main_frame.columnconfigure(0, weight=1)

		top_bar = tk.Frame(main_frame)
		top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
		top_bar.columnconfigure(1, weight=1)

		browse_button = tk.Button(top_bar, text="Open Folder", command=self.select_folder)
		browse_button.grid(row=0, column=0, padx=(0, 10), sticky="w")

		self.folder_label = tk.Label(top_bar, text="No folder selected", anchor="w")
		self.folder_label.grid(row=0, column=1, sticky="ew")

		content_frame = tk.Frame(main_frame)
		content_frame.grid(row=1, column=0, sticky="nsew", padx=10)
		content_frame.rowconfigure(0, weight=1)
		content_frame.columnconfigure(0, weight=1)
		content_frame.columnconfigure(1, weight=2)

		list_frame = tk.Frame(content_frame, bd=1, relief="sunken")
		list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
		list_frame.rowconfigure(0, weight=1)
		list_frame.columnconfigure(0, weight=1)

		self.file_listbox = tk.Listbox(list_frame, exportselection=False)
		self.file_listbox.grid(row=0, column=0, sticky="nsew")
		self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

		list_scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
		list_scrollbar.grid(row=0, column=1, sticky="ns")
		self.file_listbox.config(yscrollcommand=list_scrollbar.set)

		preview_frame = tk.Frame(content_frame, bd=1, relief="sunken")
		preview_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
		preview_frame.rowconfigure(0, weight=1)
		preview_frame.columnconfigure(0, weight=1)

		self.image_label = tk.Label(preview_frame, text="Image preview will appear here", anchor="center")
		self.image_label.grid(row=0, column=0, sticky="nsew")

		self.dimension_label = tk.Label(preview_frame, text="")
		self.dimension_label.grid(row=1, column=0, sticky="ew", pady=8)

		editor_frame = tk.Frame(main_frame)
		editor_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
		editor_frame.columnconfigure(0, weight=1)

		filename_row = tk.Frame(editor_frame)
		filename_row.grid(row=0, column=0, sticky="ew")
		filename_row.columnconfigure(0, weight=1)

		self.filename_var = tk.StringVar()
		self.filename_entry = tk.Entry(filename_row, textvariable=self.filename_var)
		self.filename_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

		minus_button = tk.Button(filename_row, text="-", width=4, command=self.remove_last_token)
		minus_button.grid(row=0, column=1, padx=(0, 8))

		save_button = tk.Button(filename_row, text="Save", width=10, command=self.save_filename)
		save_button.grid(row=0, column=2)

		tag_row = tk.Frame(editor_frame)
		tag_row.grid(row=1, column=0, sticky="w", pady=(10, 0))

		for index, tag in enumerate(["[Lan]", "[Ins]", "[Cre]", "[Art]", "[Enc]", "[Pla]", "[Bat]", "[Sor]", "[Tok]", "[Leg]"]):
			btn = tk.Button(tag_row, text=tag, width=6, command=lambda value=tag: self.add_tag(value))
			btn.grid(row=0, column=index, padx=2, pady=2)

	def select_folder(self):
		folder = filedialog.askdirectory(title="Select folder containing PNG files")
		if not folder:
			return

		self.current_folder = folder
		self.folder_label.config(text=folder)
		self.load_png_files()

	def load_png_files(self):
		self.file_listbox.delete(0, tk.END)
		self.png_files = []
		self.current_file_path = None
		self.filename_var.set("")
		self.image_label.config(image="", text="Image preview will appear here")
		self.dimension_label.config(text="")
		self.root.config(bg=self.default_bg)

		if not os.path.isdir(self.current_folder):
			return

		for file_name in sorted(os.listdir(self.current_folder), key=str.lower):
			if file_name.lower().endswith(".png"):
				full_path = os.path.join(self.current_folder, file_name)
				if os.path.isfile(full_path):
					self.png_files.append(full_path)
					self.file_listbox.insert(tk.END, file_name)

		if not self.png_files:
			messagebox.showinfo("No PNG files", "No .png files were found in the selected folder.")

	def on_file_select(self, event=None):
		selection = self.file_listbox.curselection()
		if not selection:
			return

		index = selection[0]
		self.current_file_path = self.png_files[index]
		file_name = os.path.basename(self.current_file_path)
		name_without_ext, _ = os.path.splitext(file_name)
		self.filename_var.set(name_without_ext)
		self.show_preview(self.current_file_path)

	def show_preview(self, file_path: str):
		try:
			with Image.open(file_path) as img:
				width, height = img.size
				display_image = img.copy()

			display_image.thumbnail(PREVIEW_MAX_SIZE)
			self.current_photo = ImageTk.PhotoImage(display_image)
			self.image_label.config(image=self.current_photo, text="")

			is_valid = (width == REQUIRED_WIDTH and height == REQUIRED_HEIGHT)
			status = "OK" if is_valid else "ERROR"
			self.dimension_label.config(
				text=f"Dimensions: {width} x {height}  |  Required: {REQUIRED_WIDTH} x {REQUIRED_HEIGHT}  |  {status}"
			)

			if is_valid:
				self.root.config(bg=self.default_bg)
			else:
				self.root.config(bg="red")
		except Exception as exc:
			self.image_label.config(image="", text="Unable to load image preview")
			self.dimension_label.config(text=f"Error: {exc}")
			self.root.config(bg="red")

	def remove_last_token(self):
		current_name = self.filename_var.get().strip()
		if not current_name:
			return

		parts = current_name.split()
		if len(parts) <= 1:
			self.filename_var.set("")
			return

		updated = " ".join(parts[:-1])
		self.filename_var.set(updated)

	def add_tag(self, tag: str):
		current_name = self.filename_var.get().strip()
		if not current_name:
			base_tokens = []
		else:
			base_tokens = current_name.split()

		non_tag_tokens = [token for token in base_tokens if token not in TAG_SET]
		existing_tags = [token for token in base_tokens if token in TAG_SET]

		if tag not in existing_tags:
			existing_tags.append(tag)

		ordered_tags = [value for value in TAG_ORDER if value in existing_tags]
		updated_tokens = non_tag_tokens + ordered_tags
		self.filename_var.set(" ".join(updated_tokens).strip())

	def save_filename(self):
		if not self.current_file_path:
			messagebox.showwarning("No file selected", "Please select a PNG file first.")
			return

		new_name_base = self.filename_var.get().strip()
		if not new_name_base:
			messagebox.showwarning("Invalid filename", "Filename cannot be empty.")
			return

		invalid_chars = '<>:"/\\|?*'
		if any(char in new_name_base for char in invalid_chars):
			messagebox.showerror("Invalid filename", "Filename contains invalid characters.")
			return

		old_path = self.current_file_path
		folder = os.path.dirname(old_path)
		new_file_name = new_name_base + ".png"
		new_path = os.path.join(folder, new_file_name)

		if os.path.abspath(old_path) == os.path.abspath(new_path):
			messagebox.showinfo("No changes", "The filename is unchanged.")
			return

		if os.path.exists(new_path):
			messagebox.showerror("File exists", f"A file named '{new_file_name}' already exists.")
			return

		try:
			os.rename(old_path, new_path)
			self.current_file_path = new_path
			self.load_png_files()

			new_basename = os.path.basename(new_path)
			for index, path in enumerate(self.png_files):
				if os.path.basename(path) == new_basename:
					self.file_listbox.selection_clear(0, tk.END)
					self.file_listbox.selection_set(index)
					self.file_listbox.activate(index)
					self.file_listbox.see(index)
					self.on_file_select()
					break

			messagebox.showinfo("Saved", f"Renamed to: {new_file_name}")
		except Exception as exc:
			messagebox.showerror("Rename failed", str(exc))


if __name__ == "__main__":
	root = tk.Tk()
	app = PngRenamerApp(root)
	root.mainloop()
