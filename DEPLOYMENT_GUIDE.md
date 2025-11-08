# คู่มือการ Deploy AdGenius AI Platform

เอกสารนี้แนะนำวิธีการ deploy แพลตฟอร์ม AdGenius AI บน Cloud Platform ต่างๆ โดยไม่ต้องรันบนเครื่องของคุณ

---

## 🚀 ตัวเลือกการ Deploy (แนะนำ)

### 1. **AWS (Amazon Web Services)** ⭐ แนะนำสูงสุด

**ข้อดี:**
- มีบริการครบวงจร และมั่นคง
- ราคาเริ่มต้นต่ำ (Free Tier 12 เดือน)
- Scale ได้ง่าย
- มี MongoDB Atlas integration ที่ดี

**วิธี Deploy:**

#### A. ใช้ AWS Elastic Beanstalk (ง่ายที่สุด)
```bash
# 1. ติดตั้ง AWS CLI และ EB CLI
pip install awsebcli awscli

# 2. กำหนดค่า AWS credentials
aws configure

# 3. สร้าง Elastic Beanstalk application
eb init -p docker adgenius-ai --region ap-southeast-1

# 4. สร้าง environment และ deploy
eb create adgenius-production

# 5. เปิดแอปพลิเคชัน
eb open
```

**ค่าใช้จ่ายโดยประมาณ:**
- t3.small instance: ~$15/เดือน
- Application Load Balancer: ~$16/เดือน
- MongoDB Atlas M10: ~$57/เดือน
- **รวม: ~$88/เดือน**

#### B. ใช้ AWS ECS (Container Service)
```bash
# 1. สร้าง ECR repository
aws ecr create-repository --repository-name adgenius-ai

# 2. Build และ push Docker image
docker build -t adgenius-ai .
docker tag adgenius-ai:latest [your-ecr-url]/adgenius-ai:latest
docker push [your-ecr-url]/adgenius-ai:latest

# 3. สร้าง ECS cluster, task definition และ service ผ่าน AWS Console
```

---

### 2. **Google Cloud Platform (GCP)** ⭐ แนะนำ

**ข้อดี:**
- Free Credit $300 สำหรับผู้ใช้ใหม่
- Cloud Run ราคาถูก (pay per use)
- Integration กับ AI/ML services ดี

**วิธี Deploy:**

#### ใช้ Google Cloud Run (Serverless)
```bash
# 1. ติดตั้ง gcloud CLI
# Download จาก: https://cloud.google.com/sdk/docs/install

# 2. Login และตั้งค่า project
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]

# 3. Build และ deploy
gcloud builds submit --tag gcr.io/[YOUR_PROJECT_ID]/adgenius-ai
gcloud run deploy adgenius-ai \
  --image gcr.io/[YOUR_PROJECT_ID]/adgenius-ai \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars "MONGODB_URI=[YOUR_MONGODB_URI]" \
  --memory 2Gi \
  --cpu 2
```

**ค่าใช้จ่ายโดยประมาณ:**
- Cloud Run: ~$10-30/เดือน (ตาม usage)
- MongoDB Atlas M10: ~$57/เดือน
- **รวม: ~$67-87/เดือน**

---

### 3. **Microsoft Azure** 

**ข้อดี:**
- Free Credit $200 สำหรับผู้ใช้ใหม่
- Azure App Service ใช้งานง่าย
- Support ดีเยี่ยม

**วิธี Deploy:**

```bash
# 1. ติดตั้ง Azure CLI
# Download จาก: https://docs.microsoft.com/cli/azure/install-azure-cli

# 2. Login
az login

# 3. สร้าง resource group
az group create --name adgenius-rg --location southeastasia

# 4. สร้าง App Service plan
az appservice plan create --name adgenius-plan --resource-group adgenius-rg --is-linux --sku B1

# 5. สร้าง Web App และ deploy
az webapp create --resource-group adgenius-rg --plan adgenius-plan --name adgenius-ai --deployment-container-image-name [your-dockerhub]/adgenius-ai:latest

# 6. ตั้งค่า environment variables
az webapp config appsettings set --resource-group adgenius-rg --name adgenius-ai --settings MONGODB_URI=[YOUR_MONGODB_URI]
```

