import ffmpeg

(
    ffmpeg
    .input('test.mp3')
    .output('F:\\workspace\\out.mp3', format='mp3', audio_bitrate=16000, ac=1, ar='16k')
    .run()
)