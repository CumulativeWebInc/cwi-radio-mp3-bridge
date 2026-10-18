#!/usr/bin/env python3
"""Radio 365 HLS-to-MP3 bridge. Pulls HLS, serves 128k MP3."""
import subprocess
import http.server
import socketserver
import os

HLS_URL = os.environ.get('HLS_URL', 'https://radio.cumulativeweb.com/live.m3u8')
PORT = int(os.environ.get('PORT', '10000'))

class MP3Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/stream.mp3', '/', '/live.mp3'):
            self.send_response(200)
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            proc = subprocess.Popen([
                'ffmpeg', '-re', '-i', HLS_URL,
                '-acodec', 'libmp3lame', '-ab', '128k', '-ac', '2', '-ar', '44100',
                '-f', 'mp3', '-'
            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                while True:
                    data = proc.stdout.read(8192)
                    if not data:
                        break
                    self.wfile.write(data)
            except:
                pass
            finally:
                proc.terminate()
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true,"service":"cwi-radio-mp3-bridge"}')
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(("0.0.0.0", PORT), MP3Handler, bind_and_activate=False) as httpd:
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    print(f"MP3 bridge serving on port {PORT}", flush=True)
    httpd.serve_forever()
