from typing import Sequence

from typing_extensions import NotRequired, TypedDict


TimestampStr = str


class DojoFeedItemAttachmentMetadataJson(TypedDict):
    mimetype: str


class DojoFeedItemAttachmentJson(TypedDict):
    path: str
    type: str
    metadata: DojoFeedItemAttachmentMetadataJson


class DojoFeedItemContentsJson(TypedDict):
    body: str
    attachments: Sequence[DojoFeedItemAttachmentJson]


class DojoFeedItemJson(TypedDict):
    _id: str
    time: TimestampStr
    targetId: NotRequired[str]
    targetType: NotRequired[str]
    senderId: NotRequired[str]
    headerText: NotRequired[str]
    headerSubtext: NotRequired[str]
    senderName: NotRequired[str]
    type: NotRequired[str]
    contents: NotRequired[DojoFeedItemContentsJson]


class DojoFeedResponseJson(TypedDict):
    _items: Sequence[DojoFeedItemJson]
