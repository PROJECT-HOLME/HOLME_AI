# HOLME_AI

- 백엔드와 연결 시 고려해야 할 것들
    - ai_speaker_play_music_yes()와 ai_speaker_stop_music()는 두 개의 요청을 보낸다
    - 누구 스피커를 통해 백엔드로 요청을 보낼 수 있는 인스턴스는 3 종류이다
        - aircon_payload (InstanceType: 3)
        - ai_speaker_payload (InstanceType: 7)
        - soundbar_payload (InstanceType: 7)