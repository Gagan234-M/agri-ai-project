# Deploy Your Agricultural AI Website to Mobile 📱

## Option 1: **ngrok** (Easiest - 5 minutes)

### What is ngrok?
Exposes your local Flask app to the internet with a public URL.

### Steps:

#### 1. Install ngrok
```bash
# Go to https://ngrok.com/download
# Download and extract ngrok for Windows
# Add to PATH or use from same folder
```

#### 2. Start your Flask app normally
```bash
cd agri_ai_project
python app.py
```
(Runs on http://127.0.0.1:5000)

#### 3. Open another terminal and run ngrok
```bash
ngrok http 5000
```

#### 4. You'll see output like:
```
Forwarding                    https://abc123def456.ngrok.io -> http://localhost:5000
```

#### 5. Share link with friend
Send: `https://abc123def456.ngrok.io`

Your friend opens it on mobile and can use the app!

**⏱️ Duration:** Works while laptop is on and ngrok is running  
**📱 Mobile Access:** Full access from any device worldwide  
**💰 Cost:** Free (5 connections/minute limit) or paid for unlimited

---

## Option 2: **Render** (Best - Permanent hosting)

### What is Render?
Free cloud platform that deploys your app permanently.

### Steps:

#### 1. Prepare your code
Ensure these files exist in your project:
```
requirements.txt  ✅ (already have)
app.py            ✅ (already have)
```

#### 2. Create `runtime.txt` (tells Render which Python version)
```
python-3.10.12
```

#### 3. Create `Procfile` (tells Render how to run app)
```
web: python app.py
```

#### 4. Prepare your app for deployment
Modify `app.py` last line:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### 5. Push to GitHub
```bash
git init
git add .
git commit -m "Deploy agriculture AI"
git push origin main
```

#### 6. Deploy on Render
- Go to https://render.com
- Connect GitHub account
- Click "New +" → "Web Service"
- Select your repository
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Deploy!

#### 7. Get your URL
Render gives you: `https://agri-ai.onrender.com`

Your friend accesses it anytime from mobile!

**⏱️ Duration:** Permanent (24/7)  
**📱 Mobile Access:** Full access from anywhere  
**💰 Cost:** Free tier available  
**🎯 Best for:** Production/long-term hosting

---

## Option 3: **Heroku** (Popular but now paid)

Heroku is simple but moved to paid-only model.

If you have paid account:
```bash
# Install Heroku CLI
heroku login
heroku create your-agri-ai
git push heroku main
```

---

## Option 4: **Railway.app** (Easy & Free)

### Steps:

#### 1. Create account at https://railway.app

#### 2. Connect GitHub repository

#### 3. Railway auto-detects Python app

#### 4. Get automatic URL like: `https://agri-ai.up.railway.app`

**Cost:** Free tier (5 GB/month)  
**Duration:** Permanent

---

## Option 5: **Local Network Sharing** (Works at home/office)

### Share within same WiFi network

#### Modify app.py:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Get your laptop's IP:
```powershell
ipconfig
```
Look for IPv4 Address like: `192.168.1.100`

#### Friend opens:
```
http://192.168.1.100:5000
```

**Duration:** Only while laptop is on and on same WiFi  
**Cost:** Free  
**Range:** Same WiFi network only

---

## Quick Comparison

| Method | Setup Time | Cost | Duration | Access | Best For |
|--------|-----------|------|----------|--------|----------|
| **ngrok** | 5 min | Free | While running | Worldwide | Quick demo |
| **Render** | 15 min | Free | 24/7 | Worldwide | Production |
| **Railway** | 15 min | Free | 24/7 | Worldwide | Production |
| **Local WiFi** | 2 min | Free | While laptop on | Same WiFi | Testing |
| **Heroku** | 15 min | Paid | 24/7 | Worldwide | Not recommended |

---

## 🚀 Recommended Path

### For Quick Demo:
```
1. Use ngrok (5 minutes)
2. Keep laptop on while friend tests
3. Share public URL
```

### For Permanent Access:
```
1. Use Render (15 minutes setup)
2. App runs 24/7 on their servers
3. Your friend accesses anytime
4. Perfect for presentation/demo
```

---

## Step-by-Step: Deploy to Render (Easiest Permanent)
this
### 1. Create necessary files in your project folder:

**File: `runtime.txt`**
```
python-3.10.12
```

**File: `Procfile`**
```
web: python app.py
```

### 2. Modify `app.py` last lines:
```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 3. Update `requirements.txt`:
```
flask
tensorflow
numpy
pillow
matplotlib
opencv-python
lime
scikit-image
scikit-learn
werkzeug
gunicorn
```

### 4. Create GitHub repository:
```bash
git init
git add .
git commit -m "Agriculture AI App"
git remote add origin https://github.com/YOUR_USERNAME/agri-ai.git
git push -u origin main
```

### 5. Deploy on Render:
- Go to https://render.com
- Sign up with GitHub
- Click "New +" → "Web Service"
- Select repository
- Click "Deploy"
- Get your live URL!

### 6. Your friend opens:
```
https://your-agri-ai.onrender.com
```

---

## ⚠️ Important Notes

### For TensorFlow on Cloud:
```
# Add to requirements.txt
tensorflow==2.12.0  # Specify version for compatibility
```

### Environment Variables:
If you store API keys, use Render Environment Variables (they provide UI for this)

### Model File Size:
`plant_disease_model.h5` must be included in repository  
(Render will deploy it)

### Mobile Optimization:
Your UI already looks good on mobile! ✅

---

## Testing Mobile Access

### 1. After deployment, test on:
- Your mobile phone
- Friend's mobile phone
- Different networks (WiFi + 4G)
- Different browsers

### 2. Check if working:
```
✅ Upload image
✅ See disease prediction
✅ View explanations
✅ Multilingual support
✅ Warnings displayed
```

---

## Troubleshooting

### Issue: "Connection refused"
**Solution:** Ensure Flask is running on `0.0.0.0` not just `localhost`

### Issue: "Port already in use"
**Solution:** Change port number or stop other services

### Issue: "Model file not found"
**Solution:** Ensure `plant_disease_model.h5` is in repository

### Issue: "Image upload fails"
**Solution:** Check upload folder permissions

---

## My Recommendation 🎯

### For your presentation:

**Best:** Deploy to **Render.app** (15 min)
- Permanent URL
- Works 24/7
- Works on any device anywhere
- Free tier available
- Perfect for demo

Your friend can access anytime without you turning on laptop!

---

## Quick Links

- **ngrok:** https://ngrok.com
- **Render:** https://render.com
- **Railway:** https://railway.app
- **GitHub:** https://github.com

---

## Need Help?

Ask me:
1. "Deploy to Render step by step"
2. "How to set up ngrok now"
3. "How to share on local WiFi"
4. "Troubleshoot deployment error: [error message]"

I can guide you through any step! 🌾
