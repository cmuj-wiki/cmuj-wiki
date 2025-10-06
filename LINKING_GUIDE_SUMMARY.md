# 🔗 Quiz Linking - Quick Reference for You

## ✅ Recommended Steps - DONE!

All recommended steps are complete:

- ✅ **GitHub Actions** - Auto-validates quizzes on PRs
- ✅ **Quiz index updated** - Shows new quizzes
- ✅ **Linking instructions** - Complete guide for students
- ✅ **Examples created** - 3 working quizzes

---

## 📚 Student Linking Instructions - What They Need to Know

### **For Students Adding Quiz for Etyka (or any subject):**

**Two comprehensive guides created:**

1. **[docs/testy/quizzes/README.md](docs/testy/quizzes/README.md)** - Main quiz creation guide
   - Now includes linking section
   - Quick example for etyka

2. **[docs/testy/quizzes/JAK_DODAC_I_POLACZYC.md](docs/testy/quizzes/JAK_DODAC_I_POLACZYC.md)** - Complete linking guide
   - Step-by-step with etyka example
   - Multiple linking scenarios
   - URL building examples
   - Troubleshooting section

---

## 🎯 Quick Answer: Etyka Quiz Example

**Student wants to add quiz for "Etyka w medycynie":**

### Step 1: Create Quiz File

**Location:** `docs/testy/quizzes/etyka-kazusy-medyczne.md`

```markdown
# Etyka w medycynie - Kazusy medyczne

Quiz sprawdzający znajomość dylematów etycznych.

## Czy lekarz może ujawnić dane pacjenta bez zgody?

- [ ] Tak, zawsze
- [x] Nie, tylko w wyjątkowych przypadkach
- [ ] Tak, jeśli rodzina pyta

> Lekarz objęty jest tajemnicą lekarską.
```

### Step 2: Link on Etyka Page

**Edit:** `docs/semestr-X/etyka.md` (wherever etyka page is)

**Add:**
```markdown
## 📝 Sprawdź swoją wiedzę

[🎯 Rozwiąż quiz - Kazusy medyczne](../testy/sesja.html?quiz=etyka-kazusy-medyczne){: .md-button}
```

### Step 3: Done!

After commit, quiz builds automatically and link works.

---

## 🗂️ File Structure for Reference

```
docs/
├── semestr-X/
│   └── etyka.md                          ← Link from here
└── testy/
    ├── sesja.html                        ← Quiz player page
    ├── index.md                          ← Main quiz list (updated ✅)
    └── quizzes/
        ├── README.md                     ← Creation guide (updated ✅)
        ├── JAK_DODAC_I_POLACZYC.md      ← Linking guide (NEW ✅)
        ├── _TEMPLATE.md                  ← Template to copy
        ├── etyka-kazusy-medyczne.md     ← Student creates this
        ├── anatomia-osteologia.md        ← Example 1
        └── biochemia-bialka.md           ← Example 2
```

---

## 🔗 URL Building Rules (for students)

### Pattern:
```
../testy/sesja.html?quiz=FILENAME-WITHOUT-MD
```

### Examples:

| Quiz File | Link URL |
|-----------|----------|
| `etyka-kazusy-medyczne.md` | `../testy/sesja.html?quiz=etyka-kazusy-medyczne` |
| `fizjologia-serce.md` | `../testy/sesja.html?quiz=fizjologia-serce` |
| `anatomia-kości.md` | `../testy/sesja.html?quiz=anatomia-kości` |

### Why `../testy/`?

- Subject page: `docs/semestr-X/etyka.md`
- Quiz player: `docs/testy/sesja.html`
- `..` = go up one level (from semestr-X to docs)
- Then go into `testy/`

---

## 📖 What Students See in Docs

### Main README (docs/testy/quizzes/README.md):

Shows at top of quizzes folder, includes:
- How to create quiz
- **NEW:** Quick linking section
- Example for etyka
- Link to detailed guide

### Detailed Linking Guide (JAK_DODAC_I_POLACZYC.md):

Complete guide with:
- Where to put files
- How to name files
- Full etyka example
- Multiple linking scenarios
- URL building rules
- Troubleshooting
- Copy-paste templates

