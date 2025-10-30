#!/usr/bin/env python3
"""
LAN Multi-User Communication Client
Full-featured GUI client with video, audio, screen sharing, chat, and file transfer
"""

import socket
import threading
import struct
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import pyaudio
import base64
import io
import os
from datetime import datetime
import mss
import time
class LANClient:
    def __init__(self, master):
        self.master = master
        self.master.title("LAN Communication System")
        self.master.geometry("1200x800")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Connection state
        self.connected = False
        self.username = None
        self.server_ip = None
        self.tcp_socket = None
        self.udp_socket = None
        self.udp_port = 0
        
        # Streaming state
        self.video_streaming = False
        self.audio_streaming = False
        self.presenting = False
        self.presenter = None
        
        # Video components
        self.video_cap = None
        self.video_frames = {}  # {username: frame}
        
        # Audio components
        self.audio = pyaudio.PyAudio()
        self.audio_input_stream = None
        self.audio_output_stream = None
        
        # Users list
        self.users = []
        
        # Running flag
        self.running = True
        
        # Build UI
        self.build_connection_ui()
    
    def build_connection_ui(self):
        """Build connection dialog"""
        frame = ttk.Frame(self.master, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="LAN Communication System", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Server IP:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.server_entry = ttk.Entry(frame, width=30)
        self.server_entry.grid(row=2, column=1, padx=5, pady=5)
        self.server_entry.insert(0, "192.168.1.100")
        
        ttk.Label(frame, text="TCP Port:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.tcp_port_entry = ttk.Entry(frame, width=30)
        self.tcp_port_entry.grid(row=3, column=1, padx=5, pady=5)
        self.tcp_port_entry.insert(0, "5555")
        
        ttk.Label(frame, text="UDP Port:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.udp_port_entry = ttk.Entry(frame, width=30)
        self.udp_port_entry.grid(row=4, column=1, padx=5, pady=5)
        self.udp_port_entry.insert(0, "5556")
        
        self.connect_btn = ttk.Button(frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.status_label = ttk.Label(frame, text="", foreground="red")
        self.status_label.grid(row=6, column=0, columnspan=2)
    def send_message(self, data):
     """Send a JSON message via TCP to the server"""
     if self.tcp_socket:
        try:
            msg = json.dumps(data).encode('utf-8')
            # Send message length first
            self.tcp_socket.sendall(struct.pack('>I', len(msg)) + msg)
        except Exception as e:
            print(f"Send message error: {e}")

    def recv_message(self):
     """Receive a JSON message via TCP from the server"""
     if self.tcp_socket:
        try:
            # First, read 4 bytes for message length
            raw_len = self.tcp_socket.recv(4)
            if not raw_len:
                return None
            msg_len = struct.unpack('>I', raw_len)[0]
            # Then read the actual message
            data = b''
            while len(data) < msg_len:
                packet = self.tcp_socket.recv(msg_len - len(data))
                if not packet:
                    return None
                data += packet
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Receive message error: {e}")
            return None

    def connect_to_server(self):
        """Connect to server"""
        self.username = self.username_entry.get().strip()
        self.server_ip = self.server_entry.get().strip()
        
        if not self.username or not self.server_ip:
            self.status_label.config(text="Please enter username and server IP")
            return
        
        try:
            tcp_port = int(self.tcp_port_entry.get())
            udp_port = int(self.udp_port_entry.get())
            
            self.status_label.config(text="Connecting...", foreground="blue")
            self.master.update()
            
            # Create TCP socket
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((self.server_ip, tcp_port))
            
            # Create UDP socket
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(('', 0))  # Bind to any available port
            self.udp_port = self.udp_socket.getsockname()[1]
            
            # Register with server
            self.send_message({
                'type': 'register',
                'username': self.username,
                'udp_port': self.udp_port
            })
            
            # Wait for registration response
            response = self.recv_message()
            if response and response['type'] == 'registered':
                self.connected = True
                self.users = response['users']
                self.presenter = response.get('presenter')
                
                # Build main UI
                self.build_main_ui()
                
                # Load chat history
                for msg in response.get('chat_history', []):
                    self.display_chat_message(msg)
                
                # Start receiver threads
                threading.Thread(target=self.receive_tcp_messages, daemon=True).start()
                threading.Thread(target=self.receive_udp_streams, daemon=True).start()
                
                print(f"Connected to server as {self.username}")
            else:
                raise Exception("Registration failed")
                
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {e}", foreground="red")
            if self.tcp_socket:
                self.tcp_socket.close()
            if self.udp_socket:
                self.udp_socket.close()
    
    def build_main_ui(self):
        """Build main application UI"""
        # Clear connection UI
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Create main layout
        # Top: Video grid
        video_frame = ttk.LabelFrame(self.master, text="Video Conference", padding="5")
        video_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.video_container = ttk.Frame(video_frame)
        self.video_container.pack(fill=tk.BOTH, expand=True)
        
        # Video controls
        video_controls = ttk.Frame(video_frame)
        video_controls.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.video_btn = ttk.Button(video_controls, text="Start Video", command=self.toggle_video)
        self.video_btn.pack(side=tk.LEFT, padx=5)
        
        self.audio_btn = ttk.Button(video_controls, text="Start Audio", command=self.toggle_audio)
        self.audio_btn.pack(side=tk.LEFT, padx=5)
        
        # Middle: Screen sharing
        screen_frame = ttk.LabelFrame(self.master, text="Screen Sharing", padding="5")
        screen_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.screen_label = ttk.Label(screen_frame, text="No presentation active", anchor=tk.CENTER)
        self.screen_label.pack(fill=tk.BOTH, expand=True)
        
        screen_controls = ttk.Frame(screen_frame)
        screen_controls.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.present_btn = ttk.Button(screen_controls, text="Start Presenting", command=self.toggle_presenting)
        self.present_btn.pack(side=tk.LEFT, padx=5)
        
        # Bottom: Chat and controls
        bottom_frame = ttk.Frame(self.master)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left: Users list
        users_frame = ttk.LabelFrame(bottom_frame, text="Users", padding="5")
        users_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        self.users_listbox = tk.Listbox(users_frame, width=20)
        self.users_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_users_list()
        
        # Center: Chat
        chat_frame = ttk.LabelFrame(bottom_frame, text="Group Chat", padding="5")
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        chat_input_frame = ttk.Frame(chat_frame)
        chat_input_frame.pack(fill=tk.X, pady=5)
        
        self.chat_entry = ttk.Entry(chat_input_frame)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        ttk.Button(chat_input_frame, text="Send", command=self.send_chat).pack(side=tk.LEFT)
        
        # Right: File sharing
        file_frame = ttk.LabelFrame(bottom_frame, text="File Sharing", padding="5")
        file_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        ttk.Button(file_frame, text="Upload File", command=self.upload_file).pack(fill=tk.X, pady=2)
        
        self.files_listbox = tk.Listbox(file_frame, width=25, height=8)
        self.files_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(file_frame, text="Download Selected", command=self.download_file).pack(fill=tk.X, pady=2)
        
        # Initialize video display
        self.update_video_grid()
    
    def toggle_video(self):
        """Toggle video streaming"""
        if not self.video_streaming:
            try:
                self.video_cap = cv2.VideoCapture(0)
                if not self.video_cap.isOpened():
                    messagebox.showerror("Error", "Cannot access webcam")
                    return
                
                self.video_streaming = True
                self.video_btn.config(text="Stop Video")
                threading.Thread(target=self.stream_video, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"Video error: {e}")
        else:
            self.video_streaming = False
            self.video_btn.config(text="Start Video")
            if self.video_cap:
                self.video_cap.release()
                self.video_cap = None
    
    def stream_video(self):
        """Stream video to server"""
        while self.video_streaming and self.running:
            try:
                ret, frame = self.video_cap.read()
                if ret:
                    # Resize and compress
                    frame = cv2.resize(frame, (320, 240))
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                    
                    # Create packet: type(1) + username_len(1) + username + frame_data
                    username_bytes = self.username.encode('utf-8')
                    packet = bytes([1, len(username_bytes)]) + username_bytes + buffer.tobytes()
                    
                    # Send via UDP
                    self.udp_socket.sendto(packet, (self.server_ip, int(self.udp_port_entry.get())))
                    
                    # Update own video
                    self.video_frames[self.username] = frame
                    
                time.sleep(0.033)  # ~30 FPS
            except Exception as e:
                print(f"Video stream error: {e}")
                break
    
    def toggle_audio(self):
        """Toggle audio streaming"""
        if not self.audio_streaming:
            try:
                # Input stream (microphone)
                self.audio_input_stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024
                )
                
                # Output stream (speakers)
                self.audio_output_stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    output=True,
                    frames_per_buffer=1024
                )
                
                self.audio_streaming = True
                self.audio_btn.config(text="Stop Audio")
                threading.Thread(target=self.stream_audio, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"Audio error: {e}")
        else:
            self.audio_streaming = False
            self.audio_btn.config(text="Start Audio")
            if self.audio_input_stream:
                self.audio_input_stream.stop_stream()
                self.audio_input_stream.close()
            if self.audio_output_stream:
                self.audio_output_stream.stop_stream()
                self.audio_output_stream.close()
    
    def stream_audio(self):
        """Stream audio to server"""
        while self.audio_streaming and self.running:
            try:
                data = self.audio_input_stream.read(1024, exception_on_overflow=False)
                
                # Create packet: type(2) + username_len + username + audio_data
                username_bytes = self.username.encode('utf-8')
                packet = bytes([2, len(username_bytes)]) + username_bytes + data
                
                # Send via UDP
                self.udp_socket.sendto(packet, (self.server_ip, int(self.udp_port_entry.get())))
            except Exception as e:
                print(f"Audio stream error: {e}")
                break
    
    def toggle_presenting(self):
        """Toggle screen sharing"""
        if not self.presenting:
            self.send_message({'type': 'start_presenting'})
            self.presenting = True
            self.present_btn.config(text="Stop Presenting")
            threading.Thread(target=self.stream_screen, daemon=True).start()
        else:
            self.send_message({'type': 'stop_presenting'})
            self.presenting = False
            self.present_btn.config(text="Start Presenting")
    
    def stream_screen(self):
        """Stream screen to server"""
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            
            while self.presenting and self.running:
                try:
                    # Capture screen
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                    
                    # Resize
                    img.thumbnail((800, 600), Image.LANCZOS)
                    
                    # Convert to base64
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    img_str = base64.b64encode(buffer.getvalue()).decode()
                    
                    # Send to server
                    self.send_message({
                        'type': 'screen_frame',
                        'frame': img_str
                    })
                    
                    time.sleep(0.1)  # 10 FPS for screen sharing
                except Exception as e:
                    print(f"Screen share error: {e}")
                    break
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.send_message({
                'type': 'chat',
                'message': message
            })
            self.chat_entry.delete(0, tk.END)
    
    def display_chat_message(self, msg):
        """Display chat message"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = msg.get('timestamp', '')
        username = msg.get('username', '')
        message = msg.get('message', '')
        self.chat_display.insert(tk.END, f"[{timestamp}] {username}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def upload_file(self):
        """Upload file to server"""
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                filename = os.path.basename(filepath)
                with open(filepath, 'rb') as f:
                    filedata = base64.b64encode(f.read()).decode()
                
                filesize = os.path.getsize(filepath)
                
                self.send_message({
                    'type': 'file_upload',
                    'filename': filename,
                    'filesize': filesize,
                    'filedata': filedata
                })
                
                messagebox.showinfo("Success", f"File '{filename}' uploaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")
    
    def download_file(self):
        """Download selected file"""
        selection = self.files_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to download")
            return
        
        filename = self.files_listbox.get(selection[0])
        
        # Request file from server
        self.send_message({
            'type': 'file_download',
            'filename': filename
        })
    
    def receive_tcp_messages(self):
        """Receive and process TCP messages from server"""
        while self.running and self.connected:
            try:
                msg = self.recv_message()
                if not msg:
                    print("Disconnected from server")
                    break
                
                self.process_tcp_message(msg)
            except Exception as e:
                print(f"TCP receive error: {e}")
                break
    
    def process_tcp_message(self, msg):
        """Process received TCP messages"""
        msg_type = msg.get('type')
        
        if msg_type == 'chat':
            self.display_chat_message(msg)
        
        elif msg_type == 'user_joined':
            self.users = msg['users']
            self.update_users_list()
            self.display_chat_message({
                'username': 'System',
                'message': f"{msg['username']} joined the session",
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
        
        elif msg_type == 'user_left':
            self.users = msg['users']
            self.update_users_list()
            self.display_chat_message({
                'username': 'System',
                'message': f"{msg['username']} left the session",
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            # Remove their video frame
            if msg['username'] in self.video_frames:
                del self.video_frames[msg['username']]
                self.update_video_grid()
            
            # Clear presenter if they left
            if self.presenter == msg['username']:
                self.presenter = None
                self.screen_label.config(text="No presentation active", image='')
        
        elif msg_type == 'presenter_changed':
            self.presenter = msg['presenter']
            if self.presenter:
                self.screen_label.config(text=f"{self.presenter} is presenting...")
                if self.presenter == self.username:
                    self.present_btn.config(text="Stop Presenting", state=tk.NORMAL)
                else:
                    self.present_btn.config(text="Start Presenting", state=tk.DISABLED)
            else:
                self.screen_label.config(text="No presentation active", image='')
                self.present_btn.config(text="Start Presenting", state=tk.NORMAL)
        
        elif msg_type == 'screen_frame':
            if msg['presenter'] == self.presenter and msg['presenter'] != self.username:
                # Display screen frame
                try:
                    img_data = base64.b64decode(msg['frame'])
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Resize to fit display area
                    display_width = self.screen_label.winfo_width() or 800
                    display_height = self.screen_label.winfo_height() or 600
                    img.thumbnail((display_width, display_height), Image.LANCZOS)
                    
                    photo = ImageTk.PhotoImage(img)
                    self.screen_label.config(image=photo, text='')
                    self.screen_label.image = photo  # Keep reference
                except Exception as e:
                    print(f"Screen frame display error: {e}")
        
        elif msg_type == 'file_available':
            # Add file to listbox
            filename = msg['filename']
            if filename not in [self.files_listbox.get(i) for i in range(self.files_listbox.size())]:
                self.files_listbox.insert(tk.END, filename)
            
            self.display_chat_message({
                'username': 'System',
                'message': f"{msg['username']} shared file: {filename} ({msg['filesize']} bytes)",
                'timestamp': msg['timestamp']
            })
        
        elif msg_type == 'file_data':
            # Save downloaded file
            try:
                filename = msg['filename']
                filedata = base64.b64decode(msg['filedata'])
                
                # Ask user where to save
                save_path = filedialog.asksaveasfilename(initialfile=filename)
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(filedata)
                    messagebox.showinfo("Success", f"File saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {e}")
    
    def receive_udp_streams(self):
        """Receive UDP video and audio streams"""
        while self.running and self.connected:
            try:
                data, addr = self.udp_socket.recvfrom(65535)
                
                if len(data) < 2:
                    continue
                
                stream_type = data[0]  # 1=video, 2=audio
                username_len = data[1]
                
                if len(data) < 2 + username_len:
                    continue
                
                username = data[2:2+username_len].decode('utf-8')
                payload = data[2+username_len:]
                
                if stream_type == 1:  # Video
                    # Decode video frame
                    try:
                        nparr = np.frombuffer(payload, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if frame is not None:
                            self.video_frames[username] = frame
                    except Exception as e:
                        print(f"Video decode error: {e}")
                
                elif stream_type == 2:  # Audio
                    # Play audio
                    if self.audio_output_stream and self.audio_streaming:
                        try:
                            self.audio_output_stream.write(payload)
                        except Exception as e:
                            print(f"Audio playback error: {e}")
            
            except Exception as e:
                if self.running:
                    print(f"UDP receive error: {e}")
    
    def update_users_list(self):
        """Update the users listbox"""
        self.users_listbox.delete(0, tk.END)
        for user in self.users:
            display_name = f"{user} (You)" if user == self.username else user
            self.users_listbox.insert(tk.END, display_name)
    
    def update_video_grid(self):
        """Update video display grid"""
        # Clear existing video labels
        for widget in self.video_container.winfo_children():
            widget.destroy()
        
        # Create grid for video frames
        num_videos = len(self.video_frames)
        if num_videos == 0:
            label = ttk.Label(self.video_container, text="No active video streams", anchor=tk.CENTER)
            label.pack(expand=True, fill=tk.BOTH)
            return
        
        # Calculate grid dimensions
        cols = min(3, num_videos)
        rows = (num_videos + cols - 1) // cols
        
        for i, (username, frame) in enumerate(self.video_frames.items()):
            row = i // cols
            col = i % cols
            
            # Create frame widget
            video_widget = ttk.Frame(self.video_container, relief=tk.RIDGE, borderwidth=2)
            video_widget.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # Username label
            name_label = ttk.Label(video_widget, text=username, anchor=tk.CENTER)
            name_label.pack(side=tk.TOP)
            
            # Video display
            try:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                photo = ImageTk.PhotoImage(img)
                
                video_label = tk.Label(video_widget, image=photo)
                video_label.image = photo  # Keep reference
                video_label.pack(expand=True)
            except Exception as e:
                error_label = ttk.Label(video_widget, text=f"Error: {e}")
                error_label.pack()
        
        # Configure grid weights for responsive layout
        for i in range(cols):
            self.video_container.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            self.video_container.grid_rowconfigure(i, weight=1)
        
        # Schedule next update
        if self.running:
            self.master.after(100, self.update_video_grid)
    
    def on_closing(self):
        """Handle window close event"""
        if self.connected:
            self.video_streaming = False
            self.audio_streaming = False
            self.presenting = False

            if self.tcp_socket:
                try:
                    self.tcp_socket.close()
                except:
                    pass
            if self.udp_socket:
                try:
                    self.udp_socket.close()
                except:
                    pass

        self.running = False
        self.master.destroy()
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    client_app = LANClient(root)
    root.mainloop()
