import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

class EncryptApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hide Message in Image")
        self.root.geometry("400x300")
        
        # Variables
        self.image_path = ""
        self.image = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Title
        tk.Label(self.root, text="Hide Secret Message", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Image selection
        tk.Button(self.root, text="Select Image", command=self.select_image, 
                 width=20, height=2).pack(pady=5)
        
        self.image_label = tk.Label(self.root, text="No image selected", fg="gray")
        self.image_label.pack(pady=5)
        
        # Message input
        tk.Label(self.root, text="Secret Message:").pack(pady=(20,5))
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(pady=5)
        
        # Key input
        tk.Label(self.root, text="Password:").pack(pady=(10,5))
        self.key_entry = tk.Entry(self.root, width=40, show="*")
        self.key_entry.pack(pady=5)
        
        # Encrypt button
        tk.Button(self.root, text="Hide Message", command=self.hide_message,
                 bg="green", fg="white", width=20, height=2).pack(pady=20)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.image = cv2.imread(file_path)
            filename = file_path.split('/')[-1]
            self.image_label.config(text=f"Selected: {filename}", fg="black")
    
    def derive_key(self, user_key):
        return hashlib.sha256(user_key.encode()).digest()[:16]
    
    def encrypt_message(self, message, user_key):
        key = self.derive_key(user_key)
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + encrypted_data
    
    def hide_message(self):
        # Check inputs
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image!")
            return
        
        message = self.message_entry.get().strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        
        password = self.key_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        try:
            # Encrypt message
            encrypted_bytes = self.encrypt_message(message, password)
            
            # Hide in image using LSB 
            x_enc = self.image.copy()
            n, m, z = 0, 0, 0
            encrypted_len = len(encrypted_bytes)
            
            # Check if image can hold the data
            total_pixels = x_enc.shape[0] * x_enc.shape[1] * 3
            if encrypted_len * 8 > total_pixels:
                messagebox.showerror("Error", "Message too long for this image!")
                return
            
            # Embed encrypted message 
            for i in range(encrypted_len):
                char_val = encrypted_bytes[i]
                for bit_pos in range(8):
                    bit = (char_val >> (7 - bit_pos)) & 1
                    org_val = x_enc[n, m, z]
                    x_enc[n, m, z] = (org_val & 254) | bit
                    z = (z + 1) % 3
                    if z == 0:
                        m += 1
                        if m == x_enc.shape[1]:
                            m = 0
                            n = n + 1
            
            # Save the result
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            
            if save_path:
                cv2.imwrite(save_path, x_enc)
                messagebox.showinfo("Success", "Message hidden successfully!")
                
                # Clear inputs
                self.message_entry.delete(0, tk.END)
                self.key_entry.delete(0, tk.END)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide message: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EncryptApp()
    app.run()