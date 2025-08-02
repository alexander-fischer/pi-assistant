import numpy as np
import openwakeword
from openwakeword.model import Model
from loguru import logger
from pia.config import WAKEWORD_MODEL, WAKEWORD_THRESHOLD


class WakewordDetector:
    def __init__(
        self,
        path_to_model: str = WAKEWORD_MODEL,
        threshold: float = WAKEWORD_THRESHOLD,
    ) -> None:
        openwakeword.utils.download_models()  # type: ignore

        self.model: Model = Model(
            wakeword_models=[path_to_model],
            inference_framework="onnx",
        )

        self.threshold: float = threshold

    def check(self, frame: np.ndarray) -> bool:
        if frame.size == 0:
            return False

        scores: dict[str, float] = self.model.predict(frame)  # type: ignore
        score: float = next(iter(scores.values()), 0.0)

        if score < self.threshold:
            return False

        logger.info(f"Wakeword detected (score={score:.3f})")
        return True

    def reset(self):
        self.model.reset()
