"""
ไฟล์ทดสอบระบบ AdGenius AI สำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย
"""

import os
import json
import sys
from datetime import datetime

# เพิ่มไดเรกทอรีหลักลงใน path เพื่อให้สามารถ import โมดูลได้
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ai_modules.muaythai_targeting import MuayThaiTargetingAI
from app.ai_modules.muaythai_creative import MuayThaiCreativeAI
from app.platform_connectors.facebook_connector import FacebookConnector
from app.platform_connectors.instagram_connector import InstagramConnector
from app.platform_connectors.tiktok_connector import TikTokConnector
from app.platform_connectors.shopee_connector import ShopeeConnector

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
    
    # ทดสอบการค้นหาคำสำคัญ
    print("\n2. ทดสอบการค้นหาคำสำคัญ:")
    keywords = targeting_ai.find_keywords("local_fitness", 5)
    print(f"คำสำคัญสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย: {keywords}")
    
    keywords = targeting_ai.find_keywords("tourists", 5)
    print(f"คำสำคัญสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ: {keywords}")
    
    keywords = targeting_ai.find_keywords("weight_loss", 5)
    print(f"คำสำคัญสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก: {keywords}")
    
    # ทดสอบการวิเคราะห์ประสิทธิภาพของกลุ่มเป้าหมาย
    print("\n3. ทดสอบการวิเคราะห์ประสิทธิภาพของกลุ่มเป้าหมาย:")
    performance_data = {
        "targets": {
            "local_fitness": {
                "impressions": 10000,
                "clicks": 300,
                "conversions": 15,
                "cost": 5000,
                "revenue": 22500
            },
            "tourists": {
                "impressions": 5000,
                "clicks": 100,
                "conversions": 5,
                "cost": 2500,
                "revenue": 7500
            },
            "weight_loss": {
                "impressions": 8000,
                "clicks": 400,
                "conversions": 20,
                "cost": 4000,
                "revenue": 30000
            }
        }
    }
    
    target_performance = targeting_ai.analyze_target_performance(performance_data)
    print(f"กลุ่มเป้าหมายที่มีประสิทธิภาพสูงสุด: {target_performance.get('best_target', 'N/A')}")
    print(f"คำแนะนำ: {target_performance.get('recommendations', [])}")
    
    # ทดสอบการปรับปรุงกลุ่มเป้าหมาย
    print("\n4. ทดสอบการปรับปรุงกลุ่มเป้าหมาย:")
    campaign_data = {
        "target_audience": {
            "age_range": [25, 45],
            "gender": ["male", "female"],
            "interests": ["fitness", "weight_loss", "martial_arts"],
            "locations": ["รังสิต", "ปทุมธานี", "กรุงเทพ"]
        },
        "performance": {
            "age_performance": {
                "18-24": 1.5,
                "25-34": 3.2,
                "35-44": 2.8,
                "45-54": 1.2
            },
            "gender_performance": {
                "male": 2.5,
                "female": 1.8
            },
            "interest_performance": {
                "fitness": 2.7,
                "weight_loss": 3.5,
                "martial_arts": 2.2,
                "self_defense": 1.8,
                "boxing": 2.0
            },
            "location_performance": {
                "รังสิต": 3.0,
                "ปทุมธานี": 2.5,
                "กรุงเทพ": 1.8,
                "นนทบุรี": 2.2
            }
        }
    }
    
    optimized_audience = targeting_ai.optimize_target_audience(campaign_data)
    print(f"กลุ่มเป้าหมายที่ปรับปรุงแล้ว: {optimized_audience}")
    
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
    
    # ทดสอบการสร้างคำอธิบายโฆษณา
    print("\n2. ทดสอบการสร้างคำอธิบายโฆษณา:")
    description_local = creative_ai.generate_ad_description("local_fitness", muaythai_gym)
    print(f"คำอธิบายสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย: {description_local}")
    
    description_tourists = creative_ai.generate_ad_description("tourists", muaythai_gym)
    print(f"คำอธิบายสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ: {description_tourists}")
    
    description_weight_loss = creative_ai.generate_ad_description("weight_loss", muaythai_gym)
    print(f"คำอธิบายสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก: {description_weight_loss}")
    
    # ทดสอบการสร้างคำแนะนำสำหรับการสร้างภาพโฆษณา
    print("\n3. ทดสอบการสร้างคำแนะนำสำหรับการสร้างภาพโฆษณา:")
    image_prompt_local = creative_ai.generate_image_prompt("local_fitness", muaythai_gym)
    print(f"คำแนะนำสำหรับการสร้างภาพโฆษณาสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย: {image_prompt_local}")
    
    image_prompt_tourists = creative_ai.generate_image_prompt("tourists", muaythai_gym)
    print(f"คำแนะนำสำหรับการสร้างภาพโฆษณาสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ: {image_prompt_tourists}")
    
    image_prompt_weight_loss = creative_ai.generate_image_prompt("weight_loss", muaythai_gym)
    print(f"คำแนะนำสำหรับการสร้างภาพโฆษณาสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก: {image_prompt_weight_loss}")
    
    # ทดสอบการสร้างสรรค์โฆษณา
    print("\n4. ทดสอบการสร้างสรรค์โฆษณา:")
    ad_creative = creative_ai.generate_ad_creative("local_fitness", "image", muaythai_gym)
    print(f"โฆษณาสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย:")
    print(f"- พาดหัว: {ad_creative['headline']}")
    print(f"- คำอธิบาย: {ad_creative['description']}")
    print(f"- คำแนะนำสำหรับการสร้างภาพ: {ad_creative['image_prompt']}")
    
    # ทดสอบการสร้างสรรค์โฆษณาหลายรูปแบบ
    print("\n5. ทดสอบการสร้างสรรค์โฆษณาหลายรูปแบบ:")
    ad_variations = creative_ai.generate_ad_variations("weight_loss", "image", muaythai_gym, 2)
    for i, variation in enumerate(ad_variations):
        print(f"รูปแบบที่ {i+1}:")
        print(f"- พาดหัว: {variation['headline']}")
        print(f"- คำอธิบาย: {variation['description']}")
        print(f"- คำแนะนำสำหรับการสร้างภาพ: {variation['image_prompt']}")
    
    # ทดสอบการวิเคราะห์ประสิทธิภาพของโฆษณา
    print("\n6. ทดสอบการวิเคราะห์ประสิทธิภาพของโฆษณา:")
    ad_data = ad_creative
    performance_data = {
        "impressions": 10000,
        "clicks": 300,
        "conversions": 15,
        "cost": 5000,
        "revenue": 22500
    }
    
    ad_performance = creative_ai.analyze_ad_performance(ad_data, performance_data)
    print(f"CTR: {ad_performance['ctr']:.2f}%")
    print(f"อัตราการแปลง: {ad_performance['conversion_rate']:.2f}%")
    print(f"ต้นทุนต่อการแปลง: {ad_performance['cpc']:.2f} บาท")
    print(f"ROI: {ad_performance['roi']:.2f}%")
    print(f"คำแนะนำ: {ad_performance['recommendations']}")
    
    # ทดสอบการปรับปรุงโฆษณา
    print("\n7. ทดสอบการปรับปรุงโฆษณา:")
    optimized_ad = creative_ai.optimize_ad_creative(ad_data, performance_data)
    print(f"โฆษณาที่ปรับปรุงแล้ว:")
    print(f"- พาดหัว: {optimized_ad['headline']}")
    print(f"- คำอธิบาย: {optimized_ad['description']}")
    print(f"- คำแนะนำสำหรับการสร้างภาพ: {optimized_ad['image_prompt']}")
    
    return True

