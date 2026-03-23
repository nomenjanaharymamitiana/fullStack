#!/usr/bin/env python3
import re
import time
from datetime import datetime

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class WorkshopFlagCatcher:
    def __init__(self):
        self.flag_pattern = re.compile(r'CCOI26\{[^}]+\}', re.IGNORECASE)
        self.found_flags = []
        self.clipboard_history = []
        self.start_time = datetime.now()
    
    def extract_flags_from_text(self, text):
        """Extract flags from any text input"""
        if not text:
            return []
        
        flags = self.flag_pattern.findall(text)
        unique_flags = list(set(flags))  # Remove duplicates
        
        for flag in unique_flags:
            if flag not in self.found_flags:
                self.found_flags.append(flag)
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"🚀 FLAG FOUND at {timestamp}: {flag}")
                self.save_flag(flag, timestamp)
        
        return unique_flags
    
    def save_flag(self, flag, timestamp):
        """Save flag to file with timestamp"""
        with open('workshop_flags.txt', 'a') as f:
            f.write(f"[{timestamp}] {flag}\n")
        
        # Also save to clipboard for quick submission
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(flag)
                print("📋 Flag copied to clipboard!")
            except:
                print("⚠️  Could not copy to clipboard")
        else:
            print("⚠️  pyperclip not available - manual copy required")
    
    def monitor_clipboard(self, interval=1):
        """Monitor clipboard for flag patterns"""
        print("📋 Monitoring clipboard for flags...")
        print("Workshop tips for finding hidden flags:")
        print("- Look in speaker's code examples")
        print("- Check slide backgrounds/watermarks")
        print("- Listen for specific phrases")
        print("- Watch for encoded text (base64, hex)")
        print("- Check speaker's terminal/shell")
        print("- Look in URLs, file names, comments")
        print("- Pay attention to 'mistakes' or 'typos'")
        print("- Check chat messages and reactions")
        print()
        
        try:
            if CLIPBOARD_AVAILABLE:
                import pyperclip
                last_clipboard = ""
                
                while True:
                    try:
                        current_clipboard = pyperclip.paste()
                        
                        if current_clipboard != last_clipboard:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            print(f"[{timestamp}] Clipboard changed: {current_clipboard[:100]}...")
                            
                            flags = self.extract_flags_from_text(current_clipboard)
                            if flags:
                                print(f"🎯 Found {len(flags)} flag(s) in clipboard!")
                            
                            # Also check for potential encoded flags
                            self.check_encoded_content(current_clipboard, timestamp)
                            
                            last_clipboard = current_clipboard
                    
                    except Exception as e:
                        print(f"Clipboard error: {e}")
                    
                    time.sleep(interval)
            else:
                print("❌ pyperclip not available. Use manual mode instead.")
                return False
        
        except Exception as e:
            print(f"Clipboard monitoring error: {e}")
            return False
    
    def check_encoded_content(self, text, timestamp):
        """Check for various encoded flag patterns"""
        import base64
        import binascii
        
        # Check for base64 encoded flags
        try:
            # Remove whitespace and try to decode
            clean_text = ''.join(text.split())
            if len(clean_text) % 4 == 0:  # Valid base64 length
                decoded = base64.b64decode(clean_text).decode('utf-8', errors='ignore')
                flags = self.extract_flags_from_text(decoded)
                if flags:
                    print(f"🔓 Base64 decoded flags: {flags}")
        except:
            pass
        
        # Check for hex encoded flags
        try:
            clean_hex = ''.join(c for c in text if c in '0123456789ABCDEFabcdef')
            if len(clean_hex) % 2 == 0 and len(clean_hex) > 10:
                decoded = binascii.unhexlify(clean_hex).decode('utf-8', errors='ignore')
                flags = self.extract_flags_from_text(decoded)
                if flags:
                    print(f"🔓 Hex decoded flags: {flags}")
        except:
            pass
        
        # Check for potential ROT13
        try:
            rot13_text = text.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 'NOPQRSTUVWXYZnopqrstuvwxyzabcdefghijklm'))
            flags = self.extract_flags_from_text(rot13_text)
            if flags:
                print(f"🔓 ROT13 decoded flags: {flags}")
        except:
            pass
    
    def manual_input_mode(self):
        """Manual flag checking mode"""
        print("🎯 Manual Flag Input Mode")
        print("Paste any suspicious text here to check for flags")
        print("Type 'quit' to exit")
        print()
        
        while True:
            text = input("Enter text to check: ").strip()
            if text.lower() in ['quit', 'exit', 'q']:
                break
            
            flags = self.extract_flags_from_text(text)
            if flags:
                print(f"🚀 FLAGS FOUND: {flags}")
            else:
                print("❌ No flags found")
            
            # Check for encoded content
            self.check_encoded_content(text, datetime.now().strftime("%H:%M:%S"))
    
    def show_workshop_tips(self):
        """Display workshop flag hunting tips"""
        tips = [
            "🎯 WORKSHOP FLAG HUNTING TIPS",
            "",
            "📍 WHERE FLAGS MIGHT BE HIDDEN:",
            "• Speaker's code examples and demos",
            "• Slide backgrounds/watermarks",
            "• Terminal commands or file names",
            "• URLs, domains, or IP addresses",
            "• 'Typos' or deliberate mistakes",
            "• Chat messages from speaker",
            "• Voice instructions (listen carefully!)",
            "• Screen sharing annotations",
            "• File names in demos",
            "• Comments in code",
            "",
            "🔍 WHAT TO LOOK FOR:",
            "• CCOI26{...} format",
            "• Encoded strings (base64, hex)",
            "• Unusual character sequences",
            "• Hidden text in backgrounds",
            "• Audio cues in speech",
            "",
            "⚡ QUICK ACTIONS:",
            "• Screenshot suspicious content",
            "• Copy-paste text immediately",
            "• Take notes of timestamps",
            "• Record audio if possible",
            "",
            "🚨 REMEMBER:",
            "• Only 10 submission attempts allowed",
            "• No replay available",
            "• Must be present live!",
            "• Flag format: CCOI26{...}"
        ]
        
        for tip in tips:
            print(tip)
        
        print()

if __name__ == "__main__":
    catcher = WorkshopFlagCatcher()
    
    print("🎯 Discord Workshop Flag Catcher")
    print("=" * 50)
    
    # Show tips
    catcher.show_workshop_tips()
    
    # Choose mode
    print("Choose mode:")
    print("1. Monitor clipboard (requires pyperclip)")
    print("2. Manual input mode")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        catcher.monitor_clipboard()
    elif choice == "2":
        catcher.manual_input_mode()
    else:
        print("Invalid choice. Starting manual mode...")
        catcher.manual_input_mode()
