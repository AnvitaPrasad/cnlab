# LAN-Based All-in-One Collaboration Suite

A comprehensive multi-user communication application for Local Area Networks (LAN) featuring video conferencing, audio chat, screen sharing, text messaging, and file transfer.

## 📋 Features

### ✅ Core Modules Implemented

1. **Multi-User Video Conferencing**
   - Real-time webcam capture and transmission
   - UDP-based video streaming for low latency
   - Dynamic grid layout for multiple participants
   - 320x240 resolution at ~30 FPS
   - JPEG compression for bandwidth efficiency

2. **Multi-User Audio Conferencing**
   - Microphone capture and transmission
   - UDP-based audio streaming
   - 16kHz sample rate, mono channel
   - Real-time audio playback

3. **Screen Sharing / Slide Presentation**
   - Full screen capture
   - TCP-based transmission for reliability
   - 800x600 resolution at ~10 FPS
   - JPEG compression (60% quality)
   - Single presenter mode with controls

4. **Group Text Chat**
   - Real-time messaging
   - TCP-based reliable delivery
   - Persistent chat history
   - Timestamps for all messages
   - System notifications (user join/leave)

5. **File Sharing**
   - Upload files to server
   - Broadcast file availability to all clients
   - Download files on demand
   - Base64 encoding for reliable transfer
   - File size display

## 🔧 System Requirements

### Hardware
- Webcam (for video conferencing)
- Microphone (for audio conferencing)
- Speakers/Headphones (for audio playback)
- Network: LAN connection (WiFi or Ethernet)

### Software
- **Operating System**: macOS, Linux, or Windows 10/11
- **Python**: 3.8 or higher
- **Dependencies**: See requirements.txt

## 📦 Installation

### Step 1: Install Python Dependencies

The following packages are required:
- `opencv-python` - Video capture and processing
- `numpy` - Array operations
- `Pillow` - Image processing
- `pyaudio` - Audio I/O
- `mss` - Screen capture

**Installation (Already done in your virtual environment):**
```bash
# Activate your virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows

# Install dependencies
pip install opencv-python numpy Pillow pyaudio mss
```

### Step 2: Additional Setup (macOS)

On macOS, you may need to grant permissions:
1. **Camera Access**: System Preferences → Security & Privacy → Camera
2. **Microphone Access**: System Preferences → Security & Privacy → Microphone
3. **Screen Recording**: System Preferences → Security & Privacy → Screen Recording

## 🚀 Quick Start Guide

### Starting the Server

1. **Open a terminal** in the project directory

2. **Run the server:**
   ```bash
   /Users/anvitaprasad/Desktop/cnlabstuff/.venv/bin/python server.py
   ```

3. **Note the Server IP address** displayed in the terminal:
   ```
   ==================================================
   LAN Communication Server
   ==================================================
   Server IP: 192.168.1.100  ← Use this IP in clients
   TCP Port: 5555
   UDP Port: 5556
   ==================================================
   ```

### Starting the Client(s)

1. **Open a new terminal** (keep server running)

2. **Run the client:**
   ```bash
   /Users/anvitaprasad/Desktop/cnlabstuff/.venv/bin/python client.py
   ```

3. **Fill in the connection details:**
   - **Username**: Choose any unique username (e.g., "Alice")
   - **Server IP**: Enter the IP shown by the server (e.g., "192.168.1.100")
   - **TCP Port**: 5555 (default)
   - **UDP Port**: 5556 (default)

4. **Click "Connect"**

5. **Repeat steps 1-4** in additional terminals to simulate multiple users (use different usernames)

## 🧪 Testing Instructions

### Test 1: Basic Connection
**Objective**: Verify client-server connectivity

1. Start the server
2. Start 2-3 clients with different usernames
3. **Expected Result**: 
   - All clients connect successfully
   - Users list shows all connected participants
   - System messages appear in chat: "User X joined the session"

### Test 2: Group Chat
**Objective**: Test text messaging

1. Connect multiple clients (2+)
2. Type a message in one client and press Enter/Send
3. **Expected Result**: 
   - Message appears in all clients' chat windows
   - Format: `[HH:MM:SS] Username: Message`
   - Chat history preserved when new users join

