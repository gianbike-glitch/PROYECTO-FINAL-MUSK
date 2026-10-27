def calculate_total(importes):
    return sum(importes)

def calculate_average(importes):
    if len(importes) == 0:
        return 0
    total = calculate_total(importes)
    media = total/len(importes)
    return media