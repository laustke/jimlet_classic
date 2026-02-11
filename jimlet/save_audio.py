from pathlib import Path
import os
import logging
import soundfile as sf
import numpy as np

logger = logging.getLogger(__name__)

def save_audio(
    wav: np.ndarray,
    sample_rate: int,
    output_file: str,
) -> None:


    output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not os.access(output_path.parent, os.W_OK):
        raise PermissionError(
            f"No write permission for directory: {output_path.parent}"
        )


    data = wav.squeeze()

    BLOCK = 16384
    channels = 1 if data.ndim == 1 else data.shape[1]

    with sf.SoundFile(
        file=str(output_path),
        mode="w",
        samplerate=sample_rate,
        channels=channels,
        format="WAV",
        subtype="PCM_16",
    ) as f:
        for i in range(0, len(data), BLOCK):
            f.write(data[i:i + BLOCK])

