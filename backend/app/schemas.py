from pydantic import BaseModel
from typing import Optional

class StrokeInput(BaseModel):
    chest_pain: int = 0
    shortness_of_breath: int = 0
    irregular_heartbeat: int = 0
    fatigue_weakness: int = 0
    dizziness: int = 0
    swelling_edema: int = 0
    pain_neck_jaw_shoulder_back: int = 0
    excessive_sweating: int = 0
    persistent_cough: int = 0
    nausea_vomiting: int = 0
    high_blood_pressure: int = 0
    chest_discomfort_activity: int = 0
    cold_hands_feet: int = 0
    snoring_sleep_apnea: int = 0
    anxiety_feeling_of_doom: int = 0
    
    # Basic
    age: int
    weight: float | None = None
    height: float | None = None

    # lifestyle (NEW – all optional)
    smoking: int = 0
    alcohol: int = 0
    physical_inactivity: int = 0
    high_salt_diet: int = 0
    poor_sleep: int = 0
    high_stress: int = 0