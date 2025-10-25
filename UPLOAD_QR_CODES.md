# Upload QR Codes - Quick Guide

## You Have These QR Code Images

### 1. Ko-fi QR Code
![Ko-fi QR](https://i.imgur.com/your-kofi-qr.png)
- **Source**: The image you provided
- **Destination**: `assets/kofi-qr.png`
- **Links to**: https://ko-fi.com/B0B21ND7UZ

### 2. Lightning QR Code  
![Lightning QR](https://i.imgur.com/your-lightning-qr.png)
- **Source**: The Alby wallet screenshot you provided
- **Address**: havenhelpful360120@getalby.com
- **Destination**: `assets/lightning-qr.png`

## How to Upload

### Option 1: Save from Screenshots (Easiest)
1. Open the images you sent in chat
2. Right-click each QR code → Save Image As...
3. Save Ko-fi QR as: `C:\Users\gerry\OLLAMA PROXY\ollama_pulse_check\assets\kofi-qr.png`
4. Save Lightning QR as: `C:\Users\gerry\OLLAMA PROXY\ollama_pulse_check\assets\lightning-qr.png`
5. Run: `git add assets/*.png && git commit -m "feat: add donation QR codes" && git push`

### Option 2: Use PowerShell to Download (if you have URLs)
```powershell
cd "C:\Users\gerry\OLLAMA PROXY\ollama_pulse_check"

# If you have the images hosted somewhere:
Invoke-WebRequest -Uri "YOUR_KOFI_QR_URL" -OutFile "assets\kofi-qr.png"
Invoke-WebRequest -Uri "YOUR_LIGHTNING_QR_URL" -OutFile "assets\lightning-qr.png"

git add assets/*.png
git commit -m "feat: add donation QR codes"
git push
```

### Option 3: Generate Fresh QR Codes
```powershell
# Install qrcode library
pip install qrcode[pil]

# Generate Ko-fi QR
python -c "import qrcode; qr = qrcode.make('https://ko-fi.com/B0B21ND7UZ'); qr.save('assets/kofi-qr.png')"

# Generate Lightning QR  
python -c "import qrcode; qr = qrcode.make('lightning:havenhelpful360120@getalby.com'); qr.save('assets/lightning-qr.png')"

git add assets/*.png
git commit -m "feat: add donation QR codes"
git push
```

## Verify Upload

After uploading, verify the QR codes are accessible:
- Ko-fi: https://raw.githubusercontent.com/AccidentalJedi/ollama_pulse_check/main/assets/kofi-qr.png
- Lightning: https://raw.githubusercontent.com/AccidentalJedi/ollama_pulse_check/main/assets/lightning-qr.png

## Test the Footer

Run this to see how the donation footer looks:
```powershell
cd "C:\Users\gerry\OLLAMA PROXY\ollama_pulse_check"
python -c "from scripts.post_to_nostr import add_donation_footer; print(add_donation_footer('# Test Report\n\nSome content here.'))"
```

## Next: Test Auto-Posting

Once QR codes are uploaded:
```powershell
# Make sure you have a report to post
ls docs/reports/pulse-*.md

# Test posting (requires NOSTR keys in environment)
python scripts\post_to_nostr.py
```

---

**Quick Command to Upload QR Codes:**
```powershell
# 1. Save your QR images to assets/ folder
# 2. Then run:
cd "C:\Users\gerry\OLLAMA PROXY\ollama_pulse_check"
git add assets/*.png
git commit -m "feat: add donation QR codes for Ko-fi and Lightning"
git push origin main
```

