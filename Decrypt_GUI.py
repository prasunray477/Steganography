import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import cv2
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

class DecryptApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Extract Message from Image")
        self.root.geometry("450x400")
        
        # Variables
        self.image_path = ""
        self.image = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Title
        tk.Label(self.root, text="Extract Hidden Message", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Image selection
        tk.Button(self.root, text="Select Stego Image", command=self.select_image,
                 width=20, height=2).pack(pady=5)
        
        self.image_label = tk.Label(self.root, text="No image selected", fg="gray")
        self.image_label.pack(pady=5)
        
        # Password input
        tk.Label(self.root, text="Password:").pack(pady=(20,5))
        self.key_entry = tk.Entry(self.root, width=40, show="*")
        self.key_entry.pack(pady=5)
        
        # Extract button
        tk.Button(self.root, text="Extract Message", command=self.extract_message,
                 bg="blue", fg="white", width=20, height=2).pack(pady=20)
        
        # Result display
        tk.Label(self.root, text="Extracted Message:").pack(pady=(10,5))
        self.result_text = scrolledtext.ScrolledText(self.root, width=50, height=8)
        self.result_text.pack(pady=5, padx=10)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.image = cv2.imread(file_path)
            filename = file_path.split('/')[-1]
            self.image_label.config(text=f"Selected: {filename}", fg="black")
    
    def derive_key(self, user_key):
        return hashlib.sha256(user_key.encode()).digest()[:16]
    
    def decrypt_message(self, cipher_bytes, user_key):
        key = self.derive_key(user_key)
        iv = cipher_bytes[:16]
        encrypted_data = cipher_bytes[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()
    
    def extract_message(self):
        # Check inputs
        if not self.image_path:
            messagebox.showerror("Error", "Please select a stego image!")
            return
        
        password = self.key_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Please enter the password!")
            return
        
        try:
            
            # Extract data using LSB 
            n, m, z = 0, 0, 0
            extracted_bytes = bytearray()
            
            # Extract approximately 1000 bytes
            max_extract = min(1000, (self.image.shape[0] * self.image.shape[1] * 3) // 8)
            
            for i in range(max_extract):
                val = 0
                for bit_pos in range(8):
                    bit = self.image[n, m, z] & 1
                    val = (val << 1) | bit
                    z = (z + 1) % 3
                    if z == 0:
                        m += 1
                        if m == self.image.shape[1]:
                            m = 0
                            n = n + 1
                            if n >= self.image.shape[0]:
                                break
                
                extracted_bytes.append(val)
                
                # Try to decrypt every 16 bytes
                if len(extracted_bytes) >= 32 and len(extracted_bytes) % 16 == 0:
                    try:
                        decrypted = self.decrypt_message(bytes(extracted_bytes), password)
                        
                        if all(ord(c) < 127 and ord(c) > 31 for c in decrypted) or decrypted.isascii():
                            # Display the result
                            self.result_text.delete(1.0, tk.END)
                            self.result_text.insert(1.0, decrypted)
                            messagebox.showinfo("Success", "Message extracted successfully!")
                            self.key_entry.delete(0, tk.END)
                            return
                    except:
                        continue
            
            # If decryption failed
            messagebox.showerror("Error", "Could not decrypt message. Check your password!")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, "Failed to extract message")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DecryptApp()
    app.run()