# 🚀 QUICK START REFERENCE

## One-Page Quick Reference for LAN Collaboration Suite

---

## 📋 PREREQUISITES CHECKLIST
- [x] Python 3.8+ installed
- [x] Virtual environment created (.venv)
- [x] Dependencies installed (opencv, numpy, pillow, pyaudio, mss)
- [ ] Webcam available
- [ ] Microphone available
- [ ] On same LAN network

---

## ⚡ FASTEST WAY TO TEST (3 Steps)

### Step 1: Start Server (Terminal 1)
```bash
cd /Users/anvitaprasad/Desktop/cnlabstuff
source .venv/bin/activate
python server.py
```
**→ Note the Server IP shown!** (e.g., 192.168.1.100)

### Step 2: Start Client 1 (Terminal 2)
```bash
cd /Users/anvitaprasad/Desktop/cnlabstuff
source .venv/bin/activate
python client.py
```
- Username: `Alice`
- Server IP: `[IP from Step 1]`
- Click "Connect"

### Step 3: Start Client 2 (Terminal 3)
```bash
cd /Users/anvitaprasad/Desktop/cnlabstuff
source .venv/bin/activate
python client.py
```
- Username: `Bob`
- Server IP: `[same IP]`
- Click "Connect"

**Now test the features!**

---

## 🎮 FEATURE TEST SEQUENCE

| # | Feature | Action | Expected Result |
|---|---------|--------|----------------|
| 1 | **Chat** | Type message, press Enter | Appears on all clients |
| 2 | **Video** | Click "Start Video" | Webcam appears in grid |
| 3 | **Audio** | Click "Start Audio" | Can hear each other |
| 4 | **Screen Share** | Click "Start Presenting" | Screen visible to others |
| 5 | **File Share** | Click "Upload File" | File appears in list |

---

## 🔧 COMMON COMMANDS

### Start Server
```bash
cd /Users/anvitaprasad/Desktop/cnlabstuff
source .venv/bin/activate
python server.py
```

### Start Client
```bash
cd /Users/anvitaprasad/Desktop/cnlabstuff
source .venv/bin/activate
python client.py
```

### Stop Server
Press `Ctrl+C` in server terminal

### Install Dependencies (if needed)
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Check Python Version
```bash
python --version
```
Should be 3.8 or higher

---

## 🐛 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Can't connect | Check server IP, ensure server running |
| No camera | Grant permissions: System Prefs → Privacy → Camera |
| No mic | Grant permissions: System Prefs → Privacy → Microphone |
| No screen share | Grant permissions: System Prefs → Privacy → Screen Recording |
| Module error | Run: `pip install opencv-python numpy Pillow pyaudio mss` |
| Port in use | Server already running or kill: `lsof -ti:5555 \| xargs kill` |

---

## 📁 FILE STRUCTURE

```
cnlabstuff/
├── server.py              ← Run this first
├── client.py              ← Run this second (multiple times)
├── README.md              ← Full documentation
├── TESTING_GUIDE.md       ← Detailed testing steps
├── QUICK_REFERENCE.md     ← This file
├── requirements.txt       ← Dependencies list
├── START_SERVER.sh        ← Server launcher script
├── START_CLIENT.sh        ← Client launcher script
└── .venv/                 ← Virtual environment
```

---

## 🔌 DEFAULT PORTS

- **TCP Port:** 5555 (Control, Chat, Files)
- **UDP Port:** 5556 (Video, Audio)

---

## 💡 TESTING TIPS

1. **Test on same computer first** - Use localhost or actual IP
2. **Use different usernames** - Alice, Bob, Charlie, etc.
3. **Grant all permissions** - Camera, Microphone, Screen Recording
4. **Use headphones for audio** - Prevents echo/feedback
5. **Start simple** - Test chat first, then add video, etc.
6. **Check server logs** - Shows all connections and events
7. **Close other apps** - Especially those using camera/mic

---

## ✅ 30-SECOND VALIDATION TEST

```bash
# Terminal 1
python server.py

# Terminal 2
python client.py  # Username: Alice

# Terminal 3
python client.py  # Username: Bob

# In Alice's client:
1. Type "Hello" → Send
2. Click "Start Video"

# In Bob's client:
1. See "Hello" message ✓
2. See Alice's video ✓

# If both work → System is functional! ✓
```

---

## 📞 NEED MORE HELP?

1. **Full Guide:** See `README.md`
2. **Detailed Testing:** See `TESTING_GUIDE.md`
3. **Code Comments:** All code is commented
4. **Console Output:** Check terminal for error messages

---

## 🎯 MINIMUM TEST FOR SUBMISSION

Before submitting, verify:
- [ ] Server starts and shows IP
- [ ] 2+ clients can connect
- [ ] Chat works
- [ ] Video works (2+ cameras visible)
- [ ] Screen sharing works
- [ ] File upload/download works
- [ ] All features work together

---

## 🏆 PROJECT DELIVERABLES

All ready in this folder:
- ✅ Server Application (server.py)
- ✅ Client Application (client.py)
- ✅ Source Code (fully commented)
- ✅ Technical Documentation (README.md)
- ✅ User Guide (TESTING_GUIDE.md, QUICK_REFERENCE.md)

**You're all set for submission!** 🎉

---

**Remember:**
- Server runs first, clients connect to it
- Use same network (LAN)
- Grant system permissions when prompted
- Check server terminal for IP address
- Use headphones for audio testing

**Good luck with your demonstration!** 🚀