**ค่าใช้จ่ายโดยประมาณ:**
- Basic B1 App Service: ~$13/เดือน
- MongoDB Atlas: ~$57/เดือน
- **รวม: ~$70/เดือน**

---

### 4. **DigitalOcean** ⭐ ราคาถูก แนะนำสำหรับ Startup

**ข้อดี:**
- ราคาถูกสุด
- ใช้งานง่าย
- มี App Platform และ Kubernetes

**วิธี Deploy:**

#### A. ใช้ DigitalOcean App Platform (แนะนำ)
```bash
# 1. สร้างบัญชี DigitalOcean
# https://www.digitalocean.com/

# 2. Install doctl CLI
# Download จาก: https://docs.digitalocean.com/reference/doctl/how-to/install/

# 3. Authenticate
doctl auth init

# 4. สร้าง app spec file (app.yaml)
# Deploy ผ่าน Web Console หรือ CLI
doctl apps create --spec app.yaml
```

**app.yaml:**
```yaml
name: adgenius-ai
services:
- name: backend
  github:
    repo: [your-github-username]/adgenius-ai
    branch: main
    deploy_on_push: true
  dockerfile_path: Dockerfile
  http_port: 5000
  instance_count: 1
  instance_size_slug: basic-xs
  routes:
  - path: /
  envs:
  - key: MONGODB_URI
    value: ${MONGODB_URI}
  - key: SECRET_KEY
    value: ${SECRET_KEY}
databases:
- name: mongodb
  engine: MONGODB
  version: "6"
```

**ค่าใช้จ่ายโดยประมาณ:**
- Basic Droplet: ~$12/เดือน
- Managed MongoDB: ~$15/เดือน (หรือใช้ MongoDB Atlas)
- **รวม: ~$27-69/เดือน** (ถูกสุด!)

---

### 5. **Heroku** (ง่ายที่สุดสำหรับผู้เริ่มต้น)

**ข้อดี:**
- Deploy ง่ายมาก
- Free tier (จำกัด)
- เหมาะสำหรับ testing

**วิธี Deploy:**

```bash
# 1. ติดตั้ง Heroku CLI
# Download จาก: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. สร้าง app
heroku create adgenius-ai

# 4. Add MongoDB
heroku addons:create mongolab:sandbox

# 5. ตั้งค่า environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-api-key

# 6. Deploy
git push heroku main

# 7. เปิด app
heroku open
```

**ค่าใช้จ่ายโดยประมาณ:**
- Hobby Dyno: $7/เดือน
- MongoDB (mLab): $15-20/เดือน (หรือใช้ Atlas free)
- **รวม: ~$7-27/เดือน** (ถูกสุดสำหรับเริ่มต้น)

---

## 🗄️ Database Options (MongoDB)

### 1. **MongoDB Atlas** ⭐ แนะนำสูงสุด
- Free tier (512MB storage)
- Managed service
- Auto-scaling
- Backup อัตโนมัติ

**ลงทะเบียน:**
1. ไปที่ https://www.mongodb.com/cloud/atlas/register
2. สร้าง Free Cluster
3. เลือก region: Singapore (ap-southeast-1)
4. ดึง Connection String มาใส่ใน environment variables

### 2. **MongoDB บน Docker** (สำหรับ dev)
```bash
docker-compose up mongodb
```

---

## 📊 เปรียบเทียบราคา

| Platform | ราคา/เดือน | ความง่าย | Scalability | แนะนำสำหรับ |
|----------|-----------|----------|-------------|-------------|
| **DigitalOcean App Platform** | $27-69 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Startup, SME |
| **Heroku** | $7-27 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Testing, POC |
| **Google Cloud Run** | $67-87 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Production, Scale |
| **Azure App Service** | $70 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Enterprise |
| **AWS Elastic Beanstalk** | $88 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise |

