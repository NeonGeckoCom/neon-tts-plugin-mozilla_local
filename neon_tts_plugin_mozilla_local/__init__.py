# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

from neon_utils.configuration_utils import get_neon_tts_config
from neon_utils.logger import LOG
from neon_utils.parse_utils import format_speak_tags
try:
    from neon_audio.tts import TTS, TTSValidator
except ImportError:
    from mycroft.tts import TTS, TTSValidator
from mycroft.metrics import Stopwatch

LOG.name = "MozillaTTS"


class MozillaLocalTTS(TTS):

    def __init__(self, lang="en-us", config=None):
        config = config or get_neon_tts_config().get("mozilla_local", {})
        super(MozillaLocalTTS, self).__init__(lang, config, MozillaTTSValidator(self),
                                              audio_ext="mp3",
                                              ssml_tags=["speak"])
        self.manager = ModelManager()
        self.models = self.manager.list_models()
        self.preferred_model = config.get("preferred_model", "tacotron2-DDC")
        self._get_synthesizer(lang)  # Make sure we have a model available in init

    def get_tts(self, sentence, wav_file, speaker=None):
        stopwatch = Stopwatch()
        speaker = speaker or dict()
        # Read utterance data from passed configuration
        request_lang = speaker.get("language",  self.lang)

        to_speak = format_speak_tags(sentence)
        LOG.debug(to_speak)
        if to_speak:
            synthesizer = self._get_synthesizer(request_lang)
            with stopwatch:
                wav_data = synthesizer.tts(sentence)
            LOG.debug(f"Synthesis time={stopwatch.time}")

            with stopwatch:
                synthesizer.save_wav(wav_data, wav_file)
            LOG.debug(f"File access time={stopwatch.time}")
        return wav_file, None

    def _get_synthesizer(self, language) -> Synthesizer:
        if '-' in language:
            language = language.split('-')[0]
        stopwatch = Stopwatch()
        with stopwatch:
            model_name = None

            for model in self.models:
                _, lang, dataset, name = model.split('/')
                print(f"{lang}|{name}")
                if language in lang:
                    model_name = model
                    if name == self.preferred_model:
                        break

            model_path, config_path, model_item = self.manager.download_model(model_name)
            vocoder_name = model_item.get("default_vocoder", "vocoder_models/universal/libri-tts/fullband-melgan")
            vocoder_path, vocoder_config_path, _ = self.manager.download_model(vocoder_name)
            speakers_file_path = ''
            encoder_path = ''
            encoder_config_path = ''
            use_cuda = False

            synthesizer = Synthesizer(
                model_path,
                config_path,
                speakers_file_path,
                vocoder_path,
                vocoder_config_path,
                encoder_path,
                encoder_config_path,
                use_cuda,
            )
        LOG.debug(f"Get synthesizer time={stopwatch.time}")
        return synthesizer


class MozillaTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MozillaTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_dependencies(self):
        try:
            from TTS.utils.manage import ModelManager
        except ImportError:
            raise Exception(
                'MozillaTTS dependencies not installed, please run pip install TTS')

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return MozillaLocalTTS
