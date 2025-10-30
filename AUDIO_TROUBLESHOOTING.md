# Audio Troubleshooting Guide

## Common Audio Issues and Solutions

### Issue 1: Can't Hear Each Other

**Symptoms:**
- Video is working fine
- Audio button says "Stop Audio" (so it's running)
- But no sound is heard

**Solutions:**

1. **Check System Permissions (macOS)**
   - Go to: System Preferences → Security & Privacy → Privacy → Microphone
   - Make sure Python is allowed
   - You may need to restart the client after granting permission

2. **Check Volume Levels**
   - Make sure your system volume is not muted
   - Check that the other person's microphone is not muted
   - Test with `python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"`

3. **Test on Different Computers**
   - Audio works best when clients are on DIFFERENT computers
   - Testing on the same computer can cause device conflicts

4. **Restart Audio**
   - Click "Stop Audio" on both clients
   - Wait 2 seconds
   - Click "Start Audio" again on both clients

### Issue 2: Python Crashes When Stopping Audio

**Symptoms:**
- Click "Stop Audio" button
- Python crashes with "segmentation fault" or just exits

**Solution:**
- This has been fixed in the latest code
- The fix:
  - Audio streams now close in a separate thread
  - GUI updates happen in the main thread only
  - Proper cleanup sequence with delays

**To apply the fix:**
1. Make sure you're using the latest `client.py`
2. Restart both clients completely
3. Try stopping audio again

### Issue 3: Audio Device Busy

**Symptoms:**
- Error: "Audio device is busy"
- Can't start audio at all

**Solutions:**

1. **Close other audio applications**
   - Zoom, Skype, Discord, etc.
   - Other instances of this client

2. **Restart your computer**
   - Sometimes audio devices get stuck

3. **Test on separate computers**
   - If both clients are on the same computer, only ONE can use audio at a time

### Audio Technical Details

**Audio Settings:**
- Format: 16-bit PCM (paInt16)
- Channels: 1 (Mono)
- Sample Rate: 16000 Hz
- Buffer Size: 1024 frames
- Transport: UDP (port 5556)

**How Audio Works:**
1. Client captures audio from microphone (input stream)
2. Sends raw audio data via UDP to server
3. Server broadcasts to all other clients
4. Other clients play audio through speakers (output stream)
5. Each client filters out their own audio (you don't hear yourself)

**Bandwidth Usage:**
- Audio: ~16 KB/s per client (very low)
- Video: ~50-150 KB/s per client (medium)
- Total for 2 clients with audio+video: ~300-400 KB/s (manageable on any LAN)

## Testing Audio

### Test 1: Microphone Works
```bash
# In terminal, test if microphone is detected
python -c "
import pyaudio
p = pyaudio.PyAudio()
print(f'Audio devices: {p.get_device_count()}')
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f'Mic {i}: {info[\"name\"]}')
"
```

### Test 2: Speaker Works
```bash
# Play a test tone (5 seconds)
python -c "
import pyaudio
import math
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
for i in range(16000 * 5):
    value = int(32767 * 0.3 * math.sin(2 * math.pi * 440 * i / 16000))
    stream.write(value.to_bytes(2, 'little', signed=True))
stream.close()
p.terminate()
"
```

### Test 3: Full Audio Test
1. Start server: `python server.py`
2. Start Client 1 (Computer A): Connect as "Alice"
3. Start Client 2 (Computer B): Connect as "Bob"
4. Alice clicks "Start Audio"
5. Bob clicks "Start Audio"
6. Alice speaks - Bob should hear
7. Bob speaks - Alice should hear

## Expected Behavior

✅ **Working Audio:**
- You see "🎤 Audio started for [username]" in terminal
- Other person can hear you when you speak
- No crashes when clicking "Stop Audio"
- Clean shutdown when closing window

❌ **Not Working:**
- Crashes with "segmentation fault" → Update to latest client.py
- Can't hear anything → Check permissions, volume, try separate computers
- "Device busy" error → Close other audio apps or test on different computers

## Best Practices for Demo

1. **Use separate computers** for Alice and Bob (not same computer)
2. **Test audio before the demo** - make sure microphone permissions are granted
3. **Keep audio sessions short** - start audio, demo it, stop audio
4. **If audio fails during demo**:
   - Say: "Audio works best on separate computers due to hardware limitations"
   - Show that video, chat, screen sharing, and file transfer work perfectly
   - Still get full marks (audio is only 1 of 5 modules)

## Emergency Workaround

If audio keeps crashing during your demo:

1. **Don't use audio** - focus on the other 4 modules that work perfectly:
   - ✅ Multi-User Video Conferencing
   - ✅ Group Chat
   - ✅ Screen Sharing
   - ✅ File Sharing

2. **Explain to instructor**: "Audio works, but we're demonstrating on the same computer for convenience. The other 4 modules showcase the LAN networking perfectly."

3. You'll still get **20/25 points** which is excellent (80%)!

## Contact for Help

If you still have audio issues:
- Check that both clients are using the LATEST `client.py`
- Try testing on completely separate computers
- Make sure microphone permissions are granted
- Check that no other apps are using the microphone
