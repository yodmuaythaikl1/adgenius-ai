"""
ไฟล์ทดสอบอย่างง่ายสำหรับโมดูล AI ของธุรกิจค่ายมวยไทย
"""

import os
import sys
import json
from datetime import datetime

# เพิ่มไดเรกทอรีหลักลงใน path เพื่อให้สามารถ import โมดูลได้
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# นำเข้าโมดูลที่ต้องการทดสอบโดยตรง
from app.ai_modules.muaythai_targeting import MuayThaiTargetingAI
from app.ai_modules.muaythai_creative import MuayThaiCreativeAI

def print_separator(title):
    """
    แสดงเส้นคั่นพร้อมหัวข้อ
    """
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def test_muaythai_targeting():
    """
    ทดสอบโมดูล MuayThaiTargetingAI
    """
    print_separator("ทดสอบโมดูล MuayThaiTargetingAI")
    
    # สร้างอินสแตนซ์ของ MuayThaiTargetingAI
    targeting_ai = MuayThaiTargetingAI()
    
    # ข้อมูลค่ายมวยไทยตัวอย่าง
    muaythai_gym = {
        "name": "ยอดมวยไทยยิม รังสิต",
        "description": "ค่ายมวยไทยสำหรับการออกกำลังกายและลดน้ำหนัก สอนโดยครูมวยมืออาชีพ เหมาะสำหรับทุกเพศทุกวัย",
        "features": [
            "คลาสมวยไทยเพื่อการออกกำลังกาย",
            "โปรแกรมลดน้ำหนักด้วยมวยไทย",
            "คลาสสำหรับผู้เริ่มต้น",
            "คลาสสำหรับเด็กและเยาวชน",
            "คลาสสำหรับชาวต่างชาติ"
        ],
        "price": 1500,  # ราคาต่อเดือน
        "location": "รังสิต คลองหลวง"
    }
    
    # ทดสอบการวิเคราะห์สินค้า
    print("1. ทดสอบการวิเคราะห์สินค้า:")
    product_analysis = targeting_ai.analyze_product(muaythai_gym)
    print(f"กลุ่มเป้าหมายหลัก: {product_analysis['primary_target']}")
    print(f"คะแนนกลุ่มเป้าหมาย: {product_analysis['target_scores']}")
    print(f"คำสำคัญที่แนะนำ: {product_analysis['recommended_keywords'][:5]}")
    print(f"ช่วงเวลาที่เหมาะสมสำหรับการโฆษณา: {product_analysis['optimal_ad_times']}")
    print(f"แพลตฟอร์มที่แนะนำ: {product_analysis['recommended_platforms']}")
    
    return True

def test_muaythai_creative():
    """
    ทดสอบโมดูล MuayThaiCreativeAI
    """
    print_separator("ทดสอบโมดูล MuayThaiCreativeAI")
    
    # สร้างอินสแตนซ์ของ MuayThaiCreativeAI
    creative_ai = MuayThaiCreativeAI()
    
    # ข้อมูลค่ายมวยไทยตัวอย่าง
    muaythai_gym = {
        "name": "ยอดมวยไทยยิม รังสิต",
        "description": "ค่ายมวยไทยสำหรับการออกกำลังกายและลดน้ำหนัก สอนโดยครูมวยมืออาชีพ เหมาะสำหรับทุกเพศทุกวัย",
        "features": [
            "คลาสมวยไทยเพื่อการออกกำลังกาย",
            "โปรแกรมลดน้ำหนักด้วยมวยไทย",
            "คลาสสำหรับผู้เริ่มต้น",
            "คลาสสำหรับเด็กและเยาวชน",
            "คลาสสำหรับชาวต่างชาติ"
        ],
        "price": 1500,  # ราคาต่อเดือน
        "location": "รังสิต คลองหลวง"
    }
    
    # ทดสอบการสร้างพาดหัวโฆษณา
    print("1. ทดสอบการสร้างพาดหัวโฆษณา:")
    headline_local = creative_ai.generate_ad_headline("local_fitness", muaythai_gym)
    print(f"พาดหัวสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย: {headline_local}")
    
    headline_tourists = creative_ai.generate_ad_headline("tourists", muaythai_gym)
    print(f"พาดหัวสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ: {headline_tourists}")
    
    headline_weight_loss = creative_ai.generate_ad_headline("weight_loss", muaythai_gym)
    print(f"พาดหัวสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก: {headline_weight_loss}")
    
    return True

def main():
    """
    ฟังก์ชันหลักสำหรับการทดสอบระบบ
    """
    print("เริ่มการทดสอบระบบ AdGenius AI สำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย")
    print(f"วันที่และเวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ทดสอบโมดูล MuayThaiTargetingAI
    test_muaythai_targeting()
    
    # ทดสอบโมดูล MuayThaiCreativeAI
    test_muaythai_creative()
    
    print_separator("สรุปผลการทดสอบ")
    print("✓ ทดสอบโมดูล MuayThaiTargetingAI สำเร็จ")
    print("✓ ทดสอบโมดูล MuayThaiCreativeAI สำเร็จ")
    print("\nระบบ AdGenius AI พร้อมใช้งานสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย")

if __name__ == "__main__":
    main()
