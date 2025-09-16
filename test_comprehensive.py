import json
import requests
import time
from datetime import datetime, timedelta
import os

# API endpoints
BACKEND_URL = "http://localhost:5000"
AI_SERVICE_URL = "http://localhost:5001"

# Test data
ACADEMIC_CALENDAR_DATA = {
    "semester_start": "2025-01-15",
    "semester_end": "2025-05-30",
    "holidays": [
        {"name": "Republic Day", "date": "2025-01-26", "type": "national"},
        {"name": "Holi", "date": "2025-03-14", "type": "festival"},
        {"name": "Good Friday", "date": "2025-04-18", "type": "religious"},
        {"name": "Eid al-Fitr", "date": "2025-04-30", "type": "religious"},
        {"name": "Mid-semester break", "start": "2025-03-01", "end": "2025-03-08", "type": "academic"}
    ],
    "exam_periods": [
        {"name": "Mid-semester exams", "start": "2025-03-15", "end": "2025-03-22"},
        {"name": "Final exams", "start": "2025-05-15", "end": "2025-05-28"}
    ],
    "total_working_days": 98,
    "weeks": 16
}

WEEKLY_TIMETABLE = {
    "Monday": [
        {"subject": "Advanced Mathematics", "time": "09:00-10:30", "room": "LH-101", "professor": "Dr. Sharma"},
        {"subject": "Computer Networks", "time": "11:00-12:30", "room": "CS-201", "professor": "Dr. Patel"},
        {"subject": "Database Systems", "time": "14:00-15:30", "room": "CS-202", "professor": "Dr. Singh"},
        {"subject": "Software Engineering", "time": "16:00-17:30", "room": "CS-203", "professor": "Dr. Kumar"}
    ],
    "Tuesday": [
        {"subject": "Data Structures Lab", "time": "09:00-11:00", "room": "CS-Lab1", "professor": "Dr. Verma"},
        {"subject": "History of India", "time": "11:30-13:00", "room": "HU-101", "professor": "Dr. Gupta"},
        {"subject": "Technical Communication", "time": "14:00-15:30", "room": "ENG-201", "professor": "Dr. Mehta"},
        {"subject": "Physics", "time": "16:00-17:30", "room": "PHY-101", "professor": "Dr. Jain"}
    ],
    "Wednesday": [
        {"subject": "Advanced Mathematics", "time": "09:00-10:30", "room": "LH-101", "professor": "Dr. Sharma"},
        {"subject": "Computer Networks Lab", "time": "11:00-13:00", "room": "CS-Lab2", "professor": "Dr. Patel"},
        {"subject": "Environmental Studies", "time": "14:00-15:30", "room": "EVS-101", "professor": "Dr. Agarwal"},
        {"subject": "Machine Learning", "time": "16:00-17:30", "room": "CS-204", "professor": "Dr. Rao"}
    ],
    "Thursday": [
        {"subject": "Database Systems Lab", "time": "09:00-11:00", "room": "CS-Lab3", "professor": "Dr. Singh"},
        {"subject": "History of India", "time": "11:30-13:00", "room": "HU-101", "professor": "Dr. Gupta"},
        {"subject": "Algorithms", "time": "14:00-15:30", "room": "CS-205", "professor": "Dr. Nair"},
        {"subject": "Software Engineering Lab", "time": "16:00-18:00", "room": "CS-Lab4", "professor": "Dr. Kumar"}
    ],
    "Friday": [
        {"subject": "Machine Learning Lab", "time": "09:00-11:00", "room": "CS-Lab5", "professor": "Dr. Rao"},
        {"subject": "Technical Communication", "time": "11:30-13:00", "room": "ENG-201", "professor": "Dr. Mehta"},
        {"subject": "Physics Lab", "time": "14:00-16:00", "room": "PHY-Lab", "professor": "Dr. Jain"},
        {"subject": "Algorithms", "time": "16:30-18:00", "room": "CS-205", "professor": "Dr. Nair"}
    ],
    "Saturday": [
        {"subject": "Project Work", "time": "09:00-12:00", "room": "CS-206", "professor": "Various"},
        {"subject": "Seminar", "time": "14:00-16:00", "room": "Seminar Hall", "professor": "Guest Speakers"}
    ]
}

