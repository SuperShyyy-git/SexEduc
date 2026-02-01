"""
Clear all video URLs from lessons to stop Error 153
Run this script to temporarily remove broken video URLs
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sex_education_system.settings')
django.setup()

from courses.models import Lesson

print("=" * 60)
print("CLEARING VIDEO URLs FROM LESSONS")
print("=" * 60)

# Find all lessons with video URLs
lessons_with_videos = Lesson.objects.filter(video_url__isnull=False).exclude(video_url='')
count = lessons_with_videos.count()

print(f"\nFound {count} lesson(s) with video URLs")

if count > 0:
    print("\nClearing video URLs...")
    for lesson in lessons_with_videos:
        print(f"  - {lesson.course.title}: {lesson.title}")
        lesson.video_url = ''  # Clear the URL
        lesson.save()
    
    print(f"\n✅ Successfully cleared {count} video URL(s)")
    print("\nThe Error 153 message should now be gone!")
    print("\nTo add videos later:")
    print("1. Go to http://127.0.0.1:8000/admin/")
    print("2. Edit a lesson")
    print("3. Add a PUBLIC YouTube video URL")
else:
    print("\nNo video URLs found in database.")

print("\n" + "=" * 60)