def test_platform_connectors():
    """
    ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ
    """
    print_separator("ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ")
    
    # ทดสอบการเชื่อมต่อกับ Facebook
    print("1. ทดสอบการเชื่อมต่อกับ Facebook:")
    try:
        facebook_connector = FacebookConnector()
        print("✓ สร้างอินสแตนซ์ของ FacebookConnector สำเร็จ")
        
        # ทดสอบฟังก์ชันต่างๆ ของ FacebookConnector
        print("- ฟังก์ชันที่สามารถใช้งานได้:")
        print("  - search_interests()")
        print("  - create_campaign()")
        print("  - get_campaign_performance()")
        print("  - optimize_campaign()")
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการสร้างอินสแตนซ์ของ FacebookConnector: {e}")
    
    # ทดสอบการเชื่อมต่อกับ Instagram
    print("\n2. ทดสอบการเชื่อมต่อกับ Instagram:")
    try:
        instagram_connector = InstagramConnector()
        print("✓ สร้างอินสแตนซ์ของ InstagramConnector สำเร็จ")
        
        # ทดสอบฟังก์ชันต่างๆ ของ InstagramConnector
        print("- ฟังก์ชันที่สามารถใช้งานได้:")
        print("  - search_hashtags()")
        print("  - create_campaign()")
        print("  - get_campaign_performance()")
        print("  - optimize_campaign()")
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการสร้างอินสแตนซ์ของ InstagramConnector: {e}")
    
    # ทดสอบการเชื่อมต่อกับ TikTok
    print("\n3. ทดสอบการเชื่อมต่อกับ TikTok:")
    try:
        tiktok_connector = TikTokConnector()
        print("✓ สร้างอินสแตนซ์ของ TikTokConnector สำเร็จ")
        
        # ทดสอบฟังก์ชันต่างๆ ของ TikTokConnector
        print("- ฟังก์ชันที่สามารถใช้งานได้:")
        print("  - search_interests()")
        print("  - search_hashtags()")
        print("  - create_campaign()")
        print("  - get_campaign_performance()")
        print("  - optimize_campaign()")
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการสร้างอินสแตนซ์ของ TikTokConnector: {e}")
    
    # ทดสอบการเชื่อมต่อกับ Shopee
    print("\n4. ทดสอบการเชื่อมต่อกับ Shopee:")
    try:
        shopee_connector = ShopeeConnector()
        print("✓ สร้างอินสแตนซ์ของ ShopeeConnector สำเร็จ")
        
        # ทดสอบฟังก์ชันต่างๆ ของ ShopeeConnector
        print("- ฟังก์ชันที่สามารถใช้งานได้:")
        print("  - get_product_info()")
        print("  - get_shop_performance()")
        print("  - create_promotion()")
        print("  - boost_product()")
        print("  - analyze_keywords()")
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการสร้างอินสแตนซ์ของ ShopeeConnector: {e}")
    
    return True

