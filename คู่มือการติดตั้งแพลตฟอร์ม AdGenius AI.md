# คู่มือการติดตั้งแพลตฟอร์ม AdGenius AI

## สารบัญ
1. [บทนำ](#บทนำ)
2. [ความต้องการของระบบ](#ความต้องการของระบบ)
3. [การติดตั้งระบบ](#การติดตั้งระบบ)
   - [การติดตั้งแบบ Local](#การติดตั้งแบบ-local)
   - [การติดตั้งแบบ Cloud](#การติดตั้งแบบ-cloud)
4. [การตั้งค่า API Key](#การตั้งค่า-api-key)
5. [การเริ่มต้นใช้งานระบบ](#การเริ่มต้นใช้งานระบบ)
6. [การอัปเดตระบบ](#การอัปเดตระบบ)
7. [การแก้ไขปัญหา](#การแก้ไขปัญหา)
8. [การติดต่อสนับสนุน](#การติดต่อสนับสนุน)

## บทนำ

คู่มือนี้จะแนะนำวิธีการติดตั้งแพลตฟอร์ม AdGenius AI ซึ่งเป็นแพลตฟอร์ม AI สำหรับการยิงโฆษณาแบบครบวงจรที่สามารถรองรับ Facebook, Instagram, TikTok และ Shopee เพื่อให้ผู้ขายสามารถเข้าถึงกลุ่มเป้าหมายได้อย่างแม่นยำ

## ความต้องการของระบบ

### ฮาร์ดแวร์
- CPU: 2 คอร์ขึ้นไป
- RAM: 4GB ขึ้นไป
- พื้นที่ว่าง: 10GB ขึ้นไป

### ซอฟต์แวร์
- ระบบปฏิบัติการ: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- Python 3.8 หรือสูงกว่า
- Node.js 14 หรือสูงกว่า
- MongoDB 4.4 หรือสูงกว่า
- Git

## การติดตั้งระบบ

### การติดตั้งแบบ Local

#### 1. ติดตั้ง Python, Node.js, และ MongoDB

**สำหรับ Windows:**

1. ดาวน์โหลดและติดตั้ง Python จาก [python.org](https://www.python.org/downloads/)
2. ดาวน์โหลดและติดตั้ง Node.js จาก [nodejs.org](https://nodejs.org/)
3. ดาวน์โหลดและติดตั้ง MongoDB จาก [mongodb.com](https://www.mongodb.com/try/download/community)

**สำหรับ macOS:**

```bash
# ติดตั้ง Homebrew (ถ้ายังไม่มี)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# ติดตั้ง Python
brew install python

# ติดตั้ง Node.js
brew install node

# ติดตั้ง MongoDB
brew tap mongodb/brew
brew install mongodb-community
```

**สำหรับ Ubuntu:**

```bash
# อัปเดตแพ็คเกจ
sudo apt update

# ติดตั้ง Python
sudo apt install python3 python3-pip

# ติดตั้ง Node.js
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs

# ติดตั้ง MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### 2. โคลนโปรเจค

```bash
# โคลนโปรเจค
git clone https://github.com/adgenius-ai/adgenius-platform.git

# เข้าไปยังไดเรกทอรีของโปรเจค
cd adgenius-platform
```

#### 3. ติดตั้งแพ็คเกจที่จำเป็นสำหรับ Backend

```bash
# สร้าง virtual environment (แนะนำ)
python -m venv venv

# เปิดใช้งาน virtual environment
# สำหรับ Windows
venv\Scripts\activate
# สำหรับ macOS/Linux
source venv/bin/activate

# ติดตั้งแพ็คเกจที่จำเป็น
pip install -r requirements.txt
```

#### 4. ติดตั้งแพ็คเกจที่จำเป็นสำหรับ Frontend

```bash
# เข้าไปยังไดเรกทอรีของ Frontend
cd frontend

# ติดตั้งแพ็คเกจที่จำเป็น
npm install

# กลับไปยังไดเรกทอรีหลัก
cd ..
```

#### 5. ตั้งค่าไฟล์ .env

สร้างไฟล์ .env ในไดเรกทอรีหลักของโปรเจคและกำหนดค่าต่อไปนี้:

```
# การตั้งค่าฐานข้อมูล
MONGODB_URI=mongodb://localhost:27017/adgenius

# การตั้งค่า API Key
FACEBOOK_API_KEY=your_facebook_api_key
INSTAGRAM_API_KEY=your_instagram_api_key
TIKTOK_API_KEY=your_tiktok_api_key
SHOPEE_API_KEY=your_shopee_api_key
OPENAI_API_KEY=your_openai_api_key

# การตั้งค่าอื่นๆ
JWT_SECRET=your_jwt_secret
PORT=5000
```

### การติดตั้งแบบ Cloud

#### 1. การติดตั้งบน AWS

1. สร้าง EC2 Instance (แนะนำ t2.medium หรือสูงกว่า)
2. เชื่อมต่อกับ EC2 Instance ผ่าน SSH
3. ติดตั้ง Python, Node.js, และ MongoDB ตามขั้นตอนสำหรับ Ubuntu ด้านบน
4. โคลนโปรเจคและติดตั้งแพ็คเกจที่จำเป็นตามขั้นตอนด้านบน
5. ตั้งค่าไฟล์ .env
6. ตั้งค่า Security Group เพื่อเปิดพอร์ต 5000 (Backend) และ 3000 (Frontend)

#### 2. การติดตั้งบน Google Cloud Platform

1. สร้าง VM Instance (แนะนำ e2-medium หรือสูงกว่า)
2. เชื่อมต่อกับ VM Instance ผ่าน SSH
3. ติดตั้ง Python, Node.js, และ MongoDB ตามขั้นตอนสำหรับ Ubuntu ด้านบน
4. โคลนโปรเจคและติดตั้งแพ็คเกจที่จำเป็นตามขั้นตอนด้านบน
5. ตั้งค่าไฟล์ .env
6. ตั้งค่า Firewall Rules เพื่อเปิดพอร์ต 5000 (Backend) และ 3000 (Frontend)

#### 3. การติดตั้งบน Microsoft Azure

1. สร้าง Virtual Machine (แนะนำ Standard_B2s หรือสูงกว่า)
2. เชื่อมต่อกับ Virtual Machine ผ่าน SSH
3. ติดตั้ง Python, Node.js, และ MongoDB ตามขั้นตอนสำหรับ Ubuntu ด้านบน
4. โคลนโปรเจคและติดตั้งแพ็คเกจที่จำเป็นตามขั้นตอนด้านบน
5. ตั้งค่าไฟล์ .env
6. ตั้งค่า Network Security Group เพื่อเปิดพอร์ต 5000 (Backend) และ 3000 (Frontend)

## การตั้งค่า API Key

### Facebook และ Instagram API Key

1. ไปที่ [Facebook for Developers](https://developers.facebook.com/)
2. สร้างแอปพลิเคชันใหม่
3. เพิ่มผลิตภัณฑ์ "Marketing API"
4. รับ API Key และเพิ่มลงในไฟล์ .env

### TikTok API Key

1. ไปที่ [TikTok for Developers](https://developers.tiktok.com/)
2. สร้างแอปพลิเคชันใหม่
3. เพิ่มผลิตภัณฑ์ "TikTok Ads API"
4. รับ API Key และเพิ่มลงในไฟล์ .env

### Shopee API Key

1. ไปที่ [Shopee Open Platform](https://open.shopee.com/)
2. สร้างแอปพลิเคชันใหม่
3. รับ API Key และเพิ่มลงในไฟล์ .env

### OpenAI API Key

1. ไปที่ [OpenAI Platform](https://platform.openai.com/)
2. สร้างบัญชีหรือเข้าสู่ระบบ
3. ไปที่ "API Keys" และสร้าง API Key ใหม่
4. เพิ่ม API Key ลงในไฟล์ .env

## การเริ่มต้นใช้งานระบบ

### การเริ่มต้น Backend

```bash
# เปิดใช้งาน virtual environment (ถ้าใช้)
# สำหรับ Windows
venv\Scripts\activate
# สำหรับ macOS/Linux
source venv/bin/activate

# เริ่มต้น Backend
python run.py
```

Backend จะทำงานที่ http://localhost:5000

### การเริ่มต้น Frontend

```bash
# เข้าไปยังไดเรกทอรีของ Frontend
cd frontend

# เริ่มต้น Frontend
npm start
```

Frontend จะทำงานที่ http://localhost:3000

### การเริ่มต้นระบบแบบ Production

สำหรับการใช้งานในสภาพแวดล้อมการผลิต (Production) แนะนำให้ใช้ PM2 เพื่อจัดการกระบวนการ:

```bash
# ติดตั้ง PM2
npm install -g pm2

# เริ่มต้น Backend
pm2 start run.py --name adgenius-backend --interpreter python

# เริ่มต้น Frontend
cd frontend
pm2 start npm --name adgenius-frontend -- start

# ตรวจสอบสถานะ
pm2 status

# ตั้งค่าให้เริ่มต้นอัตโนมัติเมื่อระบบเริ่มทำงาน
pm2 startup
pm2 save
```

## การอัปเดตระบบ

### การอัปเดตจาก GitHub

```bash
# เข้าไปยังไดเรกทอรีของโปรเจค
cd adgenius-platform

# ดึงการเปลี่ยนแปลงล่าสุดจาก GitHub
git pull

# อัปเดตแพ็คเกจ Backend
pip install -r requirements.txt

# อัปเดตแพ็คเกจ Frontend
cd frontend
npm install
cd ..

# รีสตาร์ทระบบ (ถ้าใช้ PM2)
pm2 restart all
```

### การอัปเดตแบบ Manual

1. สำรองไฟล์ .env และข้อมูลสำคัญอื่นๆ
2. ลบไดเรกทอรีของโปรเจคเดิม
3. โคลนโปรเจคใหม่จาก GitHub
4. ติดตั้งแพ็คเกจที่จำเป็นตามขั้นตอนด้านบน
5. คืนค่าไฟล์ .env และข้อมูลสำคัญอื่นๆ
6. เริ่มต้นระบบใหม่

## การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อกับฐานข้อมูล

**ปัญหา**: ไม่สามารถเชื่อมต่อกับฐานข้อมูล MongoDB ได้

**วิธีแก้ไข**:
1. ตรวจสอบว่า MongoDB กำลังทำงานอยู่:
   ```bash
   # สำหรับ Windows
   sc query mongodb
   # สำหรับ macOS
   brew services list
   # สำหรับ Ubuntu
   sudo systemctl status mongod
   ```
2. ตรวจสอบ URI ของ MongoDB ในไฟล์ .env
3. ตรวจสอบว่าพอร์ต 27017 เปิดอยู่:
   ```bash
   # สำหรับ Windows
   netstat -an | findstr 27017
   # สำหรับ macOS/Linux
   netstat -an | grep 27017
   ```

### ปัญหาการเริ่มต้น Backend

**ปัญหา**: ไม่สามารถเริ่มต้น Backend ได้

**วิธีแก้ไข**:
1. ตรวจสอบว่าได้ติดตั้งแพ็คเกจที่จำเป็นทั้งหมดแล้ว:
   ```bash
   pip install -r requirements.txt
   ```
2. ตรวจสอบว่าไฟล์ .env มีการตั้งค่าที่ถูกต้อง
3. ตรวจสอบล็อกเพื่อดูข้อผิดพลาด:
   ```bash
   python run.py
   ```

### ปัญหาการเริ่มต้น Frontend

**ปัญหา**: ไม่สามารถเริ่มต้น Frontend ได้

**วิธีแก้ไข**:
1. ตรวจสอบว่าได้ติดตั้งแพ็คเกจที่จำเป็นทั้งหมดแล้ว:
   ```bash
   cd frontend
   npm install
   ```
2. ตรวจสอบว่าพอร์ต 3000 ไม่ได้ถูกใช้งานโดยแอปพลิเคชันอื่น:
   ```bash
   # สำหรับ Windows
   netstat -an | findstr 3000
   # สำหรับ macOS/Linux
   netstat -an | grep 3000
   ```
3. ลองเริ่มต้น Frontend ด้วยพอร์ตอื่น:
   ```bash
   cd frontend
   PORT=3001 npm start
   ```

### ปัญหาการเชื่อมต่อกับ API

**ปัญหา**: ไม่สามารถเชื่อมต่อกับ API ของแพลตฟอร์มต่างๆ ได้

**วิธีแก้ไข**:
1. ตรวจสอบว่า API Key ในไฟล์ .env ถูกต้อง
2. ตรวจสอบว่าบัญชีของคุณมีสิทธิ์ในการเข้าถึง API ที่ต้องการ
3. ตรวจสอบว่าแอปพลิเคชันของคุณได้รับการอนุมัติจากแพลตฟอร์มนั้นๆ แล้ว
4. ตรวจสอบล็อกเพื่อดูข้อผิดพลาด

## การติดต่อสนับสนุน

หากคุณมีคำถามหรือต้องการความช่วยเหลือเพิ่มเติม สามารถติดต่อทีมสนับสนุนของเราได้ที่:

- อีเมล: support@adgenius-ai.com
- โทรศัพท์: 02-123-4567
- เว็บไซต์: https://www.adgenius-ai.com/support
- GitHub Issues: https://github.com/adgenius-ai/adgenius-platform/issues

ทีมสนับสนุนของเราพร้อมให้บริการตลอด 24 ชั่วโมงทุกวัน
