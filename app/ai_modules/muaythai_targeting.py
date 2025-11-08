"""
โมดูล AI สำหรับการกำหนดกลุ่มเป้าหมายสำหรับธุรกิจค่ายมวยไทยแบบออกกำลังกาย
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from datetime import datetime
from app.utils.logger import get_logger

# ตั้งค่า logger
logger = get_logger(__name__)

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
        
        logger.info("MuayThaiTargetingAI initialized successfully")
    
    def analyze_product(self, product_data: Dict) -> Dict:
        """
        วิเคราะห์ข้อมูลสินค้าหรือบริการเพื่อระบุกลุ่มเป้าหมายที่เหมาะสม
        
        Args:
            product_data: ข้อมูลสินค้าหรือบริการ
            
        Returns:
            Dict: ผลการวิเคราะห์กลุ่มเป้าหมาย
        """
        logger.info(f"Analyzing product data: {product_data}")
        
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
            if any(keyword in feature_lower for keyword in ["authentic", "traditional", "culture", "experience", "ประสบการณ์", "วัฒนธรรม"]):
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
        if any(keyword in description_lower for keyword in ["authentic", "traditional", "culture", "experience", "ประสบการณ์", "วัฒนธรรม"]):
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
        
        logger.info(f"Product analysis result: {result}")
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
        logger.info(f"Finding keywords for target group: {target_group}, limit: {limit}")
        
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
    
    def analyze_target_performance(self, performance_data: Dict) -> Dict:
        """
        วิเคราะห์ประสิทธิภาพของกลุ่มเป้าหมาย
        
        Args:
            performance_data: ข้อมูลประสิทธิภาพ
            
        Returns:
            Dict: ผลการวิเคราะห์ประสิทธิภาพ
        """
        logger.info(f"Analyzing target performance: {performance_data}")
        
        # ตรวจสอบข้อมูลประสิทธิภาพ
        if not performance_data or "targets" not in performance_data:
            return {"error": "Invalid performance data"}
        
        targets = performance_data["targets"]
        results = {}
        
        for target, data in targets.items():
            # คำนวณอัตราการคลิก (CTR)
            impressions = data.get("impressions", 0)
            clicks = data.get("clicks", 0)
            ctr = (clicks / impressions) * 100 if impressions > 0 else 0
            
            # คำนวณอัตราการแปลง (Conversion Rate)
            conversions = data.get("conversions", 0)
            conversion_rate = (conversions / clicks) * 100 if clicks > 0 else 0
            
            # คำนวณต้นทุนต่อการแปลง (Cost Per Conversion)
            cost = data.get("cost", 0)
            cpc = cost / conversions if conversions > 0 else 0
            
            # คำนวณผลตอบแทนจากการลงทุน (ROI)
            revenue = data.get("revenue", 0)
            roi = ((revenue - cost) / cost) * 100 if cost > 0 else 0
            
            # สร้างผลลัพธ์
            results[target] = {
                "ctr": ctr,
                "conversion_rate": conversion_rate,
                "cpc": cpc,
                "roi": roi,
                "performance_score": (ctr * 0.3) + (conversion_rate * 0.4) + (roi * 0.3)  # คะแนนประสิทธิภาพ
            }
        
        # หากลุ่มเป้าหมายที่มีประสิทธิภาพสูงสุด
        if results:
            best_target = max(results.items(), key=lambda x: x[1]["performance_score"])
            results["best_target"] = best_target[0]
            
            # สร้างคำแนะนำ
            recommendations = []
            
            for target, data in results.items():
                if target != "best_target":
                    if data["ctr"] < 1.0:
                        recommendations.append(f"เพิ่ม CTR สำหรับกลุ่ม {target} โดยปรับปรุงข้อความและรูปภาพโฆษณา")
                    
                    if data["conversion_rate"] < 2.0:
                        recommendations.append(f"เพิ่มอัตราการแปลงสำหรับกลุ่ม {target} โดยปรับปรุงหน้าลงจอดและข้อเสนอ")
                    
                    if data["roi"] < 100:
                        recommendations.append(f"เพิ่ม ROI สำหรับกลุ่ม {target} โดยลดต้นทุนหรือเพิ่มรายได้ต่อการแปลง")
            
            results["recommendations"] = recommendations
        
        logger.info(f"Target performance analysis result: {results}")
        return results
    
    def optimize_target_audience(self, campaign_data: Dict) -> Dict:
        """
        ปรับปรุงกลุ่มเป้าหมายโดยอัตโนมัติเพื่อเพิ่มประสิทธิภาพ
        
        Args:
            campaign_data: ข้อมูลแคมเปญ
            
        Returns:
            Dict: กลุ่มเป้าหมายที่ปรับปรุงแล้ว
        """
        logger.info(f"Optimizing target audience: {campaign_data}")
        
        # ตรวจสอบข้อมูลแคมเปญ
        if not campaign_data or "target_audience" not in campaign_data:
            return {"error": "Invalid campaign data"}
        
        target_audience = campaign_data["target_audience"]
        performance = campaign_data.get("performance", {})
        
        # ปรับปรุงกลุ่มเป้าหมาย
        optimized_audience = target_audience.copy()
        
        # ปรับปรุงช่วงอายุ
        if "age_range" in target_audience and performance:
            age_performance = performance.get("age_performance", {})
            
            if age_performance:
                best_age_group = max(age_performance.items(), key=lambda x: x[1])
                age_min, age_max = map(int, best_age_group[0].split("-"))
                
                current_min, current_max = target_audience["age_range"]
                
                # ปรับช่วงอายุให้ใกล้เคียงกับกลุ่มที่มีประสิทธิภาพสูงสุด
                optimized_audience["age_range"] = [
                    max(current_min, age_min - 5),
                    min(current_max, age_max + 5)
                ]
        
        # ปรับปรุงเพศ
        if "gender" in target_audience and performance:
            gender_performance = performance.get("gender_performance", {})
            
            if gender_performance:
                best_gender = max(gender_performance.items(), key=lambda x: x[1])[0]
                
                # หากเพศใดเพศหนึ่งมีประสิทธิภาพสูงกว่าอีกเพศมาก ให้เน้นเพศนั้น
                if gender_performance.get(best_gender, 0) > 2 * gender_performance.get("other", 0):
                    optimized_audience["gender"] = [best_gender]
        
        # ปรับปรุงความสนใจ
        if "interests" in target_audience and performance:
            interest_performance = performance.get("interest_performance", {})
            
            if interest_performance:
                # เรียงลำดับความสนใจตามประสิทธิภาพ
                sorted_interests = sorted(interest_performance.items(), key=lambda x: x[1], reverse=True)
                
                # เลือกความสนใจที่มีประสิทธิภาพสูงสุด 5 อันดับแรก
                top_interests = [interest for interest, _ in sorted_interests[:5]]
                
                # รวมความสนใจที่มีประสิทธิภาพสูงสุดกับความสนใจเดิม
                optimized_audience["interests"] = list(set(top_interests + target_audience["interests"]))
        
        # ปรับปรุงตำแหน่งที่ตั้ง
        if "locations" in target_audience and performance:
            location_performance = performance.get("location_performance", {})
            
            if location_performance:
                # เรียงลำดับตำแหน่งที่ตั้งตามประสิทธิภาพ
                sorted_locations = sorted(location_performance.items(), key=lambda x: x[1], reverse=True)
                
                # เลือกตำแหน่งที่ตั้งที่มีประสิทธิภาพสูงสุด 3 อันดับแรก
                top_locations = [location for location, _ in sorted_locations[:3]]
                
                # รวมตำแหน่งที่ตั้งที่มีประสิทธิภาพสูงสุดกับตำแหน่งที่ตั้งเดิม
                optimized_audience["locations"] = list(set(top_locations + target_audience["locations"]))
        
        logger.info(f"Optimized target audience: {optimized_audience}")
        return {"optimized_audience": optimized_audience}
    
    def generate_audience_insights(self, audience_data: Dict) -> Dict:
        """
        สร้างข้อมูลเชิงลึกเกี่ยวกับกลุ่มเป้าหมาย
        
        Args:
            audience_data: ข้อมูลกลุ่มเป้าหมาย
            
        Returns:
            Dict: ข้อมูลเชิงลึกเกี่ยวกับกลุ่มเป้าหมาย
        """
        logger.info(f"Generating audience insights: {audience_data}")
        
        # ตรวจสอบข้อมูลกลุ่มเป้าหมาย
        if not audience_data:
            return {"error": "Invalid audience data"}
        
        insights = {}
        
        # วิเคราะห์ข้อมูลประชากรศาสตร์
        if "demographics" in audience_data:
            demographics = audience_data["demographics"]
            
            # วิเคราะห์อายุ
            if "age" in demographics:
                age_data = demographics["age"]
                insights["age"] = {
                    "most_common": max(age_data.items(), key=lambda x: x[1])[0],
                    "distribution": age_data
                }
            
            # วิเคราะห์เพศ
            if "gender" in demographics:
                gender_data = demographics["gender"]
                insights["gender"] = {
                    "most_common": max(gender_data.items(), key=lambda x: x[1])[0],
                    "distribution": gender_data
                }
            
            # วิเคราะห์รายได้
            if "income" in demographics:
                income_data = demographics["income"]
                insights["income"] = {
                    "most_common": max(income_data.items(), key=lambda x: x[1])[0],
                    "distribution": income_data
                }
        
        # วิเคราะห์ความสนใจ
        if "interests" in audience_data:
            interests = audience_data["interests"]
            
            # เรียงลำดับความสนใจตามความนิยม
            sorted_interests = sorted(interests.items(), key=lambda x: x[1], reverse=True)
            
            insights["interests"] = {
                "top_5": [interest for interest, _ in sorted_interests[:5]],
                "distribution": interests
            }
        
        # วิเคราะห์พฤติกรรม
        if "behaviors" in audience_data:
            behaviors = audience_data["behaviors"]
            
            # เรียงลำดับพฤติกรรมตามความนิยม
            sorted_behaviors = sorted(behaviors.items(), key=lambda x: x[1], reverse=True)
            
            insights["behaviors"] = {
                "top_5": [behavior for behavior, _ in sorted_behaviors[:5]],
                "distribution": behaviors
            }
        
        # วิเคราะห์ตำแหน่งที่ตั้ง
        if "locations" in audience_data:
            locations = audience_data["locations"]
            
            # เรียงลำดับตำแหน่งที่ตั้งตามความนิยม
            sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
            
            insights["locations"] = {
                "top_3": [location for location, _ in sorted_locations[:3]],
                "distribution": locations
            }
        
        # สร้างคำแนะนำ
        recommendations = []
        
        # คำแนะนำตามอายุ
        if "age" in insights:
            most_common_age = insights["age"]["most_common"]
            
            if "18-24" in most_common_age:
                recommendations.append("เน้นการโฆษณาบน TikTok และ Instagram สำหรับกลุ่มอายุน้อย")
            elif "25-34" in most_common_age:
                recommendations.append("เน้นการโฆษณาบน Facebook และ Instagram สำหรับกลุ่มวัยทำงาน")
            elif "35-44" in most_common_age:
                recommendations.append("เน้นการโฆษณาบน Facebook และ YouTube สำหรับกลุ่มวัยทำงานตอนกลาง")
            else:
                recommendations.append("เน้นการโฆษณาบน Facebook สำหรับกลุ่มอายุมากกว่า 45 ปี")
        
        # คำแนะนำตามเพศ
        if "gender" in insights:
            most_common_gender = insights["gender"]["most_common"]
            
            if most_common_gender == "male":
                recommendations.append("เน้นเนื้อหาเกี่ยวกับการฝึกทักษะและการต่อสู้สำหรับกลุ่มผู้ชาย")
            elif most_common_gender == "female":
                recommendations.append("เน้นเนื้อหาเกี่ยวกับการลดน้ำหนักและการออกกำลังกายสำหรับกลุ่มผู้หญิง")
        
        # คำแนะนำตามความสนใจ
        if "interests" in insights:
            top_interests = insights["interests"]["top_5"]
            
            if "fitness" in top_interests:
                recommendations.append("เน้นเนื้อหาเกี่ยวกับประโยชน์ของมวยไทยต่อสุขภาพและการออกกำลังกาย")
            
            if "weight_loss" in top_interests:
                recommendations.append("เน้นเนื้อหาเกี่ยวกับการลดน้ำหนักด้วยมวยไทยและผลลัพธ์ที่เห็นได้ชัด")
            
            if "martial_arts" in top_interests:
                recommendations.append("เน้นเนื้อหาเกี่ยวกับเทคนิคและทักษะมวยไทย")
            
            if "thai_culture" in top_interests:
                recommendations.append("เน้นเนื้อหาเกี่ยวกับวัฒนธรรมและประวัติศาสตร์ของมวยไทย")
        
        insights["recommendations"] = recommendations
        
        logger.info(f"Audience insights: {insights}")
        return insights
