import simpleaudio as sa
import threading
import os

class SafeAudioPlayer:
    def __init__(self):
        self._play_obj = None
        self._lock = threading.Lock()
        self.silent_mode = False
        self.available = self._check_audio_available()

    def _check_audio_available(self):
        try:
            # Attempt to load a dummy wave object
            sa.WaveObject(audio_data=b'\x00\x00'*100, num_channels=1, bytes_per_sample=2, sample_rate=44100)
            return True
        except Exception as e:
            print(f"[Audio] System audio not available: {e}")
            return False

    def enable_silent_mode(self):
        self.silent_mode = True
        print("[Audio] Silent mode enabled")

    def disable_silent_mode(self):
        self.silent_mode = False
        print("[Audio] Silent mode disabled")

    def play(self, wave_obj):
        if self.silent_mode or not self.available:
            print("[Audio] Skipping playback (silent or unavailable)")
            return
        try:
            with self._lock:
                if self._play_obj and self._play_obj.is_playing():
                    self._play_obj.stop()
                self._play_obj = wave_obj.play()
        except Exception as e:
            print(f"[Audio] Playback error: {e}")
            self.available = False  # Disable further attempts

    def stop(self):
        try:
            with self._lock:
                if self._play_obj and self._play_obj.is_playing():
                    self._play_obj.stop()
                    self._play_obj = None
        except Exception as e:
            print(f"[Audio] Stop error: {e}")
