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
        self.master.title("🌐 LAN Collaboration Suite")
        self.master.geometry("1400x900")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Sleek modern color scheme - Deep dark theme with neon accents
        self.colors = {
            'bg_dark': '#0d1117',           # Deep dark background
            'bg_medium': '#161b22',         # Card background
            'bg_light': '#21262d',          # Input background
            'bg_hover': '#30363d',          # Hover state
            'accent_cyan': '#58a6ff',       # Bright cyan
            'accent_purple': '#bc8cff',     # Soft purple
            'accent_green': '#3fb950',      # Green success
            'accent_red': '#f85149',        # Red accent
            'accent_orange': '#ff9500',     # Orange accent
            'text_light': '#c9d1d9',        # Light text
            'text_dim': '#8b949e',          # Dimmed text
            'border': '#30363d',            # Border color
            'success': '#3fb950',
            'error': '#f85149'
        }
        
        # Configure main window background
        self.master.configure(bg=self.colors['bg_dark'])
        
        # Connection state
        self.connected = False
        self.username = None
        self.server_ip = None
        self.server_tcp_port = 5555
        self.server_udp_port = 5556
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
        # Create styled frame
        frame = tk.Frame(self.master, bg=self.colors['bg_dark'])
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Center container with rounded effect
        center = tk.Frame(frame, bg=self.colors['bg_medium'], padx=50, pady=50)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Large icon/logo area
        logo_frame = tk.Frame(center, bg=self.colors['bg_medium'])
        logo_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Title with modern styling
        title = tk.Label(logo_frame, text="🌐", 
                        font=('SF Pro Display', 48),
                        bg=self.colors['bg_medium'], 
                        fg=self.colors['accent_cyan'])
        title.pack()
        
        title_text = tk.Label(logo_frame, text="LAN Collaboration Suite", 
                        font=('SF Pro Display', 26, 'bold'),
                        bg=self.colors['bg_medium'], 
                        fg=self.colors['text_light'])
        title_text.pack(pady=(10, 0))
        
        subtitle = tk.Label(logo_frame, text="Connect • Collaborate • Communicate", 
                           font=('SF Pro Display', 12),
                           bg=self.colors['bg_medium'], 
                           fg=self.colors['text_dim'])
        subtitle.pack(pady=(5, 0))
        
        # Divider line
        divider = tk.Frame(center, bg=self.colors['border'], height=1)
        divider.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        
        # Input fields with modern styling
        fields = [
            ("👤  Username", "username_entry", "", self.colors['accent_cyan']),
            ("🌐  Server IP", "server_entry", "127.0.0.1", self.colors['accent_purple']),
            ("🔌  TCP Port", "tcp_port_entry", "5555", self.colors['accent_green']),
            ("📡  UDP Port", "udp_port_entry", "5556", self.colors['accent_orange'])
        ]
        
        for idx, (label_text, attr_name, default_val, accent_color) in enumerate(fields, start=2):
            # Container for each field
            field_container = tk.Frame(center, bg=self.colors['bg_medium'])
            field_container.grid(row=idx, column=0, columnspan=2, pady=10, sticky='ew')
            
            # Label
            label = tk.Label(field_container, text=label_text, 
                           font=('SF Pro Display', 11),
                           bg=self.colors['bg_medium'], 
                           fg=self.colors['text_dim'],
                           anchor='w')
            label.pack(anchor='w', pady=(0, 5))
            
            # Entry with custom styling and border
            entry_frame = tk.Frame(field_container, bg=accent_color, bd=0)
            entry_frame.pack(fill='x')
            
            entry = tk.Entry(entry_frame, width=35, 
                           font=('SF Pro Display', 12),
                           bg=self.colors['bg_light'], 
                           fg=self.colors['text_light'],
                           insertbackground=accent_color,
                           relief=tk.FLAT,
                           bd=0,
                           highlightthickness=0)
            entry.pack(padx=2, pady=2, ipady=8)
            
            if default_val:
                entry.insert(0, default_val)
                entry.config(fg=self.colors['text_dim'])
                
                # Add focus events for placeholder effect
                def on_focus_in(e, ent=entry, color=accent_color):
                    if ent.get() in ["127.0.0.1", "5555", "5556"]:
                        ent.config(fg=self.colors['text_light'])
                
                def on_focus_out(e, ent=entry):
                    if not ent.get():
                        ent.config(fg=self.colors['text_dim'])
                
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)
            
            setattr(self, attr_name, entry)
        
        # Stylish connect button with gradient effect
        btn_container = tk.Frame(center, bg=self.colors['bg_medium'])
        btn_container.grid(row=7, column=0, columnspan=2, pady=30)
        
        self.connect_btn = tk.Button(btn_container, text="🚀  CONNECT TO SERVER", 
                                     command=self.connect_to_server,
                                     font=('SF Pro Display', 13, 'bold'),
                                     bg=self.colors['accent_cyan'],
                                     fg='#000000',
                                     activebackground=self.colors['accent_purple'],
                                     activeforeground='#000000',
                                     relief=tk.FLAT,
                                     bd=0,
                                     padx=50,
                                     pady=15,
                                     cursor='hand2')
        self.connect_btn.pack()
        
        # Hover effect
        def on_enter(e):
            self.connect_btn.config(bg=self.colors['accent_purple'])
        def on_leave(e):
            self.connect_btn.config(bg=self.colors['accent_cyan'])
        
        self.connect_btn.bind('<Enter>', on_enter)
        self.connect_btn.bind('<Leave>', on_leave)
        
        # Status label
        self.status_label = tk.Label(center, text="", 
                                     font=('SF Pro Display', 11),
                                     bg=self.colors['bg_medium'], 
                                     fg=self.colors['error'])
        self.status_label.grid(row=8, column=0, columnspan=2, pady=(10, 0))
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
            self.server_tcp_port = int(self.tcp_port_entry.get())
            self.server_udp_port = int(self.udp_port_entry.get())
            tcp_port = self.server_tcp_port
            udp_port = self.server_udp_port
            
            self.status_label.config(text="Connecting...", foreground=self.colors['accent_cyan'])
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
            self.status_label.config(text=f"Connection failed: {e}", foreground=self.colors['error'])
            if self.tcp_socket:
                self.tcp_socket.close()
            if self.udp_socket:
                self.udp_socket.close()
    
    def build_main_ui(self):
        """Build main application UI"""
        # Clear connection UI
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Configure main window
        self.master.configure(bg=self.colors['bg_dark'])
        
        # Top bar with user info and controls
        top_bar = tk.Frame(self.master, bg=self.colors['bg_medium'], height=60)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Left side - User info
        left_info = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        left_info.pack(side=tk.LEFT, padx=20)
        
        # Connection status indicator (pulsing green dot)
        status_dot = tk.Label(left_info, text="⬤", 
                             font=('SF Pro Display', 14),
                             bg=self.colors['bg_medium'], 
                             fg=self.colors['success'])
        status_dot.pack(side=tk.LEFT, padx=(0, 8))
        
        user_label = tk.Label(left_info, text=f"{self.username}", 
                font=('SF Pro Display', 13, 'bold'),
                bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'])
        user_label.pack(side=tk.LEFT)
        
        server_label = tk.Label(left_info, text=f"connected to {self.server_ip}", 
                font=('SF Pro Display', 10),
                bg=self.colors['bg_medium'], 
                fg=self.colors['text_dim'])
        server_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Right side - Large clear QUIT button
        quit_container = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        quit_container.pack(side=tk.RIGHT, padx=15, pady=10)
        
        quit_btn = tk.Button(quit_container, text="⏻  QUIT", 
                            command=self.on_closing,
                            font=('SF Pro Display', 11, 'bold'),
                            bg=self.colors['accent_red'],
                            fg='#000000',
                            activebackground='#ff1744',
                            activeforeground='#000000',
                            relief=tk.FLAT,
                            bd=0,
                            padx=25,
                            pady=10,
                            cursor='hand2')
        quit_btn.pack()
        
        # Hover effect for quit button
        def on_quit_enter(e):
            quit_btn.config(bg='#ff1744', font=('SF Pro Display', 11, 'bold'))
        def on_quit_leave(e):
            quit_btn.config(bg=self.colors['accent_red'], font=('SF Pro Display', 11, 'bold'))
        
        quit_btn.bind('<Enter>', on_quit_enter)
        quit_btn.bind('<Leave>', on_quit_leave)
        
        # Create main layout with styled frames
        # Top: Video grid
        video_frame = self._create_styled_frame(self.master, "📹 Video Conference")
        video_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.video_container = tk.Frame(video_frame, bg=self.colors['bg_dark'])
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Video controls
        video_controls = tk.Frame(video_frame, bg=self.colors['bg_medium'])
        video_controls.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.video_btn = self._create_control_button(video_controls, "📹 Start Video", self.toggle_video, self.colors['accent_cyan'])
        self.video_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.audio_btn = self._create_control_button(video_controls, "🎤 Start Audio", self.toggle_audio, self.colors['accent_purple'])
        self.audio_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Middle: Screen sharing
        screen_frame = self._create_styled_frame(self.master, "🖥️ Screen Sharing")
        screen_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.screen_label = tk.Label(screen_frame, text="No presentation active", 
                                     font=('Helvetica Neue', 14),
                                     bg=self.colors['bg_dark'], 
                                     fg=self.colors['text_dim'],
                                     anchor=tk.CENTER)
        self.screen_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        screen_controls = tk.Frame(screen_frame, bg=self.colors['bg_medium'])
        screen_controls.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.present_btn = self._create_control_button(screen_controls, "🖥️ Start Presenting", self.toggle_presenting, self.colors['accent_green'])
        self.present_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Bottom: Chat and controls
        bottom_frame = tk.Frame(self.master, bg=self.colors['bg_dark'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Left: Users list
        users_frame = self._create_styled_frame(bottom_frame, "👥 Online Users")
        users_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        self.users_listbox = tk.Listbox(users_frame, width=20,
                                        font=('SF Pro Display', 10),
                                        bg=self.colors['bg_dark'],
                                        fg=self.colors['text_light'],
                                        selectbackground=self.colors['accent_cyan'],
                                        selectforeground='#000000',
                                        relief=tk.FLAT,
                                        bd=0,
                                        highlightthickness=0)
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_users_list()
        
        # Center: Chat
        chat_frame = self._create_styled_frame(bottom_frame, "💬 Group Chat")
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=10, 
                                                      state=tk.DISABLED, wrap=tk.WORD,
                                                      font=('SF Pro Display', 10),
                                                      bg=self.colors['bg_dark'],
                                                      fg=self.colors['text_light'],
                                                      relief=tk.FLAT,
                                                      bd=0,
                                                      highlightthickness=0)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        chat_input_frame = tk.Frame(chat_frame, bg=self.colors['bg_medium'])
        chat_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chat_entry = tk.Entry(chat_input_frame,
                                   font=('SF Pro Display', 11),
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['text_light'],
                                   insertbackground=self.colors['accent_cyan'],
                                   relief=tk.FLAT,
                                   bd=0)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=8)
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        send_btn = self._create_control_button(chat_input_frame, "📤 Send", self.send_chat, self.colors['accent_cyan'])
        send_btn.pack(side=tk.LEFT)
        
        # Right: File sharing
        file_frame = self._create_styled_frame(bottom_frame, "📁 Files")
        file_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        
        upload_btn = self._create_control_button(file_frame, "📤 Upload", self.upload_file, self.colors['accent_green'])
        upload_btn.pack(fill=tk.X, padx=5, pady=5)
        
        self.files_listbox = tk.Listbox(file_frame, width=25, height=8,
                                        font=('SF Pro Display', 9),
                                        bg=self.colors['bg_dark'],
                                        fg=self.colors['text_light'],
                                        selectbackground=self.colors['accent_purple'],
                                        selectforeground='#000000',
                                        relief=tk.FLAT,
                                        bd=0,
                                        highlightthickness=0)
        self.files_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        download_btn = self._create_control_button(file_frame, "📥 Download", self.download_file, self.colors['accent_cyan'])
        download_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Initialize video display
        self.update_video_grid()
    
    def _create_styled_frame(self, parent, title):
        """Create a styled frame with title"""
        # Outer container with subtle border
        outer = tk.Frame(parent, bg=self.colors['border'], bd=0)
        container = tk.Frame(outer, bg=self.colors['bg_medium'], bd=0)
        container.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        # Title bar with gradient-like effect
        title_bar = tk.Frame(container, bg=self.colors['bg_medium'], height=40)
        title_bar.pack(side=tk.TOP, fill=tk.X)
        title_bar.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(title_bar, text=title, 
                font=('SF Pro Display', 13, 'bold'),
                bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'])
        title_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Subtle divider line
        divider = tk.Frame(container, bg=self.colors['border'], height=1)
        divider.pack(fill=tk.X)
        
        return outer
    
    def _create_control_button(self, parent, text, command, color):
        """Create a styled control button with hover effects"""
        # Determine text color - black for all buttons for better visibility
        btn = tk.Button(parent, text=text, 
                        command=command,
                        font=('SF Pro Display', 11, 'bold'),
                        bg=color,
                        fg='#000000',  # Black text for all buttons
                        activebackground=color,
                        activeforeground='#000000',
                        relief=tk.FLAT,
                        bd=0,
                        padx=20,
                        pady=10,
                        cursor='hand2')
        
        # Add hover effects
        def on_enter(e):
            btn.config(bg=self._lighten_color(color))
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color slightly for hover effect"""
        # Simple lightening - just for visual effect
        color_map = {
            self.colors['accent_cyan']: '#7eb8ff',
            self.colors['accent_purple']: '#d4a3ff',
            self.colors['accent_green']: '#56c96a',
            self.colors['accent_orange']: '#ffad33',
            self.colors['accent_red']: '#ff6961'
        }
        return color_map.get(hex_color, hex_color)
    
    def toggle_video(self):
        """Toggle video streaming"""
        if not self.video_streaming:
            try:
                # Try to open camera with proper backend
                self.video_cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # macOS specific
                
                # Wait a bit for camera to initialize
                time.sleep(0.5)
                
                if not self.video_cap.isOpened():
                    # Try again without backend specification
                    self.video_cap = cv2.VideoCapture(0)
                    time.sleep(0.5)
                
                if not self.video_cap.isOpened():
                    messagebox.showerror("Error", 
                        "Cannot access webcam.\n\n" +
                        "Please grant Camera permission:\n" +
                        "System Preferences → Security & Privacy → Camera\n" +
                        "Enable for Terminal/Python, then restart the client.")
                    return
                
                # Test read
                ret, test_frame = self.video_cap.read()
                if not ret or test_frame is None:
                    messagebox.showerror("Error", "Camera opened but cannot read frames. Try restarting the client.")
                    self.video_cap.release()
                    return
                
                self.video_streaming = True
                # Update button in main thread
                self.master.after(0, lambda: self.video_btn.config(text="⏹️ Stop Video"))
                threading.Thread(target=self.stream_video, daemon=True).start()
                print(f"✅ Video started successfully for {self.username}")
            except Exception as e:
                messagebox.showerror("Error", f"Video error: {e}\n\nTry restarting the client.")
                if self.video_cap:
                    try:
                        self.video_cap.release()
                    except:
                        pass
        else:
            # Stop video streaming
            self.video_streaming = False
            
            # Wait for thread to notice
            time.sleep(0.2)
            
            # Update button in main thread
            self.master.after(0, lambda: self.video_btn.config(text="📹 Start Video"))
            
            # Safely close camera in separate thread
            threading.Thread(target=self._close_camera, daemon=True).start()
            
            # Remove own video from display
            if self.username in self.video_frames:
                del self.video_frames[self.username]
            
            print(f"Video stopped for {self.username}")
    
    def _close_camera(self):
        """Safely close camera without blocking"""
        try:
            if self.video_cap:
                try:
                    self.video_cap.release()
                except Exception as e:
                    print(f"Camera close error: {e}")
                self.video_cap = None
        except Exception as e:
            print(f"Error closing camera: {e}")
    
    def stream_video(self):
        """Stream video to server"""
        print(f"📹 Starting video stream for {self.username}")
        frame_count = 0
        error_count = 0
        
        while self.video_streaming and self.running:
            try:
                ret, frame = self.video_cap.read()
                if not ret or frame is None:
                    error_count += 1
                    if error_count > 10:
                        print(f"⚠️ Camera read failed multiple times, stopping video")
                        self.video_streaming = False
                        break
                    time.sleep(0.1)
                    continue
                
                error_count = 0  # Reset on successful read
                
                # Resize and compress MORE to avoid UDP packet size limit (65507 bytes)
                frame = cv2.resize(frame, (320, 240))
                
                # Try higher compression first
                encode_param = [cv2.IMWRITE_JPEG_QUALITY, 40]  # Lower quality = smaller
                _, buffer = cv2.imencode('.jpg', frame, encode_param)
                
                # Check size and reduce if needed
                if len(buffer) > 60000:  # Safety margin
                    encode_param = [cv2.IMWRITE_JPEG_QUALITY, 30]
                    _, buffer = cv2.imencode('.jpg', frame, encode_param)
                
                if len(buffer) > 60000:  # Still too big, resize smaller
                    frame = cv2.resize(frame, (240, 180))
                    encode_param = [cv2.IMWRITE_JPEG_QUALITY, 40]
                    _, buffer = cv2.imencode('.jpg', frame, encode_param)
                
                # Create packet: type(1) + username_len(1) + username + frame_data
                username_bytes = self.username.encode('utf-8')
                packet = bytes([1, len(username_bytes)]) + username_bytes + buffer.tobytes()
                
                # Final size check
                if len(packet) > 65000:
                    print(f"⚠️ Packet too large ({len(packet)} bytes), skipping frame")
                    continue
                
                # Send via UDP (using stored port, not GUI widget)
                self.udp_socket.sendto(packet, (self.server_ip, self.server_udp_port))
                
                # Update own video (thread-safe) - resize back for display
                display_frame = cv2.resize(frame, (320, 240))
                self.video_frames[self.username] = display_frame.copy()
                
                frame_count += 1
                if frame_count % 90 == 0:  # Log every 90 frames (3 seconds)
                    print(f"📹 Sent {frame_count} video frames")
                
                time.sleep(0.033)  # ~30 FPS
            except Exception as e:
                # Only print error once, not repeatedly
                if frame_count % 30 == 0:
                    print(f"Video stream error: {e}")
                time.sleep(0.1)
        
        print(f"📹 Video stream stopped for {self.username}")
    
    def toggle_audio(self):
        """Toggle audio streaming"""
        if not self.audio_streaming:
            try:
                # Check if audio device is available
                if self.audio.get_device_count() == 0:
                    messagebox.showerror("Error", "No audio devices found")
                    return
                
                print(f"🎤 Opening audio devices for {self.username}...")
                
                # Get default devices
                try:
                    default_input = self.audio.get_default_input_device_info()
                    default_output = self.audio.get_default_output_device_info()
                    print(f"   Input device: {default_input['name']}")
                    print(f"   Output device: {default_output['name']}")
                except Exception as e:
                    print(f"   Warning: Could not get default device info: {e}")
                
                # Input stream (microphone) - with better error handling
                try:
                    self.audio_input_stream = self.audio.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048,
                        input_device_index=None,  # Use default
                        stream_callback=None
                    )
                    print(f"   ✓ Microphone opened")
                except Exception as e:
                    raise Exception(f"Microphone error: {e}")
                
                # Output stream (speakers)
                try:
                    self.audio_output_stream = self.audio.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        output=True,
                        frames_per_buffer=2048,
                        output_device_index=None,  # Use default
                        stream_callback=None
                    )
                    print(f"   ✓ Speakers opened")
                except Exception as e:
                    # Close input stream if output fails
                    if self.audio_input_stream:
                        try:
                            self.audio_input_stream.close()
                        except:
                            pass
                    raise Exception(f"Speaker error: {e}")
                
                self.audio_streaming = True
                # Update button in main thread
                self.master.after(0, lambda: self.audio_btn.config(text="⏹️ Stop Audio"))
                threading.Thread(target=self.stream_audio, daemon=True).start()
                print(f"🎤 Audio started successfully for {self.username}")
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Audio error: {e}")
                
                if "already in use" in error_msg.lower() or "device unavailable" in error_msg.lower():
                    self.master.after(0, lambda: messagebox.showerror("Error", 
                        "Audio device is busy.\n\n" +
                        "This can happen when testing on the same computer.\n" +
                        "Close the other client's audio first, or test on separate computers."))
                elif "-9999" in error_msg or "Unanticipated host error" in error_msg:
                    self.master.after(0, lambda: messagebox.showerror("Audio Error", 
                        "Audio device initialization failed.\n\n" +
                        "Solutions:\n" +
                        "1. Grant Microphone permission in System Preferences\n" +
                        "2. Close other apps using microphone/speakers\n" +
                        "3. Try restarting the client\n" +
                        "4. Check if headphones/mic are properly connected"))
                else:
                    self.master.after(0, lambda e=e: messagebox.showerror("Error", f"Audio error: {e}"))
        else:
            # Stop audio streaming
            self.audio_streaming = False
            
            # Wait a moment for threads to notice the flag
            time.sleep(0.3)
            
            # Update button in main thread
            self.master.after(0, lambda: self.audio_btn.config(text="🎤 Start Audio"))
            
            # Safely close streams in a separate thread to avoid blocking
            threading.Thread(target=self._close_audio_streams, daemon=True).start()
            
            print(f"🎤 Audio stopping for {self.username}...")
    
    def _close_audio_streams(self):
        """Safely close audio streams without blocking"""
        try:
            if self.audio_input_stream:
                try:
                    self.audio_input_stream.stop_stream()
                    self.audio_input_stream.close()
                except Exception as e:
                    print(f"Input stream close error: {e}")
                self.audio_input_stream = None
        except Exception as e:
            print(f"Error closing input: {e}")
        
        try:
            if self.audio_output_stream:
                try:
                    self.audio_output_stream.stop_stream()
                    self.audio_output_stream.close()
                except Exception as e:
                    print(f"Output stream close error: {e}")
                self.audio_output_stream = None
        except Exception as e:
            print(f"Error closing output: {e}")
    
    def stream_audio(self):
        """Stream audio to server"""
        packet_count = 0
        while self.audio_streaming and self.running:
            try:
                if not self.audio_input_stream:
                    break
                    
                data = self.audio_input_stream.read(2048, exception_on_overflow=False)
                
                # Create packet: type(2) + username_len + username + audio_data
                username_bytes = self.username.encode('utf-8')
                packet = bytes([2, len(username_bytes)]) + username_bytes + data
                
                # Send via UDP (using stored port, not GUI widget)
                self.udp_socket.sendto(packet, (self.server_ip, self.server_udp_port))
                
                packet_count += 1
                # Log every 50 packets to confirm sending
                if packet_count % 50 == 0:
                    print(f"🎙️ Sent {packet_count} audio packets")
                    
            except OSError as e:
                # Stream was closed, exit gracefully
                print(f"Audio stream closed: {e}")
                break
            except Exception as e:
                print(f"Audio stream error: {e}")
                break
        
        print(f"🎤 Audio streaming thread ended for {self.username} (sent {packet_count} packets)")
    
    def toggle_presenting(self):
        """Toggle screen sharing"""
        if not self.presenting:
            self.send_message({'type': 'start_presenting'})
            self.presenting = True
            self.present_btn.config(text="⏹️ Stop Presenting")
            threading.Thread(target=self.stream_screen, daemon=True).start()
        else:
            self.send_message({'type': 'stop_presenting'})
            self.presenting = False
            self.present_btn.config(text="🖥️ Start Presenting")
    
    def stream_screen(self):
        """Stream screen to server"""
        print(f"📺 Starting screen share for {self.username}")
        frame_count = 0
        
        try:
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
                        
                        frame_count += 1
                        if frame_count % 30 == 0:  # Log every 30 frames
                            print(f"📺 Sent {frame_count} screen frames")
                        
                        time.sleep(0.1)  # 10 FPS for screen sharing
                    except Exception as e:
                        print(f"Screen share frame error: {e}")
                        time.sleep(0.5)  # Wait before retry
                        
        except Exception as e:
            print(f"Screen share fatal error: {e}")
        finally:
            print(f"📺 Screen share stopped for {self.username}")
    
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
                    if self.running:  # Only print if we didn't intentionally close
                        print("Disconnected from server")
                    break
                
                self.process_tcp_message(msg)
            except OSError as e:
                # Socket was closed (expected during shutdown)
                if self.running:
                    print(f"Connection closed: {e}")
                break
            except Exception as e:
                if self.running:
                    print(f"TCP receive error: {e}")
                break
        
        # Mark as disconnected
        self.connected = False
    
    def process_tcp_message(self, msg):
        """Process received TCP messages"""
        msg_type = msg.get('type')
        
        if msg_type == 'chat':
            self.display_chat_message(msg)
        
        elif msg_type == 'user_joined':
            self.users = msg['users']
            self.master.after(0, self.update_users_list)
            self.display_chat_message({
                'username': 'System',
                'message': f"{msg['username']} joined the session",
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
        
        elif msg_type == 'user_left':
            self.users = msg['users']
            self.master.after(0, self.update_users_list)
            self.display_chat_message({
                'username': 'System',
                'message': f"{msg['username']} left the session",
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            # Remove their video frame
            if msg['username'] in self.video_frames:
                del self.video_frames[msg['username']]
            
            # Clear presenter if they left
            if self.presenter == msg['username']:
                self.presenter = None
                self.master.after(0, lambda: self.screen_label.config(text="No presentation active", image=''))
        
        elif msg_type == 'presenter_changed':
            self.presenter = msg['presenter']
            if self.presenter:
                self.master.after(0, lambda: self.screen_label.config(text=f"{self.presenter} is presenting..."))
                if self.presenter == self.username:
                    self.master.after(0, lambda: self.present_btn.config(text="⏹️ Stop Presenting", state=tk.NORMAL))
                else:
                    self.master.after(0, lambda: self.present_btn.config(text="🖥️ Start Presenting", state=tk.DISABLED))
            else:
                self.master.after(0, lambda: self.screen_label.config(text="No presentation active", image=''))
                self.master.after(0, lambda: self.present_btn.config(text="🖥️ Start Presenting", state=tk.NORMAL))
        
        elif msg_type == 'screen_frame':
            if msg['presenter'] == self.presenter and msg['presenter'] != self.username:
                # Display screen frame
                try:
                    img_data = base64.b64decode(msg['frame'])
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Resize to fit display area
                    display_width = 800
                    display_height = 600
                    img.thumbnail((display_width, display_height), Image.LANCZOS)
                    
                    photo = ImageTk.PhotoImage(img)
                    # Update GUI in main thread
                    self.master.after(0, lambda p=photo: self._update_screen_display(p))
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
                    # Decode video frame (in background thread is OK)
                    try:
                        nparr = np.frombuffer(payload, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if frame is not None:
                            # Just store the frame, GUI will display it
                            self.video_frames[username] = frame.copy()
                    except Exception as e:
                        pass  # Silently skip bad frames
                
                elif stream_type == 2:  # Audio
                    # Play audio (can be done in background thread)
                    try:
                        if self.audio_output_stream and self.audio_streaming:
                            # Only play audio from others, not ourselves
                            if username != self.username:
                                # Log occasionally for debugging
                                if not hasattr(self, '_audio_packet_count'):
                                    self._audio_packet_count = {}
                                
                                if username not in self._audio_packet_count:
                                    self._audio_packet_count[username] = 0
                                
                                self._audio_packet_count[username] += 1
                                
                                # Log every 50 packets
                                if self._audio_packet_count[username] % 50 == 0:
                                    print(f"🔊 Received {self._audio_packet_count[username]} audio packets from {username}")
                                
                                self.audio_output_stream.write(payload, exception_on_underflow=False)
                    except Exception as e:
                        # Log audio playback errors occasionally
                        if not hasattr(self, '_audio_error_logged'):
                            self._audio_error_logged = True
                            print(f"⚠️ Audio playback error: {e}")
            
            except Exception as e:
                if self.running:
                    pass  # Silently handle UDP errors
    
    def update_users_list(self):
        """Update the users listbox"""
        self.users_listbox.delete(0, tk.END)
        for user in self.users:
            display_name = f"{user} (You)" if user == self.username else user
            self.users_listbox.insert(tk.END, display_name)
    
    def _update_screen_display(self, photo):
        """Update screen display in main thread"""
        try:
            self.screen_label.config(image=photo, text='')
            self.screen_label.image = photo  # Keep reference
        except:
            pass
    
    def update_video_grid(self):
        """Update video display grid - MUST run in main thread"""
        if not self.running or not self.connected:
            return
        
        try:
            # Clear existing video labels
            for widget in self.video_container.winfo_children():
                widget.destroy()
            
            # Create grid for video frames
            num_videos = len(self.video_frames)
            if num_videos == 0:
                label = tk.Label(self.video_container, 
                               text="📹 No active video streams\n\nClick 'Start Video' to begin", 
                               font=('Helvetica Neue', 13),
                               anchor=tk.CENTER, 
                               bg=self.colors['bg_dark'], 
                               fg=self.colors['text_dim'])
                label.pack(expand=True, fill=tk.BOTH)
                self.master.after(200, self.update_video_grid)
                return
            
            # Calculate grid dimensions
            cols = min(3, num_videos)
            rows = (num_videos + cols - 1) // cols
            
            for i, (username, frame) in enumerate(list(self.video_frames.items())):
                row = i // cols
                col = i % cols
                
                try:
                    # Create frame container with modern styling
                    video_frame = tk.Frame(self.video_container, 
                                         bg=self.colors['bg_light'],
                                         relief=tk.FLAT,
                                         highlightbackground=self.colors['accent_cyan'],
                                         highlightthickness=2)
                    video_frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
                    
                    # Username label with gradient-like effect
                    name_label = tk.Label(video_frame, 
                                        text=f"👤 {username}", 
                                        bg=self.colors['bg_medium'], 
                                        fg=self.colors['accent_cyan'], 
                                        font=('Helvetica Neue', 10, 'bold'),
                                        pady=5)
                    name_label.pack(side=tk.TOP, fill=tk.X)
                    
                    # Video display
                    # Convert BGR to RGB
                    frame_copy = frame.copy()
                    rgb_frame = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb_frame)
                    photo = ImageTk.PhotoImage(img)
                    
                    video_label = tk.Label(video_frame, image=photo, bg=self.colors['bg_dark'])
                    video_label.image = photo  # Keep reference
                    video_label.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)
                    
                except Exception as e:
                    # Silently skip this frame, will try again in next update
                    pass
            
            # Configure grid weights for responsive layout
            for i in range(cols):
                self.video_container.grid_columnconfigure(i, weight=1)
            for i in range(rows):
                self.video_container.grid_rowconfigure(i, weight=1)
            
        except Exception as e:
            # Silently handle errors
            pass
        
        # Schedule next update
        self.master.after(200, self.update_video_grid)
    
    def on_closing(self):
        """Handle window close event"""
        if self.connected:
            self.video_streaming = False
            self.audio_streaming = False
            self.presenting = False
            self.running = False
            
            # Wait a moment for threads to stop
            time.sleep(0.3)
            
            # Use safe audio stream closing
            self._close_audio_streams()
            
            # Use safe camera closing
            self._close_camera()
            
            # Close sockets
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
        else:
            self.running = False
        
        try:
            self.master.destroy()
        except:
            pass
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    client_app = LANClient(root)
    root.mainloop()
