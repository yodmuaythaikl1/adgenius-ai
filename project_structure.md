# โครงสร้างโปรเจค AdGenius AI Backend

```
adgenius_ai_backend/
├── app/
│   ├── __init__.py                 # Initialize Flask application
│   ├── config.py                   # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               # API routes
│   │   ├── auth.py                 # Authentication endpoints
│   │   ├── campaigns.py            # Campaign management endpoints
│   │   ├── analytics.py            # Analytics endpoints
│   │   └── users.py                # User management endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── campaign.py             # Campaign model
│   │   ├── ad.py                   # Advertisement model
│   │   └── analytics.py            # Analytics model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Authentication service
│   │   ├── campaign_service.py     # Campaign management service
│   │   ├── analytics_service.py    # Analytics service
│   │   └── user_service.py         # User management service
│   ├── platform_connectors/
│   │   ├── __init__.py
│   │   ├── facebook_connector.py   # Facebook API connector
│   │   ├── instagram_connector.py  # Instagram API connector
│   │   ├── tiktok_connector.py     # TikTok API connector
│   │   └── shopee_connector.py     # Shopee API connector
│   ├── ai_modules/
│   │   ├── __init__.py
│   │   ├── targeting.py            # AI for audience targeting
│   │   ├── creative.py             # AI for creative generation
│   │   └── optimization.py         # AI for campaign optimization
│   └── utils/
│       ├── __init__.py
│       ├── validators.py           # Input validation utilities
│       ├── helpers.py              # Helper functions
│       └── logger.py               # Logging utilities
├── tests/
│   ├── __init__.py
│   ├── test_api.py                 # API tests
│   ├── test_models.py              # Model tests
│   ├── test_services.py            # Service tests
│   ├── test_platform_connectors.py # Platform connector tests
│   └── test_ai_modules.py          # AI module tests
├── migrations/                     # Database migrations
├── logs/                           # Log files
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
├── run.py                          # Application entry point
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
└── README.md                       # Project documentation
```

## คำอธิบายโครงสร้าง

### app/

โฟลเดอร์หลักที่มีโค้ดของแอปพลิเคชัน

- **__init__.py**: สร้าง Flask application และกำหนดค่าเริ่มต้น
- **config.py**: การตั้งค่าต่างๆ ของแอปพลิเคชัน

### app/api/

โมดูลที่จัดการ API endpoints

- **routes.py**: กำหนด API routes หลัก
- **auth.py**: endpoints สำหรับการยืนยันตัวตน (login, register, etc.)
- **campaigns.py**: endpoints สำหรับการจัดการแคมเปญ
- **analytics.py**: endpoints สำหรับการวิเคราะห์ข้อมูล
- **users.py**: endpoints สำหรับการจัดการผู้ใช้

### app/models/

โมดูลที่กำหนดโครงสร้างข้อมูล

- **user.py**: โมเดลผู้ใช้
- **campaign.py**: โมเดลแคมเปญ
- **ad.py**: โมเดลโฆษณา
- **analytics.py**: โมเดลข้อมูลวิเคราะห์

### app/services/

โมดูลที่มีตรรกะทางธุรกิจ

- **auth_service.py**: บริการสำหรับการยืนยันตัวตน
- **campaign_service.py**: บริการสำหรับการจัดการแคมเปญ
- **analytics_service.py**: บริการสำหรับการวิเคราะห์ข้อมูล
- **user_service.py**: บริการสำหรับการจัดการผู้ใช้

### app/platform_connectors/

โมดูลที่เชื่อมต่อกับ API ของแพลตฟอร์มต่างๆ

- **facebook_connector.py**: เชื่อมต่อกับ Facebook API
- **instagram_connector.py**: เชื่อมต่อกับ Instagram API
- **tiktok_connector.py**: เชื่อมต่อกับ TikTok API
- **shopee_connector.py**: เชื่อมต่อกับ Shopee API

### app/ai_modules/

โมดูลที่มีตรรกะ AI

- **targeting.py**: AI สำหรับการกำหนดกลุ่มเป้าหมาย
- **creative.py**: AI สำหรับการสร้างสรรค์โฆษณา
- **optimization.py**: AI สำหรับการเพิ่มประสิทธิภาพแคมเปญ

### app/utils/

โมดูลที่มีฟังก์ชันช่วยเหลือ

- **validators.py**: ฟังก์ชันสำหรับการตรวจสอบข้อมูลนำเข้า
- **helpers.py**: ฟังก์ชันช่วยเหลือทั่วไป
- **logger.py**: ฟังก์ชันสำหรับการบันทึกล็อก

### tests/

โฟลเดอร์ที่มีการทดสอบ

- **test_api.py**: การทดสอบ API
- **test_models.py**: การทดสอบโมเดล
- **test_services.py**: การทดสอบบริการ
- **test_platform_connectors.py**: การทดสอบตัวเชื่อมต่อแพลตฟอร์ม
- **test_ai_modules.py**: การทดสอบโมดูล AI

### ไฟล์อื่นๆ

- **migrations/**: โฟลเดอร์สำหรับการอัปเดตฐานข้อมูล
- **logs/**: โฟลเดอร์สำหรับไฟล์ล็อก
- **.env.example**: ตัวอย่างไฟล์สำหรับตัวแปรสภาพแวดล้อม
- **.gitignore**: ไฟล์ที่กำหนดไฟล์และโฟลเดอร์ที่ git ควรละเว้น
- **requirements.txt**: รายการ dependencies ของ Python
- **run.py**: จุดเริ่มต้นของแอปพลิเคชัน
- **Dockerfile**: การตั้งค่าสำหรับ Docker
- **docker-compose.yml**: การตั้งค่าสำหรับ Docker Compose
- **README.md**: เอกสารโปรเจค
