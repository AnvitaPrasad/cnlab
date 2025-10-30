# LAN Collaboration Suite - Technical Documentation

## Project Overview

**Project Name:** LAN-Based All-in-One Collaboration Suite  
**Purpose:** Multi-user communication application for Local Area Networks  
**Architecture:** Client-Server Model  
**Programming Language:** Python 3  
**Development Date:** October 2025

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Communication Protocols](#communication-protocols)
3. [Module Descriptions](#module-descriptions)
4. [Network Protocol Specification](#network-protocol-specification)
5. [Data Structures](#data-structures)
6. [Threading Model](#threading-model)
7. [Security Considerations](#security-considerations)
8. [Performance Analysis](#performance-analysis)
9. [Future Enhancements](#future-enhancements)

---

## 1. System Architecture

### 1.1 Overall Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Client 1 │  │ Client 2 │  │ Client N │             │
│  │  (Alice) │  │  (Bob)   │  │ (Charlie)│             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼────────────────────┘
        │ TCP/UDP     │ TCP/UDP     │ TCP/UDP
        │             │             │
┌───────▼─────────────▼─────────────▼────────────────────┐
│                    CENTRAL SERVER                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Connection Manager                              │  │
│  │  - Client Registry                               │  │
│  │  - Session State                                 │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  TCP Handler (Port 5555)                         │  │
│  │  - Control Messages                              │  │
│  │  - Chat Relay                                    │  │
│  │  - File Transfer                                 │  │
│  │  - Screen Sharing                                │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  UDP Handler (Port 5556)                         │  │
│  │  - Video Stream Relay                            │  │
│  │  - Audio Stream Relay                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Component Breakdown

#### Server Components

1. **TCP Socket Server**
   - Accepts incoming client connections
   - Maintains persistent connections
   - Handles control messages
   - Routes chat messages
   - Manages file transfers

2. **UDP Socket Server**
   - Receives media streams (video/audio)
   - Broadcasts to all clients
   - Low-latency, connectionless

3. **Client Manager**
   - Tracks connected clients
   - Stores client metadata (username, address, UDP port)
   - Handles disconnections

4. **Session Manager**
   - Maintains chat history
   - Tracks current presenter
   - Stores shared files

#### Client Components

1. **Connection Handler**
   - TCP connection to server
   - UDP socket for media streaming
   - Reconnection logic

2. **GUI (Tkinter)**
   - Video grid display
   - Screen sharing viewer
   - Chat interface
   - File sharing panel
   - Control buttons

3. **Media Capture**
   - Video: OpenCV (cv2.VideoCapture)
   - Audio: PyAudio
   - Screen: MSS (Multi-Screen Shot)

4. **Media Playback**
   - Video: PIL/ImageTk display
   - Audio: PyAudio output stream

---

## 2. Communication Protocols

### 2.1 Protocol Selection Rationale

| Feature | Protocol | Reason |
|---------|----------|--------|
| Chat | TCP | Reliable delivery, messages must not be lost |
| File Transfer | TCP | Integrity critical, error correction needed |
| Screen Sharing | TCP | Image clarity important, packet order matters |
| Video Streaming | UDP | Low latency prioritized, some packet loss acceptable |
| Audio Streaming | UDP | Real-time requirement, buffering undesirable |

### 2.2 TCP Message Format

All TCP messages use a length-prefixed JSON format:

```
┌────────────┬──────────────────────┐
│ Length (4) │  JSON Message (N)    │
│   bytes    │      bytes           │
└────────────┴──────────────────────┘
```

- **Length Field**: 4 bytes, big-endian unsigned integer
- **Message Field**: UTF-8 encoded JSON

**Example:**
```python
{
    "type": "chat",
    "username": "Alice",
    "message": "Hello World",
    "timestamp": "14:30:45"
}
```

### 2.3 UDP Packet Format

Binary format for efficiency:

```
┌──────┬──────────────┬──────────┬─────────────────┐
│ Type │ Username Len │ Username │    Payload      │
│ (1)  │     (1)      │   (N)    │      (...)      │
└──────┴──────────────┴──────────┴─────────────────┘
```

- **Type**: 1 byte (1=Video, 2=Audio)
- **Username Length**: 1 byte (0-255)
- **Username**: N bytes, UTF-8 encoded
- **Payload**: Remaining bytes (compressed video/audio data)

---

## 3. Module Descriptions

### 3.1 Multi-User Video Conferencing

**Implementation Details:**

1. **Capture** (Client-side)
   - Device: Webcam (cv2.VideoCapture(0))
   - Resolution: 320x240 pixels
   - Frame Rate: ~30 FPS
   - Compression: JPEG with 50% quality
   - Average Size: 5-10 KB per frame

2. **Transmission**
   - Protocol: UDP
   - Packet Structure: [Type:1][UserLen][Username][JPEGData]
   - Destination: Server UDP port

3. **Relay** (Server-side)
   - Receives from one client
   - Extracts username and frame data
   - Broadcasts to all other clients' UDP ports
   - No processing or mixing

4. **Display** (Client-side)
   - Receives UDP packets
   - Decodes JPEG to numpy array
   - Converts BGR to RGB
   - Displays in Tkinter Label via PIL/ImageTk
   - Updates grid layout dynamically

**Code Snippet (Client Video Capture):**
```python
def stream_video(self):
    while self.video_streaming and self.running:
        ret, frame = self.video_cap.read()
        if ret:
            frame = cv2.resize(frame, (320, 240))
            _, buffer = cv2.imencode('.jpg', frame, 
                                    [cv2.IMWRITE_JPEG_QUALITY, 50])
            
            username_bytes = self.username.encode('utf-8')
            packet = bytes([1, len(username_bytes)]) + \
                     username_bytes + buffer.tobytes()
            
            self.udp_socket.sendto(packet, 
                                  (self.server_ip, self.udp_port))
        time.sleep(0.033)  # ~30 FPS
```

### 3.2 Multi-User Audio Conferencing

**Implementation Details:**

1. **Capture** (Client-side)
   - Device: Default microphone
   - Format: PCM 16-bit
   - Channels: 1 (Mono)
   - Sample Rate: 16,000 Hz
   - Buffer Size: 1024 frames
   - Bitrate: ~256 Kbps

2. **Transmission**
   - Protocol: UDP
   - Packet: [Type:2][UserLen][Username][AudioData]
   - No additional compression (raw PCM)

3. **Relay** (Server-side)
   - Direct broadcast to all clients
   - No mixing (clients mix locally in hardware)

4. **Playback** (Client-side)
   - PyAudio output stream
   - Direct playback of received audio
   - Buffering handled by PyAudio

**Code Snippet (Client Audio Capture):**
```python
def stream_audio(self):
    while self.audio_streaming and self.running:
        data = self.audio_input_stream.read(1024, 
                                            exception_on_overflow=False)
        
        username_bytes = self.username.encode('utf-8')
        packet = bytes([2, len(username_bytes)]) + \
                 username_bytes + data
        
        self.udp_socket.sendto(packet, 
                              (self.server_ip, self.udp_port))
```

### 3.3 Screen Sharing

**Implementation Details:**

1. **Capture** (Presenter Client)
   - Tool: MSS (Multi-Screen Shot)
   - Source: Primary monitor
   - Capture Rate: ~10 FPS
   - Processing:
     - Capture full screen
     - Resize to max 800x600
     - Convert to JPEG (60% quality)
     - Base64 encode

2. **Transmission**
   - Protocol: TCP (reliable delivery)
   - Message Type: "screen_frame"
   - Payload: Base64-encoded JPEG

3. **Relay** (Server)
   - Receives from presenter
   - Validates presenter status
   - Broadcasts to all viewers (exclude presenter)

4. **Display** (Viewer Clients)
   - Decode Base64
   - Create PIL Image
   - Resize to fit display area
   - Convert to PhotoImage for Tkinter

**Code Snippet (Screen Capture):**
```python
def stream_screen(self):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while self.presenting and self.running:
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, 
                                 screenshot.rgb)
            img.thumbnail((800, 600), Image.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=60)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            self.send_message({
                'type': 'screen_frame',
                'frame': img_str
            })
            time.sleep(0.1)  # 10 FPS
```

### 3.4 Group Text Chat

**Implementation Details:**

1. **Client Sends Message**
   ```json
   {
       "type": "chat",
       "message": "Hello everyone!"
   }
   ```

2. **Server Processing**
   - Receives message
   - Adds metadata (username, timestamp)
   - Appends to chat_history
   - Broadcasts to all clients

3. **Broadcast Message**
   ```json
   {
       "type": "chat",
       "username": "Alice",
       "message": "Hello everyone!",
       "timestamp": "14:30:45"
   }
   ```

4. **Client Display**
   - Receives message
   - Formats: `[14:30:45] Alice: Hello everyone!`
   - Appends to ScrolledText widget
   - Auto-scrolls to bottom

**Server Code:**
```python
if msg_type == 'chat':
    chat_msg = {
        'type': 'chat',
        'username': username,
        'message': msg['message'],
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    self.chat_history.append(chat_msg)
    self.broadcast_tcp(chat_msg)
```

### 3.5 File Sharing

**Implementation Details:**

1. **Upload Process**
   - Client selects file via filedialog
   - Reads file as binary
   - Base64 encodes data
   - Sends to server with metadata

2. **Server Storage**
   - Stores file data in memory (dict)
   - Key: filename
   - Value: Base64-encoded data

3. **Notification**
   - Server broadcasts "file_available" to all
   - Includes: filename, size, uploader, timestamp

4. **Download Process**
   - Viewer requests file by name
   - Server sends file data
   - Client decodes Base64
   - Writes to disk

**Upload Message:**
```json
{
    "type": "file_upload",
    "filename": "document.pdf",
    "filesize": 524288,
    "filedata": "base64_encoded_data..."
}
```

**Download Request:**
```json
{
    "type": "file_download",
    "filename": "document.pdf"
}
```

---

## 4. Network Protocol Specification

### 4.1 TCP Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `register` | Client → Server | Initial connection, includes username and UDP port |
| `registered` | Server → Client | Confirms registration, sends current state |
| `chat` | Bidirectional | Chat message |
| `user_joined` | Server → Clients | Notify of new user |
| `user_left` | Server → Clients | Notify of disconnection |
| `start_presenting` | Client → Server | Request to become presenter |
| `stop_presenting` | Client → Server | End presentation |
| `presenter_changed` | Server → Clients | Presenter status update |
| `screen_frame` | Bidirectional | Screen capture frame |
| `file_upload` | Client → Server | Upload file data |
| `file_available` | Server → Clients | Notify of new file |
| `file_download` | Client → Server | Request file |
| `file_data` | Server → Client | Send requested file |

### 4.2 Session Lifecycle

```
Client                          Server
  |                               |
  |------ TCP Connect ----------->|
  |                               |
  |------ register ------------->|
  |       {username, udp_port}    |
  |                               |
  |<----- registered -------------|
  |       {users, chat_history}   |
  |                               |
  |<----- user_joined ------------|
  |       (to other clients)      |
  |                               |
  |                               |
  |====== Active Session ========|
  |  - Chat messages             |
  |  - Media streams (UDP)       |
  |  - File transfers            |
  |                               |
  |                               |
  |----- Disconnect / Close ----->|
  |                               |
  |<----- user_left -------------|
  |       (to other clients)      |
  |                               |
```

---

## 5. Data Structures

### 5.1 Server Data Structures

**Client Registry:**
```python
self.clients = {
    'Alice': {
        'tcp': <socket_object>,
        'address': ('192.168.1.101', 54321),
        'udp_port': 61234
    },
    'Bob': {
        'tcp': <socket_object>,
        'address': ('192.168.1.102', 54322),
        'udp_port': 61235
    }
}
```

**Chat History:**
```python
self.chat_history = [
    {
        'type': 'chat',
        'username': 'Alice',
        'message': 'Hello!',
        'timestamp': '14:30:45'
    },
    ...
]
```

**File Storage:**
```python
self.files = {
    'document.pdf': 'base64_encoded_data...',
    'image.png': 'base64_encoded_data...'
}
```

### 5.2 Client Data Structures

**Video Frames:**
```python
self.video_frames = {
    'Alice': <numpy_array>,
    'Bob': <numpy_array>
}
```

**Users List:**
```python
self.users = ['Alice', 'Bob', 'Charlie']
```

---

## 6. Threading Model

### 6.1 Server Threads

```
Main Thread
├─ TCP Listener (blocking accept loop)
│
├─ UDP Handler Thread
│  └─ Receive and relay video/audio packets
│
└─ Client Handler Threads (one per client)
   ├─ Receive TCP messages
   ├─ Process messages
   └─ Send responses
```

### 6.2 Client Threads

```
Main Thread (GUI Event Loop)
│
├─ TCP Receiver Thread
│  └─ Receive and process server messages
│
├─ UDP Receiver Thread
│  └─ Receive video/audio streams
│
├─ Video Sender Thread (when video active)
│  └─ Capture and send video frames
│
├─ Audio Sender Thread (when audio active)
│  └─ Capture and send audio data
│
└─ Screen Sender Thread (when presenting)
   └─ Capture and send screen frames
```

### 6.3 Thread Synchronization

- **Locks**: `threading.Lock()` used for `clients` dictionary on server
- **Daemon Threads**: All background threads are daemon threads
- **Graceful Shutdown**: `self.running` flag for clean thread termination

---

## 7. Security Considerations

### 7.1 Current Security Posture

**⚠️ WARNING:** This application is designed for trusted LAN environments only.

**Security Limitations:**
1. **No Encryption**: All data (including video/audio) transmitted in plaintext
2. **No Authentication**: Username-based identification only, no passwords
3. **No Authorization**: All users have equal permissions
4. **No Input Validation**: Minimal validation of user inputs
5. **No Session Tokens**: No secure session management

### 7.2 Suitable Environments

✅ **Safe to Use:**
- Private home networks
- Isolated lab networks
- Educational environments
- Offline scenarios
- Development/testing

❌ **NOT Safe:**
- Public WiFi
- Internet connections
- Networks with untrusted users
- Production environments
- Sensitive/confidential communications

### 7.3 Potential Security Enhancements

For production use, implement:
1. **TLS/SSL** for TCP connections
2. **DTLS** for UDP streams
3. **Password authentication** with hashing (bcrypt/scrypt)
4. **Access control lists** (ACL)
5. **Input sanitization** and validation
6. **Rate limiting** to prevent DoS
7. **Logging and monitoring**

---

## 8. Performance Analysis

### 8.1 Bandwidth Requirements

**Per User (All Features Active):**
- Video (outgoing): ~300 Kbps
- Audio (outgoing): ~128 Kbps
- Screen sharing (when presenting): ~600 Kbps
- Chat: Negligible (<1 Kbps)
- **Total per user**: ~500 Kbps typical, 1+ Mbps when presenting

**Server (N Users):**
- Relays all streams to all users
- Bandwidth: O(N²) complexity
- Example (5 users, all streaming video):
  - Input: 5 × 300 Kbps = 1.5 Mbps
  - Output: 5 × 4 × 300 Kbps = 6 Mbps
  - **Total: ~7.5 Mbps**

### 8.2 Latency Analysis

| Component | Latency | Notes |
|-----------|---------|-------|
| Video capture | ~33ms | 30 FPS |
| Video encoding | ~5-10ms | JPEG compression |
| Network transmission | ~1-5ms | LAN, varies by network |
| Video decoding | ~5-10ms | JPEG decompression |
| Display refresh | ~100ms | Tkinter update cycle |
| **Total Video Latency** | **~150-250ms** | Acceptable for conferencing |
| | |
| Audio capture | ~64ms | 1024 frames @ 16kHz |
| Network transmission | ~1-5ms | LAN |
| Audio playback | ~64ms | Buffer playback |
| **Total Audio Latency** | **~130-200ms** | Acceptable, slight echo possible |

### 8.3 Scalability

**Tested Configurations:**
- 2-3 users: Excellent performance
- 4-5 users: Good performance
- 6-10 users: Degraded performance (increased latency)
- 10+ users: Not recommended (high bandwidth, CPU usage)

**Bottlenecks:**
1. Server bandwidth (N² growth)
2. Client video grid rendering
3. GUI update frequency

**Optimization Strategies:**
- Reduce video resolution/quality
- Lower frame rates
- Implement selective forwarding unit (SFU)
- Use hardware acceleration for encoding/decoding

---

## 9. Future Enhancements

### 9.1 Planned Features

1. **Recording**
   - Record video/audio sessions
   - Save chat transcripts
   - Export files

2. **Advanced Video**
   - Speaker detection (active speaker highlight)
   - Virtual backgrounds
   - Filters and effects

3. **Enhanced Audio**
   - Echo cancellation
   - Noise suppression
   - Audio mixing on server

4. **Better File Sharing**
   - Persistent file storage
   - File browser
   - Drag-and-drop upload

5. **Session Management**
   - Scheduled sessions
   - Waiting room
   - Moderator controls

6. **Quality of Service**
   - Adaptive bitrate
   - Automatic quality adjustment
   - Network condition detection

### 9.2 Architecture Improvements

1. **Database Integration**
   - PostgreSQL for user management
   - Redis for session state
   - MinIO for file storage

2. **Microservices**
   - Separate services for video, audio, chat
   - Load balancing across multiple servers
   - Horizontal scaling

3. **WebRTC Integration**
   - Peer-to-peer connections (when possible)
   - Better NAT traversal
   - Lower latency

4. **REST API**
   - HTTP API for control plane
   - Easier integration with other tools
   - Mobile app support

---

## 10. Conclusion

This LAN Collaboration Suite successfully implements all five required modules:

✅ **Multi-User Video Conferencing** - Real-time webcam streaming  
✅ **Multi-User Audio Conferencing** - Voice communication  
✅ **Screen Sharing** - Presentation mode  
✅ **Group Text Chat** - Messaging system  
✅ **File Sharing** - Upload/download files  

The application demonstrates fundamental networking concepts including socket programming, TCP/UDP protocols, client-server architecture, and real-time multimedia streaming.

**Project Status:** Complete and ready for deployment in LAN environments.

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Author:** Computer Networks Lab Project Team
