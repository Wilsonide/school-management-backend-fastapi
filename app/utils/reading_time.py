def calculate_reading_time(content: str) -> int:
    words = len(content.split())
    return max(1, round(words / 200))  # 200 wpm average