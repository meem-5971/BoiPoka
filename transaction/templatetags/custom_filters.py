# transaction/templatetags/custom_filters.py
from django import template

register = template.Library()

# Function to convert English numbers to Bangla numbers
def convert_to_bangla_numbers(value):
    english_to_bangla = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
    return ''.join(english_to_bangla.get(char, char) for char in str(value))

# Registering the filter to be available in templates
register.filter('convert_to_bangla_numbers', convert_to_bangla_numbers)

# Optional: A date format function if needed
def convert_to_bangla_date(value):
    # Example of converting a date to Bangla (modify based on your format)
    bangla_months = {
        'Jan': 'জানু', 'Feb': 'ফেব', 'Mar': 'মার্চ', 'Apr': 'এপ্রিল', 'May': 'মে', 'Jun': 'জুন',
        'Jul': 'জুলাই', 'Aug': 'অগাস্ট', 'Sep': 'সেপ্ট', 'Oct': 'অক্টো', 'Nov': 'নভে', 'Dec': 'ডিসে'
    }
    formatted_date = value.strftime('%d %b %Y')  # Example format: 01 Jan 2024
    date_parts = formatted_date.split()
    bangla_date = f"{convert_to_bangla_numbers(date_parts[0])} {bangla_months.get(date_parts[1], date_parts[1])} {convert_to_bangla_numbers(date_parts[2])}"
    return bangla_date

register.filter('convert_to_bangla_date', convert_to_bangla_date)
