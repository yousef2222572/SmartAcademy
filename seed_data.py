import os
from pathlib import Path

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'academy_ecommerce.settings'
)

import django
django.setup()

from django.core.files import File

from academy_core.models import Sections, Lessons


BASE_DIR = Path(__file__).resolve().parent

VIDEO_DIR = (
    BASE_DIR
    / 'academy_core'
    / 'static'
    / 'videos'
)

VIDEO_FILES = [
    'python.mp4',
    'javascript.mp4',
    'django.mp4',
    'web.mp4',
    'git.mp4',
]

LESSON_DATA = [
    (
        'Introduction',
        'Introduction and overview of the topic.'
    ),
    (
        'Core Concepts',
        'Learn the core concepts and important ideas.'
    ),
    (
        'Practical Exercise',
        'Apply what you learned in a practical example.'
    ),
]


def create_lessons_with_videos():

    # Remp4e old lessons first
    Lessons.objects.all().delete()

    # Find available videos
    available_videos = []

    for filename in VIDEO_FILES:

        video_path = VIDEO_DIR / filename

        if not video_path.exists():
            print(f'Warning: video not found: {video_path}')
            continue

        available_videos.append(video_path)

    if not available_videos:
        raise FileNotFoundError(
            f'No demo videos found in: {VIDEO_DIR}'
        )

    sections = Sections.objects.all().order_by(
        'track_id',
        'id'
    )

    created_lessons = 0

    for section in sections:

        for lesson_index, (lesson_name, lesson_title) in enumerate(
            LESSON_DATA,
            start=1
        ):

            video_path = available_videos[
                created_lessons % len(available_videos)
            ]

            with open(video_path, 'rb') as video_file:

                lesson = Lessons(
                    lesson_name=f'{lesson_index}. {lesson_name}',
                    lesson_title=lesson_title,
                    section=section,
                )

                lesson.lesson_video.save(
                    video_path.name,
                    File(video_file),
                    save=False
                )

                lesson.save()

            created_lessons += 1

    print()
    print('Lessons and demo videos created successfully.')
    print(f'Sections found: {sections.count()}')
    print(f'Lessons created: {created_lessons}')
    print()


if __name__ == '__main__':
    create_lessons_with_videos()