### Test 3: Video Conferencing
**Objective**: Test video streaming

1. Connect 2+ clients
2. Click "Start Video" on one client
3. Wait 2-3 seconds
4. Click "Start Video" on another client
5. **Expected Result**:
   - Each client sees their own video and others' videos
   - Videos appear in a grid layout
   - ~30 FPS smooth playback
   - Minimal lag (<1 second)

### Test 4: Audio Conferencing
**Objective**: Test audio streaming

1. Connect 2 clients on different computers (or use headphones to prevent echo)
2. Click "Start Audio" on both clients
3. Speak into microphone
4. **Expected Result**:
   - Other participants hear your voice
   - Minimal latency
   - Clear audio quality

### Test 5: Screen Sharing
**Objective**: Test presentation mode

1. Connect 2+ clients
2. On one client, click "Start Presenting"
3. **Expected Result**:
   - Screen sharing area shows "Username is presenting..."
   - Presenter's screen appears on other clients
   - Other clients cannot start presenting (button disabled)
4. Click "Stop Presenting"
5. **Expected Result**:
   - Presentation stops on all clients
   - Button re-enabled for others

### Test 6: File Sharing
**Objective**: Test file transfer

1. Connect 2+ clients
2. On one client, click "Upload File"
3. Select any file (try a small PDF or image first)
4. **Expected Result**:
   - Success message appears
   - All clients see file in "File Sharing" list
   - System message in chat: "User shared file: filename.ext"
5. On another client, select the file and click "Download Selected"
6. Choose save location
7. **Expected Result**:
   - File downloads successfully
   - Content matches original file

### Test 7: User Disconnection
**Objective**: Test graceful disconnect handling

