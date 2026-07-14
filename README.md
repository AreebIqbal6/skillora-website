# Skillora Website

Welcome to the official repository for the **Skillora** website. This is a custom-built, high-performance static website designed for a modern software development agency. It uses pure HTML, CSS, and Vanilla JavaScript with a few lightweight libraries for advanced animations.

## Tech Stack

- **HTML5** (Semantic structure)
- **Vanilla CSS3** (Custom variables, responsive grid/flexbox layouts, custom theming)
- **Vanilla JavaScript** (DOM manipulation, theme toggling, form handling)
- **GSAP & ScrollTrigger** (High-performance scroll animations and transitions)
- **Lenis** (Smooth scrolling experience)

## Project Structure

```text
/
├── index.html       # Main landing page containing all sections
├── styles.css       # Core stylesheet (light/dark themes, responsive design)
├── script.js        # Logic for GSAP animations, theme toggle, and modals
├── images/          # Local image assets (logos, work showcase)
└── README.md        # Project documentation
```

## How to Run Locally

Since this is a static website with no backend dependencies, you do not need a complex build process. 

**Option 1: Using npx serve (Recommended)**
If you have Node.js installed, open a terminal in the root directory and run:
```bash
npx -y serve . -p 3000
```
Then visit `http://localhost:3000` in your browser.

**Option 2: Using VS Code Live Server**
1. Open the project folder in VS Code.
2. Install the **Live Server** extension.
3. Right-click `index.html` and select **Open with Live Server**.

## Contact Form (FormSubmit)

The contact form in the footer is fully functional and uses [FormSubmit.co](https://formsubmit.co/) to handle submissions without a backend.
- Submissions are sent directly to `info@skilloraofficial.com`.
- **Note to Team:** If you change the destination email address in `index.html`, the new email must be activated. FormSubmit will send an activation link to the new address upon the first submission.

## CSS Architecture & Theming

- **Dark Mode by Default:** The site is designed dark-mode first.
- **Light Mode:** Toggled via a button in the navigation bar. The toggle script applies a `.light-mode` class to the `<html>` root element. CSS variables in `styles.css` intercept this class to switch out colors automatically.
- **Cache Busting:** If you update `styles.css` or `script.js`, remember to bump the `?v=` version number in `index.html` (e.g., `href="styles.css?v=6"`) to force client browsers to download the fresh files instead of using cached versions.
