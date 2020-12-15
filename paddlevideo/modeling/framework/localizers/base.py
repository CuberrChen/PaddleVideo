# Copyright (c) 2020  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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

from abc import abstractmethod
from ... import builder
import paddle.nn as nn


class BaseLocalizer(nn.Layer):
    """Base class for Localization.
    All localizer should subclass it.
    All subclass should overwrite:
    - Methods:``train_step``, define your train step.
    - Methods:``valid_step``, define your valid step, always the same as train_step.
    - Methods:``test_step``, define your test step.
    """
    def __init__(self, backbone, loss):
        super().__init__()
        self.backbone = builder.build_backbone(backbone)
        self.loss = builder.build_loss(loss)
        self.init_weights()

    def init_weights(self):
        """Initialize the model network weights. """
        if getattr(self.backbone, 'init_weights'):
            self.backbone.init_weights()
        else:
            pass

    def forward(self, imgs):
        """Call backbone forward.
        """
        preds = self.backbone(imgs)
        return preds

    @abstractmethod
    def train_step(self, data_batch, **kwargs):
        """Training step.  input_data_batch -> loss_metric
        """
        raise NotImplementedError

    @abstractmethod
    def val_step(self, data_batch, **kwargs):
        """Validating setp. input_data_batch -> loss_metric
        """
        raise NotImplementedError

    @abstractmethod
    def test_step(self, data_batch, **kwargs):
        """Tets setp. to get acc in test data. input_data_batch -> output
        """
        raise NotImplementedError
