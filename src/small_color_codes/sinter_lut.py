from sinter import Decoder, CompiledDecoder
import stim
import pathlib
import numpy as np
from small_color_codes.lut import LutDecoder


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

    def decode_via_files(
        self,
        *,
        num_shots: int,
        num_dets: int,
        num_obs: int,
        dem_path: pathlib.Path,
        dets_b8_in_path: pathlib.Path,
        obs_predictions_b8_out_path: pathlib.Path,
        tmp_dir: pathlib.Path,
    ) -> None:

        dem = stim.DetectorErrorModel.from_file(dem_path)
        lut_decoder = LutDecoder(model=dem)
        shots = stim.read_shot_data_file(
            path=dets_b8_in_path,
            format="b8",
            num_detectors=dem.num_detectors,
            bit_packed=False,
        )
        predictions = lut_decoder.decode_batch(shots)
        stim.write_shot_data_file(
            data=predictions,
            path=obs_predictions_b8_out_path,
            format="b8",
            num_observables=dem.num_observables,
        )