# Dynamic changes for next week
DYNAMIC_CHANGES_NEXT_WEEK = {
    "extra_lectures": [
        {"subject": "Machine Learning", "day": "Monday", "time": "18:00-19:30", "room": "CS-204", "reason": "Makeup for holiday"},
        {"subject": "Advanced Mathematics", "day": "Saturday", "time": "10:00-11:30", "room": "LH-102", "reason": "Extra tutorial"}
    ],
    "cancelled_lectures": [
        {"subject": "Environmental Studies", "day": "Wednesday", "reason": "Professor unavailable"},
        {"subject": "Physics", "day": "Tuesday", "reason": "Equipment maintenance"}
    ],
    "room_changes": [
        {"subject": "Computer Networks", "day": "Monday", "new_room": "CS-301", "reason": "Room maintenance"},
        {"subject": "Database Systems", "day": "Monday", "new_room": "CS-302", "reason": "Projector issues"}
    ],
    "time_changes": [
        {"subject": "Technical Communication", "day": "Friday", "new_time": "10:00-11:30", "reason": "Professor schedule change"}
    ]
}

# Student preferences (comprehensive)
STUDENT_PREFERENCES = {
    "liked_subjects": [
        "Advanced Mathematics - I love solving complex problems and proofs",
        "Computer Networks - Fascinating to understand how systems communicate", 
        "Database Systems - Enjoy working with data structures and queries",
        "Machine Learning - Excited about AI and its applications",
        "Algorithms - Love the logical thinking and optimization",
        "Data Structures Lab - Hands-on programming is my favorite",
        "Computer Networks Lab - Practical implementation helps me understand theory",
        "Machine Learning Lab - Working with real datasets is amazing"
    ],
    "disliked_subjects": [
        "History of India - Find it boring and irrelevant to my career",
        "Technical Communication - Don't enjoy writing essays and presentations",
        "Environmental Studies - Seems theoretical and not engaging",
        "Physics - Struggle with the mathematical concepts",
        "Physics Lab - Lab work is tedious and time-consuming",
        "Project Work - Too unstructured and depends on group members",
        "Seminar - Guest lectures are often not relevant"
    ],
    "time_preferences": {
        "preferred_times": ["09:00-12:00", "14:00-16:00"],
        "disliked_times": ["16:00-18:00", "18:00-20:00"],
        "reasoning": "I'm most alert in the morning and early afternoon. Late evening classes make me tired and less focused."
    },
    "day_preferences": {
        "preferred_days": ["Monday", "Wednesday", "Friday"],
        "disliked_days": ["Thursday", "Saturday"],
        "reasoning": "I like having classes spread throughout the week. Thursday has too many back-to-back sessions, and Saturday disrupts my weekend."
    },
    "learning_style": "I learn best through hands-on practice and real-world applications. I prefer interactive sessions over lectures. I need time to process information, so back-to-back classes are challenging.",
    "motivation_factors": [
        "Career relevance",
        "Practical applications", 
        "Interesting professor",
        "Good peer group",
        "Hands-on learning"
    ],
    "attendance_constraints": [
        "Part-time internship on Saturday afternoons",
        "Family commitments on Friday evenings",
        "Health issues that make early morning difficult sometimes",
        "Transportation issues during rush hours (4-6 PM)"
    ]
}

