# Redesign UI/UX for Fertility Prediction Web App

This plan addresses your request to completely revamp the UI/UX of the machine learning web application. We will create a beautiful, elegant, and dynamic experience using Bootstrap, custom CSS, and a new result page.

## Proposed Changes

### 1. Aesthetic Enhancements & Minimalist Design
- **Color Palette**: We will introduce a sophisticated, pastel-driven color palette (e.g., soft pinks, elegant warm grays, and muted greens) to make the interface feel modern, inviting, and elegant.
- **Input Fields**: Redesign the form fields to be minimalist—removing heavy borders, using soft shadows, and subtle focus animations.
- **Mini Buttons**: The "Predict" and "Back" buttons will be styled as elegant mini-buttons with smooth hover effects.
- **FontAwesome**: We will continue using FontAwesome but enhance its integration, ensuring icons perfectly complement the minimal inputs.

### 2. Illustration of a Pregnant Woman
- I will generate a beautiful, modern, minimal vector-style illustration of a pregnant woman.
- This illustration will be placed prominently on the web app (either on the landing page or as a hero image) to set the mood and context.

### 3. Dynamic JS and New Result Page (`result.html`)
- **Current Flow**: The app currently shows results on the same page via AJAX.
- **New Flow**: When the doctor clicks "Predict", the JavaScript will handle a dynamic loading state, and then the app will navigate to a dedicated **Result Page**.
- **Result Page Content**:
    - The final prediction (Success/Failure) with probability.
    - **Feature Statistics**: A detailed breakdown of which features strongly influenced the prediction.
    - **Percentage Bars**: Beautiful progress/percentage bars showing the level of each key feature (e.g., Sperm Motility, BMI, Stress Level) relative to ideal ranges.
    - An elegant "Back" mini-button to return to the form.

### App Modifications

#### [MODIFY] `app.py`
- Update the `/predict` route. We will change it to either render `result.html` directly upon form submission, or have a new `/result` route that takes prediction data. To keep JS dynamic, we can keep the AJAX request in `/predict`, but upon success, redirect the user to `/result?data=...` or store the result in the session and redirect. Using Flask sessions is the cleanest approach.

#### [NEW] `app/templates/result.html`
- Create the new result page with the prediction outcome, feature statistics, and percentage bars.

#### [MODIFY] `app/templates/index.html`
- Redesign the form layout.
- Add the generated illustration.
- Update classes and structure for the new elegant, minimalist look.

#### [MODIFY] `app/static/css/style.css`
- Complete overhaul of the CSS to implement the new aesthetic, color blends, minimalist inputs, and mini buttons.

#### [MODIFY] `app/static/js/app.js`
- Update the form submission logic. Instead of showing results on the same page, we will show a smooth dynamic loading animation, then redirect to the result page.

## User Review Required
> [!IMPORTANT]
> The `/predict` API will be modified to use Flask sessions to pass data to the new `/result` page. Are you okay with enabling Flask sessions (which requires setting a secret key in `app.py`)? Alternatively, I can implement a pure frontend redirect with query parameters. Session is generally cleaner. Please let me know if you approve this overall plan!
