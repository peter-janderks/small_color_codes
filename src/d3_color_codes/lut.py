from stimbposd.dem_to_matrices import detector_error_model_to_check_matrices
import stim
import numpy.typing as npt
import numpy as np
from collections import defaultdict

class LutDecoder:
    def __init__(
        self,
        model: stim.DetectorErrorModel,
    ):
        self._matrices = detector_error_model_to_check_matrices(
            model, allow_undecomposed_hyperedges=True
        )
        self.num_detectors = model.num_detectors
        self.num_errors = self._matrices.check_matrix.shape[1]

        self.lut: dict[bytes, npt.NDArray[np.int8]] = defaultdict(
            lambda: np.zeros(self.num_errors, dtype=np.int8)
        )
        syndrome_weights: dict[bytes, tuple[npt.NDArray[np.int8_], int]] = {}


        # Add all-zero key to syndrome_weights
        zero_state = np.zeros(self.num_errors, dtype=np.int8)
        zero_syndrome = self._matrices.check_matrix @ zero_state % 2
        zero_syndrome_bytes = zero_syndrome.astype(np.int8).tobytes()
        syndrome_weights[zero_syndrome_bytes] = (zero_state.copy(), 0)

        for i in range(self.num_errors):
            indices = [i]
            state = np.zeros(self.num_errors, dtype=np.int8)
            state[indices] = 1
            syndrome = self._matrices.check_matrix @ state % 2
            syndrome_bytes = syndrome.astype(np.int8).tobytes()
            val = syndrome_weights.get(syndrome_bytes)
            weight = state.sum()
            if val is None or weight < val[1]:
                syndrome_weights[syndrome_bytes] = (state.copy(), weight)

        for i in range(self.num_errors):
            for j in range(i + 1, self.num_errors):
                indices = [i, j]
            state = np.zeros(self.num_errors, dtype=np.int8)
            state[indices] = 1
            syndrome = self._matrices.check_matrix @ state % 2
            syndrome_bytes = syndrome.astype(np.int8).tobytes()
            val = syndrome_weights.get(syndrome_bytes)
            weight = state.sum()
            if val is None or weight < val[1]:
                syndrome_weights[syndrome_bytes] = (state.copy(), weight)
        
        for key, v in syndrome_weights.items():
            self.lut[key] = np.array(v[0])




    def decode(self, syndrome: np.ndarray) -> np.ndarray:
        """
        Decode the syndrome and return a prediction of which observables were flipped

        Parameters
        ----------
        syndrome : np.ndarray
            A single shot of syndrome data. This should be a binary array with a length equal to the
            number of detectors in the `stim.Circuit` or `stim.DetectorErrorModel`. E.g. the syndrome might be
            one row of shot data sampled from a `stim.CompiledDetectorSampler`.

        Returns
        -------
        np.ndarray
            A binary numpy array `predictions` which predicts which observables were flipped.
            Its length is equal to the number of observables in the `stim.Circuit` or `stim.DetectorErrorModel`.
            `predictions[i]` is 1 if the decoder predicts observable `i` was flipped and 0 otherwise.
        """
        
        corr = self.lut[syndrome.astype(np.int8).tobytes()]
        return (self._matrices.observables_matrix @ corr) % 2

    def decode_batch(
        self,
        shots: np.ndarray,
        *,
        bit_packed_shots: bool = False,
        bit_packed_predictions: bool = False,
    ) -> np.ndarray:
        """
        Decode a batch of shots of syndrome data. This is just a helper method, equivalent to iterating over each
        shot and calling `BPOSD.decode` on it.

        Parameters
        ----------
        shots : np.ndarray
            A binary numpy array of dtype `np.uint8` or `bool` with shape `(num_shots, num_detectors)`, where
            here `num_shots` is the number of shots and `num_detectors` is the number of detectors in the `stim.Circuit` or `stim.DetectorErrorModel`.

        Returns
        -------
        np.ndarray
            A 2D numpy array `predictions` of dtype bool, where `predictions[i, :]` is the output of
            `self.decode(shots[i, :])`.
        """
        if bit_packed_shots:
            shots = np.unpackbits(shots, axis=1, bitorder="little")[
                :, : self.num_detectors
            ]
        predictions = np.zeros(
            (shots.shape[0], self._matrices.observables_matrix.shape[0]), dtype=bool
        )
        for i in range(shots.shape[0]):
            predictions[i, :] = self.decode(shots[i, :])
        if bit_packed_predictions:
            predictions = np.packbits(predictions, axis=1, bitorder="little")
        return predictions
