import re
from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()


@register.filter(name='youtube_embed')
def youtube_embed(url):
    """
    Convert a YouTube URL to a privacy-enhanced embed URL.
    Handles:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&t=123s
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID (already embed format)
    - https://m.youtube.com/watch?v=VIDEO_ID (mobile)
    - https://www.youtube.com/v/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    if not url:
        return url
    
    # Clean up the URL
    url = url.strip()
    
    # Already a privacy-enhanced embed URL
    if 'youtube-nocookie.com/embed/' in url:
        return url
    
    # Already a regular embed URL - convert to privacy-enhanced
    if 'youtube.com/embed/' in url:
        return url.replace('youtube.com/embed/', 'youtube-nocookie.com/embed/')
    
    # Extract video ID from different URL formats
    video_id = None
    
    # Format: https://www.youtube.com/watch?v=VIDEO_ID or mobile
    match = re.search(r'(?:youtube\.com|m\.youtube\.com)/watch\?v=([a-zA-Z0-9_-]+)', url)
    if match:
        video_id = match.group(1)
    
    # Format: https://youtu.be/VIDEO_ID
    if not video_id:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
    
    # Format: https://www.youtube.com/v/VIDEO_ID
    if not video_id:
        match = re.search(r'youtube\.com/v/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
    
    # Format: https://www.youtube.com/shorts/VIDEO_ID
    if not video_id:
        match = re.search(r'youtube\.com/shorts/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
    
    if video_id:
        # Use privacy-enhanced mode (youtube-nocookie.com)
        # This prevents tracking and can reduce embedding errors
        return f'https://www.youtube-nocookie.com/embed/{video_id}'
    
    # Return original URL if we can't parse it
    return url
