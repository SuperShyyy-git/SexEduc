"""
Force clear ALL video URLs - set to NULL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sex_education_system.settings')
django.setup()

from courses.models import Lesson

print("=" * 60)
print("FORCE CLEARING ALL VIDEO URLs")
print("=" * 60)

lessons = Lesson.objects.all()
count = 0

for lesson in lessons:
    if lesson.video_url:
        print(f"Clearing: {lesson.title} - Current URL: {lesson.video_url}")
        lesson.video_url = None  # Set to NULL, not empty string
        lesson.save()
        count += 1

print(f"\n✅ Cleared {count} video URLs")
print(f"Total lessons in database: {lessons.count()}")

# Verify
remaining = Lesson.objects.filter(video_url__isnull=False).exclude(video_url='')
print(f"Lessons with video URLs remaining: {remaining.count()}")

if remaining.count() == 0:
    print("\n✅✅✅ ALL VIDEO URLs SUCCESSFULLY CLEARED! ✅✅✅")
else:
    print("\n⚠️ Some URLs still remain:")
    for l in remaining:
        print(f"  - {l.title}: {l.video_url}")

print("=" * 60)
