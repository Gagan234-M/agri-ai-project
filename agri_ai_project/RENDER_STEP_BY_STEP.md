# Deploy to Render.app - Complete Step-by-Step Guide

## Overview
You'll deploy your Flask app to Render so your friend can access it 24/7 without your laptop being on.

**Total time: ~20 minutes**

---

## STEP 1: Prepare Your Project Files

### 1.1 Create `runtime.txt`
This tells Render which Python version to use.

**Location:** `c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project\runtime.txt`

**Content:**
```
python-3.10.12
```

### 1.2 Create `Procfile`
This tells Render how to start your app.

**Location:** `c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project\Procfile`

**Content:**
```
web: gunicorn app:app
```

### 1.3 Update `requirements.txt`
Add `gunicorn` (needed for production server).

**Location:** `c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project\requirements.txt`

**Current content:**
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
```

**Replace with:**
```
flask
tensorflow==2.12.0
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

### 1.4 Modify `app.py`
Change the last line to support environment variables.

**Find this (at the very end of app.py):**
```python
if __name__ == '__main__':

    app.run(debug=True)
```

**Replace with:**
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 1.5 Check Your Project Structure
```
agri_ai_project/
├── app.py
├── requirements.txt
├── runtime.txt              ← NEW
├── Procfile                 ← NEW
├── plant_disease_model.h5
├── image_enhancement.py
├── explainability.py
├── grad_cam.py
├── translations.py
├── static/
├── templates/
└── dataset/
```

---

## STEP 2: Create GitHub Repository

### 2.1 Install Git (if not already installed)
Download from: https://git-scm.com/download/win

