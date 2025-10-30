# 🧪 STEP-BY-STEP TESTING GUIDE

## Complete Testing Procedure for LAN Collaboration Suite

---

## ⚙️ INITIAL SETUP (One-Time)

### Already Completed ✅
- [x] Python virtual environment created
- [x] Dependencies installed (opencv-python, numpy, Pillow, pyaudio, mss)
- [x] Code files ready (server.py, client.py)

---

## 🚀 TEST SESSION 1: Basic Functionality

### Step 1: Start the Server

1. **Open Terminal 1** (⌘+Space, type "Terminal", press Enter)

2. **Navigate to project directory:**
   ```bash
   cd /Users/anvitaprasad/Desktop/cnlabstuff
   ```

3. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
   You should see `(.venv)` appear in your prompt.

4. **Start the server:**
   ```bash
   python server.py
   ```

5. **IMPORTANT: Note the Server IP**
   You'll see output like:
   ```
   ==================================================
   LAN Communication Server
   ==================================================
   Server IP: 192.168.1.100  ← COPY THIS IP ADDRESS!
   TCP Port: 5555
   UDP Port: 5556
   ==================================================
   ```

6. **Leave this terminal running** - DO NOT CLOSE IT!

---

### Step 2: Start Client 1 (Alice)

1. **Open Terminal 2** (⌘+T for new tab, or open new window)

2. **Navigate and activate:**
   ```bash
   cd /Users/anvitaprasad/Desktop/cnlabstuff
   source .venv/bin/activate
   python client.py
   ```

3. **A GUI window will appear** - Fill in:
   - **Username:** `Alice`
   - **Server IP:** `192.168.1.100` (use the IP from Step 1.5)
   - **TCP Port:** `5555` (already filled)
   - **UDP Port:** `5556` (already filled)

4. **Click "Connect"**

5. **Expected Result:**
   - ✅ Window changes to main interface
   - ✅ Users list shows "Alice (You)"
   - ✅ Server terminal shows: `[SERVER] Alice registered from...`

---

### Step 3: Start Client 2 (Bob)

1. **Open Terminal 3** (another new terminal)

2. **Repeat Client 1 steps but use username:** `Bob`
   ```bash
   cd /Users/anvitaprasad/Desktop/cnlabstuff
   source .venv/bin/activate
   python client.py
   ```
   - Username: `Bob`
   - Server IP: `192.168.1.100` (same as before)
   - Click "Connect"

3. **Expected Results:**
   - ✅ Bob's window shows main interface
   - ✅ Bob's users list shows: "Alice" and "Bob (You)"
   - ✅ Alice's users list updates to show: "Alice (You)" and "Bob"
   - ✅ Both clients see: `[System] Bob joined the session`
   - ✅ Server shows: `[SERVER] Bob registered from...`

---

### Step 4: Test Group Chat

1. **In Alice's window:**
   - Type in chat input box: `Hello everyone!`
   - Press **Enter** or click **Send**

2. **Expected Results:**
   - ✅ Message appears in Alice's chat: `[HH:MM:SS] Alice: Hello everyone!`
   - ✅ Message appears in Bob's chat: `[HH:MM:SS] Alice: Hello everyone!`

3. **In Bob's window:**
   - Type: `Hi Alice, I can see your message!`
   - Press Enter

4. **Expected Results:**
   - ✅ Both clients see Bob's message
   - ✅ Messages show correct timestamps
   - ✅ Chat history preserved

**✅ TEST PASSED IF:** Messages appear on all clients in real-time

---

### Step 5: Test Video Conferencing

**⚠️ IMPORTANT:** Grant camera permissions if prompted!

1. **In Alice's window:**
   - Click **"Start Video"** button

2. **Expected Results (within 2-3 seconds):**
   - ✅ Alice's button changes to "Stop Video"
   - ✅ Alice sees her own video in the video grid
   - ✅ Bob sees Alice's video appear in his video grid
   - ✅ Video labeled "Alice"

3. **In Bob's window:**
   - Click **"Start Video"**

4. **Expected Results:**
   - ✅ Alice now sees: her video + Bob's video (2 videos total)
   - ✅ Bob sees: his video + Alice's video (2 videos total)
   - ✅ Videos update smoothly (~30 FPS)
   - ✅ Grid layout arranges videos automatically

5. **Test Stop:**
   - Click "Stop Video" in Alice's window
   - ✅ Alice's video disappears from Bob's screen
   - ✅ Bob still sees his own video

**✅ TEST PASSED IF:** Both clients see each other's webcam feeds with minimal lag