---

## 🎯 Different Linking Styles (for students to choose)

### Style 1: Simple Button
```markdown
[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button}
```

### Style 2: Primary Button (bigger)
```markdown
[🎯 Rozwiąż quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button .md-button--primary}
```

### Style 3: Info Box
```markdown
!!! tip "Test z etyki"
    Kazusy medyczne - 10 pytań

    [Rozpocznij quiz](../testy/sesja.html?quiz=etyka-kazusy){: .md-button}
```

### Style 4: Quiz Card (like in index.md)
```markdown
<div class="quiz-card">
    <h3>Kazusy medyczne</h3>
    <p>Dylematy etyczne w praktyce</p>
    <a href="../testy/sesja.html?quiz=etyka-kazusy" class="quiz-start-btn">
        ▶️ Rozpocznij test
    </a>
</div>
```

### Style 5: Simple List
```markdown
- [Quiz 1: Kazusy](../testy/sesja.html?quiz=etyka-kazusy)
- [Quiz 2: Kodeks](../testy/sesja.html?quiz=etyka-kodeks)
```

---

## ✅ What's Been Updated

### 1. Main Quiz Index (docs/testy/index.md)
- ✅ Lists new quizzes
- ✅ Shows examples
- ✅ Links to creation guide

### 2. README.md
- ✅ Added linking section
- ✅ Quick etyka example
- ✅ Links to detailed guide

### 3. JAK_DODAC_I_POLACZYC.md (NEW)
- ✅ Complete linking tutorial
- ✅ Etyka example walkthrough
- ✅ Multiple scenarios
- ✅ URL building rules
- ✅ Troubleshooting

### 4. GitHub Actions
- ✅ Auto-validates quiz format
- ✅ Runs on PRs
- ✅ Shows errors before merge

---

## 🎓 For You to Communicate to Students

**When announcing the quiz system, tell them:**

1. **Creating quizzes:**
   - Read: `docs/testy/quizzes/README.md`
   - Copy: `_TEMPLATE.md`
   - Edit in GitHub (pencil icon)
   - Use `[x]` for correct answers

2. **Linking to subject pages:**
   - Full guide: `docs/testy/quizzes/JAK_DODAC_I_POLACZYC.md`
   - Quick example in README
   - Pattern: `../testy/sesja.html?quiz=FILENAME`

3. **Examples to learn from:**
   - `anatomia-osteologia.md`
   - `biochemia-bialka.md`
   - `histologia-zestaw-demo/`

---

## 🐛 Common Student Questions - Answers Ready

**Q: Where do I put my etyka quiz file?**
A: `docs/testy/quizzes/etyka-temat.md`

**Q: How do I link it from etyka page?**
A: See `JAK_DODAC_I_POLACZYC.md` - full example with etyka

**Q: What's the URL format?**
A: `../testy/sesja.html?quiz=FILENAME-WITHOUT-MD`

**Q: Can I see an example?**
A: Yes! Look at `anatomia-osteologia.md` and how it's linked in `index.md`

**Q: Where's the etyka page to edit?**
A: Search for `etyka.md` in `docs/semestr-X/` folders

**Q: Does the quiz name have to match?**
A: Yes! File `etyka-kazusy.md` → URL `?quiz=etyka-kazusy`

---

## 🚀 Ready to Deploy

Everything is built and documented. Students have:

✅ Quiz creation guide (README.md)
✅ Linking guide (JAK_DODAC_I_POLACZYC.md)
✅ Examples to learn from
✅ Templates to copy
✅ Clear etyka example
✅ Multiple linking styles

**Just push to main and announce!**

---

## 📞 Quick Test After Deploy

1. Visit: `/testy/quizzes/README.md` - linking section visible?
2. Visit: `/testy/quizzes/JAK_DODAC_I_POLACZYC.md` - guide loads?
3. Visit: `/testy/index.md` - new quizzes listed?
4. Click quiz link - loads correctly?

All should work ✅

---

**Students can now create AND link quizzes without any help from you!** 🎉
