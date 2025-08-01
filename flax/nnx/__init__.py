# Copyright 2024 The Flax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flax.linen.pooling import avg_pool as avg_pool
from flax.linen.pooling import max_pool as max_pool
from flax.linen.pooling import min_pool as min_pool
from flax.linen.pooling import pool as pool
from flax.typing import Initializer as Initializer

from .bridge import wrappers as wrappers
from .filterlib import WithTag as WithTag
from .filterlib import PathContains as PathContains
from .filterlib import OfType as OfType
from .filterlib import Any as Any
from .filterlib import All as All
from .filterlib import Not as Not
from .filterlib import Everything as Everything
from .filterlib import Nothing as Nothing
from .graph import GraphDef as GraphDef
from .graph import GraphState as GraphState
from .graph import PureState as PureState
from .object import Object as Object
from .object import Data as Data
from .object import data as data
from .object import register_data_type as register_data_type
from .object import is_data_type as is_data_type
from .helpers import Sequential as Sequential
from .helpers import TrainState as TrainState
from .module import M as M
from .module import Module as Module
from .graph import merge as merge
from .graph import UpdateContext as UpdateContext
from .graph import update_context as update_context
from .graph import current_update_context as current_update_context
from .graph import split as split
from .graph import update as update
from .graph import clone as clone
from .graph import pop as pop
from .graph import state as state
from .graph import graphdef as graphdef
from .graph import iter_graph as iter_graph
from .graph import call as call
from .graph import SplitContext as SplitContext
from .graph import split_context as split_context
from .graph import MergeContext as MergeContext
from .graph import merge_context as merge_context
from .graph import variables as variables
from .graph import freeze as freeze
from .graph import mutable as mutable
from .graph import pure as pure
from .graph import cached_partial as cached_partial
from .nn import initializers as initializers
from .nn.activations import celu as celu
from .nn.activations import elu as elu
from .nn.activations import gelu as gelu
from .nn.activations import glu as glu
from .nn.activations import hard_sigmoid as hard_sigmoid
from .nn.activations import hard_silu as hard_silu
from .nn.activations import hard_swish as hard_swish
from .nn.activations import hard_tanh as hard_tanh
from .nn.activations import leaky_relu as leaky_relu
from .nn.activations import log_sigmoid as log_sigmoid
from .nn.activations import log_softmax as log_softmax
from .nn.activations import logsumexp as logsumexp
from .nn.activations import one_hot as one_hot
from .nn.activations import relu as relu
from .nn.activations import relu6 as relu6
from .nn.activations import selu as selu
from .nn.activations import sigmoid as sigmoid
from .nn.activations import silu as silu
from .nn.activations import soft_sign as soft_sign
from .nn.activations import softmax as softmax
from .nn.activations import softplus as softplus
from .nn.activations import standardize as standardize
from .nn.activations import swish as swish
from .nn.activations import tanh as tanh
from .nn.attention import MultiHeadAttention as MultiHeadAttention
from .nn.attention import combine_masks as combine_masks
from .nn.attention import dot_product_attention as dot_product_attention
from .nn.attention import make_attention_mask as make_attention_mask
from .nn.attention import make_causal_mask as make_causal_mask
from .nn.recurrent import RNNCellBase as RNNCellBase
from .nn.recurrent import LSTMCell as LSTMCell
from .nn.recurrent import GRUCell as GRUCell
from .nn.recurrent import OptimizedLSTMCell as OptimizedLSTMCell
from .nn.recurrent import SimpleCell as SimpleCell
from .nn.recurrent import RNN as RNN
from .nn.recurrent import Bidirectional as Bidirectional
from .nn.linear import Conv as Conv
from .nn.linear import ConvTranspose as ConvTranspose
from .nn.linear import Embed as Embed
from .nn.linear import Linear as Linear
from .nn.linear import LinearGeneral as LinearGeneral
from .nn.linear import Einsum as Einsum
from .nn.lora import LoRA as LoRA
from .nn.lora import LoRALinear as LoRALinear
from .nn.lora import LoRAParam as LoRAParam
from .nn.normalization import BatchNorm as BatchNorm
from .nn.normalization import LayerNorm as LayerNorm
from .nn.normalization import RMSNorm as RMSNorm
from .nn.normalization import GroupNorm as GroupNorm
from .nn.stochastic import Dropout as Dropout
from .rnglib import Rngs as Rngs
from .rnglib import RngStream as RngStream
from .rnglib import RngState as RngState
from .rnglib import RngKey as RngKey
from .rnglib import RngCount as RngCount
from .rnglib import fork_rngs as fork_rngs
from .rnglib import reseed as reseed
from .rnglib import split_rngs as split_rngs
from .rnglib import restore_rngs as restore_rngs
from .spmd import PARTITION_NAME as PARTITION_NAME
from .spmd import get_partition_spec as get_partition_spec
from .spmd import get_named_sharding as get_named_sharding
from .spmd import with_partitioning as with_partitioning
from .spmd import with_sharding_constraint as with_sharding_constraint
from .statelib import State as State
from .statelib import to_flat_state as to_flat_state
from .statelib import from_flat_state as from_flat_state
from .statelib import to_pure_dict as to_pure_dict
from .statelib import replace_by_pure_dict as replace_by_pure_dict
from .statelib import filter_state as filter_state
from .statelib import merge_state as merge_state
from .statelib import split_state as split_state
from .statelib import map_state as map_state
from .training import metrics as metrics
from .variablelib import Param as Param
# this needs to be imported before optimizer to prevent circular import
from .training import optimizer as optimizer
from .training.metrics import Metric as Metric
from .training.metrics import MultiMetric as MultiMetric
from .training.optimizer import OptState as OptState
from .training.optimizer import OptArray as OptArray
from .training.optimizer import OptVariable as OptVariable
from .training.optimizer import Optimizer as Optimizer
from .training.optimizer import ModelAndOptimizer as ModelAndOptimizer
from .training.optimizer import OptState as OptState
from .transforms.autodiff import DiffState as DiffState
from .transforms.autodiff import grad as grad
from .transforms.autodiff import value_and_grad as value_and_grad
from .transforms.autodiff import custom_vjp as custom_vjp
from .transforms.autodiff import remat as remat
from .transforms.compilation import jit as jit
from .transforms.compilation import shard_map as shard_map
from .transforms.compilation import StateSharding as StateSharding
from .transforms.iteration import Carry as Carry
from .transforms.iteration import scan as scan
from .transforms.iteration import vmap as vmap
from .transforms.iteration import pmap as pmap
from .transforms.transforms import eval_shape as eval_shape
from .transforms.transforms import cond as cond
from .transforms.transforms import switch as switch
from .transforms.transforms import checkify as checkify
from .transforms.iteration import while_loop as while_loop
from .transforms.iteration import fori_loop as fori_loop
from .transforms.iteration import StateAxes as StateAxes
from .variablelib import A as A
from .variablelib import BatchStat as BatchStat
from .variablelib import Cache as Cache
from .variablelib import Intermediate as Intermediate
from .variablelib import Perturbation as Perturbation
from .variablelib import Variable as Variable
from .variablelib import VariableMetadata as VariableMetadata
from .variablelib import with_metadata as with_metadata
from .variablelib import variable_type_from_name as variable_type_from_name
from .variablelib import variable_name_from_type as variable_name_from_type
from .variablelib import register_variable_name as register_variable_name
from .variablelib import mutable_array as mutable_array
from .variablelib import MutableArray as MutableArray
from .variablelib import is_mutable_array as is_mutable_array
from .variablelib import use_mutable_arrays as use_mutable_arrays
from .variablelib import using_mutable_arrays as using_mutable_arrays
from .visualization import display as display
from .extract import to_tree as to_tree
from .extract import from_tree as from_tree
from .extract import NodeStates as NodeStates
from .summary import tabulate as tabulate
from . import traversals as traversals

# alias VariableState
VariableState = Variable

import typing as _tp

if not _tp.TYPE_CHECKING:
  def __getattr__(name):
    if name == "VariableState":
      import warnings
      warnings.warn(
          "'VariableState' was removed, this is just an alias to 'Variable'. "
          "Plase use 'Variable' directly instead.",
          DeprecationWarning,
          stacklevel=2,
      )
    if name not in globals():
      raise AttributeError(f"Module {__name__} has no attribute '{name}'")

    return globals()[name]
