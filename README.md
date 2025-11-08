# AdGenius AI - ระบบหลังบ้าน

ระบบหลังบ้านสำหรับแพลตฟอร์ม AdGenius AI ที่ช่วยในการยิงโฆษณาแบบครบวงจรบนหลายแพลตฟอร์ม (Facebook, Instagram, TikTok, Shopee) โดยใช้เทคโนโลยี AI

## โครงสร้างของระบบ

ระบบหลังบ้านของ AdGenius AI ประกอบด้วยส่วนต่างๆ ดังนี้:

1. **Core API Service** - บริการหลักที่จัดการการร้องขอจากส่วนหน้า (Frontend) และประสานงานกับบริการอื่นๆ
2. **Platform Connectors** - โมดูลที่เชื่อมต่อกับ API ของแพลตฟอร์มต่างๆ (Facebook, Instagram, TikTok, Shopee)
3. **AI Modules** - โมดูล AI สำหรับการกำหนดกลุ่มเป้าหมาย, การสร้างสรรค์โฆษณา, และการเพิ่มประสิทธิภาพแคมเปญ
4. **Database** - ฐานข้อมูลสำหรับเก็บข้อมูลผู้ใช้, แคมเปญ, และข้อมูลอื่นๆ
5. **Authentication Service** - บริการสำหรับการยืนยันตัวตนและการจัดการสิทธิ์

## เทคโนโลยีที่ใช้

- **Backend Framework**: Flask (Python)
- **Database**: MongoDB
- **AI/ML**: TensorFlow, scikit-learn, OpenAI API
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI
- **Testing**: pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## การติดตั้งและการใช้งาน

### ความต้องการของระบบ

- Python 3.8+
- MongoDB
- Docker (optional)

### การติดตั้ง

1. โคลนโปรเจค:
   ```
   git clone https://github.com/yourusername/adgenius-ai-backend.git
   cd adgenius-ai-backend
   ```

2. สร้าง virtual environment และติดตั้ง dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # สำหรับ Linux/Mac
   # หรือ
   venv\Scripts\activate  # สำหรับ Windows
   pip install -r requirements.txt
   ```

3. ตั้งค่าตัวแปรสภาพแวดล้อม:
   ```
   cp .env.example .env
   # แก้ไขไฟล์ .env ตามการตั้งค่าของคุณ
   ```

4. รันเซิร์ฟเวอร์:
   ```
   python run.py
   ```

### การใช้งานกับ Docker

1. สร้าง Docker image:
   ```
   docker build -t adgenius-ai-backend .
   ```

2. รัน Docker container:
   ```
   docker run -p 5000:5000 -d adgenius-ai-backend
   ```

## API Endpoints

API documentation จะสามารถเข้าถึงได้ที่ `http://localhost:5000/api/docs` หลังจากรันเซิร์ฟเวอร์

## การทดสอบ

รันการทดสอบด้วยคำสั่ง:
```
pytest
```

## การใช้งานกับธุรกิจลิปสติก

ระบบนี้สามารถปรับแต่งให้เหมาะกับธุรกิจลิปสติกได้โดย:

1. การกำหนดกลุ่มเป้าหมายที่เหมาะสมสำหรับผลิตภัณฑ์ลิปสติก
2. การสร้างสรรค์โฆษณาที่เน้นคุณสมบัติของลิปสติก (สี, เนื้อ, ความติดทน, ส่วนผสม)
3. การวิเคราะห์เทรนด์และคู่แข่งในตลาดลิปสติก
4. การปรับแต่งแคมเปญให้เหมาะกับช่วงเวลาและเทศกาลต่างๆ

## License

MIT License
