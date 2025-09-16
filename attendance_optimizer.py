import json
import requests
from datetime import datetime, timedelta

# Your current realistic attendance scenario
CURRENT_ATTENDANCE = {
    # Current semester progress (6 weeks completed, 10 weeks remaining)
    "total_classes_completed": 240,
    "attended_classes": 168,  # 70% current attendance
    "current_percentage": 70.0,
    
    # Subject-wise breakdown
    "subject_attendance": {
        # LIKED SUBJECTS (Your favorites)
        "Advanced Mathematics": {
            "total": 20, "attended": 18, "percentage": 90.0,
            "remaining_in_semester": 33, "type": "liked"
        },
        "Computer Networks": {
            "total": 18, "attended": 16, "percentage": 88.9,
            "remaining_in_semester": 30, "type": "liked"
        },
        "Machine Learning": {
            "total": 18, "attended": 17, "percentage": 94.4,
            "remaining_in_semester": 30, "type": "liked"
        },
        "Database Systems": {
            "total": 18, "attended": 17, "percentage": 94.4,
            "remaining_in_semester": 30, "type": "liked"
        },
        "Algorithms": {
            "total": 18, "attended": 16, "percentage": 88.9,
            "remaining_in_semester": 30, "type": "liked"
        },
        
        # PRACTICAL LABS (Liked - hands-on learning)
        "Data Structures Lab": {
            "total": 12, "attended": 12, "percentage": 100.0,
            "remaining_in_semester": 20, "type": "liked"
        },
        "Computer Networks Lab": {
            "total": 12, "attended": 11, "percentage": 91.7,
            "remaining_in_semester": 20, "type": "liked"
        },
        "Machine Learning Lab": {
            "total": 12, "attended": 12, "percentage": 100.0,
            "remaining_in_semester": 20, "type": "liked"
        },
        "Database Systems Lab": {
            "total": 12, "attended": 11, "percentage": 91.7,
            "remaining_in_semester": 20, "type": "liked"
        },
        
        # DISLIKED SUBJECTS (Boring/irrelevant to you)
        "History of India": {
            "total": 18, "attended": 8, "percentage": 44.4,
            "remaining_in_semester": 30, "type": "disliked"
        },
        "Environmental Studies": {
            "total": 16, "attended": 7, "percentage": 43.8,
            "remaining_in_semester": 27, "type": "disliked"
        },
        "Technical Communication": {
            "total": 18, "attended": 10, "percentage": 55.6,
            "remaining_in_semester": 30, "type": "disliked"
        },
        "Physics": {
            "total": 18, "attended": 12, "percentage": 66.7,
            "remaining_in_semester": 30, "type": "disliked"
        },
        "Physics Lab": {
            "total": 12, "attended": 8, "percentage": 66.7,
            "remaining_in_semester": 20, "type": "disliked"
        },
        
        # NEUTRAL/MIXED (Important but not loved)
        "Software Engineering": {
            "total": 18, "attended": 15, "percentage": 83.3,
            "remaining_in_semester": 30, "type": "neutral"
        },
        "Software Engineering Lab": {
            "total": 12, "attended": 10, "percentage": 83.3,
            "remaining_in_semester": 20, "type": "neutral"
        },
        "Project Work": {
            "total": 12, "attended": 6, "percentage": 50.0,
            "remaining_in_semester": 20, "type": "disliked"
        },
        "Seminar": {
            "total": 12, "attended": 4, "percentage": 33.3,
            "remaining_in_semester": 20, "type": "disliked"
        }
    }
}

