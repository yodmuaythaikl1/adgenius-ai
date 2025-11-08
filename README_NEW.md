# 🎯 AdGenius AI - แพลตฟอร์ม AI สำหรับการยิงโฆษณาแบบครบวงจร

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> แพลตฟอร์มที่ใช้ AI ในการจัดการโฆษณาบน Facebook, Instagram, TikTok และ Shopee อย่างอัจฉริยะ

---

## ✨ Features หลัก

### 🤖 AI-Powered Features
- **Intelligent Audience Targeting** - กำหนดกลุ่มเป้าหมายอัจฉริยะด้วย Machine Learning
- **Creative Generation** - สร้างโฆษณา (ข้อความ, รูปภาพ, วิดีโอ) ด้วย Generative AI
- **Campaign Optimization** - ปรับปรุงประสิทธิภาพแคมเปญแบบอัตโนมัติ
- **Predictive Analytics** - วิเคราะห์และคาดการณ์ผลลัพธ์

### 🌐 Multi-Platform Support
- ✅ Facebook Ads
- ✅ Instagram Ads
- ✅ TikTok Ads
- ✅ Shopee Ads

### 📊 Advanced Analytics
- Real-time performance tracking
- ROI และ ROAS analysis
- A/B testing insights
- Demographic insights

---

## 🚀 Quick Start

### ⚡ Deploy ทันที (5 นาที)

**Option 1: Heroku (แนะนำสำหรับผู้เริ่มต้น)**

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

หรือ:
```bash
heroku create adgenius-ai-[your-name]
heroku addons:create mongolab:sandbox
git push heroku main
```