1. Connect 3+ clients with video enabled
2. Close one client window
3. **Expected Result**:
   - Other clients see "User X left the session"
   - User removed from users list
   - Video grid updates (removed user's video disappears)
   - If presenter disconnects, presentation stops

### Test 8: Concurrent Features
**Objective**: Test all features simultaneously

1. Connect 3+ clients
2. Start video on all clients
3. Start audio on all clients
4. Start presenting on one client
5. Send chat messages
6. Upload and download files
7. **Expected Result**:
   - All features work concurrently
   - No crashes or freezes
   - Smooth performance

## 🏗️ Architecture

### Network Protocol

**Client-Server Architecture**
- **Server**: Central hub managing all connections and data relay
- **Clients**: Connect to server for all communications

**Communication Protocols**
- **TCP (Port 5555)**: Control messages, chat, file transfer
  - Reliable, ordered delivery
  - Length-prefixed JSON messages
- **UDP (Port 5556)**: Video and audio streams
  - Low latency, allows some packet loss
  - Custom binary packet format

### Data Flow

```
Video/Audio: Client → UDP → Server → UDP → Other Clients
Chat/Files:  Client → TCP → Server → TCP → All Clients
Screen:      Presenter → TCP → Server → TCP → Viewers
```

### Message Format

**TCP Messages** (JSON):
```json
{
  "type": "message_type",
  "data": "..."
}
```

**UDP Packets** (Binary):
```
[Type:1][Username_Len:1][Username:N][Payload:...]
Type: 1=Video, 2=Audio
```

## 📝 Usage Guide

### Main Interface Layout

```
┌─────────────────────────────────────────────┐
│         Video Conference                    │
│  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │ User1  │  │ User2  │  │ User3  │        │
│  │ [video]│  │ [video]│  │ [video]│        │
│  └────────┘  └────────┘  └────────┘        │
│  [Start Video] [Start Audio]                │
├─────────────────────────────────────────────┤
│         Screen Sharing                      │
│  ┌─────────────────────────────────────┐   │
│  │    [Presentation Area]              │   │
│  └─────────────────────────────────────┘   │
│  [Start Presenting]                         │
├─────────────────────────────────────────────┤
│ Users   │  Group Chat      │ File Sharing  │
│ • User1 │ [Chat Display]   │ [File List]   │
│ • User2 │                  │               │
│ • User3 │ [Message Input]  │ [Upload]      │
│         │ [Send]           │ [Download]    │
└─────────────────────────────────────────────┘
```

### Controls

- **Start/Stop Video**: Toggle webcam streaming
- **Start/Stop Audio**: Toggle microphone
- **Start/Stop Presenting**: Share your screen (exclusive)
- **Send**: Send chat message (or press Enter)
- **Upload File**: Select and share a file
- **Download Selected**: Download selected file from list

## 🔍 Troubleshooting

### Camera Not Working
- **macOS**: Grant Camera permission in System Preferences
- **Linux**: Check `/dev/video0` permissions
- **All**: Ensure no other app is using the camera

### Microphone Not Working
- Check microphone permissions
- Verify microphone is not muted
- Try adjusting system volume

### Connection Failed
- Verify server is running
- Check IP address matches server's displayed IP
- Ensure both devices on same LAN
- Check firewall settings (allow ports 5555, 5556)

### High Latency / Lag
- Close bandwidth-heavy applications
- Reduce number of simultaneous video streams
- Use wired Ethernet instead of WiFi

### Audio Echo
- Use headphones instead of speakers
- Reduce speaker volume
- Enable echo cancellation if available

## 📊 Performance Specifications

| Feature | Resolution/Quality | FPS/Rate | Protocol | Bandwidth* |
|---------|-------------------|----------|----------|------------|
| Video | 320x240, JPEG 50% | ~30 FPS | UDP | ~200-400 Kbps/stream |
| Audio | 16kHz Mono | 16000 Hz | UDP | ~128 Kbps |
| Screen | 800x600, JPEG 60% | ~10 FPS | TCP | ~500-800 Kbps |
| Chat | Text | Real-time | TCP | <1 Kbps |
| Files | Variable | On-demand | TCP | Variable |

*Bandwidth estimates per stream

## 🔐 Security Notes

⚠️ **Important**: This application is designed for trusted LAN environments only.

- No encryption implemented
- No authentication beyond username
- All data transmitted in plaintext
- Suitable for: Internal networks, lab environments, offline scenarios
- **Not suitable for**: Public networks, sensitive data, production use

## 📄 Project Structure

```
cnlabstuff/
├── server.py           # Server application
├── client.py           # Client application
├── server (1).py       # Original server code
├── client (1).py       # Original client code
├── README.md           # This file
├── .venv/              # Virtual environment
└── requirements.txt    # Python dependencies (create if needed)
```

## 🎓 Educational Value

This project demonstrates:
- Socket programming (TCP & UDP)
- Client-server architecture
- Real-time multimedia streaming
- Multi-threading
- GUI development (Tkinter)
- Network protocols
- Data serialization (JSON, Base64)
- Binary packet structures
- Session management

## 📚 Technical Details

### Key Technologies
- **Networking**: Python `socket` module
- **Video**: OpenCV (`cv2`)
- **Audio**: PyAudio
- **GUI**: Tkinter
- **Screen Capture**: MSS (Multi-Screen Shot)
- **Image Processing**: Pillow (PIL)
- **Data Structures**: NumPy

### Threading Model
- Main thread: GUI event loop
- TCP receiver thread: Process control messages
- UDP receiver thread: Process media streams
- Video sender thread: Capture and send video
- Audio sender thread: Capture and send audio
- Screen sender thread: Capture and send screen

## 🐛 Known Limitations

1. **Scalability**: Optimized for 3-5 users; performance degrades with 10+ users
2. **No Encryption**: All data transmitted unencrypted
3. **Single Presenter**: Only one user can present at a time
4. **No Recording**: Sessions are not recorded
5. **Limited Error Recovery**: Network interruptions may require restart
6. **Platform-Specific Audio**: PyAudio may require additional setup on some systems

## 📞 Support

For issues or questions:
1. Check Troubleshooting section
2. Verify all dependencies installed
3. Check system permissions
4. Review console output for error messages

## 📜 License

This is an educational project created for academic purposes.

---

**Created for**: Computer Networks Laboratory Project  
**Due Date**: October 30, 2025  
**Project**: LAN-Based All-in-One Collaboration Suite