def calculate_optimal_attendance_strategy():
    """Calculate optimal attendance strategy based on preferences"""
    
    print("🎯 OPTIMAL ATTENDANCE STRATEGY FOR 70.5% MINIMUM")
    print("=" * 60)
    
    # Target minimum attendance
    TARGET_PERCENTAGE = 70.5
    
    # Calculate total semester projection
    total_current_classes = sum(subject["total"] for subject in CURRENT_ATTENDANCE["subject_attendance"].values())
    total_remaining_classes = sum(subject["remaining_in_semester"] for subject in CURRENT_ATTENDANCE["subject_attendance"].values())
    total_semester_classes = total_current_classes + total_remaining_classes
    
    print(f"📊 SEMESTER OVERVIEW:")
    print(f"   Current: {CURRENT_ATTENDANCE['attended_classes']}/{total_current_classes} classes = {CURRENT_ATTENDANCE['current_percentage']}%")
    print(f"   Remaining: {total_remaining_classes} classes")
    print(f"   Total Semester: {total_semester_classes} classes")
    print(f"   Target: {TARGET_PERCENTAGE}% minimum")
    
    # Calculate minimum classes needed overall
    classes_needed_total = (TARGET_PERCENTAGE * total_semester_classes / 100) - CURRENT_ATTENDANCE["attended_classes"]
    classes_needed_total = max(0, int(classes_needed_total))
    
    print(f"   📈 Need to attend: {classes_needed_total} more classes")
    
    # Categorize subjects
    liked_subjects = {}
    disliked_subjects = {}
    neutral_subjects = {}
    
    for subject_name, data in CURRENT_ATTENDANCE["subject_attendance"].items():
        if data["type"] == "liked":
            liked_subjects[subject_name] = data
        elif data["type"] == "disliked":
            disliked_subjects[subject_name] = data
        else:
            neutral_subjects[subject_name] = data
    
    print(f"\n🎓 SUBJECT CATEGORIZATION:")
    print(f"   ❤️  Liked subjects: {len(liked_subjects)}")
    print(f"   😞 Disliked subjects: {len(disliked_subjects)}")
    print(f"   ⚖️  Neutral subjects: {len(neutral_subjects)}")
    
    # Strategy 1: Attend ALL liked subjects, minimum for disliked
    print(f"\n💡 STRATEGY 1: MAXIMIZE LIKED, MINIMIZE DISLIKED")
    print("-" * 50)
    
    liked_remaining = sum(data["remaining_in_semester"] for data in liked_subjects.values())
    liked_attendance_plan = liked_remaining  # Attend all liked classes
    
    print(f"✅ LIKED SUBJECTS (Attend ALL {liked_attendance_plan} classes):")
    for subject, data in liked_subjects.items():
        current_percent = data["percentage"]
        remaining = data["remaining_in_semester"]
        if remaining > 0:
            final_total = data["total"] + remaining
            final_attended = data["attended"] + remaining
            final_percent = (final_attended / final_total) * 100
            print(f"   {subject}: {current_percent:.1f}% → {final_percent:.1f}% (attend all {remaining} classes)")
        else:
            print(f"   {subject}: {current_percent:.1f}% (no remaining classes)")
    
    # Calculate remaining classes needed after attending all liked subjects
    remaining_classes_needed = classes_needed_total - liked_attendance_plan
    remaining_classes_needed = max(0, remaining_classes_needed)
    
    print(f"\n😞 DISLIKED SUBJECTS (Attend minimum {remaining_classes_needed} total):")
    
    # Prioritize disliked subjects by current attendance (lowest first)
    disliked_sorted = sorted(disliked_subjects.items(), key=lambda x: x[1]["percentage"])
    
    classes_allocated = 0
    disliked_plan = {}
    
    for subject, data in disliked_sorted:
        remaining = data["remaining_in_semester"]
        current_percent = data["percentage"]
        
        # Calculate minimum needed for 70.5% in this subject
        total_semester = data["total"] + remaining
        min_needed_for_subject = (70.5 * total_semester / 100) - data["attended"]
        min_needed_for_subject = max(0, int(min_needed_for_subject))
        min_needed_for_subject = min(min_needed_for_subject, remaining)
        
        # Allocate classes based on remaining budget
        if classes_allocated < remaining_classes_needed:
            classes_to_attend = min(min_needed_for_subject, remaining_classes_needed - classes_allocated)
            classes_to_attend = max(classes_to_attend, min_needed_for_subject)  # Ensure subject minimum
        else:
            classes_to_attend = min_needed_for_subject  # Only subject minimum
        
        classes_to_attend = min(classes_to_attend, remaining)
        classes_allocated += classes_to_attend
        disliked_plan[subject] = classes_to_attend
        
        # Calculate final percentage
        final_total = data["total"] + remaining
        final_attended = data["attended"] + classes_to_attend
        final_percent = (final_attended / final_total) * 100
        
        skip_classes = remaining - classes_to_attend
        print(f"   {subject}: {current_percent:.1f}% → {final_percent:.1f}% (attend {classes_to_attend}/{remaining}, skip {skip_classes})")
    
    # Handle neutral subjects
    print(f"\n⚖️ NEUTRAL SUBJECTS (Strategic attendance):")
    for subject, data in neutral_subjects.items():
        remaining = data["remaining_in_semester"]
        current_percent = data["percentage"]
        
        # Attend enough to maintain 75% (between liked and disliked)
        total_semester = data["total"] + remaining
        target_75 = (75 * total_semester / 100) - data["attended"]
        attend_classes = max(0, min(int(target_75), remaining))
        
        final_total = data["total"] + remaining
        final_attended = data["attended"] + attend_classes
        final_percent = (final_attended / final_total) * 100
        
        skip_classes = remaining - attend_classes
        print(f"   {subject}: {current_percent:.1f}% → {final_percent:.1f}% (attend {attend_classes}/{remaining}, skip {skip_classes})")
    
    # Calculate final statistics
    total_attend_plan = (
        liked_attendance_plan + 
        sum(disliked_plan.values()) + 
        sum(max(0, min(int((75 * (data["total"] + data["remaining_in_semester"]) / 100) - data["attended"]), data["remaining_in_semester"])) for data in neutral_subjects.values())
    )
    
    total_skip_plan = total_remaining_classes - total_attend_plan
    final_attendance = CURRENT_ATTENDANCE["attended_classes"] + total_attend_plan
    final_percentage = (final_attendance / total_semester_classes) * 100
    
    print(f"\n🎯 STRATEGY SUMMARY:")
    print(f"   Total remaining classes: {total_remaining_classes}")
    print(f"   Plan to attend: {total_attend_plan} classes")
    print(f"   Can safely skip: {total_skip_plan} classes")
    print(f"   Final attendance: {final_attendance}/{total_semester_classes} = {final_percentage:.1f}%")
    
    if final_percentage >= TARGET_PERCENTAGE:
        print(f"   ✅ SUCCESS: Exceeds {TARGET_PERCENTAGE}% target by {final_percentage - TARGET_PERCENTAGE:.1f}%")
    else:
        print(f"   ❌ WARNING: Falls short by {TARGET_PERCENTAGE - final_percentage:.1f}%")
    
    # Weekly schedule optimization
    print(f"\n📅 WEEKLY SCHEDULE OPTIMIZATION:")
    print("-" * 40)
    
    # Your time preferences
    preferred_times = ["09:00-10:30", "11:00-12:30", "14:00-15:30"]  # Morning and early afternoon
    disliked_times = ["16:00-17:30", "17:30-19:00", "19:00-20:30"]  # Late afternoon/evening
    
    print(f"✅ PRIORITIZE for preferred times ({', '.join(preferred_times)}):")
    for subject in liked_subjects.keys():
        print(f"   • {subject} (attend ALL classes)")
    
    print(f"\n⏰ STRATEGIC ATTENDANCE for disliked times:")
    for subject, attend_count in disliked_plan.items():
        total_remaining = disliked_subjects[subject]["remaining_in_semester"]
        if attend_count < total_remaining:
            skip_count = total_remaining - attend_count
            print(f"   • {subject}: Attend {attend_count}, Skip {skip_count} (skip during late hours)")
    
    # Calculate savings
    total_hours_saved = total_skip_plan * 1.5  # Assuming 1.5 hours per class
    
    print(f"\n💰 TIME SAVINGS:")
    print(f"   Classes you can skip: {total_skip_plan}")
    print(f"   Time saved: ~{total_hours_saved:.0f} hours")
    print(f"   Use this time for: internship, projects, or preferred subject study")
    
    return {
        "strategy": "maximize_liked_minimize_disliked",
        "total_attend": total_attend_plan,
        "total_skip": total_skip_plan,
        "final_percentage": final_percentage,
        "liked_attendance": liked_attendance_plan,
        "disliked_plan": disliked_plan,
        "time_saved_hours": total_hours_saved
    }

if __name__ == "__main__":
    print("🚀 PERSONALIZED ATTENDANCE OPTIMIZATION")
    print("Based on your preferences and current attendance data\n")
    
    strategy = calculate_optimal_attendance_strategy()
    
    print(f"\n" + "=" * 60)
    print("🎊 CONGRATULATIONS! Your optimal strategy is ready!")
    print("This plan ensures 70.5% minimum attendance while maximizing")
    print("time spent in subjects you love and minimizing boring classes.")
    print("=" * 60)