**Option 2: DigitalOcean (ราคาถูก)**
- [คู่มือ Deploy DigitalOcean](./QUICK_START.md#2-deploy-บน-digitalocean)

**Option 3: Google Cloud Run (Scale ได้ดี)**
```bash
gcloud run deploy adgenius-ai --source . --region asia-southeast1
```

📖 **[อ่านคู่มือ Quick Start แบบเต็ม →](./QUICK_START.md)**

---

## 📋 ข้อกำหนดของระบบ

### สำหรับ Development
- Python 3.10+
- MongoDB 6.0+
- Redis (Optional)
- 4GB RAM ขึ้นไป

### สำหรับ Production
- Cloud Platform (AWS/GCP/Azure/DigitalOcean/Heroku)
- MongoDB Atlas (แนะนำ)
- 2GB RAM ขึ้นไป

---

## 🛠️ การติดตั้งและพัฒนา Local

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/adgenius-ai.git
cd adgenius-ai
```

### 2. สร้าง Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Environment Variables
```bash
# Copy template
cp .env.example .env

# แก้ไข .env ใส่ค่าจริง
# - MONGODB_URI
# - SECRET_KEY
# - OPENAI_API_KEY
# - Facebook/TikTok/Shopee API Keys
```

### 5. รัน Application
```bash
python run.py
```

เปิดเบราว์เซอร์: http://localhost:5000

---

## 🐳 รันด้วย Docker

### Quick Start
```bash
# Build และ run
docker-compose up

# เข้าใช้งาน
open http://localhost:5000
```

### Production Mode
```bash
docker-compose --profile production up
```

---

## 📁 โครงสร้างโปรเจกต์

```
adgenius-ai/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── api/                    # API endpoints
│   │   ├── auth.py
│   │   ├── campaigns.py
│   │   ├── analytics.py
│   │   └── users.py
│   ├── models/                 # Database models
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── ad.py
│   │   └── analytics.py
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── campaign_service.py
│   │   └── analytics_service.py
│   ├── platform_connectors/    # API integrations
│   │   ├── facebook_connector.py
│   │   ├── instagram_connector.py
│   │   ├── tiktok_connector.py
│   │   └── shopee_connector.py
│   ├── ai_modules/             # AI/ML modules
│   │   ├── audience_targeting.py
│   │   ├── creative_generation.py
│   │   └── campaign_optimization.py
│   └── utils/                  # Utilities
│       ├── validators.py
│       ├── helpers.py
│       └── logger.py
├── tests/                      # Test files
├── docs/                       # Documentation
├── static/                     # Static files
├── logs/                       # Log files
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

---

## 🧪 การทดสอบ

```bash
# รัน unit tests
pytest

# รัน tests พร้อม coverage
pytest --cov=app --cov-report=html

# รัน specific test
pytest tests/test_campaigns.py
```

---

## 📚 เอกสารประกอบ

### คู่มือการใช้งาน
- 📖 [Quick Start Guide](./QUICK_START.md) - เริ่มต้นใช้งานอย่างรวดเร็ว
- 🚀 [Deployment Guide](./DEPLOYMENT_GUIDE.md) - คู่มือ Deploy แบบละเอียด
- 🔧 [Installation Guide](./คู่มือการติดตั้งแพลตฟอร์ม%20AdGenius%20AI.md) - คู่มือติดตั้งภาษาไทย
- 📊 [API Documentation](./static/API_DOCS.md) - เอกสาร API

### คู่มือธุรกิจ
- 🥊 [Muay Thai Gym Business Guide](./คู่มือการใช้งาน%20AdGenius%20AI%20สำหรับธุรกิจค่ายมวยไทย.md)
- 📈 [Advertising Strategy](./กลยุทธ์การโฆษณาสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย.md)

### Technical Documentation
- 🏗️ [Architecture](./สถาปัตยกรรมแพลตฟอร์ม%20AI%20สำหรับการยิงโฆษณาแบบครบวงจร.md)
- 🤖 [AI Modules](./phase3_core_ai_modules_concept_and_technology.md)
- 🔌 [API Integration](./phase4_facebook_instagram_api_integration.md)

---

## 🔑 API Keys ที่จำเป็น

### 1. MongoDB Atlas (ฟรี 512MB)
```
https://www.mongodb.com/cloud/atlas/register
```

### 2. OpenAI API (สำหรับ AI Features)
```
https://platform.openai.com/api-keys
```

### 3. Facebook & Instagram
```
https://developers.facebook.com/
```

### 4. TikTok for Business
```
https://ads.tiktok.com/marketing_api/
```

### 5. Shopee Open Platform
```
https://open.shopee.com/
```

---

## 💰 ประมาณการค่าใช้จ่าย

| Platform | ราคา/เดือน | เหมาะสำหรับ |
|----------|-----------|------------|
| **Heroku** | $7-27 | 🧪 ทดลอง, POC |
| **DigitalOcean** | $27-69 | 🚀 Startup, SME |
| **Google Cloud** | $67-87 | 📈 Scale, Growth |
| **AWS/Azure** | $88+ | 🏢 Enterprise |

💡 **แนะนำ:** เริ่มจาก Heroku → ย้ายไป DigitalOcean → Scale ด้วย GCP/AWS

---

## 🤝 Contributing

เรายินดีรับ contributions! โปรด:

1. Fork โปรเจกต์
2. สร้าง feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

---

## 📝 License

โปรเจกต์นี้อยู่ภายใต้ [MIT License](LICENSE)

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- OpenAI สำหรับ GPT API
- Meta สำหรับ Marketing API
- TikTok สำหรับ Business API
- Shopee สำหรับ Open Platform
- MongoDB Atlas สำหรับ database hosting

---

## 📞 Support

- 📧 Email: support@adgenius.ai
- 💬 GitHub Issues: [Create an issue](https://github.com/yourusername/adgenius-ai/issues)
- 📖 Documentation: [Full Docs](./docs/)

---

## 🗺️ Roadmap

### Q1 2025
- [x] Core API Development
- [x] Facebook/Instagram Integration
- [x] TikTok Integration
- [x] Shopee Integration
- [x] Basic AI Features

### Q2 2025
- [ ] Advanced AI Features
- [ ] React Frontend
- [ ] Mobile App (React Native)
- [ ] Multi-language Support
- [ ] Advanced Analytics Dashboard

### Q3 2025
- [ ] Line Ads Integration
- [ ] Google Ads Integration
- [ ] Automated Reporting
- [ ] White-label Solution
- [ ] API for Partners

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/adgenius-ai&type=Date)](https://star-history.com/#yourusername/adgenius-ai&Date)

---

<div align="center">

**Made with ❤️ for Digital Marketers**

[Website](https://adgenius.ai) • [Documentation](./docs/) • [Report Bug](https://github.com/yourusername/adgenius-ai/issues) • [Request Feature](https://github.com/yourusername/adgenius-ai/issues)

</div>