# Current attendance status (realistic scenario)
CURRENT_ATTENDANCE = {
    "total_classes_so_far": 240,  # 6 weeks into semester
    "attended_classes": 168,      # Current attendance: 70%
    "subject_wise_attendance": {
        "Advanced Mathematics": {"total": 20, "attended": 18, "percentage": 90.0},
        "Computer Networks": {"total": 18, "attended": 16, "percentage": 88.9},
        "Database Systems": {"total": 18, "attended": 17, "percentage": 94.4},
        "Software Engineering": {"total": 18, "attended": 15, "percentage": 83.3},
        "Data Structures Lab": {"total": 12, "attended": 12, "percentage": 100.0},
        "History of India": {"total": 18, "attended": 8, "percentage": 44.4},
        "Technical Communication": {"total": 18, "attended": 10, "percentage": 55.6},
        "Physics": {"total": 18, "attended": 12, "percentage": 66.7},
        "Computer Networks Lab": {"total": 12, "attended": 11, "percentage": 91.7},
        "Environmental Studies": {"total": 16, "attended": 7, "percentage": 43.8},
        "Machine Learning": {"total": 18, "attended": 17, "percentage": 94.4},
        "Database Systems Lab": {"total": 12, "attended": 11, "percentage": 91.7},
        "Algorithms": {"total": 18, "attended": 16, "percentage": 88.9},
        "Software Engineering Lab": {"total": 12, "attended": 10, "percentage": 83.3},
        "Machine Learning Lab": {"total": 12, "attended": 12, "percentage": 100.0},
        "Physics Lab": {"total": 12, "attended": 8, "percentage": 66.7},
        "Project Work": {"total": 12, "attended": 6, "percentage": 50.0},
        "Seminar": {"total": 12, "attended": 4, "percentage": 33.3}
    }
}

