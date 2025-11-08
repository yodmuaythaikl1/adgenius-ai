import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import './App.css'
import './custom.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="adgenius-app">
      <header className="app-header">
        <h1>AdGenius AI</h1>
        <p>แพลตฟอร์ม AI สำหรับการยิงโฆษณาแบบครบวงจร</p>
      </header>
      
      <main className="app-main">
        <section className="hero-section">
          <div className="hero-content">
            <h2>ยิงโฆษณาอย่างชาญฉลาดด้วย AI</h2>
            <p>เข้าถึงกลุ่มเป้าหมายได้แม่นยำ ประหยัดงบประมาณ เพิ่มยอดขาย</p>
            <Button className="cta-button">เริ่มต้นใช้งาน</Button>
          </div>
        </section>
        
        <section className="features-section">
          <h2>คุณสมบัติเด่น</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>การกำหนดกลุ่มเป้าหมายด้วย AI</h3>
              <p>ค้นหากลุ่มเป้าหมายที่เหมาะสมที่สุดสำหรับสินค้าของคุณ</p>
            </div>
            <div className="feature-card">
              <h3>การสร้างสรรค์โฆษณาด้วย AI</h3>
              <p>สร้างเนื้อหาโฆษณาที่น่าสนใจและตรงกลุ่มเป้าหมาย</p>
            </div>
            <div className="feature-card">
              <h3>การเพิ่มประสิทธิภาพแคมเปญด้วย AI</h3>
              <p>ปรับปรุงแคมเปญโฆษณาอัตโนมัติเพื่อผลลัพธ์ที่ดีที่สุด</p>
            </div>
            <div className="feature-card">
              <h3>รองรับหลายแพลตฟอร์ม</h3>
              <p>Facebook, Instagram, TikTok, และ Shopee</p>
            </div>
          </div>
        </section>
      </main>
      
      <footer className="app-footer">
        <p>© 2025 AdGenius AI. สงวนลิขสิทธิ์.</p>
      </footer>
    </div>
  )
}

export default App
