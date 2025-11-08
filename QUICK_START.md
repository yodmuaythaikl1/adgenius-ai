# 🚀 Quick Start Guide - AdGenius AI

คู่มือเริ่มต้นใช้งาน AdGenius AI แบบรวดเร็ว

---

## ⚡ วิธีที่เร็วที่สุด (5 นาที)

### 1. Deploy บน Heroku (แนะนำสำหรับผู้เริ่มต้น)

#### ขั้นตอนที่ 1: เตรียมบัญชี
```bash
# 1. สมัคร Heroku ฟรี
https://signup.heroku.com/

# 2. สมัคร MongoDB Atlas ฟรี
https://www.mongodb.com/cloud/atlas/register

# 3. สมัคร OpenAI API Key (สำหรับ AI features)
https://platform.openai.com/api-keys
```

#### ขั้นตอนที่ 2: Deploy ด้วย 1 คลิก
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

หรือใช้ CLI:
```bash
# ติดตั้ง Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku

# Login
heroku login

# Clone repo (ถ้ายังไม่มี)
git clone [your-repo-url]
cd adgenius-ai

# Create app
heroku create adgenius-ai-[your-name]

# Add MongoDB
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32)
heroku config:set OPENAI_API_KEY=your-openai-key-here
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open app
heroku open
```

**เสร็จแล้ว!** 🎉 แอปของคุณพร้อมใช้งานที่: `https://adgenius-ai-[your-name].herokuapp.com`

---

### 2. Deploy บน DigitalOcean (ราคาถูก ประสิทธิภาพดี)

#### ขั้นตอนแบบง่าย (ผ่าน Web UI)

1. **สมัครบัญชี DigitalOcean**
   - ไปที่: https://www.digitalocean.com/
   - รับ Free Credit $200 (ใช้ได้ 60 วัน)

2. **สร้าง App**
   - คลิก "Create" → "Apps"
   - เชื่อมต่อ GitHub repository
   - เลือก branch: `main`
   - เลือก region: Singapore
   - เลือก plan: Basic ($12/month)

3. **ตั้งค่า Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   MONGODB_URI=your-mongodb-atlas-uri
   OPENAI_API_KEY=your-openai-key
   FLASK_ENV=production
   ```

4. **Deploy!**
   - คลิก "Create Resource"
   - รอ 5-10 นาที
   - เสร็จแล้ว! 🎊

---

### 3. Deploy บน Google Cloud Run (แนะนำสำหรับ Scale)

```bash
# 1. ติดตั้ง Google Cloud SDK
# Download: https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. สร้าง project (ถ้ายังไม่มี)
gcloud projects create adgenius-ai-[unique-id]
gcloud config set project adgenius-ai-[unique-id]

# 4. Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 5. สร้าง .env.yaml (สำหรับ secrets)
cat > .env.yaml << EOF
SECRET_KEY: "your-secret-key"
JWT_SECRET_KEY: "your-jwt-secret-key"
MONGODB_URI: "your-mongodb-uri"
OPENAI_API_KEY: "your-openai-key"
FLASK_ENV: "production"
EOF

# 6. Deploy!
gcloud run deploy adgenius-ai \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --env-vars-file .env.yaml \
  --memory 2Gi