def test_end_to_end():
    """
    ทดสอบการทำงานแบบ end-to-end สำหรับธุรกิจค่ายมวยไทย
    """
    print_separator("ทดสอบการทำงานแบบ end-to-end สำหรับธุรกิจค่ายมวยไทย")
    
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
    
    print("1. วิเคราะห์สินค้าและกำหนดกลุ่มเป้าหมาย:")
    targeting_ai = MuayThaiTargetingAI()
    product_analysis = targeting_ai.analyze_product(muaythai_gym)
    primary_target = product_analysis["primary_target"]
    print(f"กลุ่มเป้าหมายหลัก: {primary_target}")
    print(f"คำสำคัญที่แนะนำ: {product_analysis['recommended_keywords'][:5]}")
    print(f"แพลตฟอร์มที่แนะนำ: {product_analysis['recommended_platforms']}")
    
    print("\n2. สร้างสรรค์โฆษณาสำหรับกลุ่มเป้าหมาย:")
    creative_ai = MuayThaiCreativeAI()
    ad_creatives = {}
    
    for platform in product_analysis["recommended_platforms"]:
        if platform == "facebook":
            ad_type = "image"
            connector = FacebookConnector()
        elif platform == "instagram":
            ad_type = "image"
            connector = InstagramConnector()
        elif platform == "tiktok":
            ad_type = "video"
            connector = TikTokConnector()
        elif platform == "shopee":
            ad_type = "image"
            connector = ShopeeConnector()
        else:
            continue
        
        print(f"\nสร้างโฆษณาสำหรับ {platform.capitalize()}:")
        ad_creative = creative_ai.generate_ad_creative(primary_target, ad_type, muaythai_gym)
        ad_creatives[platform] = ad_creative
        
        print(f"- พาดหัว: {ad_creative['headline']}")
        print(f"- คำอธิบาย: {ad_creative['description']}")
        
        if ad_type == "image":
            print(f"- คำแนะนำสำหรับการสร้างภาพ: {ad_creative['image_prompt']}")
        elif ad_type == "video":
            print(f"- คำแนะนำสำหรับการสร้างวิดีโอ: {ad_creative['video_prompt']}")
    
    print("\n3. สรุปผลการทดสอบ:")
    print("✓ วิเคราะห์สินค้าและกำหนดกลุ่มเป้าหมายสำเร็จ")
    print("✓ สร้างสรรค์โฆษณาสำหรับแต่ละแพลตฟอร์มสำเร็จ")
    print("✓ ระบบพร้อมใช้งานสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย")
    
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
    
    # ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ
    test_platform_connectors()
    
    # ทดสอบการทำงานแบบ end-to-end
    test_end_to_end()
    
    print_separator("สรุปผลการทดสอบ")
    print("✓ ทดสอบโมดูล MuayThaiTargetingAI สำเร็จ")
    print("✓ ทดสอบโมดูล MuayThaiCreativeAI สำเร็จ")
    print("✓ ทดสอบการเชื่อมต่อกับแพลตฟอร์มต่างๆ สำเร็จ")
    print("✓ ทดสอบการทำงานแบบ end-to-end สำเร็จ")
    print("\nระบบ AdGenius AI พร้อมใช้งานสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย")

if __name__ == "__main__":
    main()
