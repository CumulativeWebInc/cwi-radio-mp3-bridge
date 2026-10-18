# CWI Radio MP3 Bridge

HLS-to-MP3 bridge for Radio 365. Pulls the HLS stream and serves 128k MP3 for directories that cannot play HLS (Live Online Radio, Radio Garden, etc.).

## Endpoints

- `/stream.mp3` - Live 128k MP3 stream
- `/health` - Health check

## Deploy

Render.com, Docker, free tier. Set `HLS_URL` env var if different from default.