# เสร็จแล้ว! URL จะแสดงใน terminal
```

---

## 🗄️ ตั้งค่า MongoDB Atlas (ฟรี 512MB)

### ขั้นตอน:

1. **สมัครบัญชี**: https://www.mongodb.com/cloud/atlas/register

2. **สร้าง Cluster**
   - เลือก "FREE" tier (M0)
   - เลือก Provider: AWS
   - เลือก Region: Singapore (ap-southeast-1)
   - คลิก "Create Cluster"

3. **สร้าง Database User**
   - ไปที่ "Database Access"
   - คลิก "Add New Database User"
   - Username: `adgenius_admin`
   - Password: (สร้างรหัสผ่านที่แข็งแรง)
   - Role: "Read and write to any database"

4. **ตั้งค่า Network Access**
   - ไปที่ "Network Access"
   - คลิก "Add IP Address"
   - เลือก "Allow Access from Anywhere" (0.0.0.0/0)
   - หรือใส่ IP ของ server เฉพาะเจาะจง

5. **ดึง Connection String**
   - กลับไปที่ "Clusters"
   - คลิก "Connect"
   - เลือก "Connect your application"
   - Copy connection string:
   ```
   mongodb+srv://adgenius_admin:<password>@cluster0.xxxxx.mongodb.net/adgenius_ai?retryWrites=true&w=majority
   ```
   - แทนที่ `<password>` ด้วยรหัสผ่านจริง

6. **ใช้งาน**
   - นำ connection string ไปใส่ใน `MONGODB_URI` environment variable

---

## 🔑 ดึง API Keys ที่จำเป็น

### 1. OpenAI API Key (สำหรับ AI Features)
- ไปที่: https://platform.openai.com/api-keys
- สร้าง API key ใหม่
- Copy และเก็บไว้อย่างปลอดภัย

### 2. Facebook & Instagram API
- ไปที่: https://developers.facebook.com/
- สร้าง App ใหม่
- ไปที่ Settings → Basic
- Copy App ID และ App Secret

### 3. TikTok API
- ไปที่: https://ads.tiktok.com/marketing_api/
- สมัคร Developer Account
- สร้าง App และดึง credentials

### 4. Shopee API
- ไปที่: https://open.shopee.com/
- ลงทะเบียนเป็น Partner
- สร้าง App และดึง Partner ID, Partner Key

---

## ✅ ตรวจสอบว่า Deploy สำเร็จ

### 1. Health Check
```bash
curl https://your-app-url.com/health
# Expected: {"status": "healthy"}
```

### 2. API Info
```bash
curl https://your-app-url.com/
# Expected: {"name": "AdGenius AI API", "version": "1.0.0", "status": "running"}
```

### 3. ทดสอบ API
```bash
# Register user
curl -X POST https://your-app-url.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'
```

---

## 🎯 ขั้นตอนถัดไป

### 1. ตั้งค่า Domain Name (Optional)
```bash
# ซื้อ domain จาก Namecheap, GoDaddy
# ตั้งค่า DNS CNAME record ชี้ไปที่ app URL
# ติดตั้ง SSL certificate (มักจะทำอัตโนมัติ)
```

### 2. ตั้งค่า Monitoring
- **Heroku**: เปิด metrics ใน dashboard
- **DigitalOcean**: มี built-in monitoring
- **GCP**: ใช้ Cloud Monitoring
- **หรือใช้**: Sentry, DataDog, New Relic

### 3. ปรับแต่ง Configuration
- แก้ไข `CORS_ORIGINS` ให้ตรงกับ frontend URL
- ตั้งค่า rate limiting
- เพิ่ม backup schedule สำหรับ database

### 4. พัฒนา Frontend
- สร้าง React/Next.js app
- เชื่อมต่อกับ API
- Deploy บน Vercel หรือ Netlify

---

## 💰 ประมาณการค่าใช้จ่าย

### แผน Startup (ทดลอง)
- **Heroku Hobby**: $7/month
- **MongoDB Atlas Free**: $0
- **Total**: **$7/month** ✅

### แผน SME (ธุรกิจขนาดเล็ก-กลาง)
- **DigitalOcean Basic**: $12/month
- **MongoDB Atlas M10**: $0.08/hour (~$57/month)
- **Total**: **~$69/month**

### แผน Enterprise (ธุรกิจขนาดใหญ่)
- **AWS/GCP**: $100-500/month (ขึ้นกับ traffic)
- **MongoDB Atlas Dedicated**: $200+/month
- **Total**: **$300-700/month**

---

## 🆘 แก้ปัญหาเบื้องต้น

### ปัญหา: App ไม่ start
```bash
# ตรวจสอบ logs
heroku logs --tail  # สำหรับ Heroku
doctl apps logs [app-id]  # สำหรับ DigitalOcean
gcloud run logs read  # สำหรับ GCP
```

### ปัญหา: เชื่อมต่อ MongoDB ไม่ได้
- ตรวจสอบ connection string
- ตรวจสอบ Network Access ใน MongoDB Atlas
- ตรวจสอบ username/password

### ปัญหา: API ทำงานช้า
- Upgrade instance size
- เพิ่ม caching (Redis)
- ใช้ CDN สำหรับ static files

---

## 📚 เอกสารเพิ่มเติม

- [คู่มือการติดตั้งแบบเต็ม](./คู่มือการติดตั้งแพลตฟอร์ม%20AdGenius%20AI.md)
- [คู่มือการ Deploy โดยละเอียด](./DEPLOYMENT_GUIDE.md)
- [API Documentation](./static/API_DOCS.md)
- [Project Structure](./project_structure.md)

---

## 🎉 สรุป

เลือกวิธี deploy ที่เหมาะกับคุณ:

| สถานการณ์ | แนะนำ | เวลา | ราคา |
|----------|-------|------|------|
| 🧪 ทดลองใช้งาน | **Heroku** | 5 นาที | $7/เดือน |
| 🚀 ธุรกิจเริ่มต้น | **DigitalOcean** | 10 นาที | $27-69/เดือน |
| 📈 Scale ขึ้น | **Google Cloud Run** | 15 นาที | $67-87/เดือน |
| 🏢 Enterprise | **AWS/Azure** | 30 นาที | $88+/เดือน |

**แนะนำเริ่มจาก Heroku → ย้ายไป DigitalOcean เมื่อโตขึ้น → Scale ด้วย AWS/GCP** 🎯
