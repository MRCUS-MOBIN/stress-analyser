"""
Recovery Rules Knowledge Base
Maps detected stress natures, severity levels, and major contributing factors
to evidence-based personalized recovery interventions.
"""

RECOVERY_KNOWLEDGE_BASE = {
    "Academic": [
        {
            "id": "rec_pomodoro",
            "title": "Structured Pomodoro Study & Break Routine",
            "category": "Workload Management",
            "description": "Study in focused 25-minute bursts followed by 5-minute restorative breaks to reduce cognitive fatigue.",
            "estimated_time_mins": 30,
            "base_effectiveness": 8.5
        },
        {
            "id": "rec_prioritization",
            "title": "Eisenhower Matrix Workload Prioritization",
            "category": "Time & Task Strategy",
            "description": "Categorize assignments by urgency and importance to eliminate deadline pressure.",
            "estimated_time_mins": 15,
            "base_effectiveness": 8.0
        },
        {
            "id": "rec_peer_study",
            "title": "Collaborative Peer Study & Clarification",
            "category": "Academic Support",
            "description": "Connect with a classmate to break down difficult assignment concepts into smaller steps.",
            "estimated_time_mins": 45,
            "base_effectiveness": 7.8
        }
    ],
    "Performance": [
        {
            "id": "rec_mock_prep",
            "title": "Guided Exam Visualization & Self-Affirmation",
            "category": "Performance Mindset",
            "description": "Practice 10 minutes of mental simulation for upcoming exams or interviews to reduce anxiety.",
            "estimated_time_mins": 10,
            "base_effectiveness": 8.2
        },
        {
            "id": "rec_box_breathing",
            "title": "4-7-8 Deep Diaphragmatic Box Breathing",
            "category": "Anxiety Reduction",
            "description": "Regulate nervous system arousal before study sessions or mock presentations.",
            "estimated_time_mins": 8,
            "base_effectiveness": 9.0
        },
        {
            "id": "rec_reframing",
            "title": "Cognitive Reframing of Performance Expectations",
            "category": "Mindset Shift",
            "description": "Identify perfectionist thoughts and reframe them into realistic process goals.",
            "estimated_time_mins": 15,
            "base_effectiveness": 7.5
        }
    ],
    "Time-pressure": [
        {
            "id": "rec_time_block",
            "title": "Daily Time-Blocking Schedule",
            "category": "Time Management",
            "description": "Assign realistic dedicated calendar blocks for studying, meals, rest, and sleep.",
            "estimated_time_mins": 15,
            "base_effectiveness": 8.7
        },
        {
            "id": "rec_not_to_do",
            "title": "Distraction Audit & 'Not-To-Do' List",
            "category": "Focus Protection",
            "description": "Eliminate low-priority multitasking activities during high workload windows.",
            "estimated_time_mins": 10,
            "base_effectiveness": 7.9
        }
    ],
    "Sleep-related": [
        {
            "id": "rec_digital_detox",
            "title": "90-Min Pre-Bedtime Digital Screen Wind-Down",
            "category": "Sleep Hygiene",
            "description": "Turn off high-blue-light screens 90 minutes before bedtime to activate melatonin synthesis.",
            "estimated_time_mins": 90,
            "base_effectiveness": 9.2
        },
        {
            "id": "rec_sleep_sanctuary",
            "title": "Consistent Sleep-Wake Cycle & Cool Environment",
            "category": "Circadian Alignment",
            "description": "Go to sleep and wake up at exact set hours to stabilize sleep architecture.",
            "estimated_time_mins": 480,
            "base_effectiveness": 9.0
        },
        {
            "id": "rec_pmr_relaxation",
            "title": "Progressive Muscle Relaxation (PMR)",
            "category": "Body Wind-Down",
            "description": "Systematically tense and release muscle groups before sleep to relieve physical tension.",
            "estimated_time_mins": 15,
            "base_effectiveness": 8.4
        }
    ],
    "Social": [
        {
            "id": "rec_peer_walk",
            "title": "Campus Green Walk with Friend",
            "category": "Social Connection",
            "description": "Take a 20-minute outdoor walk with a friend or peer to share experiences away from screens.",
            "estimated_time_mins": 20,
            "base_effectiveness": 8.8
        },
        {
            "id": "rec_boundary_setting",
            "title": "Healthy Social Boundary Communication",
            "category": "Interpersonal Wellness",
            "description": "Communicate study schedule boundaries respectfully to peers and roommates.",
            "estimated_time_mins": 15,
            "base_effectiveness": 7.6
        }
    ],
    "Mixed": [
        {
            "id": "rec_cardio_exercise",
            "title": "30-Min Aerobic Physical Activity",
            "category": "Physical Wellness",
            "description": "Engage in moderate jogging, swimming, cycling, or gym exercise to release endorphins.",
            "estimated_time_mins": 30,
            "base_effectiveness": 9.1
        },
        {
            "id": "rec_mindful_journal",
            "title": "10-Min Gratitude & Emotional Journaling",
            "category": "Self-Reflection",
            "description": "Express bottled-up thoughts freely in a private journal to process emotional fatigue.",
            "estimated_time_mins": 10,
            "base_effectiveness": 8.3
        }
    ]
}
