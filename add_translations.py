#!/usr/bin/env python3
"""
Script to add remaining Hindi and Marathi translations to .po files
"""

import re

# All translations for remaining strings
translations = {
    "Hindi": {
        "🌙 Dark Mode": "🌙 डार्क मोड",
        "Scan with Camera": "कैमरे से स्कैन करें",
        "Enter Barcode Manually": "मैनुअली बारकोड दर्ज करें",
        "Start Camera": "कैमरा शुरू करें",
        "Stop Camera": "कैमरा बंद करें",
        "Enter Barcode Number *": "बारकोड संख्या दर्ज करें *",
        "Scan or type barcode...": "बारकोड स्कैन या टाइप करें...",
        "Search Product": "उत्पाद खोजें",
        "📷 Barcode Scanner": "📷 बारकोड स्कैनर",
        "📦 Product Found": "📦 उत्पाद मिल गया",
        "Product Name:": "उत्पाद का नाम:",
        "SKU:": "SKU:",
        "Category:": "श्रेणी:",
        "Price:": "मूल्य:",
        "Quantity:": "मात्रा:",
        "Shelf Number:": "शेल्फ संख्या:",
        "Reorder Level:": "पुनः ऑर्डर स्तर:",
        "Stock Action": "स्टॉक क्रिया",
        "Quantity *": "मात्रा *",
        "💰 SELL PRODUCT": "💰 उत्पाद बेचें",
        "📥 BUY PRODUCT": "📥 उत्पाद खरीदें",
        "Back to Products": "उत्पादों पर वापस",
        "🔄 Returns Management": "🔄 रिटर्न प्रबंधन",
        "Process Return": "रिटर्न को संसाधित करें",
        "📦 Product Found - Enter Return Quantity": "📦 उत्पाद मिल गया - वापसी मात्रा दर्ज करें",
        "Return Quantity *": "वापसी मात्रा *",
        "Quick Stock Action": "तेजी से स्टॉक क्रिया",
        "Recent Returns (Last 50)": "हाल की वापसियां (अंतिम 50)",
        "Date & Time": "तारीख और समय",
        "No returns yet. Scan a product barcode to process a return.": "अभी तक कोई रिटर्न नहीं हैं। रिटर्न को संसाधित करने के लिए एक उत्पाद बारकोड स्कैन करें।",
        "← Back to Products": "← उत्पादों पर वापस",
        "📊 Stock Movement History": "📊 स्टॉक आंदोलन इतिहास",
        "Complete audit trail of all inventory operations (BUY, SELL, RETURN)": "सभी इन्वेंटरी संचालन का पूर्ण ऑडिट ट्रेल (खरीद, बिक्री, रिटर्न)",
        "Buy Operations": "खरीद संचालन",
        "Sell Operations": "बिक्री संचालन",
        "Return Operations": "रिटर्न संचालन",
        "Total Operations": "कुल संचालन",
        "All time": "सभी समय",
        "items": "आइटम",
        "Product SKU": "उत्पाद SKU",
        "Product Name": "उत्पाद का नाम",
        "Category": "श्रेणी",
        "Operation": "संचालन",
        "Timestamp": "समय",
        "Uncategorized": "अवर्गीकृत",
        "BUY": "खरीद",
        "SELL": "बिक्री",
        "RETURN": "वापसी",
        "No stock movements recorded yet": "अभी तक कोई स्टॉक आंदोलन दर्ज नहीं हुए हैं",
        "Start by adding products and performing buy/sell/return operations": "उत्पाद जोड़कर और खरीद/बिक्री/रिटर्न संचालन करके शुरू करें",
    },
    "Marathi": {
        "🌙 Dark Mode": "🌙 डार्क मोड",
        "Scan with Camera": "कैमेरा असे स्कॅन करा",
        "Enter Barcode Manually": "मॅन्युअली बारकोड प्रविष्ट करा",
        "Start Camera": "कैमेरा सुरु करा",
        "Stop Camera": "कैमेरा बंद करा",
        "Enter Barcode Number *": "बारकोड क्रमांक प्रविष्ट करा *",
        "Scan or type barcode...": "बारकोड स्कॅन किंवा टाइप करा...",
        "Search Product": "उत्पाद शोधा",
        "📷 Barcode Scanner": "📷 बारकोड स्कॅनर",
        "📦 Product Found": "📦 उत्पाद आढळले",
        "Product Name:": "उत्पाद नाव:",
        "SKU:": "SKU:",
        "Category:": "श्रेणी:",
        "Price:": "किंमत:",
        "Quantity:": "प्रमाण:",
        "Shelf Number:": "शेल्फ क्रमांक:",
        "Reorder Level:": "पुनःऑर्डर स्तर:",
        "Stock Action": "स्टॉक क्रिया",
        "Quantity *": "प्रमाण *",
        "💰 SELL PRODUCT": "💰 उत्पाद विक्रय करा",
        "📥 BUY PRODUCT": "📥 उत्पाद खरेदी करा",
        "Back to Products": "उत्पादांत परत जा",
        "🔄 Returns Management": "🔄 परत व्यवस्थापन",
        "Process Return": "परत प्रक्रिया करा",
        "📦 Product Found - Enter Return Quantity": "📦 उत्पाद आढळले - परत प्रमाण प्रविष्ट करा",
        "Return Quantity *": "परत प्रमाण *",
        "Quick Stock Action": "द्रुत स्टॉक क्रिया",
        "Recent Returns (Last 50)": "अलीकडील परत (अंतिम 50)",
        "Date & Time": "तारीख आणि वेळ",
        "No returns yet. Scan a product barcode to process a return.": "अद्याप कोणतीही परत नाही. परत प्रक्रिया करण्यासाठी उत्पाद बारकोड स्कॅन करा.",
        "← Back to Products": "← उत्पादांत परत जा",
        "📊 Stock Movement History": "📊 स्टॉक हालचाल इतिहास",
        "Complete audit trail of all inventory operations (BUY, SELL, RETURN)": "सर्व ऑडिट ट्रेल (खरेदी, विक्रय, परत)",
        "Buy Operations": "खरेदी ऑपरेशन्स",
        "Sell Operations": "विक्रय ऑपरेशन्स",
        "Return Operations": "परत ऑपरेशन्स",
        "Total Operations": "एकूण ऑपरेशन्स",
        "All time": "सर्व वेळ",
        "items": "आयटम",
        "Product SKU": "उत्पाद SKU",
        "Product Name": "उत्पाद नाव",
        "Category": "श्रेणी",
        "Operation": "ऑपरेशन",
        "Timestamp": "टाइमस्टॅम्प",
        "Uncategorized": "अवर्गीकृत",
        "BUY": "खरेदी",
        "SELL": "विक्रय",
        "RETURN": "परत",
        "No stock movements recorded yet": "अद्याप कोणतीही स्टॉक गती रेकॉर्ड केली गेली नाही",
        "Start by adding products and performing buy/sell/return operations": "उत्पाद जोडून आणि खरेदी/विक्रय/परत ऑपरेशन्स करून सुरु करा",
    }
}

def update_po_file(filepath, lang_translations):
    """Update .po file with translations"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace empty msgstr for each translation
    for english, translated in lang_translations.items():
        # Find pattern: msgid "english_text"\nmsgstr ""
        # This is complex due to multiline strings, so we'll do simpler replacements
        pattern = f'msgid "{english}"\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{translated}"'
        content = content.replace(pattern, replacement)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")

# Update Hindi
print("Updating Hindi translations...")
update_po_file("translations/hi/LC_MESSAGES/messages.po", translations["Hindi"])

# Update Marathi  
print("Updating Marathi translations...")
update_po_file("translations/mr/LC_MESSAGES/messages.po", translations["Marathi"])

print("All translations added successfully!")
