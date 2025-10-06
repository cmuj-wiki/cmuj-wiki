# Subject Cover Images

This directory contains cover images for subject pages.

## Image Guidelines

- **Format:** PNG or JPG
- **Size:** 400x400px (square) or similar aspect ratio
- **Source:** Sora AI-generated images
- **Naming:** `{subject-slug}.png` or `{subject-slug}.jpg`

## Examples

```
anatomia.png          # For Anatomia subject
biochemia.png         # For Biochemia subject
histologia.png        # For Histologia subject
```

## Usage in Subject Pages

Images are automatically included in the YAML frontmatter:

```yaml
# In data/subjects/anatomia.yml
cover_image: "assets/images/subjects/anatomia.png"
```

The page updater script will insert the image at the top of the subject page.

## Image Optimization

Before adding images, optimize them:

```bash
# Install imagemagick if needed
brew install imagemagick  # macOS
sudo apt-get install imagemagick  # Linux

# Resize to 400x400 and optimize
convert input.png -resize 400x400^ -gravity center -extent 400x400 -quality 85 anatomia.png
```

## Current Images

(Add your images here and list them below)

- [ ] Anatomia
- [ ] Biochemia
- [ ] Histologia
- [ ] BHK
- [ ] Etyka
- [ ] Historia medycyny
- [ ] Fizjologia
- [ ] Genetyka
- [ ] Pierwsza pomoc
- [ ] (Add more as needed...)
