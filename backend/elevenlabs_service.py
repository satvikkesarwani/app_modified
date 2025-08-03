from elevenlabs import generate, save, Voice, VoiceSettings
from config import Config
import os
import tempfile

def generate_voice_audio(text, voice_id=None):
    """Generate voice audio using ElevenLabs API"""
    try:
        if not voice_id:
            voice_id = Config.ELEVENLABS_VOICE_ID
        
        # Generate audio
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.5,
                    use_speaker_boost=True
                )
            ),
            api_key=Config.ELEVENLABS_API_KEY
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            save(audio, tmp_file.name)
            return {"success": True, "audio_path": tmp_file.name}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    try:
        from elevenlabs import voices
        available_voices = voices(api_key=Config.ELEVENLABS_API_KEY)
        
        voice_list = []
        for voice in available_voices:
            voice_list.append({
                "voice_id": voice.voice_id,
                "name": voice.name,
                "category": voice.category
            })
        
        return {"success": True, "voices": voice_list}
    except Exception as e:
        return {"success": False, "error": str(e)}