# 📸 How to Add Subject Cover Images

## Quick Start

### 1. Generate Image with Sora
Generate a square image (400x400px recommended) that represents the subject.

**Example prompts:**
- Anatomia: "Medical anatomy illustration, human skeleton and organs, educational, clean design"
- Biochemia: "Molecular structure, DNA helix, proteins, scientific illustration"
- Histologia: "Microscopic tissue cells, colorful medical microscopy"

### 2. Save Image to This Directory

**Naming convention:** `{subject-slug}.png` or `{subject-slug}.jpg`

```bash
# Example file structure
docs/assets/images/subjects/
├── anatomia.png
├── biochemia.png
├── histologia.png
├── fizjologia.png
└── ...
```

### 3. Update YAML File

Edit the subject's YAML file in `data/subjects/`:

```yaml
# In data/subjects/anatomia.yml
cover_image: "assets/images/subjects/anatomia.png"
```

### 4. Run the Updater Script

```bash
python3 scripts/update_subject_pages.py --subject anatomia
# OR update all subjects at once
python3 scripts/update_subject_pages.py --all
```

### 5. Verify the Result

The image will appear at the top of the subject page:

```
http://localhost:8001/semestr-1/anatomia/
```

---

## Image Specifications

| Property | Value |
|----------|-------|
| **Dimensions** | 400x400px (square) |
| **Format** | PNG (preferred) or JPG |
| **File size** | < 200KB (optimize for web) |
| **Style** | Clean, professional, medical/scientific themed |

---

## Image Optimization (Optional)

### Using ImageMagick

```bash
# Install ImageMagick
brew install imagemagick  # macOS
sudo apt-get install imagemagick  # Linux

# Resize and optimize
convert sora-output.png \
  -resize 400x400^ \
  -gravity center \
  -extent 400x400 \
  -quality 85 \
  anatomia.png
```

### Using Online Tools
- [TinyPNG](https://tinypng.com/) - Free PNG compression
- [Squoosh](https://squoosh.app/) - Google's image optimizer
- [ImageOptim](https://imageoptim.com/) - macOS app

---

## Example: Adding Anatomia Cover Image

**Step-by-step:**

1. Generate image with Sora using prompt:
   ```
   "Medical anatomy textbook cover, human skeleton diagram, 
   clean educational illustration, square format"
   ```

2. Save the file:
   ```bash
   # Save to this directory
   docs/assets/images/subjects/anatomia.png
   ```

3. Update YAML:
   ```yaml
   # data/subjects/anatomia.yml
   cover_image: "assets/images/subjects/anatomia.png"
   ```

4. Update page:
   ```bash
   python3 scripts/update_subject_pages.py --subject anatomia
   ```

5. View result at: http://localhost:8001/semestr-1/anatomia/

---

## Troubleshooting

### Image Not Showing?

**Check:**
1. ✅ File exists in `docs/assets/images/subjects/`
2. ✅ File name matches exactly (including extension)
3. ✅ YAML path is correct: `assets/images/subjects/filename.png`
4. ✅ Ran the updater script after adding YAML field
5. ✅ Cleared browser cache / hard refresh (Cmd+Shift+R)

### Image Too Large?

Optimize it before adding:
```bash
# Reduce file size
convert input.png -quality 80 -strip output.png
```

### Image Wrong Size?

The CSS will handle sizing automatically, but for best results:
```bash
# Force 400x400
convert input.png -resize 400x400! output.png
```

---

## All Subjects Checklist

Track which subjects have cover images:

### Semester 1
- [ ] Anatomia (`anatomia.png`)
- [ ] Biochemia (`biochemia.png`)
- [ ] Histologia (`histologia.png`)
- [ ] BHK (`bhk.png`)
- [ ] Etyka (`etyka.png`)
- [ ] Historia medycyny (`historia-medycyny.png`)
- [ ] Wychowanie fizyczne (`wychowanie-fizyczne.png`)

### Semester 2
- [ ] Anatomia 2 (`anatomia.png` - can reuse)
- [ ] Biochemia 2 (`biochemia.png` - can reuse)
- [ ] Fizjologia (`fizjologia.png`)
- [ ] Genetyka (`genetyka.png`)
- [ ] Histologia 2 (`histologia.png` - can reuse)
- [ ] Pierwsza pomoc (`pierwsza-pomoc.png`)

### Future Semesters
(Add as you create YAMLs for other subjects)

---

**Pro Tip:** You can reuse the same image for multi-semester subjects (e.g., Anatomia 1 and Anatomia 2 both use `anatomia.png`)

**Questions?** Check the main README or ask in the project discussions.
