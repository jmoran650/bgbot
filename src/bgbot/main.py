import asyncio, torch, tensorflow as tf


async def main():
    x = torch.randn(5, 3)
    print("Torch tensor:", x.shape)
    y = tf.constant([[1, 2, 3]])
    print("TensorFlow tensor:", y)


if __name__ == "__main__":
    asyncio.run(main())
