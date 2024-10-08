---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
---

# Randomness

Random state in Flax NNX is radically simplified compared to systems like Haiku/Flax Linen in that it defines "random state as object state". In essence, this means that random state is just another type of state, and is stored in Variables and help by the models themselves. The main characteristic of the RNG system in Flax NNX is that its **explicit**, its **order-based**, and uses **dynamic counters**. This is a bit different from [Flax Linen's RNG system](https://flax.readthedocs.io/en/latest/guides/flax_fundamentals/rng_guide.html) which is (path + order)-based and uses a static counters.

```{code-cell} ipython3
from flax import nnx
import jax
from jax import random, numpy as jnp
```

## Rngs, RngStream, and RngState
Flax NNX provides the `nnx.Rngs` type a the main convenience API for managing random state. Following Flax Linen's footsteps, `Rngs` has the ability to create multiple named RNG streams, each with its own state, for the purpose of tight control over randomness in the context of JAX transforms. Here's a breakdown of the main RNG-related types in Flax NNX:

* **Rngs**: The main user interface. It defines a set of named `RngStream` objects.
* **nnx.RngStream**: A object that can generate a stream of RNG keys. It holds a root `key` and a `count` inside a `RngKey` and `RngCount` Variables respectively. When a new key is generated, the count is incremented.
* **nnx.RngState**: The base type for all RNG-related state.
  * **nnx.RngKey**: Variable type for holding RNG keys, it includes a `tag` attribute containing the name of the stream.
  * **nnx.RngCount**: Variable type for holding RNG counts, it includes a `tag` attribute containing the name of the stream.

To create an `Rngs` object you can simply pass a integer seed or `jax.random.key` instance to any keyword argument of your choice in the constructor. Here's an example:

```{code-cell} ipython3
rngs = nnx.Rngs(params=0, dropout=random.key(1))
nnx.display(rngs)
```

Notice that the `key` and `count` Variables contain the stream name in a `tag` attribute. This is primarily used for filtering as we'll see later.

To generate new keys, you can access one of the streams and use its `__call__` method with no arguments. This will return a new key by using `random.fold_in` with the current `key` and `count`. The `count` is then incremented so that subsequent calls will return new keys.

```{code-cell} ipython3
params_key = rngs.params()
dropout_key = rngs.dropout()

nnx.display(rngs)
```

Note that the `key` attribute does not change when a new keys are generated.

### Standard stream names
There are only two standard stream names used by Flax NNX's built-in layers, shown in the table below:

| Name     | Description                               |
|----------|-------------------------------------------|
| `params` | Used for parameter initialization         |
| `dropout`| Used by `Dropout` to create dropout masks |

`params` is used my most of the standard layers (`Linear`, `Conv`, `MultiHeadAttention`, etc) during construction to initialize their parameters. `dropout` is used by the `Dropout` and `MultiHeadAttention` to generate dropout masks. Here's a simple example of a model using `params` and `dropout` streams:

```{code-cell} ipython3
class Model(nnx.Module):
  def __init__(self, rngs: nnx.Rngs):
    self.linear = nnx.Linear(20, 10, rngs=rngs)
    self.drop = nnx.Dropout(0.1, rngs=rngs)

  def __call__(self, x):
    return nnx.relu(self.drop(self.linear(x)))

model = Model(nnx.Rngs(params=0, dropout=1))

y = model(x=jnp.ones((1, 20)))
print(f'{y.shape = }')
```

### Default stream
One of the downsides of having named streams is that the user needs to know all the possible names that a model will use when creating the `Rngs` object. While this could be solved with some documentation, Flax NNX provides a `default` stream that can be
be used as a fallback when a stream is not found. To use the default stream you can simply pass an integer seed or `jax.random.key` as the first positional argument.

```{code-cell} ipython3
rngs = nnx.Rngs(0, params=1)

key1 = rngs.params() # call params
key2 = rngs.dropout() # fallback to default
key3 = rngs() # call default directly

# test with Model that uses params and dropout
model = Model(rngs)
y = model(jnp.ones((1, 20)))

nnx.display(rngs)
```

As shown above, a key from the `default` stream can also be generated by calling the `Rngs` object itself.

> **Note**
> <br> For big projects it is recommended to use named streams to avoid potential conflicts. For small projects or quick prototyping just using the `default` stream is a good choice.

+++

## Filtering random state

Random state can be manipulated using [Filters](https://flax-nnx.readthedocs.io/en/latest/guides/filters_guide.html) just like any other type of state. It can be filtered using types (`RngState`, `RngKey`, `RngCount`) or using strings corresponding to the stream names (see [The Filter DSL](https://flax-nnx.readthedocs.io/en/latest/guides/filters_guide.html#the-filter-dsl)). Here's an example using `nnx.state` with various filters to select different substates of the `Rngs` inside a `Model`:

```{code-cell} ipython3
model = Model(nnx.Rngs(params=0, dropout=1))

rng_state = nnx.state(model, nnx.RngState) # all random state
key_state = nnx.state(model, nnx.RngKey) # only keys
count_state = nnx.state(model, nnx.RngCount) # only counts
rng_params_state = nnx.state(model, 'params') # only params
rng_dropout_state = nnx.state(model, 'dropout') # only dropout
params_key_state = nnx.state(model, nnx.All('params', nnx.RngKey)) # params keys

nnx.display(params_key_state)
```

## Reseeding
In Haiku and Flax Linen, random state explicitly passed to `apply` each time before calling the model. This makes it easy to control the randomness of the model when needed e.g. for reproducibility. In Flax NNX there are two ways to approach this:
1. By passing an `Rngs` object through the `__call__` stack manually. Standard layers like `Dropout` and `MultiHeadAttention` accept an `rngs` argument in case you want to have tight control over the random state.
2. By using `nnx.reseed` to set the random state of the model to a specific configuration. This option is less intrusive and can be used even if the model is not designed to enable manual control over the random state.

`reseed` is a function that accepts an arbitrary graph node (this include pytrees of Flax NNX Modules) and some keyword arguments containing the new seed or key value for the `RngStream`s specified by the argument names. `reseed` will then traverse the graph and update the random state of the matching `RngStream`s, this includes both setting the `key` to a possibly new value and resetting the `count` to zero.

Here's an example of how to using `reseed` to reset the random state of the `Dropout` layer and verify that the computation is identical to the first time the model was called:

```{code-cell} ipython3
model = Model(nnx.Rngs(params=0, dropout=1))
x = jnp.ones((1, 20))

y1 = model(x)
y2 = model(x)

nnx.reseed(model, dropout=1) # reset dropout RngState
y3 = model(x)

assert not jnp.allclose(y1, y2) # different
assert jnp.allclose(y1, y3)     # same
```

## Splitting Rngs
When interacting with transforms like `vmap` or `pmap` it is often necessary to split the random state such that each replica has its own unique state. This can be done in two way, either by manually splitting a key before passing it to one of the `Rngs` streams, or using the `nnx.split_rngs` decorator which will automatically split the random state of any `RngStream`s found in the inputs of the function and automatically "lower" them once the function call ends. `split_rngs` is more convenient as it works nicely with transforms so we'll show an example of that here:

```{code-cell} ipython3
rngs = nnx.Rngs(params=0, dropout=1)

@nnx.split_rngs(splits=5, only='dropout')
def f(rngs: nnx.Rngs):
  print('Inside:')
  # rngs.dropout() # ValueError: fold_in accepts a single key...
  nnx.display(rngs)

f(rngs)

print('Outside:')
rngs.dropout() # works!
nnx.display(rngs)
```

Note that `split_rngs` allows passing a Filter to the `only` keyword argument to select the `RngStream`s that should be split when inside the function, in this case we only split the `dropout` stream.

+++

## Transforms
As stated before, in Flax NNX random state is just another type of state, this means that there is nothing special about it regarding transforms. This means that you should be able to use the state handling APIs of each transform to get the results you want. In this section we will two examples of using random state in transforms, one with `pmap` where we'll see how to split the RNG state, and another one with `scan` where we'll see how to freeze the RNG state.

### Data parallel dropout
In the first example we'll explore how to use `pmap` to call our `Model` in a data parallel context. Since Model uses `Dropout` we'll need to split the random state of the `dropout` to ensure that each replica gets different dropout masks. `StateAxes` is passed to `in_axes` to specify that the `model`'s `dropout` stream will be parallelized across axis `0`, and the rest of its state will be replicated. `split_rngs` is used to split the keys of the `dropout` streams into N unique keys, one for each replica.

```{code-cell} ipython3
model = Model(nnx.Rngs(params=0, dropout=1))

num_devices = jax.local_device_count()
x = jnp.ones((num_devices, 16, 20))
state_axes = nnx.StateAxes({'dropout': 0, ...: None})

@nnx.split_rngs(splits=num_devices, only='dropout')
@nnx.pmap(in_axes=(state_axes, 0), out_axes=0)
def forward(model: Model, x: jnp.ndarray):
  return model(x)

y = forward(model, x)
print(y.shape)
```

### Recurrent dropout
Next we will explore how to implement a RNNCell that uses recurrent dropout. To do this we will simply create a `Dropout` layer that will sample keys from a custom `recurrent_dropout` stream, and we will apply dropout to the hidden state `h` of the RNNCell. A `initial_state` method will be defined to create the initial state of the RNNCell.

```{code-cell} ipython3
class Count(nnx.Variable): pass

class RNNCell(nnx.Module):
  def __init__(self, din, dout, rngs):
    self.linear = nnx.Linear(dout + din, dout, rngs=rngs)
    self.drop = nnx.Dropout(0.1, rngs=rngs, rng_collection='recurrent_dropout')
    self.dout = dout
    self.count = Count(jnp.array(0, jnp.uint32))

  def __call__(self, h, x) -> tuple[jax.Array, jax.Array]:
    h = self.drop(h) # recurrent dropout
    y = nnx.relu(self.linear(jnp.concatenate([h, x], axis=-1)))
    self.count += 1
    return y, y

  def initial_state(self, batch_size: int):
    return jnp.zeros((batch_size, self.dout))

cell = RNNCell(8, 16, nnx.Rngs(params=0, recurrent_dropout=1))
```

Next we will use `scan` over an `unroll` function to implement the `rnn_forward` operation. The key ingredient of recurrent dropout is to apply the same dropout mask across all time steps, to achieve this we'll pass `StateAxes` to `scan`'s `in_axes` specifying that the `cell`'s `recurrent_dropout` stream will be broadcasted, and the rest of the cell's state will be carried over. Also, the hidden state `h` will be the `scan`'s `Carry` variable, and the sequence `x` will be scanned over its axis `1`.

```{code-cell} ipython3
@nnx.jit
def rnn_forward(cell: RNNCell, x: jax.Array):
  h = cell.initial_state(batch_size=x.shape[0])

  # broadcast 'recurrent_dropout' RNG state to have the same mask on every step
  state_axes = nnx.StateAxes({'recurrent_dropout': None, ...: nnx.Carry})
  @nnx.scan(in_axes=(state_axes, nnx.Carry, 1), out_axes=(nnx.Carry, 1))
  def unroll(cell: RNNCell, h, x) -> tuple[jax.Array, jax.Array]:
    h, y = cell(h, x)
    return h, y

  h, y = unroll(cell, h, x)
  return y

x = jnp.ones((4, 20, 8))
y = rnn_forward(cell, x)

print(f'{y.shape = }')
print(f'{cell.count.value = }')
```
