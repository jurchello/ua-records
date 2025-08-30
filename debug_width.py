#!/usr/bin/env python3

import sys

# Add the project root to Python path
sys.path.insert(0, "/home/yurii/.local/share/gramps/gramps60/plugins/UARecords")

try:
    from configs.constants import get_person_name_length

    NAME_LENGTH = get_person_name_length()
    WIDTH_PX = NAME_LENGTH * 8

    # Test span_rest calculation
    single_field_width = WIDTH_PX
    LABEL_WIDTH = 100
    SPACING = 10

    for cols in [1, 2, 3, 4, 5]:
        span_width = (single_field_width + LABEL_WIDTH + SPACING) * cols - LABEL_WIDTH - SPACING

except Exception:
    # Fallback values
    NAME_LENGTH = 30
    WIDTH_PX = NAME_LENGTH * 8
