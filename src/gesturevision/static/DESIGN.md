# Design System Specification: The Tactile Shadow

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Tactile Shadow."** Inspired by the precision of gestural technology and the quiet luxury of high-end horology, this system avoids the "template" look of modern SaaS. We prioritize atmosphere over interface. 

The experience is defined by **Editorial Asymmetry**. Instead of rigid, centered grids, we use intentional white space (negative space) and overlapping elements to create a sense of depth and motion. Large-scale typography serves as a structural element, not just content, breaking the boundaries of traditional containers to create a signature, bespoke rhythm.

---

## 2. Colors & Atmospheric Depth
Our palette is rooted in deep obsidian tones, punctuated by metallic bronze and muted grays. This creates a high-contrast, prestigious environment that focuses the user's eye on key interaction points.

### The Palette
- **Core Background:** `surface` (#131313)
- **Primary Accent:** `primary` (#e7bf99) and `primary_container` (#b89470) — used for CTAs and moments of high intent.
- **Muted Text:** `secondary` (#c7c6c6) and `on_surface_variant` (#d2c4b8) for secondary information.

### Signature Rules
*   **The "No-Line" Rule:** 1px solid borders for sectioning are strictly prohibited. Boundaries must be defined solely through background color shifts. For example, a `surface_container_low` section sitting against a `surface` background provides enough distinction for the high-end eye.
*   **The "Glass & Gradient" Rule:** To move beyond a flat UI, main CTAs and hero elements should utilize a subtle linear gradient transitioning from `primary` to `primary_container` at a 135-degree angle. This provides a "brushed metal" soul to the interface.
*   **Surface Hierarchy & Nesting:** Treat the UI as a series of physical layers. 
    *   **Level 0 (Base):** `surface`
    *   **Level 1 (Subtle Inset):** `surface_container_lowest` (#0e0e0e)
    *   **Level 2 (Raised Element):** `surface_container` (#201f1f)
    *   **Level 3 (Interactive/Glass):** `surface_variant` (#353534) with 60% opacity and 20px backdrop-blur.

---

## 3. Typography: Editorial Authority
We pair the geometric precision of **Manrope** for high-impact display with the functional clarity of **Inter** for utility.

*   **Display (Manrope):** Use `display-lg` (3.5rem) with tight letter-spacing (-0.02em) for hero headlines. This conveys an authoritative, tech-forward voice.
*   **Headline & Title (Manrope):** Use these for section headers. Always pair a `headline-lg` with a significant amount of vertical padding to let the type "breathe."
*   **Body & Labels (Inter):** All functional text uses Inter. `body-md` (0.875rem) is our workhorse. To maintain the premium feel, increase the line-height to 1.6 for long-form content.

---

## 4. Elevation & Depth: Tonal Layering
In this system, depth is felt, not seen through heavy dropshadows. We use **Tonal Layering** to convey hierarchy.

*   **The Layering Principle:** Depth is achieved by stacking surface tiers. Place a `surface_container_high` card on a `surface_container_low` background. The subtle shift in hex value creates a soft, natural lift.
*   **Ambient Shadows:** When an element must "float" (e.g., a dropdown or modal), use a shadow with a 60px blur, 0px offset, and 4% opacity. The shadow color should be tinted with our `surface_tint` (#e7bf99) to mimic the way light reflects off bronze surfaces.
*   **The "Ghost Border" Fallback:** If a border is required for accessibility, it must be a "Ghost Border." Use the `outline_variant` token at 15% opacity. Never use 100% opaque borders.
*   **Glassmorphism:** For floating controls, use a semi-transparent `surface_container_highest` with a `backdrop-filter: blur(12px)`. This allows the background colors to bleed through, making the layout feel integrated.

---

## 5. Components

### Buttons
*   **Primary:** `primary` background with `on_primary` text. Shape: `md` (0.375rem). No border.
*   **Secondary:** Ghost style. `outline` color for text, with a 10% opacity `primary` background on hover.
*   **Tertiary:** `on_surface` text with no background. Use `label-md` with all-caps and 0.1em letter spacing for an editorial look.

### Cards & Lists
*   **Rule:** Forbid the use of divider lines.
*   **Execution:** Use `surface_container_low` for the card body. Separate internal list items using 16px or 24px of vertical white space. If separation is visually required, use a subtle background shift to `surface_container_lowest` for alternating rows.

### Input Fields
*   **Style:** Inset look. Use `surface_container_lowest` for the field background. 
*   **Active State:** Transitions to a `ghost border` using the `primary` token at 30% opacity. Labels should be `label-sm` and sit 8px above the field.

### Selection Controls (Chips/Checkboxes)
*   **Chips:** Use `surface_container_high` for unselected states. Selected states should use the `primary_container` with `on_primary_container` text.
*   **Checkboxes:** When checked, the fill is `primary`. When unchecked, it is a simple `ghost border` square.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical layouts where the headline is offset from the body copy.
*   **Do** use `primary` sparingly. It is a "light source" in a dark room; too much of it ruins the atmosphere.
*   **Do** lean into `xl` (0.75rem) roundedness for large containers to soften the "tech" edge.

### Don't
*   **Don't** use pure #000000 or pure #FFFFFF. They are too harsh for the "Tactile Shadow" aesthetic.
*   **Don't** use standard 8px grids for everything. Break the grid for images or decorative elements to create visual interest.
*   **Don't** use 1px dividers or heavy box shadows. If you need a divider, use a 24px gap instead.
*   **Don't** use high-saturation colors for errors. Use the muted `error` (#ffb4ab) to maintain the sophisticated palette.