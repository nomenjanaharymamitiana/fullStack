# Discord Workshop Flag Hunting Guide

## Workshop Details
- **Time**: 2pm GMT+4 (March 18, 2026) - **NOW!**
- **Location**: CyberCup Discord - Voice channel #workshop-live
- **Speaker**: shb4d
- **Duration**: 15 minutes
- **Language**: French

## Flag Details
- **Format**: CCOI26{...}
- **Maximum Attempts**: 10
- **No Replay Available** - Must be present live!

## Immediate Actions Required

### 1. Join Discord Now
```
Discord: discord.gg/xhKvtEYU
Voice Channel: #workshop-live
```

### 2. Start Flag Monitoring
```bash
# Install required dependencies
pip install pyperclip

# Start flag catcher
python3 workshop_flag_catcher.py
```

### 3. Flag Hunting Strategy

## Where Flags Are Typically Hidden in Workshops

### 🎯 Visual Locations
- **Slide backgrounds/watermarks**
- **Code examples in slides**
- **Terminal commands shown**
- **File names in demos**
- **URLs or domains mentioned**
- **Screen annotations**

### 🎯 Audio Locations
- **Speaker saying specific phrases**
- **"Typos" or deliberate mistakes**
- **Hidden words in speech**
- **Background audio cues**

### 🎯 Text Locations
- **Chat messages from speaker**
- **Code comments**
- **Variable names**
- **Function names**
- **Error messages**

## Flag Detection Techniques

### Automatic Detection
The flag catcher will automatically detect:
- `CCOI26{...}` patterns
- Base64 encoded flags
- Hex encoded flags
- ROT13 encoded flags

### Manual Detection
Look for:
- Unusual character sequences
- Encoded strings
- Hidden text in backgrounds
- Speaker's "mistakes"

## Quick Setup Commands

```bash
# Install dependencies
pip install pyperclip

# Start monitoring (choose mode 1 for clipboard)
python3 workshop_flag_catcher.py

# Or use manual mode (mode 2)
python3 workshop_flag_catcher.py
```

## During Workshop - Action Checklist

### Before Workshop Starts
- [ ] Join Discord voice channel
- [ ] Start flag monitoring script
- [ ] Have screenshot tool ready
- [ ] Test flag catcher with sample text

### During Workshop
- [ ] Screenshot suspicious content
- [ ] Copy-paste any code/text immediately
- [ ] Note timestamps of suspicious moments
- [ ] Listen for deliberate "mistakes"
- [ ] Watch speaker's terminal carefully
- [ ] Monitor chat for speaker messages

### After Finding Flag
- [ ] Verify format: CCOI26{...}
- [ ] Submit immediately (only 10 attempts!)
- [ ] Save flag to workshop_flags.txt
- [ ] Note how/where it was found

## Common Workshop Flag Hiding Spots

### Code Examples
```javascript
// Flag might be in comments
const apiKey = "CCOI26{hidden-flag}";
```

### Terminal Commands
```bash
$ echo "CCOI26{workshop-flag}" > secret.txt
```

### File Names
```
/CCOI26{flag-in-filename}.txt
```

### URLs/Domains
```
https://CCOI26{domain-flag}.example.com
```

### Speaker "Mistakes"
- "Oops, I meant CCOI26{typo-flag}"
- "Let me fix that... CCOI26{correction-flag}"

## Emergency Plan

### If You Miss the Flag
1. Check workshop_flags.txt (auto-saved)
2. Review your screenshots
3. Ask in chat (carefully - don't reveal flag location)
4. Check Discord chat history

### Flag Submission Tips
- Double-check format: CCOI26{...}
- No extra spaces or characters
- Submit immediately when found
- Remember: Only 10 attempts!

## Right Now - Do This:

1. **Join Discord**: discord.gg/xhKvtEYU
2. **Go to**: Voice channel #workshop-live
3. **Start monitoring**: `python3 workshop_flag_catcher.py`
4. **Be ready**: Screenshot tool + flag catcher running

The workshop is happening NOW - join immediately!