---

## 🎯 คำแนะนำตามขนาดธุรกิจ

### 🌱 Startup / ทดลองใช้งาน
**แนะนำ: Heroku หรือ DigitalOcean**
- ต้นทุนต่ำ ($7-27/เดือน)
- Deploy ง่าย
- เหมาะสำหรับ MVP

### 🏢 SME / ธุรกิจขนาดกลาง
**แนะนำ: DigitalOcean App Platform**
- ราคาเหมาะสม ($27-69/เดือน)
- Performance ดี
- Scale ได้ตามต้องการ

### 🏭 Enterprise / ธุรกิจขนาดใหญ่
**แนะนำ: AWS หรือ Google Cloud**
- Infrastructure ครบวงจร
- Security สูง
- Support ระดับ enterprise
- Auto-scaling

---

## 🔧 ขั้นตอนการ Deploy แบบทั่วไป

### 1. เตรียม Environment Variables
```bash
# คัดลอก .env.example ไปเป็น .env
cp .env.example .env

# แก้ไขค่าตัวแปรใน .env
# - ใส่ API keys จริง
# - ใส่ MongoDB URI จริง
# - เปลี่ยน SECRET_KEY เป็นค่าที่ซับซ้อน
```

### 2. ทดสอบก่อน Deploy
```bash
# ทดสอบด้วย Docker locally
docker-compose up

# ตรวจสอบว่าระบบทำงานได้
curl http://localhost:5000/health
```

### 3. Deploy
เลือกวิธี deploy ตามแพลตฟอร์มที่เลือก (ดูข้างบน)

### 4. ตั้งค่า Domain Name (Optional)
```bash
# ซื้อ domain จาก Namecheap, GoDaddy, หรือ Cloudflare
# ตั้งค่า DNS ชี้ไปที่ server ของคุณ
# ติดตั้ง SSL certificate (Let's Encrypt)
```

---

## 🔒 Security Checklist

- [ ] เปลี่ยน SECRET_KEY และ JWT_SECRET_KEY
- [ ] ตั้งค่า CORS_ORIGINS ให้ถูกต้อง
- [ ] ใช้ HTTPS (SSL/TLS)
- [ ] ตั้งค่า rate limiting
- [ ] Backup database อัตโนมัติ
- [ ] ตั้งค่า monitoring และ alerting
- [ ] ซ่อน error messages ใน production
- [ ] ใช้ environment variables สำหรับ sensitive data

---

## 📞 Support

หากมีปัญหาในการ deploy:
1. ตรวจสอบ logs: `docker-compose logs` หรือ logs ของ platform
2. อ่าน documentation ของแต่ละ platform
3. ตรวจสอบ GitHub Issues

---

## 🎓 แนะนำเพิ่มเติม

### สำหรับผู้เริ่มต้น
1. เริ่มจาก **Heroku** (ง่ายสุด, มี free tier)
2. ใช้ **MongoDB Atlas Free Tier**
3. ทดสอบระบบก่อน scale

### เมื่อมีผู้ใช้เพิ่มขึ้น
1. ย้ายไป **DigitalOcean** หรือ **Google Cloud Run**
2. Upgrade MongoDB Atlas
3. เพิ่ม CDN สำหรับ static files
4. ตั้งค่า auto-scaling

### Production-Ready
1. ใช้ **AWS** หรือ **Google Cloud** 
2. ตั้งค่า CI/CD pipeline
3. ใช้ multiple environments (dev, staging, production)
4. ตั้งค่า monitoring (Datadog, New Relic, Sentry)
5. Backup และ disaster recovery plan

---

**สรุป:** สำหรับโปรเจกต์นี้ แนะนำให้เริ่มจาก **Heroku** หรือ **DigitalOcean App Platform** เพราะ deploy ง่าย ราคาถูก และเหมาะสำหรับการเริ่มต้น 🚀
