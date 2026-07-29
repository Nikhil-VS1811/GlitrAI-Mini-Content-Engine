"""Temporary image-generation service contract.

This simulation will be replaced by a real image-generation provider in a later phase.
"""

from time import sleep


GENERATED_IMAGE_PATH = "generated/sample_output.png"
SIMULATED_GENERATION_DELAY_SECONDS = 5


def generate_image(generated_prompt: str, uploaded_image_path: str) -> str:
    """Simulate generating an image from a prompt and uploaded source image."""
    del generated_prompt, uploaded_image_path
    sleep(SIMULATED_GENERATION_DELAY_SECONDS)
    return GENERATED_IMAGE_PATH
