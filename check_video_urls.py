"""
Check all lessons with video URLs and validate them
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sex_education_system.settings')
django.setup()

from courses.models import Lesson

print("=" * 60)
print("CHECKING VIDEO URLs IN LESSONS")
print("=" * 60)

lessons_with_videos = Lesson.objects.filter(video_url__isnull=False).exclude(video_url='')
total_count = lessons_with_videos.count()

print(f"\nFound {total_count} lesson(s) with video URLs\n")

if total_count == 0:
    print("No lessons have video URLs set.")
    print("\nTo add a video:")
    print("1. Go to http://127.0.0.1:8000/admin/")
    print("2. Navigate to Courses > Lessons")
    print("3. Edit a lesson and add a YouTube URL")
else:
    for i, lesson in enumerate(lessons_with_videos, 1):
        print(f"{i}. {lesson.course.title} - {lesson.title}")
        print(f"   URL: {lesson.video_url}")
        
        # Basic validation
        url = lesson.video_url.strip()
        if 'youtube.com' in url or 'youtu.be' in url:
            print("   Status: ✅ Valid YouTube URL")
        else:
            print("   Status: ⚠️ Not a YouTube URL")
        print()

print("\n" + "=" * 60)
print("For help with video embedding, see youtube_fix_guide.md")
print("=" * 60)
