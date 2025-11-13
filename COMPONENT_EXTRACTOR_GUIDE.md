# Component Extractor & Template Browser Guide

## 🧩 Component Extractor

Extract reusable UI components from your 150 templates for easy copy-paste into your projects!

### What It Extracts:
- **Navigation Bars** (🧭) - All the different nav styles
- **Buttons** (🔘) - Creative button designs
- **Cards** (🃏) - Product cards, blog cards, pricing cards
- **Hero Sections** (🎯) - Eye-catching page headers
- **Forms** (📝) - Contact forms, signup forms
- **Footers** (⬇️) - Footer layouts
- **Headers** (⬆️) - Page headers

### How to Use:

```bash
# Extract components from ALL templates (may take a while)
python cli.py extract

# Extract from first 20 templates (faster)
python cli.py extract --limit 20

# Extract from first 50 templates
python cli.py extract --limit 50
```

### What You Get:
- Each component saved as JSON with HTML, CSS classes, source info
- Organized by category in `data/components/`
- `index.json` - searchable index of all components
- `summary.json` - stats by category

---

## 🌐 Template Browser

Browse all your templates and components in a beautiful web interface!

### Features:
✅ Browse all 150 templates with live previews
✅ Filter by source (HTML5UP, Start Bootstrap, Website Templates)
✅ Search templates by name or description
✅ View extracted components by category
✅ Copy component HTML with one click
✅ Live preview of all components

### How to Use:

```bash
# Start the browser
python cli.py browse

# Custom port
python cli.py browse --port 8080
```

Then open your browser to: **http://127.0.0.1:5000**

### Pages:
- **Home** (`/`) - Browse all templates
- **Components** (`/components`) - View components by category
- **Category View** - Click a category to see all components with copy buttons

---

## 💡 Typical Workflow:

### 1. Extract Components (One Time)
```bash
# Extract from all templates (might take a few minutes)
python cli.py extract
```

**Result:** 228+ components from just 10 templates! Imagine extracting from all 150!

### 2. Browse & Copy
```bash
# Start the browser
python cli.py browse
```

### 3. Use in Your Projects
1. Browse to find a component you like
2. Click "View Code" to see the HTML
3. Click "Copy HTML" to copy it
4. Paste into your project
5. Customize colors, text, etc.

---

## 📊 Example Results

From just **10 templates**, we extracted:
- 28 Navigation bars
- 63 Buttons
- 45 Cards
- 24 Hero sections
- 12 Forms
- 14 Footers
- 42 Headers

**Total: 228 components!**

Imagine running this on all 150 templates - you'd have **3,000+ components**!

---

## 🎯 Pro Tips:

1. **Start Small**: Extract from 20 templates first to see results quickly
   ```bash
   python cli.py extract --limit 20
   ```

2. **Then Browse**: Launch the browser and explore what you got
   ```bash
   python cli.py browse
   ```

3. **Extract More**: Once you like what you see, extract from more templates
   ```bash
   python cli.py extract --limit 100
   ```

4. **Search Components**: Use the browser's search to find specific styles

5. **Copy & Customize**: Copy the HTML and tweak colors/text for your needs

---

## 🚀 Quick Start (Right Now!)

```bash
# 1. Extract components from 30 templates (2-3 minutes)
python cli.py extract --limit 30

# 2. Start the browser
python cli.py browse

# 3. Open http://127.0.0.1:5000 in your browser

# 4. Click "Components" → Pick a category → Copy components!
```

That's it! You now have a library of hundreds of beautiful, ready-to-use components! 🎉