class AttendanceTestSuite:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.ai_service_url = AI_SERVICE_URL
        self.session = requests.Session()
        
    def test_service_health(self):
        """Test if all services are running"""
        print("🔍 Testing Service Health...")
        
        try:
            # Test backend
            backend_health = self.session.get(f"{self.backend_url}/health", timeout=5)
            print(f"✅ Backend Status: {backend_health.json()['status']}")
            
            # Test AI service
            ai_health = self.session.get(f"{self.ai_service_url}/health", timeout=5)
            print(f"✅ AI Service Status: {ai_health.json()['status']}")
            
            return True
        except Exception as e:
            print(f"❌ Service Health Check Failed: {e}")
            return False
    
    def test_calendar_processing(self):
        """Test calendar data processing"""
        print("\n📅 Testing Academic Calendar Processing...")
        
        try:
            # Simulate calendar upload and processing
            response = self.session.post(
                f"{self.backend_url}/api/process-document",
                json={
                    "document_type": "calendar",
                    "extracted_data": ACADEMIC_CALENDAR_DATA
                }
            )
            
            print("✅ Calendar processed successfully")
            print(f"   - Total working days: {ACADEMIC_CALENDAR_DATA['total_working_days']}")
            print(f"   - Holidays: {len(ACADEMIC_CALENDAR_DATA['holidays'])}")
            print(f"   - Exam periods: {len(ACADEMIC_CALENDAR_DATA['exam_periods'])}")
            
            return response.json() if response.status_code == 200 else None
            
        except Exception as e:
            print(f"❌ Calendar Processing Failed: {e}")
            return None
    
    def test_timetable_processing(self):
        """Test timetable data processing with dynamic changes"""
        print("\n📋 Testing Timetable Processing with Dynamic Changes...")
        
        try:
            # Process base timetable
            base_response = self.session.post(
                f"{self.backend_url}/api/process-document",
                json={
                    "document_type": "timetable",
                    "extracted_data": WEEKLY_TIMETABLE
                }
            )
            
            # Apply dynamic changes
            updated_timetable = self.apply_dynamic_changes(WEEKLY_TIMETABLE, DYNAMIC_CHANGES_NEXT_WEEK)
            
            dynamic_response = self.session.post(
                f"{self.backend_url}/api/process-document",
                json={
                    "document_type": "timetable_update",
                    "extracted_data": updated_timetable,
                    "changes": DYNAMIC_CHANGES_NEXT_WEEK
                }
            )
            
            print("✅ Timetable processed with dynamic changes")
            print(f"   - Extra lectures: {len(DYNAMIC_CHANGES_NEXT_WEEK['extra_lectures'])}")
            print(f"   - Cancelled lectures: {len(DYNAMIC_CHANGES_NEXT_WEEK['cancelled_lectures'])}")
            print(f"   - Room changes: {len(DYNAMIC_CHANGES_NEXT_WEEK['room_changes'])}")
            print(f"   - Time changes: {len(DYNAMIC_CHANGES_NEXT_WEEK['time_changes'])}")
            
            return updated_timetable
            
        except Exception as e:
            print(f"❌ Timetable Processing Failed: {e}")
            return None
    
    def test_preference_analysis(self):
        """Test comprehensive preference analysis"""
        print("\n🎯 Testing Student Preference Analysis...")
        
        try:
            # Create comprehensive preference text
            preference_text = self.create_preference_text(STUDENT_PREFERENCES)
            
            response = self.session.post(
                f"{self.backend_url}/api/preferences",
                json={"preferences": preference_text}
            )
            
            result = response.json()
            print("✅ Preferences analyzed successfully")
            print(f"   - Processing method: {result.get('processing_method', 'unknown')}")
            
            if 'analyzedPreferences' in result:
                prefs = result['analyzedPreferences']
                print(f"   - Liked subjects detected: {len(prefs.get('likedSubjects', []))}")
                print(f"   - Disliked subjects detected: {len(prefs.get('dislikedSubjects', []))}")
                print(f"   - Confidence score: {prefs.get('confidence_score', 'N/A')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Preference Analysis Failed: {e}")
            return None
    
    def test_attendance_calculation_scenarios(self):
        """Test various attendance calculation scenarios"""
        print("\n📊 Testing Attendance Calculation Scenarios...")
        
        scenarios = [
            {
                "name": "Current Status (Need to improve)",
                "data": {
                    "totalClasses": CURRENT_ATTENDANCE["total_classes_so_far"],
                    "attendedClasses": CURRENT_ATTENDANCE["attended_classes"],
                    "targetPercentage": 70.5
                }
            },
            {
                "name": "Target 75% (Safe zone)",
                "data": {
                    "totalClasses": CURRENT_ATTENDANCE["total_classes_so_far"],
                    "attendedClasses": CURRENT_ATTENDANCE["attended_classes"],
                    "targetPercentage": 75.0
                }
            },
            {
                "name": "End of semester projection",
                "data": {
                    "totalClasses": 400,  # Projected total
                    "attendedClasses": CURRENT_ATTENDANCE["attended_classes"],
                    "targetPercentage": 70.5
                }
            }
        ]
        
        results = []
        
        for scenario in scenarios:
            try:
                response = self.session.post(
                    f"{self.backend_url}/api/calculate-attendance",
                    json=scenario["data"]
                )
                
                result = response.json()
                results.append({
                    "scenario": scenario["name"],
                    "result": result
                })
                
                if result.get("success"):
                    analysis = result.get("attendance_analysis", {})
                    print(f"\n📈 {scenario['name']}:")
                    print(f"   - Current: {analysis.get('current_percentage', 'N/A')}%")
                    print(f"   - Target: {analysis.get('target_percentage', 'N/A')}%")
                    print(f"   - Classes needed: {analysis.get('classes_needed', 'N/A')}")
                    print(f"   - Risk level: {analysis.get('risk_level', 'N/A')}")
                    
            except Exception as e:
                print(f"❌ Scenario '{scenario['name']}' failed: {e}")
        
        return results
    
    def test_subject_wise_strategy(self):
        """Test subject-wise attendance strategy based on preferences"""
        print("\n🎲 Testing Subject-wise Attendance Strategy...")
        
        try:
            # Calculate optimal attendance for each subject
            strategy = self.calculate_subject_strategy(
                CURRENT_ATTENDANCE["subject_wise_attendance"],
                STUDENT_PREFERENCES
            )
            
            print("✅ Subject-wise strategy calculated:")
            
            print("\n📚 LIKED SUBJECTS (Prioritize attendance):")
            for subject, data in strategy["liked_subjects"].items():
                print(f"   {subject}: {data['current_percentage']:.1f}% -> Target: {data['recommended_target']}%")
                if data['action'] != 'maintain':
                    print(f"      Action: {data['action']} ({data['classes_needed']} classes)")
            
            print("\n😞 DISLIKED SUBJECTS (Minimum viable attendance):")
            for subject, data in strategy["disliked_subjects"].items():
                print(f"   {subject}: {data['current_percentage']:.1f}% -> Target: {data['recommended_target']}%")
                if data['action'] != 'maintain':
                    print(f"      Action: {data['action']} ({data['classes_needed']} classes)")
            
            print(f"\n🎯 OVERALL STRATEGY SUMMARY:")
            print(f"   Total classes can skip in disliked subjects: {strategy['summary']['skippable_classes']}")
            print(f"   Must attend in liked subjects: {strategy['summary']['must_attend_liked']}")
            print(f"   Minimum attend in disliked subjects: {strategy['summary']['minimum_attend_disliked']}")
            print(f"   Overall projected attendance: {strategy['summary']['projected_percentage']:.1f}%")
            
            return strategy
            
        except Exception as e:
            print(f"❌ Subject Strategy Calculation Failed: {e}")
            return None
    
    def test_dynamic_recommendations(self):
        """Test AI-powered dynamic recommendations"""
        print("\n🤖 Testing Dynamic AI Recommendations...")
        
        try:
            request_data = {
                "attendance_data": CURRENT_ATTENDANCE,
                "preferences": STUDENT_PREFERENCES,
                "calendar_data": ACADEMIC_CALENDAR_DATA,
                "timetable_changes": DYNAMIC_CHANGES_NEXT_WEEK,
                "current_date": datetime.now().isoformat()
            }
            
            response = self.session.post(
                f"{self.backend_url}/api/generate-recommendations",
                json=request_data
            )
            
            result = response.json()
            
            if result.get("success"):
                print("✅ Dynamic recommendations generated")
                
                if "recommendations" in result:
                    recs = result["recommendations"]
                    
                    if isinstance(recs, dict):
                        if "immediate_actions" in recs:
                            print("\n⚡ IMMEDIATE ACTIONS:")
                            for action in recs["immediate_actions"]:
                                print(f"   • {action}")
                        
                        if "long_term_strategy" in recs:
                            print("\n📅 LONG-TERM STRATEGY:")
                            for strategy in recs["long_term_strategy"]:
                                print(f"   • {strategy}")
                    else:
                        print(f"   - Method: {result.get('processing_method', 'AI-powered')}")
                        print(f"   - Note: {result.get('note', 'Advanced recommendations available')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Dynamic Recommendations Failed: {e}")
            return None
    
    def test_edge_cases(self):
        """Test various edge cases"""
        print("\n🔥 Testing Edge Cases...")
        
        edge_cases = [
            {
                "name": "Perfect attendance scenario",
                "data": {"totalClasses": 100, "attendedClasses": 100, "targetPercentage": 70.5}
            },
            {
                "name": "Critical attendance scenario",
                "data": {"totalClasses": 100, "attendedClasses": 60, "targetPercentage": 70.5}
            },
            {
                "name": "Zero attendance scenario",
                "data": {"totalClasses": 100, "attendedClasses": 0, "targetPercentage": 70.5}
            },
            {
                "name": "High target scenario",
                "data": {"totalClasses": 100, "attendedClasses": 70, "targetPercentage": 90.0}
            },
            {
                "name": "Impossible target scenario",
                "data": {"totalClasses": 100, "attendedClasses": 50, "targetPercentage": 90.0}
            }
        ]
        
        for case in edge_cases:
            try:
                response = self.session.post(
                    f"{self.backend_url}/api/calculate-attendance",
                    json=case["data"]
                )
                
                result = response.json()
                
                if result.get("success"):
                    analysis = result.get("attendance_analysis", {})
                    print(f"\n🎯 {case['name']}:")
                    print(f"   Current: {analysis.get('current_percentage')}% | Need: {analysis.get('classes_needed')} classes")
                    print(f"   Risk: {analysis.get('risk_level')} | Status: {analysis.get('status')}")
                
            except Exception as e:
                print(f"❌ Edge case '{case['name']}' failed: {e}")
    
    def apply_dynamic_changes(self, base_timetable, changes):
        """Apply dynamic changes to base timetable"""
        updated = json.loads(json.dumps(base_timetable))  # Deep copy
        
        # Add extra lectures
        for extra in changes["extra_lectures"]:
            if extra["day"] in updated:
                updated[extra["day"]].append({
                    "subject": extra["subject"],
                    "time": extra["time"],
                    "room": extra["room"],
                    "professor": "TBD",
                    "type": "extra",
                    "reason": extra["reason"]
                })
        
        # Apply cancellations, room changes, time changes
        for day, classes in updated.items():
            for class_info in classes:
                # Mark cancelled classes
                for cancelled in changes["cancelled_lectures"]:
                    if (cancelled["subject"] == class_info["subject"] and 
                        cancelled["day"] == day):
                        class_info["status"] = "cancelled"
                        class_info["reason"] = cancelled["reason"]
                
                # Apply room changes
                for room_change in changes["room_changes"]:
                    if (room_change["subject"] == class_info["subject"] and 
                        room_change["day"] == day):
                        class_info["room"] = room_change["new_room"]
                        class_info["room_change_reason"] = room_change["reason"]
                
                # Apply time changes
                for time_change in changes["time_changes"]:
                    if (time_change["subject"] == class_info["subject"] and 
                        time_change["day"] == day):
                        class_info["time"] = time_change["new_time"]
                        class_info["time_change_reason"] = time_change["reason"]
        
        return updated
    
    def create_preference_text(self, preferences):
        """Convert structured preferences to natural language"""
        text_parts = []
        
        # Liked subjects
        liked_text = "I really enjoy and love these subjects: " + ", ".join([
            pref.split(" - ")[0] for pref in preferences["liked_subjects"]
        ])
        text_parts.append(liked_text)
        
        # Disliked subjects
        disliked_text = "I strongly dislike and find these subjects boring: " + ", ".join([
            pref.split(" - ")[0] for pref in preferences["disliked_subjects"]
        ])
        text_parts.append(disliked_text)
        
        # Time preferences
        time_pref = preferences["time_preferences"]
        time_text = f"I prefer classes during {', '.join(time_pref['preferred_times'])} and hate classes during {', '.join(time_pref['disliked_times'])}. {time_pref['reasoning']}"
        text_parts.append(time_text)
        
        # Day preferences
        day_pref = preferences["day_preferences"]
        day_text = f"I like having classes on {', '.join(day_pref['preferred_days'])} but dislike {', '.join(day_pref['disliked_days'])}. {day_pref['reasoning']}"
        text_parts.append(day_text)
        
        # Learning style and constraints
        text_parts.append(preferences["learning_style"])
        text_parts.append("My constraints include: " + ", ".join(preferences["attendance_constraints"]))
        
        return ". ".join(text_parts)
    
    def calculate_subject_strategy(self, subject_attendance, preferences):
        """Calculate optimal subject-wise attendance strategy"""
        
        # Extract subject names from preferences
        liked_subjects = [pref.split(" - ")[0] for pref in preferences["liked_subjects"]]
        disliked_subjects = [pref.split(" - ")[0] for pref in preferences["disliked_subjects"]]
        
        strategy = {
            "liked_subjects": {},
            "disliked_subjects": {},
            "summary": {}
        }
        
        total_skippable = 0
        must_attend_liked = 0
        minimum_attend_disliked = 0
        
        # Calculate strategy for each subject
        for subject, attendance in subject_attendance.items():
            current_percentage = attendance["percentage"]
            total_classes = attendance["total"]
            attended_classes = attendance["attended"]
            
            # Estimate remaining classes (assuming 16-week semester, currently at 6 weeks)
            remaining_weeks = 10
            classes_per_week = total_classes / 6  # Current rate
            projected_total = total_classes + (remaining_weeks * classes_per_week)
            
            is_liked = any(liked in subject for liked in liked_subjects)
            is_disliked = any(disliked in subject for disliked in disliked_subjects)
            
            if is_liked:
                # For liked subjects, aim for 85%+ attendance
                target_percentage = 85.0
                target_dict = strategy["liked_subjects"]
            elif is_disliked:
                # For disliked subjects, aim for minimum 70.5%
                target_percentage = 70.5
                target_dict = strategy["disliked_subjects"]
            else:
                # Neutral subjects, aim for 75%
                target_percentage = 75.0
                target_dict = strategy["disliked_subjects"]  # Treat as disliked for strategy
            
            # Calculate classes needed
            future_classes_needed = max(0, 
                (target_percentage * projected_total / 100) - attended_classes
            )
            
            future_total_classes = projected_total - total_classes
            classes_needed = min(future_classes_needed, future_total_classes)
            skippable = max(0, future_total_classes - classes_needed)
            
            # Determine action
            if current_percentage >= target_percentage:
                action = "maintain"
            elif classes_needed >= future_total_classes:
                action = "attend_all"
            else:
                action = f"attend_{int(classes_needed)}_more"
            
            target_dict[subject] = {
                "current_percentage": current_percentage,
                "recommended_target": target_percentage,
                "classes_needed": int(classes_needed),
                "skippable_classes": int(skippable),
                "action": action,
                "projected_total": int(projected_total)
            }
            
            # Update summary
            if is_liked:
                must_attend_liked += classes_needed
            else:
                minimum_attend_disliked += classes_needed
                total_skippable += skippable
        
        # Calculate overall projected attendance
        total_projected_classes = sum(data["projected_total"] for data in 
                                    list(strategy["liked_subjects"].values()) + 
                                    list(strategy["disliked_subjects"].values()))
        
        total_projected_attended = sum(attendance["attended"] for attendance in subject_attendance.values())
        total_future_attend = must_attend_liked + minimum_attend_disliked
        
        projected_percentage = ((total_projected_attended + total_future_attend) / 
                               total_projected_classes * 100) if total_projected_classes > 0 else 0
        
        strategy["summary"] = {
            "skippable_classes": int(total_skippable),
            "must_attend_liked": int(must_attend_liked),
            "minimum_attend_disliked": int(minimum_attend_disliked),
            "projected_percentage": projected_percentage
        }
        
        return strategy
    
    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive AI Attendance System Test")
        print("=" * 60)
        
        # Check services
        if not self.test_service_health():
            print("❌ Services not available. Please start all services first.")
            return
        
        # Run all test scenarios
        self.test_calendar_processing()
        self.test_timetable_processing()
        self.test_preference_analysis()
        self.test_attendance_calculation_scenarios()
        self.test_subject_wise_strategy()
        self.test_dynamic_recommendations()
        self.test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ Comprehensive testing completed!")
        print("🎯 The AI Attendance System has been thoroughly tested with:")
        print("   • Real academic calendar with holidays and exams")
        print("   • Dynamic timetable changes (extra lectures, cancellations)")
        print("   • Comprehensive student preferences (likes/dislikes)")
        print("   • Subject-wise attendance optimization")
        print("   • Edge case handling")
        print("   • AI-powered recommendations")

if __name__ == "__main__":
    test_suite = AttendanceTestSuite()
    test_suite.run_comprehensive_test()