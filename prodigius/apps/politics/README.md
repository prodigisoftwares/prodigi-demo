# Politics App

The `politics` app is a core component of the Prodigius project, providing a political alignment quiz and analysis tool. It is designed to help users discover their position on a two-dimensional political spectrum and compare their results to a set of predefined politicians.

## Features

- **Political Quiz:**
  - Presents users with a series of questions, each with multiple-choice answers (A, B, Both, Neither).
  - Each question is mapped to either the economic (left/right) or social (authoritarian/libertarian) axis, with custom weights.

- **Scoring System:**
  - User answers are scored and mapped to coordinates (x, y) on a 2D political spectrum.
  - The scoring logic is implemented in `utils.py` and is based on the user's choices and question weights.

- **Politician Comparison:**
  - The app stores a set of politicians, each with their own (x, y) coordinates and a short blurb.
  - After quiz submission, the user's coordinates are compared to all politicians, and the three closest matches are shown.

- **Data Models:**
  - `Question`: The quiz questions, with order and text.
  - `Choice`: The possible answers for each question.
  - `Politician`: Public figures with coordinates and blurbs.
  - `TestSubmission`: Stores user answers and computed coordinates.

- **Admin Interface:**
  - Django admin support for managing questions, choices, and politicians.

- **Templates & Views:**
  - Views for quiz landing, taking the quiz, and displaying results.
  - Templates for each view, including partials for result rendering.

- **Testing:**
  - Comprehensive test suite for views and scoring logic.

## Mission

The mission of the `politics` app is to provide an engaging, educational, and data-driven way for users to explore their political alignment and see how they compare to well-known figures. It is designed for transparency, extensibility, and ease of integration into broader platforms.

## File Overview

- `models.py` — Data models for questions, choices, politicians, and submissions.
- `views.py` — Main views for quiz flow and scoring.
- `utils.py` — Scoring and coordinate calculation logic.
- `admin.py` — Django admin configuration.
- `urls.py` — URL routes for the app.
- `tests/` — Unit tests for views and scoring.
- `fixtures/` — Initial data for questions and choices.
- `templates/` — HTML templates for quiz and results.

## How it Works

1. **User visits the quiz page** and answers a series of questions.
2. **Answers are scored** using a weighted algorithm to determine the user's position on the political spectrum.
3. **The app finds the three closest politicians** to the user's position and displays them as results.
4. **All submissions are saved** for analysis and future reference.

## Extending the App

- Add new questions or politicians via the Django admin.
- Adjust scoring logic in `utils.py` for new axes or weights.
- Customize templates for different presentation styles.

---

For more details, see the code and comments in each file.
