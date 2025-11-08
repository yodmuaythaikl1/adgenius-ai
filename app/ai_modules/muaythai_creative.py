"""
โมดูล AI สำหรับการสร้างสรรค์โฆษณาสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย
"""

import os
import json
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime
from app.utils.logger import get_logger

# ตั้งค่า logger
logger = get_logger(__name__)

class MuayThaiCreativeAI:
    """
    คลาสสำหรับการสร้างสรรค์โฆษณาสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย
    """
    
    def __init__(self, config: Dict = None):
        """
        ฟังก์ชันเริ่มต้นสำหรับคลาส MuayThaiCreativeAI
        
        Args:
            config: การตั้งค่าสำหรับโมดูล AI
        """
        self.config = config or {}
        
        # ข้อความโฆษณาสำหรับแต่ละกลุ่มเป้าหมาย
        self.ad_headlines = {
            "local_fitness": [
                "ออกกำลังกายแบบมวยไทย เผาผลาญ 1,000 แคลอรี่ต่อชั่วโมง!",
                "เรียนมวยไทย ลดน้ำหนัก กระชับกล้ามเนื้อ ในที่เดียว",
                "มวยไทยเพื่อสุขภาพ: ออกกำลังกายแบบไทยๆ ได้ผลจริง",
                "ลดน้ำหนัก 7 กิโลใน 1 เดือนด้วยมวยไทย รับประกันผล!",
                "เปลี่ยนร่างกายของคุณด้วยมวยไทย ผลลัพธ์เห็นได้ใน 2 สัปดาห์"
            ],
            "tourists": [
                "Experience Authentic Muay Thai in Thailand",
                "Learn Thailand's National Sport from Professional Fighters",
                "Muay Thai Training: The Ultimate Thai Cultural Experience",
                "Discover the Art of 8 Limbs in the Land of Smiles",
                "Train Like a Thai Fighter: Authentic Muay Thai Experience"
            ],
            "weight_loss": [
                "ลดน้ำหนักด้วยมวยไทย: วิธีที่สนุกและได้ผลจริง",
                "เผาผลาญไขมันด้วยมวยไทย: ลดได้ถึง 7 กิโลใน 1 เดือน",
                "ลืมการวิ่งบนลู่ไปได้เลย! มวยไทยเผาผลาญไขมันได้มากกว่า 2 เท่า",
                "ลดน้ำหนักแบบยั่งยืนด้วยมวยไทย: ไม่โยโย่ ไม่หิว ไม่ทรมาน",
                "ลดพุง ลดต้นขา ลดแขน ด้วยมวยไทยเพียง 3 ครั้งต่อสัปดาห์"
            ]
        }
        
        # คำอธิบายโฆษณาสำหรับแต่ละกลุ่มเป้าหมาย
        self.ad_descriptions = {
            "local_fitness": [
                "มวยไทยไม่ใช่แค่ศิลปะการต่อสู้ แต่เป็นการออกกำลังกายที่ทรงประสิทธิภาพที่สุด เผาผลาญแคลอรี่ได้มากถึง 1,000 แคลอรี่ต่อชั่วโมง เสริมสร้างกล้ามเนื้อทั่วร่างกาย และเพิ่มความคล่องตัว มาเริ่มต้นการเดินทางสู่สุขภาพที่ดีกว่ากับเรา",
                "ค่ายมวยของเราสอนโดยครูมวยมืออาชีพที่มีประสบการณ์การแข่งขันระดับสูง คุณจะได้เรียนรู้เทคนิคมวยไทยที่ถูกต้อง พร้อมกับการออกกำลังกายที่ครบวงจร ไม่ว่าคุณจะเป็นมือใหม่หรือมีประสบการณ์ เรามีคลาสที่เหมาะกับทุกระดับ",
                "มวยไทยเป็นการออกกำลังกายแบบคาร์ดิโอที่ได้ประสิทธิภาพสูงมาก! ช่วยเผาผลาญไขมัน เสริมสร้างกล้ามเนื้อ และเพิ่มความแข็งแรงให้กับร่างกาย มาเริ่มต้นการเปลี่ยนแปลงร่างกายของคุณกับเราวันนี้"
            ],
            "tourists": [
                "Immerse yourself in Thailand's rich cultural heritage through Muay Thai, the country's national sport. Our gym offers authentic training experiences led by professional fighters, allowing you to learn traditional techniques while getting an incredible workout. Perfect for all skill levels, from beginners to advanced practitioners.",
                "Experience the true essence of Muay Thai in its homeland. Our training sessions combine traditional techniques with modern fitness approaches, providing both cultural immersion and physical benefits. Train alongside locals and fellow travelers in our welcoming, authentic environment.",
                "Discover why Muay Thai is known as the 'Art of Eight Limbs' through our authentic training programs. Our experienced instructors will guide you through traditional techniques while sharing insights into Thai culture and the spiritual aspects of this ancient martial art. Take home more than just photos – take home a skill."
            ],
            "weight_loss": [
                "มวยไทยเป็นการออกกำลังกายที่เผาผลาญแคลอรี่ได้มากถึง 1,000 แคลอรี่ต่อชั่วโมง มากกว่าการวิ่งหรือปั่นจักรยานถึง 2 เท่า ด้วยการฝึกที่ผสมผสานทั้งคาร์ดิโอและการเสริมสร้างกล้ามเนื้อ ทำให้ร่างกายเผาผลาญไขมันได้อย่างต่อเนื่องแม้หลังจากการฝึก",
                "โปรแกรมลดน้ำหนักด้วยมวยไทยของเราได้รับการออกแบบโดยผู้เชี่ยวชาญด้านโภชนาการและการออกกำลังกาย รับประกันผลลัพธ์ด้วยการติดตามน้ำหนักและสัดส่วนอย่างใกล้ชิด พร้อมให้คำแนะนำด้านอาหารที่เหมาะสม ลูกค้าของเราลดน้ำหนักได้เฉลี่ย 5-7 กิโลกรัมในเดือนแรก",
                "ลืมการลดน้ำหนักแบบน่าเบื่อไปได้เลย! มวยไทยเป็นการออกกำลังกายที่สนุก ท้าทาย และได้ผลจริง คุณจะได้เรียนรู้ทักษะใหม่ๆ พร้อมกับเผาผลาญไขมันและเสริมสร้างกล้ามเนื้อไปพร้อมกัน ไม่ต้องวิ่งบนลู่ซ้ำๆ อีกต่อไป"
            ]
        }
        
        # คำแนะนำสำหรับการสร้างภาพโฆษณา
        self.image_prompts = {
            "local_fitness": [
                "ภาพผู้ชายหรือผู้หญิงไทยกำลังฝึกมวยไทย ชกกระสอบทราย ในค่ายมวยที่ทันสมัย มีอุปกรณ์ออกกำลังกายครบครัน แสงสว่าง บรรยากาศสะอาด",
                "ภาพก่อน-หลังของลูกค้าที่ลดน้ำหนักสำเร็จด้วยมวยไทย แสดงการเปลี่ยนแปลงของรูปร่างที่ชัดเจน",
                "ภาพการฝึกมวยไทยแบบกลุ่ม ผู้เข้าร่วมหลากหลายวัยกำลังเรียนรู้ท่าทางมวยไทยพื้นฐาน บรรยากาศสนุกสนาน",
                "ภาพครูมวยกำลังสอนการชกมวยไทยแบบตัวต่อตัว แสดงให้เห็นถึงการดูแลอย่างใกล้ชิด"
            ],
            "tourists": [
                "Image of a foreign tourist learning Muay Thai techniques from a Thai trainer in an authentic gym environment with traditional equipment and Thai decorative elements",
                "Image of a diverse group of international visitors participating in a Muay Thai class, showing cultural exchange in an authentic Thai setting",
                "Image of a tourist wearing Muay Thai shorts and hand wraps, practicing kicks on Thai pads held by a professional trainer, with traditional Thai gym elements visible",
                "Image showing the before and after transformation of a foreign visitor who trained Muay Thai during their stay in Thailand"
            ],
            "weight_loss": [
                "ภาพก่อน-หลังของลูกค้าที่ลดน้ำหนักสำเร็จด้วยมวยไทย แสดงการเปลี่ยนแปลงของรูปร่างที่ชัดเจน โดยเฉพาะบริเวณหน้าท้องและต้นแขน",
                "ภาพการฝึกมวยไทยที่เน้นการเผาผลาญแคลอรี่ เช่น การชกกระสอบทรายอย่างเข้มข้น หรือการซ้อมมวยแบบต่อเนื่อง แสดงให้เห็นถึงความเหนื่อยและเหงื่อที่ออกมาก",
                "ภาพกราฟหรือแผนภูมิที่แสดงการเผาผลาญแคลอรี่ของมวยไทยเปรียบเทียบกับการออกกำลังกายรูปแบบอื่น",
                "ภาพลูกค้ากำลังวัดสัดส่วนหรือชั่งน้ำหนัก แสดงให้เห็นถึงการติดตามผลอย่างเป็นระบบ"
            ]
        }
        
        # คำแนะนำสำหรับการสร้างวิดีโอโฆษณา
        self.video_prompts = {
            "local_fitness": [
                "วิดีโอแสดงบรรยากาศการฝึกมวยไทยในค่าย มีทั้งการอบอุ่นร่างกาย การชกกระสอบทราย การซ้อมมวย และการยืดกล้ามเนื้อ แสดงให้เห็นถึงการออกกำลังกายที่ครบวงจร",
                "วิดีโอสั้นๆ แสดงการเปลี่ยนแปลงของลูกค้าตั้งแต่วันแรกจนถึงปัจจุบัน พร้อมคำบรรยายถึงน้ำหนักที่ลดลงและสัดส่วนที่เปลี่ยนไป",
                "วิดีโอสาธิตท่ามวยไทยพื้นฐานที่ใช้ในการออกกำลังกาย พร้อมคำอธิบายประโยชน์ของแต่ละท่าที่มีต่อร่างกาย"
            ],
            "tourists": [
                "Video showing foreign visitors learning Muay Thai techniques from Thai trainers, with cultural elements and authentic gym atmosphere. Include shots of the gym environment, training sessions, and satisfied customers sharing their experiences.",
                "Short documentary-style video about the cultural significance of Muay Thai in Thailand, featuring interviews with trainers and footage of training sessions with international visitors.",
                "Video tour of the gym facilities, showing the equipment, training areas, and amenities available for visitors. Include testimonials from foreign customers about their experience."
            ],
            "weight_loss": [
                "วิดีโอแสดงการเปลี่ยนแปลงของลูกค้าที่ลดน้ำหนักสำเร็จด้วยมวยไทย มีการสัมภาษณ์ถึงความรู้สึกและประสบการณ์ พร้อมภาพก่อน-หลัง",
                "วิดีโอสาธิตการฝึกมวยไทยเพื่อการลดน้ำหนัก แสดงให้เห็นถึงความเข้มข้นของการฝึกและการเผาผลาญแคลอรี่ที่สูง",
                "วิดีโอเปรียบเทียบการเผาผลาญแคลอรี่ของมวยไทยกับการออกกำลังกายรูปแบบอื่น พร้อมคำอธิบายทางวิทยาศาสตร์"
            ]
        }
        
        logger.info("MuayThaiCreativeAI initialized successfully")
    
    def generate_ad_headline(self, target_group: str, product_data: Dict = None) -> str:
        """
        สร้างพาดหัวโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            str: พาดหัวโฆษณา
        """
        logger.info(f"Generating ad headline for target group: {target_group}")
        
        if target_group in self.ad_headlines:
            headlines = self.ad_headlines[target_group]
            headline = random.choice(headlines)
            
            # ปรับแต่งพาดหัวตามข้อมูลสินค้า (ถ้ามี)
            if product_data:
                gym_name = product_data.get("name", "")
                if gym_name:
                    # เพิ่มชื่อค่ายมวยในพาดหัว (ถ้าไม่มีอยู่แล้ว)
                    if gym_name not in headline:
                        if ":" in headline:
                            parts = headline.split(":", 1)
                            headline = f"{parts[0]} ที่ {gym_name}: {parts[1]}"
                        else:
                            headline = f"{headline} ที่ {gym_name}"
            
            logger.info(f"Generated headline: {headline}")
            return headline
        
        return "เรียนมวยไทย ออกกำลังกาย ลดน้ำหนัก กระชับกล้ามเนื้อ"
    
    def generate_ad_description(self, target_group: str, product_data: Dict = None) -> str:
        """
        สร้างคำอธิบายโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            str: คำอธิบายโฆษณา
        """
        logger.info(f"Generating ad description for target group: {target_group}")
        
        if target_group in self.ad_descriptions:
            descriptions = self.ad_descriptions[target_group]
            description = random.choice(descriptions)
            
            # ปรับแต่งคำอธิบายตามข้อมูลสินค้า (ถ้ามี)
            if product_data:
                gym_name = product_data.get("name", "")
                location = product_data.get("location", "")
                price = product_data.get("price", "")
                
                if gym_name:
                    description = description.replace("ค่ายมวยของเรา", gym_name)
                    description = description.replace("our gym", gym_name)
                
                if location:
                    description += f" ตั้งอยู่ที่ {location} เดินทางสะดวก"
                
                if price:
                    description += f" ราคาเริ่มต้นเพียง {price} บาทต่อครั้ง"
            
            logger.info(f"Generated description: {description}")
            return description
        
        return "มวยไทยเป็นการออกกำลังกายที่ทรงประสิทธิภาพ ช่วยเผาผลาญแคลอรี่ได้มากถึง 1,000 แคลอรี่ต่อชั่วโมง เสริมสร้างกล้ามเนื้อทั่วร่างกาย และเพิ่มความคล่องตัว"
    
    def generate_image_prompt(self, target_group: str, product_data: Dict = None) -> str:
        """
        สร้างคำแนะนำสำหรับการสร้างภาพโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            str: คำแนะนำสำหรับการสร้างภาพโฆษณา
        """
        logger.info(f"Generating image prompt for target group: {target_group}")
        
        if target_group in self.image_prompts:
            prompts = self.image_prompts[target_group]
            prompt = random.choice(prompts)
            
            # ปรับแต่งคำแนะนำตามข้อมูลสินค้า (ถ้ามี)
            if product_data:
                gym_name = product_data.get("name", "")
                location = product_data.get("location", "")
                
                if gym_name:
                    prompt += f" ในค่ายมวย {gym_name}"
                
                if location:
                    prompt += f" ที่ตั้งอยู่ที่ {location}"
            
            logger.info(f"Generated image prompt: {prompt}")
            return prompt
        
        return "ภาพการฝึกมวยไทยในค่ายมวยที่ทันสมัย มีอุปกรณ์ออกกำลังกายครบครัน แสงสว่าง บรรยากาศสะอาด"
    
    def generate_video_prompt(self, target_group: str, product_data: Dict = None) -> str:
        """
        สร้างคำแนะนำสำหรับการสร้างวิดีโอโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            str: คำแนะนำสำหรับการสร้างวิดีโอโฆษณา
        """
        logger.info(f"Generating video prompt for target group: {target_group}")
        
        if target_group in self.video_prompts:
            prompts = self.video_prompts[target_group]
            prompt = random.choice(prompts)
            
            # ปรับแต่งคำแนะนำตามข้อมูลสินค้า (ถ้ามี)
            if product_data:
                gym_name = product_data.get("name", "")
                location = product_data.get("location", "")
                
                if gym_name:
                    prompt = prompt.replace("ค่ายมวย", f"ค่ายมวย {gym_name}")
                    prompt = prompt.replace("the gym", f"{gym_name}")
                
                if location:
                    prompt += f" แสดงให้เห็นถึงทำเลที่ตั้งที่สะดวกที่ {location}"
            
            logger.info(f"Generated video prompt: {prompt}")
            return prompt
        
        return "วิดีโอแสดงบรรยากาศการฝึกมวยไทยในค่าย มีทั้งการอบอุ่นร่างกาย การชกกระสอบทราย การซ้อมมวย และการยืดกล้ามเนื้อ"
    
    def generate_ad_creative(self, target_group: str, ad_type: str, product_data: Dict = None) -> Dict:
        """
        สร้างสรรค์โฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            ad_type: ประเภทโฆษณา (image, video, carousel)
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            Dict: ข้อมูลโฆษณา
        """
        logger.info(f"Generating ad creative for target group: {target_group}, ad type: {ad_type}")
        
        headline = self.generate_ad_headline(target_group, product_data)
        description = self.generate_ad_description(target_group, product_data)
        
        creative = {
            "headline": headline,
            "description": description,
            "target_group": target_group,
            "ad_type": ad_type
        }
        
        if ad_type == "image":
            creative["image_prompt"] = self.generate_image_prompt(target_group, product_data)
        elif ad_type == "video":
            creative["video_prompt"] = self.generate_video_prompt(target_group, product_data)
        elif ad_type == "carousel":
            # สร้างคำแนะนำสำหรับภาพหลายภาพ
            image_prompts = []
            for _ in range(3):  # สร้าง 3 ภาพสำหรับ carousel
                image_prompts.append(self.generate_image_prompt(target_group, product_data))
            creative["image_prompts"] = image_prompts
        
        logger.info(f"Generated ad creative: {creative}")
        return creative
    
    def generate_ad_variations(self, target_group: str, ad_type: str, product_data: Dict = None, num_variations: int = 3) -> List[Dict]:
        """
        สร้างสรรค์โฆษณาหลายรูปแบบสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            ad_type: ประเภทโฆษณา (image, video, carousel)
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            num_variations: จำนวนรูปแบบโฆษณาที่ต้องการ
            
        Returns:
            List[Dict]: รายการข้อมูลโฆษณา
        """
        logger.info(f"Generating {num_variations} ad variations for target group: {target_group}, ad type: {ad_type}")
        
        variations = []
        for _ in range(num_variations):
            variation = self.generate_ad_creative(target_group, ad_type, product_data)
            variations.append(variation)
        
        logger.info(f"Generated {len(variations)} ad variations")
        return variations
    
    def analyze_ad_performance(self, ad_data: Dict, performance_data: Dict) -> Dict:
        """
        วิเคราะห์ประสิทธิภาพของโฆษณา
        
        Args:
            ad_data: ข้อมูลโฆษณา
            performance_data: ข้อมูลประสิทธิภาพ
            
        Returns:
            Dict: ผลการวิเคราะห์ประสิทธิภาพ
        """
        logger.info(f"Analyzing ad performance: {performance_data}")
        
        # ตรวจสอบข้อมูลประสิทธิภาพ
        if not performance_data:
            return {"error": "Invalid performance data"}
        
        # คำนวณอัตราการคลิก (CTR)
        impressions = performance_data.get("impressions", 0)
        clicks = performance_data.get("clicks", 0)
        ctr = (clicks / impressions) * 100 if impressions > 0 else 0
        
        # คำนวณอัตราการแปลง (Conversion Rate)
        conversions = performance_data.get("conversions", 0)
        conversion_rate = (conversions / clicks) * 100 if clicks > 0 else 0
        
        # คำนวณต้นทุนต่อการแปลง (Cost Per Conversion)
        cost = performance_data.get("cost", 0)
        cpc = cost / conversions if conversions > 0 else 0
        
        # คำนวณผลตอบแทนจากการลงทุน (ROI)
        revenue = performance_data.get("revenue", 0)
        roi = ((revenue - cost) / cost) * 100 if cost > 0 else 0
        
        # สร้างผลลัพธ์
        result = {
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "cpc": cpc,
            "roi": roi,
            "performance_score": (ctr * 0.3) + (conversion_rate * 0.4) + (roi * 0.3)  # คะแนนประสิทธิภาพ
        }
        
        # สร้างคำแนะนำ
        recommendations = []
        
        if ctr < 1.0:
            recommendations.append("ปรับปรุงพาดหัวและรูปภาพโฆษณาเพื่อเพิ่ม CTR")
        
        if conversion_rate < 2.0:
            recommendations.append("ปรับปรุงคำอธิบายและข้อเสนอเพื่อเพิ่มอัตราการแปลง")
        
        if roi < 100:
            recommendations.append("ปรับปรุงกลุ่มเป้าหมายหรือลดต้นทุนเพื่อเพิ่ม ROI")
        
        result["recommendations"] = recommendations
        
        logger.info(f"Ad performance analysis result: {result}")
        return result
    
    def optimize_ad_creative(self, ad_data: Dict, performance_data: Dict) -> Dict:
        """
        ปรับปรุงโฆษณาโดยอัตโนมัติเพื่อเพิ่มประสิทธิภาพ
        
        Args:
            ad_data: ข้อมูลโฆษณา
            performance_data: ข้อมูลประสิทธิภาพ
            
        Returns:
            Dict: โฆษณาที่ปรับปรุงแล้ว
        """
        logger.info(f"Optimizing ad creative: {ad_data}")
        
        # ตรวจสอบข้อมูลโฆษณา
        if not ad_data:
            return {"error": "Invalid ad data"}
        
        # วิเคราะห์ประสิทธิภาพ
        analysis = self.analyze_ad_performance(ad_data, performance_data)
        
        # ปรับปรุงโฆษณา
        optimized_ad = ad_data.copy()
        
        # ปรับปรุงพาดหัว
        if analysis.get("ctr", 0) < 1.0:
            target_group = ad_data.get("target_group", "local_fitness")
            product_data = ad_data.get("product_data", {})
            
            # สร้างพาดหัวใหม่
            new_headline = self.generate_ad_headline(target_group, product_data)
            optimized_ad["headline"] = new_headline
            
            # เพิ่มคำที่ดึงดูดความสนใจ
            attention_words = ["ฟรี", "พิเศษ", "ด่วน", "จำกัด", "ลด", "โปรโมชัน"]
            if not any(word in new_headline for word in attention_words):
                optimized_ad["headline"] = f"{random.choice(attention_words)}! {new_headline}"
        
        # ปรับปรุงคำอธิบาย
        if analysis.get("conversion_rate", 0) < 2.0:
            target_group = ad_data.get("target_group", "local_fitness")
            product_data = ad_data.get("product_data", {})
            
            # สร้างคำอธิบายใหม่
            new_description = self.generate_ad_description(target_group, product_data)
            optimized_ad["description"] = new_description
            
            # เพิ่มการเร่งรัด (Call to Action)
            cta_phrases = ["สมัครเลย", "จองตอนนี้", "ติดต่อวันนี้", "เริ่มต้นทันที", "รับส่วนลดทันที"]
            if not any(phrase in new_description for phrase in cta_phrases):
                optimized_ad["description"] = f"{new_description} {random.choice(cta_phrases)}!"
        
        # ปรับปรุงรูปภาพ
        if ad_data.get("ad_type", "") == "image":
            target_group = ad_data.get("target_group", "local_fitness")
            product_data = ad_data.get("product_data", {})
            
            # สร้างคำแนะนำสำหรับการสร้างภาพใหม่
            new_image_prompt = self.generate_image_prompt(target_group, product_data)
            optimized_ad["image_prompt"] = new_image_prompt
        
        # ปรับปรุงวิดีโอ
        if ad_data.get("ad_type", "") == "video":
            target_group = ad_data.get("target_group", "local_fitness")
            product_data = ad_data.get("product_data", {})
            
            # สร้างคำแนะนำสำหรับการสร้างวิดีโอใหม่
            new_video_prompt = self.generate_video_prompt(target_group, product_data)
            optimized_ad["video_prompt"] = new_video_prompt
        
        logger.info(f"Optimized ad creative: {optimized_ad}")
        return optimized_ad
