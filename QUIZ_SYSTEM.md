# 🎯 CMUJ Wiki - Modular Quiz System

## Overview

A complete, production-ready quiz system that allows medical students to easily add tests without touching JavaScript. Built once by you, used forever by students.

## ✅ What's Been Built

### 1. **MkDocs Build Plugin** (`plugins/quiz_builder/`)
- **Automatically discovers** quiz markdown files in `docs/testy/quizzes/`
- **Parses and validates** quiz format during build
- **Compiles to optimized JSON** in `docs/assets/quiz-data/`
- **Supports both formats:**
  - Text-based quizzes (markdown with checkboxes)
  - Image-based quizzes (images + answers.txt)
- **Build-time validation** - errors caught before deployment
- **Installed as:** Editable pip package, registered in `mkdocs.yml`

### 2. **Student-Friendly Format** (Markdown + Checkboxes)

**Text Quizzes:**
```markdown
# Anatomy - Bones

## How many bones does an adult have?

- [ ] 204
- [x] 206
- [ ] 208

> Explanation: Adults have 206 bones.
```

**Image Quizzes:**
```
histologia-zestaw-1/
├── images/
│   ├── 1.jpg
│   └── 2.jpg
└── answers.txt  (one answer per line)
```

### 3. **Enhanced quiz-engine.js**
- **Loads JSON dynamically** via fetch API
- **Backward compatible** with hardcoded QUIZ_DATA
- **Auto-detects format** (single vs multiple choice)
- **Seamless integration** with existing UI

### 4. **Validation Script** (`scripts/validate_quizzes.py`)
- **Validates all quizzes** with one command
- **Clear error messages** with line numbers
- **Color-coded output** (errors in red, warnings in yellow)
- **Can run in CI/CD** for automated checks

### 5. **Student Documentation** (`docs/testy/quizzes/README.md`)
- **Beginner-friendly** - no programming knowledge required
- **Step-by-step guide** for adding quizzes
- **Examples and templates** included
- **Troubleshooting section** for common errors

### 6. **Template & Examples**
- `_TEMPLATE.md` - Copy-paste template with inline instructions
- `anatomia-osteologia.md` - Real quiz example (10 questions)
- `biochemia-bialka.md` - Another complete example
- `histologia-zestaw-demo/` - Image quiz example

---

## 🚀 Student Workflow (Ultra Simple!)

1. **Copy template:** `_TEMPLATE.md` → `new-quiz.md`
2. **Edit on GitHub:** Click pencil icon
3. **Write questions:** Use `[x]` for correct answers
4. **Commit:** GitHub builds automatically
5. **Done!** Quiz appears on site

**No local setup required. No code knowledge needed.**

---

## 🔧 Technical Architecture

```
Student edits .md file
         ↓
GitHub commit
         ↓
MkDocs build (GitHub Actions)
         ↓
quiz_builder plugin runs
         ↓
Validates format
         ↓
Compiles to JSON
         ↓
Deploys to GitHub Pages
         ↓
quiz-engine.js fetches JSON
         ↓
Renders interactive quiz
```

---

## 📁 File Structure

```
CMUJ_Wiki/
├── plugins/
│   └── quiz_builder/
│       └── __init__.py          # MkDocs plugin
├── scripts/
│   └── validate_quizzes.py      # Validation script
├── docs/
│   ├── testy/
│   │   └── quizzes/
│   │       ├── _TEMPLATE.md     # Copy this!
│   │       ├── README.md        # Student instructions
│   │       ├── anatomia-osteologia.md
│   │       ├── biochemia-bialka.md
│   │       └── histologia-zestaw-demo/
│   │           ├── images/
│   │           │   └── *.jpg
│   │           └── answers.txt
│   ├── assets/
│   │   └── quiz-data/           # Auto-generated JSON
│   │       ├── anatomia-osteologia.json
│   │       └── ...
│   └── javascripts/
│       └── quiz-engine.js       # Enhanced to load JSON
├── setup.py                     # Plugin installation
└── mkdocs.yml                   # Registered quiz_builder plugin
```

---

## 🎯 Key Design Decisions

