
import abc

from typing import TYPE_CHECKING

# avoid circular import
if TYPE_CHECKING: 
    from rda import Rda


class IRdaSerializable: 
    @abc.abstractmethod
    def to_rda(self)->'Rda':
        pass

    @abc.abstractmethod
    def from_rda(self, rda: 'Rda'):
        pass
