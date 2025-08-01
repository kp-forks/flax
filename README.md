<div align="center">
<img src="https://raw.githubusercontent.com/google/flax/main/images/flax_logo_250px.png" alt="logo"></img>
</div>

# Flax: A neural network library and ecosystem for JAX designed for flexibility

![Build](https://github.com/google/flax/workflows/Build/badge.svg?branch=main) [![coverage](https://badgen.net/codecov/c/gh/google/flax)](https://codecov.io/gh/google/flax)

[**Overview**](#overview)
| [**Quick install**](#quick-install)
| [**What does Flax look like?**](#what-does-flax-look-like)
| [**Documentation**](https://flax.readthedocs.io/)

Released in 2024, Flax NNX is a new simplified Flax API that is designed to make
it easier to create, inspect, debug, and analyze neural networks in
[JAX](https://jax.readthedocs.io/). It achieves this by adding first class support
for Python reference semantics. This allows users to express their models using
regular Python objects, enabling reference sharing and mutability.

Flax NNX evolved from the [Flax Linen API](https://flax-linen.readthedocs.io/), which
was released in 2020 by engineers and researchers at Google Brain in close collaboration
with the JAX team.

You can learn more about Flax NNX on the [dedicated Flax documentation site](https://flax.readthedocs.io/). Make sure you check out:

* [Flax NNX basics](https://flax.readthedocs.io/en/latest/nnx_basics.html)
* [MNIST tutorial](https://flax.readthedocs.io/en/latest/mnist_tutorial.html)
* [Why Flax NNX](https://flax.readthedocs.io/en/latest/why.html)
* [Evolution from Flax Linen to Flax NNX](https://flax.readthedocs.io/en/latest/guides/linen_to_nnx.html)

**Note:** Flax Linen's [documentation has its own site](https://flax-linen.readthedocs.io/).

The Flax team's mission is to serve the growing JAX neural network
research ecosystem - both within Alphabet and with the broader community,
and to explore the use-cases where JAX shines. We use GitHub for almost
all of our coordination and planning, as well as where we discuss
upcoming design changes. We welcome feedback on any of our discussion,
issue and pull request threads.

You can make feature requests, let us know what you are working on,
report issues, ask questions in our [Flax GitHub discussion
forum](https://github.com/google/flax/discussions).

We expect to improve Flax, but we don't anticipate significant
breaking changes to the core API. We use [Changelog](https://github.com/google/flax/tree/main/CHANGELOG.md)
entries and deprecation warnings when possible.

In case you want to reach us directly, we're at flax-dev@google.com.

## Overview

Flax is a high-performance neural network library and ecosystem for
JAX that is **designed for flexibility**:
Try new forms of training by forking an example and by modifying the training
loop, not adding features to a framework.

Flax is being developed in close collaboration with the JAX team and
comes with everything you need to start your research, including:

* **Neural network API** (`flax.nnx`): Including [`Linear`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/linear.html#flax.nnx.Linear), [`Conv`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/linear.html#flax.nnx.Conv), [`BatchNorm`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/normalization.html#flax.nnx.BatchNorm), [`LayerNorm`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/normalization.html#flax.nnx.LayerNorm), [`GroupNorm`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/normalization.html#flax.nnx.GroupNorm), [Attention](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/attention.html) ([`MultiHeadAttention`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/attention.html#flax.nnx.MultiHeadAttention)), [`LSTMCell`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/recurrent.html#flax.nnx.nn.recurrent.LSTMCell), [`GRUCell`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/recurrent.html#flax.nnx.nn.recurrent.GRUCell), [`Dropout`](https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/nn/stochastic.html#flax.nnx.Dropout).

* **Utilities and patterns**: replicated training, serialization and checkpointing, metrics, prefetching on device.

* **Educational examples**: [MNIST](https://flax.readthedocs.io/en/latest/mnist_tutorial.html), [Inference/sampling with the Gemma language model (transformer)](https://github.com/google/flax/tree/main/examples/gemma), [Transformer LM1B](https://github.com/google/flax/tree/main/examples/lm1b_nnx).

## Quick install

Flax uses JAX, so do check out [JAX installation instructions on CPUs, GPUs and TPUs](https://jax.readthedocs.io/en/latest/installation.html).

You will need Python 3.8 or later. Install Flax from PyPi:

```
pip install flax
```

To upgrade to the latest version of Flax, you can use:

```
pip install --upgrade git+https://github.com/google/flax.git
```

To install some additional dependencies (like `matplotlib`) that are required but not included
by some dependencies, you can use:

```bash
pip install "flax[all]"
```

## What does Flax look like?

We provide three examples using the Flax API: a simple multi-layer perceptron, a CNN and an auto-encoder.

To learn more about the `Module` abstraction, check out our [docs](https://flax.readthedocs.io/), our [broad intro to the Module abstraction](https://github.com/google/flax/blob/main/docs/linen_intro.ipynb). For additional concrete demonstrations of best practices, refer to our
[guides](https://flax.readthedocs.io/en/latest/guides/index.html) and
[developer notes](https://flax.readthedocs.io/en/latest/developer_notes/index.html).

Example of an MLP:

```py
class MLP(nnx.Module):
  def __init__(self, din: int, dmid: int, dout: int, *, rngs: nnx.Rngs):
    self.linear1 = Linear(din, dmid, rngs=rngs)
    self.dropout = nnx.Dropout(rate=0.1, rngs=rngs)
    self.bn = nnx.BatchNorm(dmid, rngs=rngs)
    self.linear2 = Linear(dmid, dout, rngs=rngs)

  def __call__(self, x: jax.Array):
    x = nnx.gelu(self.dropout(self.bn(self.linear1(x))))
    return self.linear2(x)
```

Example of a CNN:

```py
class CNN(nnx.Module):
  def __init__(self, *, rngs: nnx.Rngs):
    self.conv1 = nnx.Conv(1, 32, kernel_size=(3, 3), rngs=rngs)
    self.conv2 = nnx.Conv(32, 64, kernel_size=(3, 3), rngs=rngs)
    self.avg_pool = partial(nnx.avg_pool, window_shape=(2, 2), strides=(2, 2))
    self.linear1 = nnx.Linear(3136, 256, rngs=rngs)
    self.linear2 = nnx.Linear(256, 10, rngs=rngs)

  def __call__(self, x):
    x = self.avg_pool(nnx.relu(self.conv1(x)))
    x = self.avg_pool(nnx.relu(self.conv2(x)))
    x = x.reshape(x.shape[0], -1)  # flatten
    x = nnx.relu(self.linear1(x))
    x = self.linear2(x)
    return x
```

Example of an autoencoder:


```py
Encoder = lambda rngs: nnx.Linear(2, 10, rngs=rngs)
Decoder = lambda rngs: nnx.Linear(10, 2, rngs=rngs)

class AutoEncoder(nnx.Module):
  def __init__(self, rngs):
    self.encoder = Encoder(rngs)
    self.decoder = Decoder(rngs)

  def __call__(self, x) -> jax.Array:
    return self.decoder(self.encoder(x))

  def encode(self, x) -> jax.Array:
    return self.encoder(x)
```

## Citing Flax

To cite this repository:

```
@software{flax2020github,
  author = {Jonathan Heek and Anselm Levskaya and Avital Oliver and Marvin Ritter and Bertrand Rondepierre and Andreas Steiner and Marc van {Z}ee},
  title = {{F}lax: A neural network library and ecosystem for {JAX}},
  url = {http://github.com/google/flax},
  version = {0.11.0},
  year = {2024},
}
```

In the above bibtex entry, names are in alphabetical order, the version number
is intended to be that from [flax/version.py](https://github.com/google/flax/blob/main/flax/version.py), and the year corresponds to the project's open-source release.

## Note

Flax is an open source project maintained by a dedicated team at Google DeepMind, but is not an official Google product.
