#!/usr/bin/env python3
"""
Quick System Test - Verifies all components are working
"""

import socket
import json
import struct
import sys

def test_server_connection():
    """Test if server is reachable"""
    print("🔍 Testing Server Connection...")
    try:
        # Test TCP connection
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.settimeout(5)
        tcp_sock.connect(('127.0.0.1', 5555))
        print("   ✅ TCP Server (port 5555) is reachable")
        
        # Send registration message
        test_data = {
            'type': 'register',
            'username': 'TestUser',
            'udp_port': 12345
        }
        msg = json.dumps(test_data).encode('utf-8')
        tcp_sock.sendall(struct.pack('>I', len(msg)) + msg)
        print("   ✅ Registration message sent")
        
        # Try to receive response
        raw_len = tcp_sock.recv(4)
        if raw_len:
            msg_len = struct.unpack('>I', raw_len)[0]
            data = b''
            while len(data) < msg_len:
                packet = tcp_sock.recv(msg_len - len(data))
                if not packet:
                    break
                data += packet
            
            response = json.loads(data.decode('utf-8'))
            if response.get('type') == 'registered':
                print("   ✅ Server registration successful!")
                print(f"   ℹ️  Current users: {response.get('users', [])}")
                tcp_sock.close()
                return True
        
        tcp_sock.close()
        return False
        
    except ConnectionRefusedError:
        print("   ❌ Server is not running on port 5555")
        return False
    except socket.timeout:
        print("   ❌ Server connection timeout")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_udp_port():
    """Test if UDP port is accessible"""
    print("\n🔍 Testing UDP Port...")
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.settimeout(2)
        
        # Send a test packet
        test_packet = b'\x01\x08TestUser' + b'Test data'
        udp_sock.sendto(test_packet, ('127.0.0.1', 5556))
        print("   ✅ UDP packet sent to port 5556")
        
        udp_sock.close()
        return True
    except Exception as e:
        print(f"   ❌ UDP Error: {e}")
        return False

def check_dependencies():
    """Check if all required modules are installed"""
    print("\n🔍 Checking Dependencies...")
    required = ['cv2', 'numpy', 'PIL', 'pyaudio', 'mss']
    missing = []
    
    for module in required:
        try:
            if module == 'cv2':
                import cv2
                print(f"   ✅ opencv-python (cv2) - version {cv2.__version__}")
            elif module == 'numpy':
                import numpy
                print(f"   ✅ numpy - version {numpy.__version__}")
            elif module == 'PIL':
                import PIL
                print(f"   ✅ Pillow (PIL) - version {PIL.__version__}")
            elif module == 'pyaudio':
                import pyaudio
                print(f"   ✅ pyaudio - installed")
            elif module == 'mss':
                import mss
                print(f"   ✅ mss - version {mss.__version__}")
        except ImportError:
            print(f"   ❌ {module} - NOT INSTALLED")
            missing.append(module)
    
    return len(missing) == 0

def check_files():
    """Check if all required files exist"""
    print("\n🔍 Checking Project Files...")
    import os
    
    required_files = [
        'server.py',
        'client.py',
        'requirements.txt',
        'README.md',
        'TESTING_GUIDE.md',
        'QUICK_REFERENCE.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("  LAN COLLABORATION SUITE - SYSTEM TEST")
    print("=" * 60)
    
    # Check files
    files_ok = check_files()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test server
    server_ok = test_server_connection()
    
    # Test UDP
    udp_ok = test_udp_port()
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print(f"  Project Files:     {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"  Dependencies:      {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"  Server (TCP):      {'✅ PASS' if server_ok else '❌ FAIL'}")
    print(f"  Server (UDP):      {'✅ PASS' if udp_ok else '❌ FAIL'}")
    print("=" * 60)
    
    if all([files_ok, deps_ok, server_ok, udp_ok]):
        print("\n🎉 ALL TESTS PASSED! System is ready!")
        print("\nNext Steps:")
        print("1. Start the GUI client:")
        print("   python client.py")
        print("\n2. Or run multiple clients in different terminals:")
        print("   Terminal 1: python client.py  (Username: Alice)")
        print("   Terminal 2: python client.py  (Username: Bob)")
        print("\n3. In each client:")
        print("   - Server IP: 127.0.0.1")
        print("   - Click 'Connect'")
        print("   - Test features: Chat, Video, Audio, Screen Share, Files")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Please check errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
