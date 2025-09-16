import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

class GTUAttendanceSystem:
    """
    GTU-specific attendance management system for SEM-3 CSE(DS) students
    Implements all GTU policies, bonus marks, and penalty calculations
    """
    
    def __init__(self):
        # GTU Policy Constants
        self.MIN_ATTENDANCE_EXAM = 70.0  # Minimum for GTU exam eligibility
        self.MIN_ATTENDANCE_MEDICAL = 60.0  # With valid medical certificate
        self.MAX_ATTENDANCE_BONUS = 15  # Maximum attendance bonus marks
        self.FIRST_FOUR_DAYS_BONUS = 4  # Bonus for attending first 4 days
        self.ALL_CLEAR_BONUS = 4  # Additional bonus if all subjects clear
        self.MAX_TOTAL_BONUS = 23  # Maximum possible bonus (15+4+4)
        
        # SEM-3 CSE(DS) Subjects
        self.subjects = {
            "DS": {"name": "Data Structures", "type": "core", "weekly_classes": 4},
            "DBMS": {"name": "Database Management System", "type": "core", "weekly_classes": 4},
            "PS": {"name": "Probability and Statistics", "type": "core", "weekly_classes": 3},
            "DF": {"name": "Digital Fundamentals", "type": "core", "weekly_classes": 4},
            "IC": {"name": "Indian Constitution", "type": "elective", "weekly_classes": 2},
            "PCE": {"name": "Professional Communication and Ethics", "type": "elective", "weekly_classes": 2}
        }
        
        # Division System
        self.divisions = {
            "DIV-9": {"roll_range": (1, 35), "name": "Division 9"},
            "DIV-10": {"roll_range": (36, 69), "name": "Division 10"}
        }

    def calculate_current_status(self, current_attendance: float, total_classes: int, attended_classes: int) -> Dict[str, Any]:
        """Calculate current attendance status and eligibility"""
        
        status = {
            "current_attendance": current_attendance,
            "total_classes": total_classes,
            "attended_classes": attended_classes,
            "exam_eligible": current_attendance >= self.MIN_ATTENDANCE_EXAM,
            "bonus_eligible": current_attendance >= self.MIN_ATTENDANCE_EXAM,
            "medical_needed": current_attendance < self.MIN_ATTENDANCE_EXAM,
            "critical_threshold": current_attendance < self.MIN_ATTENDANCE_MEDICAL,
        }
        
        # Calculate attendance bonus marks
        if status["bonus_eligible"]:
            status["attendance_bonus"] = min(
                self.MAX_ATTENDANCE_BONUS,
                int(current_attendance * self.MAX_ATTENDANCE_BONUS / 100)
            )
        else:
            status["attendance_bonus"] = 0
            
        return status

    def calculate_required_attendance(self, current_attendance: float, remaining_classes: int, target_attendance: float = None) -> Dict[str, Any]:
        """Calculate how many classes need to be attended to maintain target percentage"""
        
        if target_attendance is None:
            target_attendance = self.MIN_ATTENDANCE_EXAM
            
        current_total = 100  # Assuming current data is based on 100 total classes for percentage calculation
        current_attended = current_attendance
        
        total_after_remaining = current_total + remaining_classes
        target_total_attended = (target_attendance / 100) * total_after_remaining
        required_additional = max(0, target_total_attended - current_attended)
        
        return {
            "target_attendance": target_attendance,
            "remaining_classes": remaining_classes,
            "required_to_attend": int(math.ceil(required_additional)),
            "can_skip": max(0, remaining_classes - int(math.ceil(required_additional))),
            "final_attendance": ((current_attended + required_additional) / total_after_remaining) * 100,
            "buffer_classes": max(0, remaining_classes - int(math.ceil(required_additional)))
        }

    def calculate_bonus_marks(self, attendance: float, attended_first_four_days: bool = False, all_subjects_clear: bool = False) -> Dict[str, int]:
        """Calculate total bonus marks based on GTU rules"""
        
        bonus_breakdown = {
            "attendance_bonus": 0,
            "first_four_days_bonus": 0,
            "all_clear_bonus": 0,
            "total_bonus": 0
        }
        
        # Attendance bonus (only if >= 70%)
        if attendance >= self.MIN_ATTENDANCE_EXAM:
            bonus_breakdown["attendance_bonus"] = min(
                self.MAX_ATTENDANCE_BONUS,
                int((attendance / 100) * self.MAX_ATTENDANCE_BONUS)
            )
            
            # First four days bonus
            if attended_first_four_days:
                bonus_breakdown["first_four_days_bonus"] = self.FIRST_FOUR_DAYS_BONUS
                
            # All clear bonus (only if other bonuses already applied and all subjects pass)
            if all_subjects_clear and bonus_breakdown["attendance_bonus"] > 0:
                bonus_breakdown["all_clear_bonus"] = self.ALL_CLEAR_BONUS
        
        bonus_breakdown["total_bonus"] = sum([
            bonus_breakdown["attendance_bonus"],
            bonus_breakdown["first_four_days_bonus"],
            bonus_breakdown["all_clear_bonus"]
        ])
        
        return bonus_breakdown

    def generate_attendance_strategy(self, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimal attendance strategy based on current status and GTU rules"""
        
        current_attendance = current_data.get("current_attendance", 72.0)
        remaining_weeks = current_data.get("remaining_weeks", 10)
        preferences = current_data.get("preferences", {})
        
        # Calculate total remaining classes (assuming 19 classes per week based on timetable)
        total_remaining_classes = remaining_weeks * 19
        
        # Different scenarios
        scenarios = {
            "maintain_current": self.calculate_required_attendance(current_attendance, total_remaining_classes, current_attendance),
            "safe_buffer": self.calculate_required_attendance(current_attendance, total_remaining_classes, 75.0),
            "bonus_optimization": self.calculate_required_attendance(current_attendance, total_remaining_classes, 80.0),
            "minimum_safe": self.calculate_required_attendance(current_attendance, total_remaining_classes, 70.1)
        }
        
        # Generate recommendations
        recommendations = self._generate_subject_specific_strategy(current_data, scenarios)
        
        return {
            "current_status": self.calculate_current_status(current_attendance, 100, int(current_attendance)),
            "scenarios": scenarios,
            "recommendations": recommendations,
            "bonus_potential": self.calculate_bonus_marks(current_attendance, True, True),
            "warnings": self._generate_warnings(current_attendance),
            "gtu_policies": self._get_gtu_policy_summary()
        }

    def _generate_subject_specific_strategy(self, current_data: Dict[str, Any], scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Generate subject-specific attendance strategy"""
        
        preferences = current_data.get("preferences", {})
        liked_subjects = preferences.get("liked", ["DS", "DBMS"])  # Default based on your preferences
        disliked_subjects = preferences.get("disliked", ["IC", "PCE"])  # Default based on your preferences
        
        strategy = {
            "priority_subjects": {},
            "flexible_subjects": {},
            "skip_recommendations": {}
        }
        
        # Prioritize liked subjects for higher attendance
        for subject in liked_subjects:
            if subject in self.subjects:
                strategy["priority_subjects"][subject] = {
                    "name": self.subjects[subject]["name"],
                    "recommendation": "Attend all classes",
                    "target_attendance": "90%+",
                    "reason": "Favorite subject + Better understanding + Higher bonus potential"
                }
        
        # Strategic attendance for disliked subjects
        for subject in disliked_subjects:
            if subject in self.subjects:
                strategy["flexible_subjects"][subject] = {
                    "name": self.subjects[subject]["name"],
                    "recommendation": "Maintain minimum 70%",
                    "target_attendance": "70-75%",
                    "reason": "Meet requirements while minimizing time in disliked subjects"
                }
                
        return strategy

    def _generate_warnings(self, current_attendance: float) -> List[str]:
        """Generate warnings based on current attendance"""
        
        warnings = []
        
        if current_attendance < self.MIN_ATTENDANCE_MEDICAL:
            warnings.append("🚨 CRITICAL: Below 60% - Exam eligibility at risk even with medical certificate!")
            
        elif current_attendance < self.MIN_ATTENDANCE_EXAM:
            warnings.append("⚠️ WARNING: Below 70% - Need medical certificate or immediate improvement!")
            
        elif current_attendance < 75:
            warnings.append("⚠️ CAUTION: Close to danger zone - Monitor carefully and maintain buffer")
            
        if current_attendance >= self.MIN_ATTENDANCE_EXAM:
            warnings.append("✅ SAFE: Currently eligible for exams and bonus marks")
            
        return warnings

    def _get_gtu_policy_summary(self) -> Dict[str, str]:
        """Return summary of key GTU policies"""
        
        return {
            "minimum_exam_eligibility": "70% mandatory for GTU exams",
            "medical_relaxation": "60% minimum with valid 14+ day medical certificate",
            "bonus_structure": "Up to 15 marks for attendance + 4 for first 4 days + 4 if all clear",
            "late_penalty": "More than 5 minutes late = absent",
            "proxy_penalty": "Strictly punished, can lose all bonus marks",
            "form_deadline": "Must maintain 70% until GTU form submission",
            "final_deadline": "Must maintain 70% until end of teaching"
        }

def analyze_student_situation(roll_number: int, current_attendance: float = 72.0) -> Dict[str, Any]:
    """Analyze specific student situation with GTU rules"""
    
    gtu_system = GTUAttendanceSystem()
    
    # Determine division
    division = "DIV-9" if roll_number <= 35 else "DIV-10"
    
    current_data = {
        "roll_number": roll_number,
        "division": division,
        "current_attendance": current_attendance,
        "remaining_weeks": 10,  # Estimated remaining weeks in semester
        "preferences": {
            "liked": ["DS", "DBMS", "PS"],  # Based on your preferences
            "disliked": ["IC", "PCE"]  # Based on your preferences
        }
    }
    
    return gtu_system.generate_attendance_strategy(current_data)

# Example usage for your current situation
if __name__ == "__main__":
    # Your current situation: 72% attendance
    result = analyze_student_situation(roll_number=25, current_attendance=72.0)
    
    print("=== GTU ATTENDANCE ANALYSIS ===")
    print(f"Current Status: {result['current_status']}")
    print(f"Bonus Potential: {result['bonus_potential']}")
    print("Warnings:", "\n".join(result['warnings']))
    print("\n=== SCENARIOS ===")
    for scenario_name, scenario_data in result['scenarios'].items():
        print(f"{scenario_name}: Need to attend {scenario_data['required_to_attend']} out of {scenario_data['remaining_classes']} remaining classes")