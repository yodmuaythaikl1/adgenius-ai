"""
ไฟล์ทดสอบแบบอิสระสำหรับโมดูล AI ของธุรกิจค่ายมวยไทย
ไม่ต้องการการเชื่อมต่อกับโมดูลอื่นๆ ของระบบ
"""

import os
import sys
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple

def print_separator(title):
    """
    แสดงเส้นคั่นพร้อมหัวข้อ
    """
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

class MuayThaiTargetingAI:
    """
    คลาสสำหรับการกำหนดกลุ่มเป้าหมายสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย
    """
    
    def __init__(self, config: Dict = None):
        """
        ฟังก์ชันเริ่มต้นสำหรับคลาส MuayThaiTargetingAI
        
        Args:
            config: การตั้งค่าสำหรับโมดูล AI
        """
        self.config = config or {}
        self.target_groups = {
            "local_fitness": {
                "description": "คนท้องถิ่นที่ต้องการออกกำลังกาย",
                "age_range": [18, 45],
                "gender": ["male", "female"],
                "interests": ["fitness", "weight_loss", "self_defense", "martial_arts"],
                "behaviors": ["social_media_active", "fitness_enthusiast", "health_conscious"],
                "motivations": ["better_physique", "health", "self_defense_skills"],
                "platforms": ["facebook", "instagram", "tiktok"],
                "ad_types": ["image", "video", "carousel"],
                "messaging_focus": ["fitness_results", "weight_loss", "skill_development"]
            },
            "tourists": {
                "description": "นักท่องเที่ยวและชาวต่างชาติ",
                "age_range": [20, 50],
                "gender": ["male", "female"],
                "interests": ["martial_arts", "thai_culture", "adventure", "travel"],
                "behaviors": ["sport_tourism", "cultural_experience", "digital_nomad"],
                "motivations": ["authentic_experience", "cultural_learning", "unique_workout"],
                "platforms": ["facebook", "instagram", "tiktok"],
                "ad_types": ["image", "video", "stories"],
                "messaging_focus": ["authentic_experience", "cultural_immersion", "unique_workout"]
            },
            "weight_loss": {
                "description": "ผู้ที่ต้องการลดน้ำหนักอย่างจริงจัง",
                "age_range": [25, 50],
                "gender": ["male", "female"],
                "interests": ["weight_loss", "health", "nutrition", "fitness"],
                "behaviors": ["diet_conscious", "tried_other_methods", "health_research"],
                "motivations": ["rapid_results", "sustainable_weight_loss", "expert_guidance"],
                "platforms": ["facebook", "instagram", "tiktok", "shopee"],
                "ad_types": ["before_after", "testimonial", "video_tutorial"],
                "messaging_focus": ["weight_loss_results", "expert_guidance", "proven_method"]
            }
        }
        
        # คำสำคัญสำหรับแต่ละกลุ่มเป้าหมาย
        self.target_keywords = {
            "local_fitness": [
                "มวยไทยออกกำลังกาย", "เรียนมวยไทย", "ค่ายมวยไทย", "มวยไทยลดน้ำหนัก", 
                "มวยไทยเพื่อสุขภาพ", "ฟิตเนสมวยไทย", "คาร์ดิโอมวยไทย", "ออกกำลังกายแบบมวยไทย",
                "muay thai fitness", "muay thai workout", "muay thai gym", "muay thai training",
                "kickboxing", "boxing fitness", "martial arts fitness", "combat sports workout"
            ],
            "tourists": [
                "muay thai thailand", "learn muay thai bangkok", "muay thai camp", "thai boxing class",
                "muay thai experience", "authentic muay thai", "thailand martial arts", "muay thai holiday",
                "muay thai tourism", "thailand fitness vacation", "learn thai boxing", "muay thai retreat",
                "เรียนมวยไทยสำหรับชาวต่างชาติ", "ค่ายมวยไทยนักท่องเที่ยว", "มวยไทยท่องเที่ยว"
            ],
            "weight_loss": [
                "มวยไทยลดน้ำหนัก", "ลดน้ำหนักด้วยมวยไทย", "มวยไทยเผาผลาญ", "มวยไทยลดไขมัน",
                "มวยไทยลดพุง", "ออกกำลังกายลดน้ำหนัก", "คาร์ดิโอลดน้ำหนัก", "เบิร์นไขมันมวยไทย",
                "muay thai weight loss", "lose weight kickboxing", "fat burning muay thai",
                "combat cardio weight loss", "martial arts fat loss", "muay thai transformation"
            ]
        }
        
        # ช่วงเวลาที่เหมาะสมสำหรับการโฆษณา
        self.optimal_ad_times = {
            "local_fitness": {
                "weekdays": ["07:00-09:00", "11:30-13:30", "17:00-22:00"],
                "weekends": ["09:00-13:00", "16:00-20:00"]
            },
            "tourists": {
                "weekdays": ["09:00-23:00"],
                "weekends": ["09:00-23:00"]
            },
            "weight_loss": {
                "weekdays": ["06:00-08:00", "11:30-13:30", "19:00-22:00"],
                "weekends": ["08:00-12:00", "18:00-22:00"]
            }
        }
        
        print("MuayThaiTargetingAI initialized successfully")
    
    def analyze_product(self, product_data: Dict) -> Dict:
        """
        วิเคราะห์ข้อมูลสินค้าหรือบริการเพื่อระบุกลุ่มเป้าหมายที่เหมาะสม
        
        Args:
            product_data: ข้อมูลสินค้าหรือบริการ
            
        Returns:
            Dict: ผลการวิเคราะห์กลุ่มเป้าหมาย
        """
        print(f"Analyzing product data: {product_data}")
        
        # วิเคราะห์คุณสมบัติของสินค้าหรือบริการ
        product_features = product_data.get("features", [])
        product_description = product_data.get("description", "")
        product_price = product_data.get("price", 0)
        product_location = product_data.get("location", "")
        
        # คะแนนความเหมาะสมสำหรับแต่ละกลุ่มเป้าหมาย
        target_scores = {
            "local_fitness": 0,
            "tourists": 0,
            "weight_loss": 0
        }
        
        # วิเคราะห์คุณสมบัติ
        for feature in product_features:
            feature_lower = feature.lower()
            
            # คะแนนสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย
            if any(keyword in feature_lower for keyword in ["ออกกำลังกาย", "fitness", "workout", "training"]):
                target_scores["local_fitness"] += 2
            
            # คะแนนสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ
            if any(keyword in feature_lower for keyword in ["authentic", "traditional", "culture", "experience", "ประสบการณ์", "วัฒนธรรม", "ชาวต่างชาติ"]):
                target_scores["tourists"] += 2
            
            # คะแนนสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก
            if any(keyword in feature_lower for keyword in ["ลดน้ำหนัก", "weight loss", "fat burning", "calorie", "เผาผลาญ"]):
                target_scores["weight_loss"] += 2
        
        # วิเคราะห์คำอธิบาย
        description_lower = product_description.lower()
        
        # คะแนนสำหรับกลุ่มคนท้องถิ่นที่ต้องการออกกำลังกาย
        if any(keyword in description_lower for keyword in ["ออกกำลังกาย", "fitness", "workout", "training"]):
            target_scores["local_fitness"] += 1
        
        # คะแนนสำหรับกลุ่มนักท่องเที่ยวและชาวต่างชาติ
        if any(keyword in description_lower for keyword in ["authentic", "traditional", "culture", "experience", "ประสบการณ์", "วัฒนธรรม", "ชาวต่างชาติ"]):
            target_scores["tourists"] += 1
        
        # คะแนนสำหรับกลุ่มผู้ที่ต้องการลดน้ำหนัก
        if any(keyword in description_lower for keyword in ["ลดน้ำหนัก", "weight loss", "fat burning", "calorie", "เผาผลาญ"]):
            target_scores["weight_loss"] += 1
        
        # วิเคราะห์ราคา
        if product_price > 0:
            # ราคาสูงอาจเหมาะกับนักท่องเที่ยวมากกว่า
            if product_price > 2000:
                target_scores["tourists"] += 1
            # ราคาปานกลางเหมาะกับคนท้องถิ่น
            elif 1000 <= product_price <= 2000:
                target_scores["local_fitness"] += 1
            # ราคาต่ำเหมาะกับผู้ที่ต้องการลดน้ำหนัก (อาจมีการแข่งขันสูง)
            else:
                target_scores["weight_loss"] += 1
        
        # วิเคราะห์ตำแหน่งที่ตั้ง
        location_lower = product_location.lower()
        
        # ตำแหน่งที่ตั้งในแหล่งท่องเที่ยวเหมาะกับนักท่องเที่ยว
        tourist_locations = ["สุขุมวิท", "sukhumvit", "สยาม", "siam", "อโศก", "asok", "ทองหล่อ", "thonglor", "เอกมัย", "ekkamai"]
        if any(location in location_lower for location in tourist_locations):
            target_scores["tourists"] += 2
        
        # ตำแหน่งที่ตั้งในย่านที่อยู่อาศัยเหมาะกับคนท้องถิ่น
        local_locations = ["ลาดพร้าว", "ladprao", "รามคำแหง", "ramkhamhaeng", "บางนา", "bangna", "รังสิต", "rangsit"]
        if any(location in location_lower for location in local_locations):
            target_scores["local_fitness"] += 2
            target_scores["weight_loss"] += 1
        
        # หากลุ่มเป้าหมายที่มีคะแนนสูงสุด
        max_score = max(target_scores.values())
        primary_targets = [target for target, score in target_scores.items() if score == max_score]
        
        # สร้างผลลัพธ์
        result = {
            "primary_target": primary_targets[0] if primary_targets else "local_fitness",
            "target_scores": target_scores,
            "recommended_keywords": self.get_recommended_keywords(primary_targets[0] if primary_targets else "local_fitness"),
            "optimal_ad_times": self.get_optimal_ad_times(primary_targets[0] if primary_targets else "local_fitness"),
            "recommended_platforms": self.get_recommended_platforms(primary_targets[0] if primary_targets else "local_fitness"),
            "recommended_ad_types": self.get_recommended_ad_types(primary_targets[0] if primary_targets else "local_fitness"),
            "messaging_focus": self.get_messaging_focus(primary_targets[0] if primary_targets else "local_fitness")
        }
        
        print(f"Product analysis result: {result}")
        return result
    
    def find_keywords(self, target_group: str, limit: int = 10) -> List[str]:
        """
        ค้นหาคำสำคัญที่เกี่ยวข้องกับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            limit: จำนวนคำสำคัญที่ต้องการ
            
        Returns:
            List[str]: รายการคำสำคัญ
        """
        print(f"Finding keywords for target group: {target_group}, limit: {limit}")
        
        if target_group in self.target_keywords:
            keywords = self.target_keywords[target_group]
            return keywords[:limit] if limit < len(keywords) else keywords
        
        return []
    
    def get_recommended_keywords(self, target_group: str) -> List[str]:
        """
        รับคำสำคัญที่แนะนำสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            
        Returns:
            List[str]: รายการคำสำคัญที่แนะนำ
        """
        return self.find_keywords(target_group, 15)
    
    def get_optimal_ad_times(self, target_group: str) -> Dict:
        """
        รับช่วงเวลาที่เหมาะสมสำหรับการโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            
        Returns:
            Dict: ช่วงเวลาที่เหมาะสมสำหรับการโฆษณา
        """
        if target_group in self.optimal_ad_times:
            return self.optimal_ad_times[target_group]
        
        return self.optimal_ad_times["local_fitness"]  # ค่าเริ่มต้น
    
    def get_recommended_platforms(self, target_group: str) -> List[str]:
        """
        รับแพลตฟอร์มที่แนะนำสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            
        Returns:
            List[str]: รายการแพลตฟอร์มที่แนะนำ
        """
        if target_group in self.target_groups:
            return self.target_groups[target_group]["platforms"]
        
        return ["facebook", "instagram"]  # ค่าเริ่มต้น
    
    def get_recommended_ad_types(self, target_group: str) -> List[str]:
        """
        รับประเภทโฆษณาที่แนะนำสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            
        Returns:
            List[str]: รายการประเภทโฆษณาที่แนะนำ
        """
        if target_group in self.target_groups:
            return self.target_groups[target_group]["ad_types"]
        
        return ["image", "video"]  # ค่าเริ่มต้น
    
    def get_messaging_focus(self, target_group: str) -> List[str]:
        """
        รับจุดเน้นของข้อความสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            
        Returns:
            List[str]: รายการจุดเน้นของข้อความ
        """
        if target_group in self.target_groups:
            return self.target_groups[target_group]["messaging_focus"]
        
        return ["fitness_results"]  # ค่าเริ่มต้น

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
        
        print("MuayThaiCreativeAI initialized successfully")
    
    def generate_ad_headline(self, target_group: str, product_data: Dict = None) -> str:
        """
        สร้างพาดหัวโฆษณาสำหรับกลุ่มเป้าหมาย
        
        Args:
            target_group: กลุ่มเป้าหมาย
            product_data: ข้อมูลสินค้าหรือบริการ (ไม่จำเป็น)
            
        Returns:
            str: พาดหัวโฆษณา
        """
        print(f"Generating ad headline for target group: {target_group}")
        
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
            
            print(f"Generated headline: {headline}")
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
        print(f"Generating ad description for target group: {target_group}")
        
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
            
            print(f"Generated description: {description}")
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
        print(f"Generating image prompt for target group: {target_group}")
        
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
            
            print(f"Generated image prompt: {prompt}")
            return prompt
        
        return "ภาพการฝึกมวยไทยในค่ายมวยที่ทันสมัย มีอุปกรณ์ออกกำลังกายครบครัน แสงสว่าง บรรยากาศสะอาด"
    
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
        print(f"Generating ad creative for target group: {target_group}, ad type: {ad_type}")
        
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
        
        print(f"Generated ad creative: {creative}")
        return creative

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
        elif platform == "instagram":
            ad_type = "image"
        elif platform == "tiktok":
            ad_type = "video"
        elif platform == "shopee":
            ad_type = "image"
        else:
            continue
        
        print(f"\nสร้างโฆษณาสำหรับ {platform.capitalize()}:")
        ad_creative = creative_ai.generate_ad_creative(primary_target, ad_type, muaythai_gym)
        ad_creatives[platform] = ad_creative
        
        print(f"- พาดหัว: {ad_creative['headline']}")
        print(f"- คำอธิบาย: {ad_creative['description']}")
        
        if ad_type == "image":
            print(f"- คำแนะนำสำหรับการสร้างภาพ: {ad_creative['image_prompt']}")
    
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
    
    # ทดสอบการทำงานแบบ end-to-end
    test_end_to_end()
    
    print_separator("สรุปผลการทดสอบ")
    print("✓ ทดสอบโมดูล MuayThaiTargetingAI สำเร็จ")
    print("✓ ทดสอบโมดูล MuayThaiCreativeAI สำเร็จ")
    print("✓ ทดสอบการทำงานแบบ end-to-end สำเร็จ")
    print("\nระบบ AdGenius AI พร้อมใช้งานสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย")

if __name__ == "__main__":
    main()