---

### Step 6: Test Audio Conferencing

**⚠️ NOTES:**
- Grant microphone permissions if prompted
- Use headphones to prevent echo/feedback
- Or test on separate computers

1. **In Alice's window:**
   - Click **"Start Audio"**
   - **Speak**: "Testing audio, can you hear me?"

2. **Expected Results:**
   - ✅ Button changes to "Stop Audio"
   - ✅ Bob hears Alice's voice (may have slight delay <1 sec)

3. **In Bob's window:**
   - Click **"Start Audio"**
   - **Speak**: "Yes, I can hear you!"

4. **Expected Results:**
   - ✅ Alice hears Bob
   - ✅ Two-way audio communication works
   - ✅ Audio is reasonably clear

5. **Test Stop:**
   - Click "Stop Audio" to end

**✅ TEST PASSED IF:** Users can hear each other speak with acceptable quality

---

### Step 7: Test Screen Sharing

1. **In Alice's window:**
   - Click **"Start Presenting"**

2. **Expected Results:**
   - ✅ Alice's button changes to "Stop Presenting"
   - ✅ Bob's screen sharing area shows: "Alice is presenting..."
   - ✅ Bob sees Alice's screen in the presentation area
   - ✅ Bob's "Start Presenting" button becomes DISABLED
   - ✅ Screen updates every ~1 second

3. **In Bob's window:**
   - Try clicking "Start Presenting"
   - ✅ Button should be disabled (only one presenter at a time)

4. **In Alice's window:**
   - Open a window, move it around, type something
   - ✅ Bob sees these changes on his screen

5. **Stop Presenting:**
   - Alice clicks "Stop Presenting"
   - ✅ Presentation area clears on Bob's screen
   - ✅ Bob's button re-enables

**✅ TEST PASSED IF:** Bob sees Alice's screen in real-time; single presenter enforced

---

### Step 8: Test File Sharing

1. **Create a test file** (in any terminal):
   ```bash
   echo "This is a test file for file sharing" > /Users/anvitaprasad/Desktop/test.txt
   ```

2. **In Alice's window:**
   - Click **"Upload File"**
   - Navigate to Desktop
   - Select `test.txt`
   - Click Open

3. **Expected Results:**
   - ✅ Success message: "File 'test.txt' uploaded successfully"
   - ✅ File appears in both Alice's and Bob's "File Sharing" list
   - ✅ Chat message: `[System] Alice shared file: test.txt (37 bytes)`

4. **In Bob's window:**
   - Click on `test.txt` in the File Sharing list (to select it)
   - Click **"Download Selected"**
   - Choose save location (e.g., Desktop as `downloaded_test.txt`)
   - Click Save

5. **Expected Results:**
   - ✅ Success message: "File saved to..."
   - ✅ File exists at save location

6. **Verify file content:**
   ```bash
   cat /Users/anvitaprasad/Desktop/downloaded_test.txt
   ```
   - ✅ Should show: "This is a test file for file sharing"

**✅ TEST PASSED IF:** File uploaded, appears in all clients, downloads correctly

---

### Step 9: Test User Disconnection

1. **Start video on both clients** (if not already)

2. **Close Bob's window** (click X or ⌘+Q)

3. **In Alice's window, Expected Results:**
   - ✅ Chat shows: `[System] Bob left the session`
   - ✅ Users list updates (Bob removed)
   - ✅ Bob's video disappears from grid
   - ✅ Alice's video remains

4. **In Server terminal:**
   - ✅ Shows: `[SERVER] Bob disconnected`

**✅ TEST PASSED IF:** Client disconnection handled gracefully without crashes

---

## 🎯 TEST SESSION 2: Multi-User Scenario (Optional)

### Start Client 3 (Charlie)

1. **Open Terminal 4**
   ```bash
   cd /Users/anvitaprasad/Desktop/cnlabstuff
   source .venv/bin/activate
   python client.py
   ```
   - Username: `Charlie`
   - Connect

2. **Expected Results:**
   - ✅ All 3 users see each other in users list
   - ✅ System messages broadcast to all
   - ✅ Chat works between all 3
   - ✅ Video grid shows up to 3 videos

### Test All Features Together

1. **All clients:**
   - Start video
   - Start audio
   - Exchange chat messages

2. **Alice:**
   - Start presenting

3. **Expected Results:**
   - ✅ All features work simultaneously
   - ✅ No crashes or freezes
   - ✅ Performance remains acceptable

**✅ TEST PASSED IF:** All features work with 3+ users concurrently

---

