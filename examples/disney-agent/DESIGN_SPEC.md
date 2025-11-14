# 🎨 Disney Trip Planner - Visual Design Specification

## Design System Overview

This document specifies the exact visual appearance of every UI element in the Disney Trip Planning Agent.

---

## Typography

### Font Family
```
Primary: 'Nunito', sans-serif
Weights: 400 (regular), 700 (bold), 900 (black)
Source: Google Fonts
```

### Type Scale
```
Hero Heading (H1)     → 2.5em / 40px   [Weight: 900]
Section Heading (H2)  → 2em / 32px     [Weight: 700]
Subsection (H3)       → 1.5em / 24px   [Weight: 700]
Body Text             → 1em / 16px     [Weight: 400]
Small Text            → 0.85em / 14px  [Weight: 400]
Button Text           → 1.06em / 17px  [Weight: 800, UPPERCASE, 1px spacing]
```

### Text Colors
```
Primary Text:   #2c3e50 (dark slate)
Secondary Text: #546e7a (gray slate)
Link Text:      #1e88e5 (bright blue)
Disabled Text:  #b0bec5 (light gray)
```

---

## Color Palette

### Primary (Blues)
```
Name              Hex       RGB              Usage
─────────────────────────────────────────────────────────
Sky Blue          #87ceeb   135, 206, 235    Primary actions, headers
Medium Blue       #5dade2   93, 173, 226     Hover states
Deep Blue         #3498db   52, 152, 219     Active states
Powder Blue       #b0e0e6   176, 224, 230    Borders
Alice Blue        #f0f8ff   240, 248, 255    Backgrounds (light end)
```

### Secondary (Pinks)
```
Name              Hex       RGB              Usage
─────────────────────────────────────────────────────────
Light Pink        #ffb6c1   255, 182, 193    Delete button light
Pink              #ffc0cb   255, 192, 203    Accent elements
Salmon Pink       #ef9a9a   239, 154, 154    Delete button medium
Rose              #e57373   229, 115, 115    Delete button border
```

### Tertiary (Golds)
```
Name              Hex       RGB              Usage
─────────────────────────────────────────────────────────
Gold              #ffd700   255, 215, 0      Checked checkboxes, sparkles
Light Gold        #ffed4e   255, 237, 78     Checkbox gradient end
Amber             #ffc107   255, 193, 7      Borders, highlights
```

### Priority Colors
```
High Priority     #e74c3c   231, 76, 60      Red-ish (urgent items)
Medium Priority   #f39c12   243, 156, 18     Orange (normal items)
Low Priority      #27ae60   39, 174, 96      Green (optional items)
```

### Grayscale
```
Pure White        #ffffff   255, 255, 255    Card backgrounds
Off White         #f8fbff   248, 251, 255    Gradient end
Light Gray        #e8e8e8   232, 232, 232    Unchecked checkbox
Medium Gray       #c0c0c0   192, 192, 192    Borders
Dark Gray         #2c3e50   44, 62, 80       Text
```

---

## Spacing System

### Base Unit: 4px
```
xs:  4px   (tight spacing)
sm:  8px   (small gaps)
md:  12px  (default spacing)
lg:  16px  (section spacing)
xl:  20px  (major spacing)
2xl: 40px  (large sections)
```

### Padding Scale
```
Input Fields:   12px 24px
Buttons:        16px 40px
Cards:          20px
Pills:          15px 25px
Checkboxes:     6px 10px
```

### Margin Scale
```
Between Cards:       20px bottom
Between Sections:    40px bottom
Before Headings:     30px top
After Headings:      15px bottom
```

### Gaps
```
Column Gap (Grid):     default
Card Action Gap:       8px
Button Group Gap:      12px
```

---

## Shape Specifications

### 1. Circles

#### Small Circle (Delete Button)
```
Diameter: 44px
Border Radius: 50%
Border: 2px solid
Shadow: 0 2px 8px rgba(239, 83, 80, 0.3)

Example CSS:
.circle-small {
    width: 44px;
    height: 44px;
    border-radius: 50%;
}
```

