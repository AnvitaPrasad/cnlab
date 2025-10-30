# 🎨 SYSTEM ARCHITECTURE DIAGRAM

## LAN Collaboration Suite - Visual Overview

---

## 🏗️ HIGH-LEVEL ARCHITECTURE

```
                    ┌─────────────────────────────────────┐
                    │    LAN COLLABORATION SUITE          │
                    └─────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
            ┌───────▼────────┐              ┌────────▼───────┐
            │  SERVER SIDE   │              │   CLIENT SIDE  │
            │   (server.py)  │              │  (client.py)   │
            └────────────────┘              └────────────────┘
```

---

## 🖥️ SERVER ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                         SERVER (server.py)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    MAIN THREAD                            │ │
│  │  - Initialization                                         │ │
│  │  - Socket Setup (TCP + UDP)                               │ │
│  │  - Accept Client Connections                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                 TCP LISTENER THREAD                       │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │  Client 1   │  │  Client 2   │  │  Client N   │      │ │
│  │  │   Handler   │  │   Handler   │  │   Handler   │      │ │
│  │  │   Thread    │  │   Thread    │  │   Thread    │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │                                                           │ │
│  │  Each handles:                                            │ │
│  │  • User registration                                      │ │
│  │  • Chat messages                                          │ │
│  │  • Screen frames                                          │ │
│  │  • File transfers                                         │ │
│  │  • Control messages                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                 UDP HANDLER THREAD                        │ │
│  │                                                           │ │
│  │  Receives:          Broadcasts to:                       │ │
│  │  • Video frames  ═══════════>  All clients               │ │
│  │  • Audio data    ═══════════>  All clients               │ │
│  │                                                           │ │
│  │  Process:                                                 │ │
│  │  1. Receive packet from any client                       │ │
│  │  2. Parse username and type                              │ │
│  │  3. Forward to all OTHER clients                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   DATA STORAGE                            │ │
│  │                                                           │ │
│  │  clients = {                                              │ │
│  │    'Alice': {tcp_socket, address, udp_port},             │ │
│  │    'Bob': {tcp_socket, address, udp_port}                │ │
│  │  }                                                        │ │
│  │                                                           │ │
│  │  chat_history = [messages...]                            │ │
│  │  files = {filename: base64_data}                         │ │
│  │  presenter = "Alice"  (or None)                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   NETWORK PORTS                           │ │
│  │                                                           │ │
│  │  🔌 TCP Port 5555 ──────> Control, Chat, Files           │ │
│  │  🔌 UDP Port 5556 ──────> Video, Audio Streams           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 CLIENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (client.py)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    MAIN THREAD (GUI)                      │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                  TKINTER GUI                        │ │ │
│  │  │                                                     │ │ │
│  │  │  ┌─────────────────────────────────────┐           │ │ │
│  │  │  │   Video Conference Grid             │           │ │ │
│  │  │  │  ┌────────┐ ┌────────┐ ┌────────┐  │           │ │ │
│  │  │  │  │ Alice  │ │  Bob   │ │Charlie │  │           │ │ │
│  │  │  │  │ Video  │ │ Video  │ │ Video  │  │           │ │ │
│  │  │  │  └────────┘ └────────┘ └────────┘  │           │ │ │
│  │  │  │  [Start Video] [Start Audio]       │           │ │ │
│  │  │  └─────────────────────────────────────┘           │ │ │
│  │  │                                                     │ │ │
│  │  │  ┌─────────────────────────────────────┐           │ │ │
│  │  │  │   Screen Sharing Viewer             │           │ │ │
│  │  │  │   [Presenter's Screen Display]      │           │ │ │
│  │  │  │   [Start Presenting]                │           │ │ │
│  │  │  └─────────────────────────────────────┘           │ │ │
│  │  │                                                     │ │ │
│  │  │  ┌──────┐  ┌──────────────┐  ┌─────────────┐      │ │ │
│  │  │  │Users │  │  Group Chat  │  │File Sharing │      │ │ │
│  │  │  │Alice │  │  Messages    │  │ file1.pdf   │      │ │ │
│  │  │  │Bob   │  │              │  │ image.png   │      │ │ │
│  │  │  │      │  │ [Input Box]  │  │ [Upload]    │      │ │ │
│  │  │  └──────┘  │ [Send]       │  │ [Download]  │      │ │ │
│  │  │            └──────────────┘  └─────────────┘      │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              BACKGROUND THREADS                       │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  TCP Receiver Thread                         │    │  │
│  │  │  • Receive server messages                   │    │  │
│  │  │  • Process chat, files, notifications        │    │  │
│  │  │  • Update GUI (thread-safe)                  │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  UDP Receiver Thread                         │    │  │
│  │  │  • Receive video/audio packets               │    │  │
│  │  │  • Decode and store frames                   │    │  │
│  │  │  • Play audio                                │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Video Sender Thread (when active)           │    │  │
│  │  │  • Capture from webcam                       │    │  │
│  │  │  • Compress (JPEG)                           │    │  │
│  │  │  • Send via UDP                              │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Audio Sender Thread (when active)           │    │  │
│  │  │  • Capture from microphone                   │    │  │
│  │  │  • Send via UDP                              │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                       │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Screen Sender Thread (when presenting)      │    │  │
│  │  │  • Capture screen                            │    │  │
│  │  │  • Compress and encode                       │    │  │
│  │  │  • Send via TCP                              │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              MEDIA COMPONENTS                         │  │
│  │                                                       │  │
│  │  📹 Video: OpenCV VideoCapture                       │  │
│  │  🎤 Audio: PyAudio Input/Output Streams              │  │
│  │  📺 Screen: MSS Screen Capture                       │  │
│  │  🖼️  Display: PIL/ImageTk for Tkinter               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAMS

### 1. VIDEO STREAMING FLOW

```
┌──────────┐                                          ┌──────────┐
│  ALICE   │                                          │   BOB    │
│ (Client) │                                          │ (Client) │
└────┬─────┘                                          └────┬─────┘
     │                                                      │
     │ 1. Capture webcam (OpenCV)                          │
     │    320x240, 30fps                                   │
     │                                                      │
     │ 2. Compress to JPEG (50%)                           │
     │    ~5-10 KB per frame                               │
     │                                                      │
     │ 3. Create UDP packet:                               │
     │    [Type:1][UserLen][Username][JPEGData]            │
     │                                                      │
     │ 4. Send UDP packet                                  │
     ├───────────────────────────────┐                     │
     │                               │                     │
     │                               ▼                     │
     │                        ┌─────────────┐              │
     │                        │   SERVER    │              │
     │                        │  UDP:5556   │              │
     │                        └─────────────┘              │
     │                               │                     │
     │                               │ 5. Server receives  │
     │                               │    Extracts: Type=1 │
     │                               │    Username="Alice" │
     │                               │                     │
     │                               │ 6. Broadcast to ALL │
     │                               │    other clients    │
     │                               │                     │
     │                               └─────────────────────┤
     │                                                     │
     │                                     7. Receive UDP  │
     │                                        packet       │
     │                                                     │
     │                                     8. Decode JPEG  │
     │                                                     │
     │                                     9. Display in   │
     │                                        video grid   │
     │                                                     ▼
     │                                              ┌─────────────┐
     │                                              │  Alice's    │
     │                                              │  Video      │
     │                                              │  Displayed  │
     │                                              └─────────────┘
```

### 2. CHAT MESSAGE FLOW

```
┌──────────┐                                          ┌──────────┐
│  ALICE   │                                          │   BOB    │
└────┬─────┘                                          └────┬─────┘
     │                                                      │
     │ 1. Types: "Hello everyone!"                         │
     │    Clicks Send                                      │
     │                                                      │
     │ 2. Create JSON message:                             │
     │    {"type":"chat", "message":"Hello everyone!"}     │
     │                                                      │
     │ 3. Send via TCP                                     │
     ├───────────────────────────────┐                     │
     │                               │                     │
     │                               ▼                     │
     │                        ┌─────────────┐              │
     │                        │   SERVER    │              │
     │                        │  TCP:5555   │              │
     │                        └─────────────┘              │
     │                               │                     │
     │                               │ 4. Receive message  │
     │                               │    Add metadata:    │
     │                               │    - username       │
     │                               │    - timestamp      │
     │                               │                     │
     │                               │ 5. Store in         │
     │                               │    chat_history     │
     │                               │                     │
     │                               │ 6. Broadcast to     │
     │                               │    ALL clients      │
     │                               │                     │
     ├───────────────────────────────┤                     │
     │                               └─────────────────────┤
     │                                                     │
     │ 7. Receive broadcast:                    7. Receive│
     │    {"type":"chat",                       message    │
     │     "username":"Alice",                             │
     │     "message":"Hello everyone!",                    │
     │     "timestamp":"14:30:45"}                         │
     │                                                     │
     │ 8. Display in chat:              8. Display in chat│
     │    [14:30:45] Alice: Hello...    [14:30:45] Alice: │
     ▼                                                     ▼
```

### 3. FILE SHARING FLOW

```
Alice Uploads                 Server Stores              Bob Downloads

┌──────────┐                ┌──────────┐                ┌──────────┐
│  Select  │                │  Notify  │                │  Select  │
│   File   │                │   All    │                │   File   │
└────┬─────┘                └────┬─────┘                └────┬─────┘
     │                           │                           │
     │ 1. Read file              │                           │
     │    Encode Base64          │                           │
     │                           │                           │
     │ 2. Send via TCP           │                           │
     │    {type:"file_upload",   │                           │
     │     filename:"doc.pdf",   │                           │
     │     filedata:"base64..."}─┼──────>3. Store in        │
     │                           │        files dict        │
     │                           │                           │
     │                           │ 4. Broadcast:             │
     │<──────────────────────────┼─────────{type:            │
     │                           │         "file_available"  │
     │                           │         filename,         │
     │                           │         filesize}─────────>
     │                           │                           │
     │ 5. File appears in list   │        5. File appears    │
     │                           │                           │
     │                           │        6. User clicks     │
     │                           │           Download        │
     │                           │                           │
     │                           │<──────7. Request:         │
     │                           │        {type:             │
     │                           │        "file_download",   │
     │                           │        filename:"doc.pdf"}│
     │                           │                           │
     │                           │ 8. Send file data ────────>
     │                           │                           │
     │                           │        9. Decode Base64   │
     │                           │           Write to disk   │
     │                           │                           │
     │                           │        ✓ Download complete│
```

---

## 🎛️ PROTOCOL SPECIFICATIONS

### TCP Message Format

```
┌──────────────────┬─────────────────────────────────────┐
│  Message Length  │         JSON Message Body           │
│    (4 bytes)     │         (Variable length)           │
│   Big-endian     │          UTF-8 encoded              │
└──────────────────┴─────────────────────────────────────┘

Example:
Length: 0x00000045 (69 bytes)
Body: {"type":"chat","username":"Alice","message":"Hi!"}
```

### UDP Packet Format

```
┌─────┬──────────────┬──────────────┬────────────────────┐
│Type │ Username Len │   Username   │      Payload       │
│ (1) │     (1)      │ (0-255 bytes)│  (Variable bytes)  │
└─────┴──────────────┴──────────────┴────────────────────┘

Type Codes:
  1 = Video Frame (JPEG compressed)
  2 = Audio Data (PCM raw)

Example Video Packet:
[0x01][0x05]['A','l','i','c','e'][JPEG binary data...]

Example Audio Packet:
[0x02][0x03]['B','o','b'][PCM audio samples...]
```

---

## 🔐 SESSION LIFECYCLE

```
┌─────────────┐
│   IDLE      │  Client not connected
└──────┬──────┘
       │
       │ User enters credentials
       │ Clicks "Connect"
       ▼
┌─────────────┐
│ CONNECTING  │  TCP socket connecting to server
└──────┬──────┘
       │
       │ TCP connected
       │ Send: {"type":"register", "username":"Alice", "udp_port":61234}
       ▼
┌─────────────┐
│ REGISTERING │  Waiting for server confirmation
└──────┬──────┘
       │
       │ Receive: {"type":"registered", "users":[...], "chat_history":[...]}
       ▼
┌─────────────────────────────────────────────┐
│                  ACTIVE                     │
│  ┌───────────────────────────────────────┐ │
│  │  TCP Thread: Receive control messages │ │
│  │  UDP Thread: Receive media streams    │ │
│  │  User can:                             │ │
│  │   - Send chat messages                │ │
│  │   - Start/stop video                  │ │
│  │   - Start/stop audio                  │ │
│  │   - Start/stop presenting             │ │
│  │   - Upload/download files             │ │
│  └───────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
               │ User closes window OR
               │ Connection lost
               ▼
        ┌─────────────┐
        │DISCONNECTING│  Cleanup resources
        └──────┬──────┘
               │
               │ Close sockets
               │ Stop threads
               │ Release camera/mic
               ▼
        ┌─────────────┐
        │   CLOSED    │  Application terminated
        └─────────────┘
```

---

## 📊 BANDWIDTH BREAKDOWN

```
Per User Bandwidth Usage (All Features Active):

┌────────────────────────────────────────────┐
│  Outgoing (Upload to Server):             │
│                                            │
│  📹 Video:    ~300 Kbps (30fps, JPEG)     │
│  🎤 Audio:    ~128 Kbps (16kHz, Mono)     │
│  💬 Chat:     ~  1 Kbps (occasional)      │
│  📺 Screen:   ~600 Kbps (when presenting) │
│  📁 Files:    Variable (on-demand)        │
│                                            │
│  TOTAL:       ~500 Kbps typical           │
│               ~1.2 Mbps when presenting   │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  Incoming (Download from Server):         │
│                                            │
│  📹 Video:    N × 300 Kbps                │
│               (N = other users)           │
│  🎤 Audio:    Mixed stream ~128 Kbps      │
│  💬 Chat:     ~  1 Kbps                   │
│  📺 Screen:   ~600 Kbps (when viewing)    │
│  📁 Files:    Variable (on-demand)        │
│                                            │
│  Example (3 users):                       │
│  Video: 2 × 300 = 600 Kbps                │
│  Audio: 128 Kbps                          │
│  TOTAL: ~800 Kbps                         │
└────────────────────────────────────────────┘

Server Bandwidth (N Users, All Streaming):

  Receive:  N × 500 Kbps
  Send:     N × (N-1) × 300 Kbps  (video)
            N × 128 Kbps           (audio)

  Example (5 users):
  Receive: 5 × 500 =  2.5 Mbps
  Send:    5 × 4 × 300 = 6 Mbps (video)
           5 × 128 = 640 Kbps (audio)
  TOTAL:   ~9 Mbps
```

---

## 🎯 FEATURE INTERACTION MATRIX

```
                    Video  Audio  Screen  Chat  Files
                    ─────  ─────  ──────  ────  ─────
Can work with:
  Video             │ —     ✅     ✅     ✅     ✅
  Audio             │ ✅    —      ✅     ✅     ✅
  Screen Sharing    │ ✅    ✅     —      ✅     ✅
  Chat              │ ✅    ✅     ✅     —      ✅
  Files             │ ✅    ✅     ✅     ✅     —

✅ = Features work together simultaneously
— = Same feature (not applicable)

All features are fully compatible and can run concurrently!
```

---

## 🔄 THREADING VISUALIZATION

```
SERVER THREADS:

  Main Thread ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      │                                      ┃
      ├─> TCP Listener ──────────────────────┨ (Blocking accept())
      │       │                              ┃
      │       ├─> Client 1 Handler Thread    ┃
      │       ├─> Client 2 Handler Thread    ┃
      │       └─> Client N Handler Thread    ┃
      │                                      ┃
      └─> UDP Handler Thread ─────────────────┨ (Non-blocking recvfrom())
                                             ┃
  All threads run concurrently ━━━━━━━━━━━━━┛


CLIENT THREADS:

  Main Thread (GUI) ━━━━━━━━━━━━━━━━━━━━━━━━┓
      │                                      ┃
      ├─> TCP Receiver ───────────────────────┨ (Blocking recv())
      │                                      ┃
      ├─> UDP Receiver ───────────────────────┨ (Blocking recvfrom())
      │                                      ┃
      ├─> Video Sender ───────────────────────┨ (when video active)
      │                                      ┃
      ├─> Audio Sender ───────────────────────┨ (when audio active)
      │                                      ┃
      └─> Screen Sender ──────────────────────┨ (when presenting)
                                             ┃
  All threads are daemon threads ━━━━━━━━━━━┛
```

---

## 📈 SCALABILITY CONSIDERATIONS

```
Number of Users vs. Server Bandwidth:

Users │ Server Bandwidth  │ Performance
──────┼──────────────────┼─────────────────
  2   │   ~1 Mbps        │ Excellent ⭐⭐⭐⭐⭐
  3   │   ~3 Mbps        │ Excellent ⭐⭐⭐⭐⭐
  5   │   ~9 Mbps        │ Good      ⭐⭐⭐⭐
  7   │  ~18 Mbps        │ Fair      ⭐⭐⭐
 10   │  ~40 Mbps        │ Poor      ⭐⭐
 15   │  ~90 Mbps        │ Not Recommended

Bandwidth grows as O(N²) for video streaming!

Recommended Maximum: 5-7 users
```

---

## 🎨 USER INTERFACE LAYOUT

```
┌──────────────────────────────────────────────────────────────┐
│  LAN Communication System                          [_][□][X] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────── Video Conference ─────────────────────┐    │
│  │                                                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │  Alice   │  │   Bob    │  │ Charlie  │          │    │
│  │  │  [VIDEO] │  │  [VIDEO] │  │  [VIDEO] │          │    │
│  │  │ 320x240  │  │ 320x240  │  │ 320x240  │          │    │
│  │  └──────────┘  └──────────┘  └──────────┘          │    │
│  │                                                      │    │
│  │  [Start Video]  [Start Audio]                       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────── Screen Sharing ────────────────────────┐   │
│  │                                                       │   │
│  │  ╔══════════════════════════════════════════════╗   │   │
│  │  ║                                              ║   │   │
│  │  ║        Presenter's Screen Display            ║   │   │
│  │  ║              (800x600 max)                   ║   │   │
│  │  ║                                              ║   │   │
│  │  ╚══════════════════════════════════════════════╝   │   │
│  │                                                       │   │
│  │  [Start Presenting]                                  │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────┬────────────────────────┬───────────────────┐   │
│  │ Users   │    Group Chat          │  File Sharing     │   │
│  ├─────────┼────────────────────────┼───────────────────┤   │
│  │• Alice  │ [14:30] Alice: Hi!     │ □ document.pdf    │   │
│  │  (You)  │ [14:31] Bob: Hello!    │ □ image.png       │   │
│  │• Bob    │ [14:32] Alice: ...     │ □ data.xlsx       │   │
│  │• Charlie│                         │                   │   │
│  │         │ ┌──────────────────┐   │ [Upload File]     │   │
│  │         │ │ Type message...  │   │ [Download Selected]│  │
│  │         │ └──────────────────┘   │                   │   │
│  │         │ [Send]                 │                   │   │
│  └─────────┴────────────────────────┴───────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Window Size: 1200x800 pixels (default)
All sections resize proportionally
```

---

**This visual guide complements the technical documentation.**  
**Refer to README.md and TECHNICAL_DOCUMENTATION.md for detailed explanations.**

