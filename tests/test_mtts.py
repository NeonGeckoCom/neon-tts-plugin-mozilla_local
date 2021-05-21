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

import os
import sys
import unittest
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "res"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_tts_plugin_mozilla_local import MozillaLocalTTS


class TestMozilla(unittest.TestCase):
    def setUp(self) -> None:
        self.mTTS = MozillaLocalTTS(config={"preferred_model": "tacotron2-DDC"})

    def doCleanups(self) -> None:
        try:
            os.remove(os.path.join(os.path.dirname(__file__), "test.wav"))
        except FileNotFoundError:
            pass
        try:
            self.mTTS.playback.stop()
            self.mTTS.playback.join()
        except AttributeError:
            pass

    def test_speak_no_params(self):
        out_file = os.path.join(os.path.dirname(__file__), "test.wav")
        file, _ = self.mTTS.get_tts("Hello.", out_file)
        self.assertEqual(file, out_file)

    def test_empty_speak(self):
        out_file = os.path.join(os.path.dirname(__file__), "test2.wav")
        file, _ = self.mTTS.get_tts("</speak>Hello.", out_file)
        self.assertFalse(os.path.isfile(out_file))


if __name__ == '__main__':
    unittest.main()