### Why Markdown + Checkboxes?
- ✅ **GitHub native** - renders with preview
- ✅ **Intuitive** - `[x]` is obvious
- ✅ **Hard to break** - forgiving syntax
- ✅ **No learning curve** - it's just text

### Why Build-Time Processing?
- ✅ **Validation** - errors caught before deployment
- ✅ **Performance** - pre-compiled JSON is fast
- ✅ **Clean separation** - complexity hidden from students
- ✅ **Professional** - students never see build process

### Why Hybrid Approach?
- ✅ **Backward compatible** - existing quizzes keep working
- ✅ **Gradual migration** - convert quizzes over time
- ✅ **Flexible** - supports both hardcoded and file-based

---

## 🛠️ For You (Maintainer)

### One-Time Setup (Already Done!)

1. **Install plugin:**
   ```bash
   pip install -e .
   ```

2. **Build site:**
   ```bash
   mkdocs build
   ```

3. **Verify:**
   ```bash
   python3 scripts/validate_quizzes.py
   ```

### Adding GitHub Actions (Optional)

Create `.github/workflows/validate-quizzes.yml`:

```yaml
name: Validate Quizzes

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python scripts/validate_quizzes.py
```

This will validate quizzes on every PR and show errors before merge.

---

## 🐛 Troubleshooting

### Plugin not found
```bash
pip install -e .  # Reinstall
```

### Build fails
```bash
mkdocs build 2>&1 | grep -E "(quiz|error)"
```

### Validate specific quiz
```bash
python3 scripts/validate_quizzes.py docs/testy/quizzes/my-quiz.md
```

### Check compiled JSON
```bash
ls docs/assets/quiz-data/
cat docs/assets/quiz-data/quiz-name.json
```

---

## 📊 Current Status

**Working:**
- ✅ MkDocs plugin compiles quizzes
- ✅ Text-based quizzes (markdown format)
- ✅ Image-based quizzes (szkiełka format)
- ✅ Validation script
- ✅ Enhanced quiz-engine.js loads JSON
- ✅ Student documentation
- ✅ Template and examples
- ✅ Backward compatibility

**Built and tested:**
- ✅ `anatomia-osteologia.md` (10 questions)
- ✅ `biochemia-bialka.md` (5 questions)
- ✅ `histologia-zestaw-demo/` (15 images)

---

## 🔮 Future Enhancements (Optional)

### Short-term:
- [ ] GitHub Actions for auto-validation
- [ ] Migrate existing hardcoded quizzes to new format
- [ ] Update testy/index.md to list new quizzes

### Long-term:
- [ ] Quiz metadata (difficulty, tags, semester)
- [ ] Question shuffle/randomization
- [ ] Export quiz results
- [ ] Import from other formats (CSV, Excel)
- [ ] Quiz analytics (most missed questions)

---

## 📝 For Students

**Everything they need:**
- `docs/testy/quizzes/README.md` - Complete guide
- `docs/testy/quizzes/_TEMPLATE.md` - Copy-paste template
- Examples to learn from

**They just need to:**
1. Copy template
2. Edit on GitHub
3. Use `[x]` for correct answers
4. Commit

**You built it. They use it. Everyone wins.**

---

## 🎉 Summary

You've built a **production-ready, scalable quiz system** that:

✅ Requires **zero code knowledge** from students
✅ Validates format **at build time**
✅ Compiles to **optimized JSON**
✅ Supports **two quiz formats** (text + images)
✅ Is **backward compatible**
✅ Has **comprehensive documentation**
✅ Can run in **CI/CD** pipelines
✅ Is **maintenance-free** for you

**Build once, use forever.** ✨

---

## 📞 Quick Commands

```bash
# Build site
mkdocs build

# Serve locally
mkdocs serve

# Validate quizzes
python3 scripts/validate_quizzes.py

# Check specific quiz
python3 scripts/validate_quizzes.py docs/testy/quizzes/quiz-name.md

# Check compiled output
ls docs/assets/quiz-data/
cat docs/assets/quiz-data/anatomia-osteologia.json
```

---

**Built with ❤️ for CMUJ medical students**
