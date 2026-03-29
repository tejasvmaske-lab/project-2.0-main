# Flask-Babel Translation Guide

## Setup Complete! ✅

Your app is now configured for multi-language support with **English, Hindi, and Marathi**.

---

## How the Translation System Works

### 1. **Language Configuration** (in `app.py`)
```python
app.config['LANGUAGES'] = {
    'en': 'English',
    'hi': 'हिंदी',
    'mr': 'मराठी'
}
```

### 2. **Switching Languages**
Users can switch languages by clicking links:
```html
<!-- Language Switcher -->
<a href="/set_language/en">English</a>
<a href="/set_language/hi">हिंदी</a>
<a href="/set_language/mr">मराठी</a>
```

The choice is saved in a cookie for 1 year.

---

## How to Add Translations

### Step 1: Mark Strings in Python (`app.py`)
Use `gettext()` or `lazy_gettext()`:

```python
from flask_babel import gettext, lazy_gettext

# Example in route
flash(gettext('Product added successfully'), 'success')

# For lazy evaluation (recommended for module level)
message = lazy_gettext('Welcome to Inventory Management')
```

### Step 2: Mark Strings in Templates (HTML)
Use the `{{ _() }}` filter:

```html
<!-- In your .html files -->
<h1>{{ _('Admin Dashboard') }}</h1>
<p>{{ _('Manage your inventory efficiently') }}</p>

<!-- With variables -->
<p>{{ _('Product %(name)s added', name=product.name) }}</p>
```

### Step 3: Extract Translatable Strings
```bash
cd c:\Users\hp\Desktop\project-2.0-main
pybabel extract -F babel.cfg -o messages.pot .
```

### Step 4: Update Translation Files
```bash
pybabel update -i messages.pot -d translations
```

This updates the `.po` files with new strings to translate.

### Step 5: Add Translations
Edit these files and add translations:
- `translations/hi/LC_MESSAGES/messages.po` (Hindi)
- `translations/mr/LC_MESSAGES/messages.po` (Marathi)

#### Example `.po` file format:
```po
#: app.py:199
msgid "Error: Cannot connect to database"
msgstr "त्रुटि: डेटाबेस से कनेक्ट नहीं हो सके"
```

### Step 6: Compile Translations
```bash
pybabel compile -d translations
```

This creates `.mo` files that Flask uses at runtime.

---

## Quick Workflow: Add New Translations

1. **Mark string in code/template** with `gettext()` or `{{ _() }}`
2. **Extract**: `pybabel extract -F babel.cfg -o messages.pot .`
3. **Update**: `pybabel update -i messages.pot -d translations`
4. **Edit**: Open `.po` files and add Hindi/Marathi translations
5. **Compile**: `pybabel compile -d translations`
6. **Restart** Flask app
7. **Test** by switching languages

---

## Example: Add Dashboard Translations

### 1. In `templates/admin_dashboard.html`, change:
```html
<!-- BEFORE -->
<h1>📦 Admin Dashboard</h1>

<!-- AFTER -->
<h1>{{ _('📦 Admin Dashboard') }}</h1>
```

### 2. Extract strings:
```bash
pybabel extract -F babel.cfg -o messages.pot .
```

### 3. Update translations:
```bash
pybabel update -i messages.pot -d translations
```

### 4. Edit `translations/hi/LC_MESSAGES/messages.po`:
```po
msgid "📦 Admin Dashboard"
msgstr "📦 व्यवस्थापक डैशबोर्ड"
```

### 5. Edit `translations/mr/LC_MESSAGES/messages.po`:
```po
msgid "📦 Admin Dashboard"
msgstr "📦 प्रशासक डॅशबोर्ड"
```

### 6. Compile:
```bash
pybabel compile -d translations
```

### 7. Restart Flask and test!

---

## Directory Structure

```
project-2.0-main/
├── app.py                          (Has babel config & routes)
├── babel.cfg                       (Babel configuration)
├── messages.pot                    (Translation template)
├── translations/
│   ├── hi/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po         (Hindi translations - EDIT THIS)
│   │       └── messages.mo         (Compiled - AUTO-GENERATED)
│   └── mr/
│       └── LC_MESSAGES/
│           ├── messages.po         (Marathi translations - EDIT THIS)
│           └── messages.mo         (Compiled - AUTO-GENERATED)
└── templates/
    ├── admin_dashboard.html        (Needs {{ _() }} filters)
    ├── employee_dashboard.html     (Needs {{ _() }} filters)
    ├── products.html               (Needs {{ _() }} filters)
    └── ...
```

---

## Common Hindi/Marathi Translations

| English | हिंदी | मराठी |
|---------|------|-------|
| Add Product | उत्पाद जोड़ें | उत्पाद जोडा |
| View Products | उत्पाद देखें | उत्पाद पहा |
| Sold | बेचा गया | विकले |
| Stock | स्टॉक | स्टॉक |
| Category | श्रेणी | श्रेणी |
| Price | कीमत | किंमत |
| Quantity | मात्रा | प्रमाण |
| Dashboard | डैशबोर्ड | डॅशबोर्ड |
| Error | त्रुटि | त्रुटी |
| Success | सफलता | यश |
| Save | सहेजें | जतन |
| Delete | हटाएं | हटवा |
| Edit | संपादित करें | संपादन |

---

## Tips & Best Practices

1. **Always use lazy_gettext() for module-level strings** that are evaluated at runtime:
   ```python
   error_message = lazy_gettext('An error occurred')
   ```

2. **Use gettext() for strings evaluated during request**:
   ```python
   @app.route('/test')
   def test():
       flash(gettext('Welcome!'), 'success')
   ```

3. **For template variables**, use format strings:
   ```html
   {{ _('Hello %(name)s', name=user.name) }}
   ```

4. **Don't mark SQL queries or technical strings** for translation - only user-facing text.

5. **Keep translation files updated** by running extract and update commands regularly.

---

## Troubleshooting

**Q: Translations not showing?**
- Did you compile? Run: `pybabel compile -d translations`
- Did you restart Flask? Stop and run `python app.py` again
- Check cookie is set: Look in browser DevTools → Application → Cookies → `lang`

**Q: Missing strings in translation file?**
- Run: `pybabel extract -F babel.cfg -o messages.pot .`
- Then: `pybabel update -i messages.pot -d translations`

**Q: How to add a new language (e.g., Gujarati)?**
1. Add to `app.config['LANGUAGES']`:
   ```python
   'gu': 'ગુજરાતી'
   ```
2. Create catalog: `pybabel init -i messages.pot -d translations -l gu`
3. Add translations to `translations/gu/LC_MESSAGES/messages.po`
4. Compile: `pybabel compile -d translations`

---

## Next Steps

1. ✅ Update all dashboard templates to use `{{ _() }}` filters
2. ✅ Extract all strings: `pybabel extract -F babel.cfg -o messages.pot .`
3. ✅ Update translation files: `pybabel update -i messages.pot -d translations`
4. ✅ Add Hindi and Marathi translations to all strings
5. ✅ Compile: `pybabel compile -d translations`
6. ✅ Add language switcher buttons to your navigation

Happy Translating! 🎉