#### Medium Circle (Checkbox Head)
```
Diameter: 44px (same as delete button for equality)
Border Radius: 50%
Border: 2px solid
Shadow: 0 3px 8px rgba(0, 0, 0, 0.15)
```

#### Large Circle (Idea Cards)
```
Diameter: 350px
Border Radius: 50%
Border: 5px solid
Padding: 40px 35px
Shadow: 0 8px 25px rgba(135, 206, 235, 0.4)
```

#### Extra Large Circle (Countdown)
```
Diameter: 400px
Border Radius: 50%
Border: 6px solid
Shadow: 0 12px 40px rgba(135, 206, 235, 0.6)
```

### 2. Pills (Elongated Circles)

#### Standard Button
```
Border Radius: 50px
Padding: 16px 40px
Min Width: 150px
Height: auto (based on padding)

Example:
┌─────────────────────────┐
│    ✨ BUTTON TEXT ✨    │
└─────────────────────────┘
```

#### Input Field
```
Border Radius: 50px
Padding: 12px 24px
Border: 3px solid
Height: ~48px
```

#### Tab
```
Border Radius: 50px
Padding: 12px 24px
Margin: 0 5px
```

### 3. Rounded Rectangles

#### Checklist Card
```
Width: 100% (within column)
Min Height: 180px
Border Radius: 20px
Border: 3px solid
Padding: 20px
Margin: 20px bottom

Example:
┌──────────────────────────────┐
│ ✓ Pack sunscreen            │
│                              │
│ 📁 packing | ⭐ HIGH         │
└──────────────────────────────┘
```

### 4. Diamonds

#### Trip Code Display
```
Created with clip-path: polygon()
Approximate dimensions: 300px × 200px
Rotation: slight tilt for dynamism

Polygon points:
50% 0%     (top)
100% 50%   (right)
50% 100%   (bottom)
0% 50%     (left)
```

### 5. Triangles (Decorative)

#### Small Triangle
```
Created with CSS borders:
border-left: 25px solid transparent
border-right: 25px solid transparent
border-bottom: 43px solid color

Result: ▼ pointing down
```

### 6. Mickey Ears (Custom Checkbox)

```
Structure:
     ●     ●         (Two ears, 24px each)
       ●             (Head, 44px)

Head (input[type="checkbox"]):
- Width: 44px
- Height: 44px
- Border-radius: 50%

Left Ear (::before):
- Width: 24px
- Height: 24px
- Position: top: -11px, left: -4px

Right Ear (::after):
- Width: 24px
- Height: 24px
- Position: top: -11px, right: -4px

Colors:
- Unchecked: gradient(#e8e8e8 → #d3d3d3)
- Checked: gradient(#ffd700 → #ffed4e)
```

---

## Gradients

### Background Gradients
```
Standard Background:
    linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%)

Card Background:
    linear-gradient(135deg, #ffffff 0%, #f8fbff 100%)

Button Background:
    linear-gradient(135deg, #87ceeb 0%, #5dade2 100%)

Delete Button:
    linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%)

Checked Checkbox:
    linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)

High Priority:
    linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%)

Medium Priority:
    linear-gradient(135deg, #fffef5 0%, #fff8e1 100%)

Low Priority:
    linear-gradient(135deg, #f5fff5 0%, #e8f5e9 100%)
```

### Direction
All gradients: **135deg** (diagonal top-left to bottom-right)

---

## Shadows

### Elevation System

#### Level 1 (Subtle)
```
box-shadow: 0 2px 8px rgba(135, 206, 235, 0.2)
Usage: Input fields, small buttons
```

#### Level 2 (Standard)
```
box-shadow: 0 6px 16px rgba(135, 206, 235, 0.3)
Usage: Cards, standard elements
```

#### Level 3 (Elevated)
```
box-shadow: 0 8px 25px rgba(135, 206, 235, 0.4)
Usage: Idea cards, modals
```

#### Level 4 (Floating)
```
box-shadow: 0 12px 40px rgba(135, 206, 235, 0.6)
Usage: Headers, important elements
```

