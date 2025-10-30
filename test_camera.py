#!/usr/bin/env python3
"""
Camera Test Script - Diagnose camera issues
"""

import cv2
import sys
import time

print("=" * 60)
print("  CAMERA DIAGNOSTIC TEST")
print("=" * 60)

print("\n🔍 Testing camera access...")

# Test 1: Try default backend
print("\nTest 1: Opening camera with default backend...")
cap = cv2.VideoCapture(0)
time.sleep(1)

if cap.isOpened():
    print("✅ Camera opened successfully!")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret and frame is not None:
        print(f"✅ Frame captured! Size: {frame.shape}")
        print(f"✅ Camera is working correctly!")
        cap.release()
        print("\n🎉 SUCCESS: Your camera is working!")
        print("\nThe issue was likely the GUI widget naming conflict.")
        print("This has been fixed in the updated client.py")
        sys.exit(0)
    else:
        print("❌ Camera opened but cannot read frames")
        cap.release()
else:
    print("❌ Cannot open camera with default backend")
    cap.release()

# Test 2: Try macOS specific backend
print("\nTest 2: Opening camera with AVFoundation backend...")
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
time.sleep(1)

if cap.isOpened():
    print("✅ Camera opened with AVFoundation!")
    ret, frame = cap.read()
    if ret and frame is not None:
        print(f"✅ Frame captured! Size: {frame.shape}")
        print(f"✅ Camera working with AVFoundation backend!")
        cap.release()
        print("\n🎉 SUCCESS: Camera works with AVFoundation!")
        sys.exit(0)
    else:
        print("❌ Camera opened but cannot read frames")
        cap.release()
else:
    print("❌ Cannot open camera with AVFoundation")
    cap.release()

# If we get here, camera access failed
print("\n" + "=" * 60)
print("❌ CAMERA ACCESS FAILED")
print("=" * 60)
print("\n📋 SOLUTION:")
print("\n1. Grant Camera Permission:")
print("   • Open System Preferences")
print("   • Go to Security & Privacy → Privacy → Camera")
print("   • Check the box for 'Terminal' or 'Python'")
print("\n2. Restart Terminal:")
print("   • Close all terminal windows")
print("   • Open a new terminal")
print("\n3. Close other apps using camera:")
print("   • Close Zoom, FaceTime, Photo Booth, etc.")
print("\n4. Try running the client again:")
print("   python client.py")
print("\n" + "=" * 60)
sys.exit(1)
