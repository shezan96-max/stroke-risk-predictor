def lifestyle_score(symptoms):
    score = 0

    score += symptoms.smoking * 2
    score += symptoms.alcohol * 1
    score += symptoms.physical_inactivity * 2
    score += symptoms.high_salt_diet * 1
    score += symptoms.poor_sleep * 1
    score += symptoms.high_stress * 1

    return score
