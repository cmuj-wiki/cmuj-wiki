# 🚀 Quiz System - Quick Start Guide

## ✅ System is Ready!

Everything is built and working. Here's what you need to know.

---

## 📦 What Was Built

1. **MkDocs Plugin** - Compiles quizzes automatically during build
2. **Markdown Format** - Students write `[x]` for correct answers
3. **Image Quiz Support** - Drop images + answers.txt in folder
4. **Validation Script** - Check format before committing
5. **Documentation** - Complete student guide with examples

---

## 🎯 Test It Now

### 1. Build the site:
```bash
mkdocs build
```

You should see:
```
✓ Compiled quiz: anatomia-osteologia.md
✓ Compiled quiz: biochemia-bialka.md
✓ Compiled image quiz: histologia-zestaw-demo (15 slides)
```

### 2. Serve locally:
```bash
mkdocs serve
```

Visit: `http://localhost:8000/testy/sesja.html?quiz=anatomia-osteologia`

You should see the quiz load and work perfectly!

### 3. Validate quizzes:
```bash
python3 scripts/validate_quizzes.py
```

You should see:
```
✅ All quizzes valid!
```

---

## 📝 Tell Students

**For students to add new quizzes:**

1. **Read:** [docs/testy/quizzes/README.md](docs/testy/quizzes/README.md)
2. **Copy:** `docs/testy/quizzes/_TEMPLATE.md`
3. **Edit:** Use `[x]` for correct answers
4. **Commit:** Everything else is automatic!

---

## 🔄 Migration Path

### Phase 1: Verify (Now)
- [x] Plugin builds quizzes ✓
- [x] Validation works ✓
- [x] Examples created ✓
- [ ] Test in production (after deploy)

### Phase 2: Expand (Next)
- [ ] Add GitHub Actions validation
- [ ] Create 2-3 more quiz examples
- [ ] Announce to students
- [ ] Update main quiz index page

### Phase 3: Migrate (Later)
- [ ] Convert hardcoded quizzes to new format
- [ ] Remove old QUIZ_DATA
- [ ] Clean up old code

---

## 🎓 GitHub Actions (Optional but Recommended)

Add `.github/workflows/validate-quizzes.yml`:

```yaml
name: Validate Quizzes

on:
  pull_request:
    paths:
      - 'docs/testy/quizzes/**'
  push:
    paths:
      - 'docs/testy/quizzes/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .

      - name: Validate quiz format
        run: python3 scripts/validate_quizzes.py
```

This will:
- ✅ Check quiz format on every PR
- ✅ Show errors before merge
- ✅ Prevent broken quizzes from going live

---

## 📊 Example Quiz Page

Create `docs/testy/nowy-quiz.md`:

```markdown
# Test anatomii

Sprawdź swoją wiedzę z anatomii!

<div id="quiz-session-container"></div>

<script>
  // Load quiz when page loads
  document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (!urlParams.has('quiz')) {
      window.location.href = 'sesja.html?quiz=anatomia-osteologia';
    }
  });
</script>
```

Or simpler - just link from index:
```markdown
[Rozwiąż quiz z anatomii](sesja.html?quiz=anatomia-osteologia)
```

---

## 🐛 Common Issues

### "Plugin not found"
```bash
pip install -e .
```

### "Quiz not loading"
Check:
1. JSON exists: `ls docs/assets/quiz-data/`
2. Build succeeded: `mkdocs build`
3. Browser console for errors

### "Validation fails"
```bash
python3 scripts/validate_quizzes.py path/to/quiz.md
```

Read error message carefully - it shows line numbers!

---

## 📁 Key Files

**For you:**
- `plugins/quiz_builder/__init__.py` - Plugin code
- `docs/javascripts/quiz-engine.js` - Frontend (updated)
- `scripts/validate_quizzes.py` - Validation
- `mkdocs.yml` - Plugin registered here
- `setup.py` - Plugin installation

**For students:**
- `docs/testy/quizzes/README.md` - Instructions
- `docs/testy/quizzes/_TEMPLATE.md` - Template
- `docs/testy/quizzes/anatomia-osteologia.md` - Example

**Auto-generated:**
- `docs/assets/quiz-data/*.json` - Compiled quizzes

---

## 🎯 Next Steps

### Immediate:
1. **Test locally** - Build and serve
2. **Deploy to GitHub Pages** - Push to main
3. **Test live** - Visit quiz page

### Soon:
4. **Add GitHub Actions** - Auto-validate PRs
5. **Update quiz index** - List new quizzes
6. **Announce to students** - Share documentation

### Later:
7. **Create more examples** - 5-10 quizzes
8. **Migrate old quizzes** - Convert hardcoded ones
9. **Collect feedback** - Improve based on usage

---

## 💡 Pro Tips

### For Best Results:
- ✅ Enable GitHub Actions validation
- ✅ Create 3-5 example quizzes first
- ✅ Have one student test the flow
- ✅ Update quiz index page
- ✅ Pin README in quiz folder

### For Students:
- ✅ Show them the template
- ✅ Point to examples
- ✅ Emphasize the `[x]` syntax
- ✅ Tell them about GitHub preview
- ✅ Encourage them to validate locally (optional)

---

## 🎉 You're Done!

The system is:
- ✅ **Built** - Plugin + validation + docs
- ✅ **Tested** - 3 example quizzes work
- ✅ **Documented** - Students have clear guide
- ✅ **Scalable** - Add unlimited quizzes
- ✅ **Maintainable** - You built it once!

**Now just deploy and let students start adding quizzes!**

---

## 📞 Quick Reference

```bash
# Build
mkdocs build

# Serve
mkdocs serve

# Validate
python3 scripts/validate_quizzes.py

# Validate specific quiz
python3 scripts/validate_quizzes.py docs/testy/quizzes/my-quiz.md

# Check JSON output
cat docs/assets/quiz-data/quiz-name.json

# Re-install plugin (if needed)
pip install -e .
```

---

**System is production-ready. Deploy and announce to students!** 🚀