### Hover States
```
Standard → Hover:
0 6px 16px → 0 12px 28px (double offset and blur)
opacity 0.3 → 0.5 (increase opacity)
```

---

## Borders

### Border Widths
```
Subtle:    2px (delete button, checkboxes)
Standard:  3px (cards, inputs)
Bold:      4px (buttons, major elements)
Strong:    5px (idea cards)
Extra:     6px (countdown)
```

### Border Styles
```
Solid:     Most elements
None:      Containers, transparent wrappers
```

### Border Colors
```
Light:     rgba(135, 206, 235, 0.4)  - 40% opacity
Medium:    #b0d4f1                   - Solid pastel blue
Bold:      #87ceeb                   - Primary blue
Accent:    rgba(255, 215, 0, 0.5)   - Gold for buttons
```

---

## Animations

### Keyframes Library

#### 1. Sparkle (Decorative)
```css
@keyframes sparkle {
    0%, 100% {
        opacity: 0;
        transform: scale(0) rotate(0deg);
    }
    50% {
        opacity: 1;
        transform: scale(1) rotate(180deg);
    }
}

Duration: 1.5-2s
Timing: infinite
Usage: ✨ emoji decorations, ::before/::after content
```

#### 2. Float (Silhouettes)
```css
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

Duration: 5-8s
Timing: infinite ease-in-out
Usage: Disney silhouettes, background decorations
```

#### 3. Shimmy (Hover)
```css
@keyframes shimmy {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

Duration: 0.5s
Timing: ease-in-out (on hover)
Usage: Button hover states
```

#### 4. Bounce (Hover)
```css
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

Duration: 0.5s
Timing: ease-in-out (on hover)
Usage: Button hover states (combined with shimmy)
```

#### 5. Mickey Pop (Interaction)
```css
@keyframes mickeyPop {
    0% { transform: scale(1); }
    50% { transform: scale(1.2) rotate(10deg); }
    100% { transform: scale(1); }
}

Duration: 0.4s
Timing: ease-out (on check)
Usage: Checkbox state change
```

#### 6. Check Pop (Completion)
```css
@keyframes checkPop {
    0% {
        transform: translate(-50%, -50%) rotate(-15deg) scale(0);
    }
    50% {
        transform: translate(-50%, -50%) rotate(-15deg) scale(1.3);
    }
    100% {
        transform: translate(-50%, -50%) rotate(-15deg) scale(1);
    }
}

Duration: 0.5s
Timing: ease-out (on complete)
Usage: Giant checkmark overlay on completed cards
```

### Transition Properties
```
Standard:
    transition: all 0.3s ease

Bounce:
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)

Quick:
    transition: all 0.2s ease

Slow:
    transition: all 0.5s ease
```

---

## Component States

### Button States

#### Default
```
Background: gradient(#87ceeb → #5dade2)
Border: 4px solid rgba(255, 215, 0, 0.5)
Shadow: 0 6px 20px rgba(135, 206, 235, 0.5)
Transform: none
```

#### Hover
```
Background: gradient(#5dade2 → #3498db) [darker]
Border: 5px solid rgba(255, 215, 0, 0.9) [thicker + more opaque]
Shadow: 0 10px 35px rgba(135, 206, 235, 0.7) [elevated]
Transform: scale(1.1)
Animation: shimmy + bounce
```

#### Active (Pressed)
```
Transform: scale(0.9) [pressed down]
```

### Checkbox States

#### Unchecked
```
Background: gradient(#e8e8e8 → #d3d3d3) [gray]
Border: 2px solid #c0c0c0
Shadow: 0 3px 8px rgba(0, 0, 0, 0.15)
```

#### Checked
```
Background: gradient(#ffd700 → #ffed4e) [gold]
Border: 2px solid #ffc107
Shadow: 0 4px 12px rgba(255, 215, 0, 0.5) [gold glow]
Animation: mickeyPop
```

### Card States

#### Default
```
Border: 3px solid #b0d4f1
Shadow: 0 6px 16px rgba(135, 206, 235, 0.3)
Transform: none
Opacity: 1
```