### 2.2 Initialize Git Repository
Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project"
git init
```

### 2.3 Add All Files
```powershell
git add .
```

### 2.4 Create Initial Commit
```powershell
git config user.email "your-email@example.com"
git config user.name "Your Name"
git commit -m "Initial commit: Agriculture AI app"
```

### 2.5 Create GitHub Account
Go to: https://github.com/signup

### 2.6 Create New Repository on GitHub
1. Click "+" → "New repository"
2. Name it: `agri-ai`
3. Description: "Agricultural Disease Detection AI"
4. Select "Public"
5. Click "Create repository"

### 2.7 Push Code to GitHub
GitHub will show you these commands. Run them:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/agri-ai.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username**

### 2.8 Verify on GitHub
Open: https://github.com/YOUR_USERNAME/agri-ai  
You should see all your files!

---

## STEP 3: Deploy on Render

### 3.1 Create Render Account
Go to: https://render.com

1. Click "Sign up"
2. Choose "Sign up with GitHub"
3. Authorize Render
4. You're logged in!

### 3.2 Create New Web Service
1. Click "New +" button
2. Select "Web Service"

### 3.3 Connect GitHub Repository
1. Click "Connect a repository"
2. Find your `agri-ai` repository
3. Click "Connect"

### 3.4 Configure Deployment

**Fill in the form:**

| Field | Value |
|-------|-------|
| Name | `agri-ai` |
| Environment | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | `Free` |

### 3.5 Review Settings
Make sure you see:
```
✅ GitHub repository: agri-ai
✅ Branch: main
✅ Environment: Python 3
✅ Build Command: pip install -r requirements.txt
✅ Start Command: gunicorn app:app
✅ Auto-deploy: On (default)
```

### 3.6 Deploy!
Click "Create Web Service"

**Wait 3-5 minutes for deployment...**

---

## STEP 4: Get Your URL

### 4.1 Wait for Green Checkmark
After deployment completes, you'll see:
```
✅ Deploy successful
```

### 4.2 Get Your Public URL
You'll see something like:
```
https://agri-ai.onrender.com
```

This is your **public website URL**!

### 4.3 Test It
1. Copy the URL
2. Open in browser
3. Try uploading an image
4. Verify it works!

### 4.4 Share with Friend
Send your friend:
```
https://agri-ai.onrender.com
```

They can open it on mobile from anywhere!

---

## STEP 5: Verify Everything Works

### 5.1 Test Basic Features
- ✅ Upload image
- ✅ See prediction
- ✅ View Grad-CAM visualization
- ✅ Change language
- ✅ See warnings for blurry images

### 5.2 Test on Mobile
Ask friend to:
1. Open URL on their phone
2. Try uploading a plant image
3. Check if predictions work
4. Check if visualizations display

### 5.3 Monitor Logs (Optional)
In Render dashboard:
1. Go to your Web Service
2. Click "Logs"
3. See real-time activity
4. Check for errors

---

## STEP 6: Common Issues & Solutions

### Issue: "Build failed"
**Solution:**
1. Go to Render dashboard
2. Click "Logs"
3. Read error message
4. Fix on your laptop
5. Push to GitHub: `git push origin main`
6. Render auto-redeploys!

### Issue: "Model file not found"
**Solution:**
```powershell
# Make sure file is committed
git add plant_disease_model.h5
git commit -m "Add trained model"
git push
```

### Issue: "Port error"
**Solution:** Verify `app.py` has:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

### Issue: "Image upload fails"
**Solution:** Check upload folder permissions
```python
# In app.py, add:
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Already present
```

### Issue: "Slow response time"
**Solution:**
- Free tier has limited resources
- Upgrade to paid ($7/month) if needed
- Or wait 1-2 minutes first time

---

## STEP 7: Make Updates (If Needed)

If you make changes to your code:

### 7.1 On Your Laptop
```powershell
cd "c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project"
git add .
git commit -m "Update: [what you changed]"
git push origin main
```

### 7.2 Render Automatically Redeploys
- Render watches your GitHub
- When you push, it automatically redeploys
- Takes 2-3 minutes
- No manual steps needed!

---

## File Checklist

Before deploying, confirm you have:

```
✅ app.py                          [MODIFIED - added host/port settings]
✅ requirements.txt                [UPDATED - added gunicorn]
✅ runtime.txt                     [NEW FILE - added]
✅ Procfile                        [NEW FILE - added]
✅ plant_disease_model.h5          [MUST EXIST - model file]
✅ image_enhancement.py            [MUST EXIST]
✅ explainability.py               [MUST EXIST]
✅ grad_cam.py                     [MUST EXIST]
✅ translations.py                 [MUST EXIST]
✅ static/uploads/                 [DIRECTORY - folder for uploads]
✅ templates/                      [DIRECTORY - if using templates]
✅ .git/                           [CREATED BY GIT INIT]
```

---

## Quick Command Reference

### One-time setup:
```powershell
cd "c:\Users\Gagan M\Downloads\agri_ai_project\agri_ai_project"
git init
git config user.email "you@example.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/agri-ai.git
git branch -M main
git push -u origin main
```

### After making changes:
```powershell
git add .
git commit -m "Your message"
git push origin main
```

---

## Expected Timeline

| Step | Time | What's Happening |
|------|------|-----------------|
| Create files | 2 min | Adding runtime.txt, Procfile |
| Git setup | 3 min | Initialize & commit |
| Push to GitHub | 2 min | Upload files to GitHub |
| Render setup | 2 min | Configure on Render |
| Deployment | 5 min | Render builds & deploys |
| **Total** | **~15 min** | **App is live!** |

---

## After Deployment

### Your app is now:
- ✅ **Live online** - Anyone can access with URL
- ✅ **24/7 Available** - Works even when your laptop is off
- ✅ **Free** - Free tier covers your needs
- ✅ **Auto-updating** - Push to GitHub, auto-redeploys
- ✅ **Mobile-friendly** - Works on phones and tablets

### Share with friend:
```
https://agri-ai.onrender.com
```

Friend can use it anytime, anywhere! 📱

---

## Next Steps

### If you see errors:
1. Check Render logs
2. Fix on your laptop
3. Push to GitHub
4. Render auto-redeploys

### If everything works:
🎉 **Congratulations! Your app is deployed!**

### Optional upgrades:
- Upgrade to paid ($7/month) for better performance
- Add custom domain (paid feature)
- Set up email notifications for deployments

---

## Support Commands

If stuck, try:

```powershell
# Check git status
git status

# See commit history
git log

# See current remote
git remote -v

# Reset if needed
git reset --hard HEAD
```

---

## Final Check

Before telling your friend:
1. ✅ Open your Render URL in browser
2. ✅ Upload a test image
3. ✅ See prediction
4. ✅ View Grad-CAM
5. ✅ Test on phone

**Ready! Share the URL with your friend!** 🌾
