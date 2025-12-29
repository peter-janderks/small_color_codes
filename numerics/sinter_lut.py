from sinter import Decoder, CompiledDecoder
import stim
import pathlib
import numpy as np
from .lut import LutDecoder

class SinterCompiledLutDecoder(CompiledDecoder):
    def __init__(self, decoder: LutDecoder):
        self.decoder = decoder

    def decode_shots_bit_packed(
        self,
        *,
        bit_packed_detection_event_data: np.ndarray,
    ) -> np.ndarray:
        return self.decoder.decode_batch(
            shots=bit_packed_detection_event_data,
            bit_packed_shots=True,
            bit_packed_predictions=True,
        )

class SinterLutDecoder(Decoder):
    def __init__(
        self,
    ):
        pass

    def compile_decoder_for_dem(
        self, *, dem: stim.DetectorErrorModel
    ) -> CompiledDecoder:
        lut_decoder = LutDecoder(model=dem)
        
        return SinterCompiledLutDecoder(lut_decoder)