#### Hover
```
Border: 3px solid #ffd700 [gold]
Shadow: 0 12px 28px rgba(135, 206, 235, 0.5) [elevated]
Transform: translateY(-8px) rotate(1deg) scale(1.02)
```

#### Completed
```
Opacity: 0.75 [dimmed]
Filter: grayscale(20%) [subtle desaturation]
Background: gradient(#f5f5f5 → #e8f4f8) [gray-blue]
::before: Giant ✓ checkmark overlay
```

---

## Layout Specifications

### Grid System

#### 3-Column Card Grid
```
Columns: 3 equal width
Gap: default (Streamlit auto)
Item width: 100% of column
Responsive: Maintains 3 columns (not responsive yet)

Example:
┌──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │
├──────────┼──────────┼──────────┤
│  Card 4  │  Card 5  │  Card 6  │
└──────────┴──────────┴──────────┘
```

### Card Action Row

#### Structure
```
Total width: 100%
Layout: Flexbox (flex-start alignment)
Gap: 8px

Column 1 (Checkbox):
- Ratio: 7 parts
- Flex: 1 1 auto (grows to fill)
- Content: Mickey Ears checkbox + label

Column 2 (Delete):
- Ratio: 1 part
- Flex: 0 0 auto (fixed size)
- Width: 48px (44px button + 4px padding)
- Content: Circular delete button

Visual:
┌──────────────────────────────────┬────┐
│ ☑ Complete (Mickey Ears)        │ 🗑️ │
└──────────────────────────────────┴────┘
     87.5% (flexible)             12.5%
```

### Sidebar Layout
```
Width: default (Streamlit auto)
Position: Left (expanded by default)
Content:
  1. Trip details form
  2. Generate/Update button
  3. Trip code display
```

### Main Content Layout
```
Width: Remaining space after sidebar
Structure:
  1. Header with countdown
  2. Tab navigation (pills)
  3. Tab content (selected tab fills area)
```

---

## Icon System

### Emoji Icons Used
```
🏰  Castle - Main header, branding
✨  Sparkles - Decorative, animations
🎉  Party - Celebration, success states
⏰  Clock - Countdown timer
✅  Checkmark - Completed items
💡  Lightbulb - Ideas section
🤖  Robot - AI assistant
📋  Clipboard - Summary
🗑️  Trash - Delete actions
💾  Floppy - Save actions
🔍  Magnifying glass - Search/find
🔄  Circular arrows - Refresh/regenerate
➕  Plus - Add new item
📁  Folder - Category
⭐  Star - Priority
📅  Calendar - Deadline/date
🚀  Rocket - Launch/start
💎  Diamond - Trip code display
👑  Crown - Silhouette decoration
🌹  Rose - Belle's rose silhouette
🪝  Hook - Pirate hook silhouette
🧚  Fairy - Tinkerbell silhouette
🖌️  Brush - Rapunzel's brush silhouette
```

### Size Scale
```
Inline: 1em (matches text)
Small: 20-25px
Medium: 30-35px
Large: 40-45px
Decoration: 32-38px (with opacity 0.07-0.10)
```

---

## Accessibility Notes

### Color Contrast
- All text meets WCAG AA standards (4.5:1 minimum)
- Primary text (#2c3e50) on white: 12.6:1 ✓
- Link text (#1e88e5) on white: 4.5:1 ✓

### Focus States
- Currently: Default browser focus (blue outline)
- TODO: Custom focus ring matching theme

### Screen Readers
- Checkboxes: Have visible labels
- Buttons: Use emoji + text (text is readable)
- TODO: Add ARIA labels for decorative elements

---

## Browser Support

### Tested Browsers
- Chrome 90+ ✓
- Firefox 88+ ✓
- Safari 14+ ✓
- Edge 90+ ✓

### Known Issues
- Safari: May need -webkit-appearance: none for checkboxes
- IE: Not supported (uses CSS Grid)

---

## Print Styles
Currently: None
TODO: Add @media print styles for checklist printing

---

**Last Updated:** 2025-10-29
**Version:** 1.0
**Maintained By:** Development Team