## 🛑 Stopping the System

1. **Close all client windows** (⌘+Q or click X)

2. **In Server terminal:**
   - Press **Ctrl+C**
   - ✅ Server should show: `[SERVER] Shutting down...`
   - ✅ All connections closed gracefully

3. **Deactivate virtual environments** (in all terminals):
   ```bash
   deactivate
   ```

---

## ✅ VERIFICATION CHECKLIST

After testing, check off each feature:

- [ ] **Server starts** and displays IP address
- [ ] **Multiple clients connect** successfully
- [ ] **Users list updates** when users join/leave
- [ ] **Group chat works** - messages broadcast to all
- [ ] **Chat history preserved** for new joiners
- [ ] **Video streaming works** - webcam feeds visible
- [ ] **Multiple videos display** in grid layout
- [ ] **Audio streaming works** - users hear each other
- [ ] **Screen sharing works** - presenter's screen visible
- [ ] **Single presenter mode** enforced correctly
- [ ] **Files upload** to server successfully
- [ ] **Files download** with correct content
- [ ] **User disconnection** handled gracefully
- [ ] **System messages** appear for join/leave events
- [ ] **Concurrent features** work without crashes
- [ ] **Server shutdown** is clean (Ctrl+C works)

---

## 🐛 TROUBLESHOOTING

### Problem: "Connection Failed"
**Solution:**
- Verify server is running
- Check IP address matches exactly
- Ensure firewall allows ports 5555, 5556

### Problem: "Cannot access webcam"
**Solution:**
- Close other apps using camera (Zoom, FaceTime, etc.)
- Grant camera permission:
  - System Preferences → Security & Privacy → Camera
  - Check box for "Terminal" or "Python"

### Problem: "Microphone not working"
**Solution:**
- Grant microphone permission:
  - System Preferences → Security & Privacy → Microphone
- Check microphone not muted in system settings

### Problem: "Screen sharing not visible"
**Solution:**
- Grant screen recording permission:
  - System Preferences → Security & Privacy → Screen Recording
  - Add Terminal or Python
- **Restart Terminal** after granting permission

### Problem: "Module not found" error
**Solution:**
```bash
source .venv/bin/activate
pip install opencv-python numpy Pillow pyaudio mss
```

### Problem: "Address already in use"
**Solution:**
- Server already running - close previous instance
- Or kill process:
  ```bash
  lsof -ti:5555 | xargs kill -9
  lsof -ti:5556 | xargs kill -9
  ```

---

## 📊 EXPECTED PERFORMANCE

| Metric | Expected Value |
|--------|----------------|
| Video Latency | < 1 second |
| Audio Latency | < 500ms |
| Screen Update Rate | ~10 FPS |
| Video Frame Rate | ~30 FPS |
| Max Concurrent Users | 3-5 (optimal) |
| Chat Response Time | < 100ms |
| File Transfer Speed | Depends on LAN (typically >10MB/s) |

---

## 📹 VIDEO DEMO CHECKLIST

When recording your demo, show:

1. ✅ Server startup with IP display
2. ✅ At least 2 clients connecting
3. ✅ Chat message exchange
4. ✅ Video conferencing with 2+ participants
5. ✅ Audio test (at least mention it's working)
6. ✅ Screen sharing demonstration
7. ✅ File upload and download
8. ✅ User disconnection and reconnection
9. ✅ All 5 features working together

---

## 🎓 PROJECT SUBMISSION

Your submission should include:

### 1. Source Code ✅
- `server.py` - Server application
- `client.py` - Client application
- `requirements.txt` - Dependencies
- All code fully commented

### 2. Documentation ✅
- `README.md` - Complete system documentation
- `TESTING_GUIDE.md` - This testing guide
- System architecture explanation
- Protocol descriptions

### 3. Demo Materials
- Screenshots of application running
- Video demonstration (optional but recommended)
- Test results documenting all features work

### 4. User Guide
- How to set up server
- How to connect clients
- Feature usage instructions
- Troubleshooting tips

**All documentation is already created in this directory!**

---

## 🎉 SUCCESS CRITERIA

Your project is complete when:

✅ All 5 core modules implemented and working
✅ Multi-user support (3+ users tested)
✅ Client-server architecture using sockets
✅ TCP and UDP protocols used appropriately
✅ Clean, intuitive GUI
✅ Graceful error handling
✅ Comprehensive documentation
✅ Successful testing on LAN

**Congratulations! Your LAN Collaboration Suite is ready!** 🚀

---

**Need Help?** Review README.md for detailed information on each component.
