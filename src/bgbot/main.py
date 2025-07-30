"""Entry point for quick sanity checks of PyTorch and TensorFlow stacks."""

from __future__ import annotations

import asyncio
import torch
import tensorflow as tf


async def main() -> None:
    """Print simple tensor shapes to verify installed libraries."""
    # PyTorch quick test
    x = torch.randn(5, 3)
    print("Torch tensor:", x.shape)

    # TensorFlow quick test
    y = tf.constant([[1, 2, 3]])
    print("TensorFlow tensor:", y)


if __name__ == "__main__":
    asyncio.run(main())