#!/usr/bin/env python3
"""
CMUJ Wiki - Quiz Validation Script

Validates quiz markdown files to ensure they follow the correct format.
Can be run locally or in CI/CD pipeline.

Usage:
    python scripts/validate_quizzes.py
    python scripts/validate_quizzes.py docs/testy/quizzes/my-quiz.md
"""

import sys
import re
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def validate_quiz_file(file_path: Path) -> tuple[bool, list[str], list[str]]:
    """
    Validate a single quiz markdown file.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Could not read file: {e}")
        return False, errors, warnings

    lines = content.split('\n')

    # Check for title (first h1)
    has_title = False
    for i, line in enumerate(lines, 1):
        if line.startswith('# '):
            has_title = True
            title = line[2:].strip()
            if not title:
                errors.append(f"Line {i}: Empty title")
            elif ' - ' not in title:
                warnings.append(f"Line {i}: Title should follow 'Subject - Topic' format")
            break

    if not has_title:
        warnings.append("No h1 title found (recommended: # Subject - Topic)")

    # Extract questions
    questions = []
    current_question = None
    current_line = 0

    for i, line in enumerate(lines, 1):
        # Question header (## ...)
        if line.startswith('## '):
            if current_question:
                questions.append((current_line, current_question))

            current_question = {
                'text': line[3:].strip(),
                'answers': [],
                'has_explanation': False,
                'has_image': False
            }
            current_line = i

        # Answer checkbox
        elif current_question and re.match(r'^-\s+\[([x ])\]\s+.+$', line, re.IGNORECASE):
            match = re.match(r'^-\s+\[([x ])\]\s+(.+)$', line, re.IGNORECASE)
            is_correct = match.group(1).lower() == 'x'
            answer_text = match.group(2).strip()
            current_question['answers'].append({
                'text': answer_text,
                'correct': is_correct,
                'line': i
            })

        # Explanation
        elif current_question and line.strip().startswith('>'):
            current_question['has_explanation'] = True

    # Add last question
    if current_question:
        questions.append((current_line, current_question))

    # Validate each question
    if not questions:
        errors.append("No questions found (questions should start with ##)")

    for q_line, q in questions:
        # Check question text
        if not q['text']:
            errors.append(f"Line {q_line}: Empty question text after ##")

        # Check for image
        if re.search(r'!\[.*?\]\(.+?\)', q['text']):
            q['has_image'] = True

        # Check answers
        if not q['answers']:
            errors.append(f"Line {q_line}: Question has no answers")
        elif len(q['answers']) < 2:
            warnings.append(f"Line {q_line}: Question has only 1 answer (should have at least 2)")

        # Check for at least one correct answer
        correct_count = sum(1 for a in q['answers'] if a['correct'])
        if correct_count == 0:
            errors.append(f"Line {q_line}: No correct answer marked (use [x] for correct answers)")

        # Check for explanation
        if not q['has_explanation']:
            warnings.append(f"Line {q_line}: No explanation provided (recommended: > Explanation)")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def validate_image_quiz(quiz_dir: Path) -> tuple[bool, list[str], list[str]]:
    """
    Validate an image-based quiz directory.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    images_dir = quiz_dir / 'images'
    answers_file = quiz_dir / 'answers.txt'

    # Check structure
    if not images_dir.exists():
        errors.append(f"Missing 'images/' directory in {quiz_dir.name}")
        return False, errors, warnings

    if not answers_file.exists():
        errors.append(f"Missing 'answers.txt' file in {quiz_dir.name}")
        return False, errors, warnings

    # Count images
    image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
    image_count = len(image_files)

    if image_count == 0:
        errors.append(f"No images found in {quiz_dir.name}/images/")

    # Read answers
    try:
        with open(answers_file, 'r', encoding='utf-8') as f:
            answers = [line.strip() for line in f if line.strip()]
    except Exception as e:
        errors.append(f"Could not read answers.txt: {e}")
        return False, errors, warnings

    answer_count = len(answers)

    if answer_count == 0:
        errors.append(f"No answers found in answers.txt")

    # Compare counts
    if image_count != answer_count:
        errors.append(
            f"Mismatch: {image_count} images but {answer_count} answers "
            f"(they should be equal)"
        )

    # Check answer format
    for i, answer in enumerate(answers, 1):
        # Remove optional numbering
        clean_answer = re.sub(r'^\d+\.\s*', '', answer)
        if not clean_answer:
            warnings.append(f"Answer {i} is empty after removing numbering")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    """Main validation function"""
    print(f"\n{Colors.BOLD}🔍 CMUJ Wiki - Quiz Validator{Colors.RESET}\n")

    quiz_dir = Path('docs/testy/quizzes')

    # Check if specific file was provided
    if len(sys.argv) > 1:
        files_to_check = [Path(sys.argv[1])]
    else:
        # Find all quiz files
        files_to_check = list(quiz_dir.glob('*.md'))
        # Exclude template, README, and documentation files
        files_to_check = [f for f in files_to_check
                         if not f.name.startswith('_')
                         and f.name.upper() not in ['README.MD', 'README']
                         and 'JAK_DODAC' not in f.name.upper()
                         and 'INSTRUKCJA' not in f.name.upper()]

        # Also check image quiz directories
        image_quizzes = [d for d in quiz_dir.iterdir()
                        if d.is_dir() and (d / 'images').exists()]

    if not files_to_check and (len(sys.argv) <= 1 and not image_quizzes):
        print(f"{Colors.YELLOW}⚠️  No quiz files found{Colors.RESET}")
        return 0

    total_checked = 0
    total_valid = 0
    total_errors = 0
    total_warnings = 0

    # Validate text quizzes
    for quiz_file in files_to_check:
        print(f"Checking {Colors.BLUE}{quiz_file.name}{Colors.RESET}...")
        is_valid, errors, warnings = validate_quiz_file(quiz_file)

        total_checked += 1
        if is_valid:
            total_valid += 1

        # Print errors
        for error in errors:
            print(f"  {Colors.RED}❌ {error}{Colors.RESET}")
            total_errors += 1

        # Print warnings
        for warning in warnings:
            print(f"  {Colors.YELLOW}⚠️  {warning}{Colors.RESET}")
            total_warnings += 1

        if not errors and not warnings:
            print(f"  {Colors.GREEN}✓ All good!{Colors.RESET}")

        print()

    # Validate image quizzes (if no specific file provided)
    if len(sys.argv) <= 1:
        for quiz_dir_path in image_quizzes:
            print(f"Checking {Colors.BLUE}{quiz_dir_path.name}/{Colors.RESET} (image quiz)...")
            is_valid, errors, warnings = validate_image_quiz(quiz_dir_path)

            total_checked += 1
            if is_valid:
                total_valid += 1

            # Print errors
            for error in errors:
                print(f"  {Colors.RED}❌ {error}{Colors.RESET}")
                total_errors += 1

            # Print warnings
            for warning in warnings:
                print(f"  {Colors.YELLOW}⚠️  {warning}{Colors.RESET}")
                total_warnings += 1

            if not errors and not warnings:
                print(f"  {Colors.GREEN}✓ All good!{Colors.RESET}")

            print()

    # Summary
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  Checked: {total_checked}")
    print(f"  Valid: {Colors.GREEN}{total_valid}{Colors.RESET}")

    if total_errors > 0:
        print(f"  Errors: {Colors.RED}{total_errors}{Colors.RESET}")
    else:
        print(f"  Errors: {total_errors}")

    if total_warnings > 0:
        print(f"  Warnings: {Colors.YELLOW}{total_warnings}{Colors.RESET}")
    else:
        print(f"  Warnings: {total_warnings}")

    print()

    # Exit code
    if total_errors > 0:
        print(f"{Colors.RED}❌ Validation failed{Colors.RESET}\n")
        return 1
    elif total_warnings > 0:
        print(f"{Colors.YELLOW}⚠️  Validation passed with warnings{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.GREEN}✅ All quizzes valid!{Colors.RESET}\n")
        return 0


if __name__ == '__main__':
    sys.exit(main())
