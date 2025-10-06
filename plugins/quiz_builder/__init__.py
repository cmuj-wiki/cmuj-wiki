"""
CMUJ Wiki - Quiz Builder Plugin for MkDocs

This plugin automatically discovers and compiles quiz files into optimized JSON.
Supports both text-based quizzes (markdown with checkboxes) and image-based quizzes.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class QuizBuilderPlugin(BasePlugin):
    """
    MkDocs plugin that compiles markdown quiz files into JSON.

    Students edit simple markdown files with checkbox syntax.
    Plugin validates and compiles them into optimized JSON for the frontend.
    """

    config_scheme = (
        ('quiz_dir', config_options.Type(str, default='testy/quizzes')),
        ('output_dir', config_options.Type(str, default='assets/quiz-data')),
        ('strict', config_options.Type(bool, default=False)),
    )

    def on_pre_build(self, config):
        """Run before the build starts - discover and compile quizzes."""
        self.errors = []
        self.warnings = []

        # Get paths
        docs_dir = Path(config['docs_dir'])
        quiz_source_dir = docs_dir / self.config['quiz_dir']
        quiz_output_dir = docs_dir / self.config['output_dir']

        # Create output directory
        quiz_output_dir.mkdir(parents=True, exist_ok=True)

        # Process text-based quizzes
        if quiz_source_dir.exists():
            self._process_text_quizzes(quiz_source_dir, quiz_output_dir)

        # Process image-based quizzes
        self._process_image_quizzes(quiz_source_dir, quiz_output_dir)

        # Report results
        self._report_results()

        return config

    def _process_text_quizzes(self, source_dir: Path, output_dir: Path):
        """Discover and compile markdown quiz files."""
        for quiz_file in source_dir.glob('**/*.md'):
            # Skip template, README, and documentation files
            if quiz_file.name.startswith('_') or quiz_file.name.upper() in ['README.MD', 'README']:
                continue
            if 'JAK_DODAC' in quiz_file.name.upper() or 'INSTRUKCJA' in quiz_file.name.upper():
                continue

            try:
                # Parse the quiz
                quiz_data = self._parse_markdown_quiz(quiz_file)

                # Generate output filename
                relative_path = quiz_file.relative_to(source_dir)
                output_file = output_dir / relative_path.with_suffix('.json')
                output_file.parent.mkdir(parents=True, exist_ok=True)

                # Write JSON
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

                print(f"✓ Compiled quiz: {relative_path}")

            except Exception as e:
                error_msg = f"Error in {quiz_file.relative_to(source_dir)}: {str(e)}"
                self.errors.append(error_msg)
                if self.config['strict']:
                    raise

    def _parse_markdown_quiz(self, file_path: Path) -> Dict[str, Any]:
        """Parse a markdown quiz file and return structured data."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from first h1
        lines = content.split('\n')
        title = "Quiz"
        subject = None
        topic = None

        # Find first h1 for title
        for line in lines:
            if line.startswith('# '):
                title_line = line[2:].strip()
                # Try to extract subject - topic format
                if ' - ' in title_line:
                    parts = title_line.split(' - ', 1)
                    subject = parts[0].strip()
                    topic = parts[1].strip() if len(parts) > 1 else None
                else:
                    subject = title_line
                break

        # Parse questions
        questions = self._extract_questions(content, file_path)

        if not questions:
            raise ValueError("No questions found in quiz file")

        return {
            "quiz_id": file_path.stem,
            "title": title,
            "subject": subject,
            "topic": topic,
            "questions": questions
        }

    def _extract_questions(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Extract questions from markdown content."""
        questions = []

        # Split by h2 (##) to get individual questions
        # Pattern: ## Question text
        question_pattern = r'^##\s+(.+?)$'

        sections = re.split(r'\n##\s+', content)

        for i, section in enumerate(sections):
            if i == 0:  # Skip content before first question
                continue

            try:
                question = self._parse_question_section(section, file_path)
                if question:
                    questions.append(question)
            except Exception as e:
                raise ValueError(f"Error parsing question {i}: {str(e)}")

        return questions

    def _parse_question_section(self, section: str, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a single question section."""
        lines = section.strip().split('\n')

        if not lines:
            return None

        # First line is the question text (after ## was removed)
        question_text = lines[0].strip()

        # Check for image in question text
        image_match = re.search(r'!\[.*?\]\((.+?)\)', question_text)
        image_url = None
        if image_match:
            image_url = image_match.group(1)
            # Remove image markdown from question text
            question_text = re.sub(r'!\[.*?\]\(.+?\)\s*', '', question_text).strip()

        # Parse answers (checkbox list items)
        answers = []
        explanation = None

        for line in lines[1:]:
            line = line.strip()

            # Checkbox answer: - [ ] or - [x]
            checkbox_match = re.match(r'^-\s+\[([x ])\]\s+(.+)$', line, re.IGNORECASE)
            if checkbox_match:
                is_correct = checkbox_match.group(1).lower() == 'x'
                answer_text = checkbox_match.group(2).strip()
                answers.append({
                    "text": answer_text,
                    "correct": is_correct
                })
                continue

            # Blockquote explanation: > Explanation text
            if line.startswith('>'):
                explanation_text = line[1:].strip()
                if explanation:
                    explanation += ' ' + explanation_text
                else:
                    explanation = explanation_text
                continue

        # Validation
        if not answers:
            raise ValueError(f"No answers found for question: {question_text[:50]}...")

        correct_count = sum(1 for a in answers if a['correct'])
        if correct_count == 0:
            raise ValueError(f"No correct answer marked for question: {question_text[:50]}...")

        # Determine question type
        question_type = 'multiple_choice' if correct_count > 1 else 'single_choice'

        result = {
            "question": question_text,
            "type": question_type,
            "points": correct_count,  # Award points based on difficulty
            "options": answers
        }

        if explanation:
            result["explanation"] = explanation

        if image_url:
            result["image"] = image_url

        return result

    def _process_image_quizzes(self, source_dir: Path, output_dir: Path):
        """Process image-based quiz directories (szkiełka format)."""
        if not source_dir.exists():
            return

        # Look for directories with images/ subdirectory and answers.txt
        for quiz_dir in source_dir.glob('**/'):
            images_dir = quiz_dir / 'images'
            answers_file = quiz_dir / 'answers.txt'

            if not (images_dir.exists() and answers_file.exists()):
                continue

            try:
                # Parse answers
                with open(answers_file, 'r', encoding='utf-8') as f:
                    answers = [line.strip() for line in f if line.strip()]

                # Find images
                image_files = sorted(images_dir.glob('*.jpg')) + sorted(images_dir.glob('*.png'))

                if len(answers) != len(image_files):
                    self.warnings.append(
                        f"Warning in {quiz_dir.name}: {len(answers)} answers but {len(image_files)} images"
                    )

                # Create quiz data
                quiz_data = {
                    "quiz_id": quiz_dir.name,
                    "title": quiz_dir.name.replace('-', ' ').title(),
                    "type": "image_quiz",
                    "questions": []
                }

                for idx, (image_file, answer) in enumerate(zip(image_files, answers), 1):
                    # Parse answer (format: "1. Answer text" or just "Answer text")
                    answer_text = re.sub(r'^\d+\.\s*', '', answer)

                    quiz_data["questions"].append({
                        "question": f"Question {idx}",
                        "image": f"{quiz_dir.name}/images/{image_file.name}",
                        "answer": answer_text,
                        "slide_number": idx
                    })

                # Write output
                output_file = output_dir / f"{quiz_dir.name}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

                print(f"✓ Compiled image quiz: {quiz_dir.name} ({len(image_files)} slides)")

            except Exception as e:
                error_msg = f"Error processing image quiz {quiz_dir.name}: {str(e)}"
                self.errors.append(error_msg)
                if self.config['strict']:
                    raise

    def _report_results(self):
        """Report compilation results."""
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.errors:
            print("\n❌ Errors:")
            for error in self.errors:
                print(f"  {error}")

            if self.config['strict']:
                raise Exception("Quiz compilation failed. See errors above.")

        if not self.errors and not self.warnings:
            print("\n✅ All quizzes compiled successfully!")
