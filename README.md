# NeonAI Mozilla TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for Local Mozilla Text-to-Speech. Note that using this module on a low-power device (i.e. Raspberry Pi)
is not recommended.

# Configuration:

```yaml
tts:
    module: mozilla_local
    mozilla_local: {"preferred_model": "tacotron2-DDC"}
```