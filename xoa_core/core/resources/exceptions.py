import typing
if typing.TYPE_CHECKING:
    from .types import IProps


class InvalidTesterTypeError(ValueError):
    def __init__(self, props: "IProps") -> None:
        self.props = props
        self.msg = f"Can't identify Tester Type: {props.product}"
        super().__init__(self.msg)


class TesterCommunicationError(Exception):
    def __init__(self, props: "IProps", error: Exception) -> None:
        self.props = props
        self.error = error
        self.msg = f"Tester with credentials: {props} encountering communication error: {error}"
        super().__init__(self.msg)


class UnknownResourceError(Exception):
    def __init__(self, tester_id) -> None:
        self.tester_id = tester_id
        self.msg = f"Unknown tester of id: <{self.tester_id}>."
        super().__init__(self.msg)


class IsDisconnectedError(Exception):
    def __init__(self, tester_id) -> None:
        self.tester_id = tester_id
        self.msg = f"Tester: <{self.tester_id}> is already disconnected."
        super().__init__(self.msg)


class IsConnectedError(Exception):
    def __init__(self, tester_id) -> None:
        self.tester_id = tester_id
        self.msg = f"Tester: <{self.tester_id}> is already connected."
        super().__init__(self.msg)
