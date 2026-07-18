#!/Users/bradfordhaile/clawd/opteee/venv/bin/python
"""Compatibility wrapper for marker_single.

Works around a Surya/transformers config-instantiation incompatibility by
marking the composed OCR config as not default-constructible before Marker
builds its model dict.
"""

from surya.recognition.model.config import SuryaOCRConfig

# transformers may instantiate composition configs with no encoder/decoder
# payload during diff/serialization; SuryaOCRConfig() raises KeyError in that
# path unless this flag is set.
SuryaOCRConfig.has_no_defaults_at_init = True


def _get_text_config(self, decoder: bool = False):
    """Disambiguate Surya's two text-like subconfigs for newer transformers."""
    return self.decoder if decoder or hasattr(self, "decoder") else self.text_encoder


SuryaOCRConfig.get_text_config = _get_text_config

from marker.scripts.convert_single import convert_single_cli


if __name__ == "__main__":
    raise SystemExit(convert_single_cli())
