from typing import Sequence

from typing_extensions import NotRequired, TypedDict


TimestampStr = str


class DojoFeedItemAttachmentMetadataJson(TypedDict):
    mimetype: str
    filename: NotRequired[str]


class DojoFeedItemAttachmentJson(TypedDict):
    path: str
    type: NotRequired[str]
    metadata: NotRequired[DojoFeedItemAttachmentMetadataJson]


class DojoFeedItemContentsJson(TypedDict):
    body: NotRequired[str]
    attachments: NotRequired[Sequence[DojoFeedItemAttachmentJson]]


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


class DojoFeedLinkJson(TypedDict):
    href: str


class DojoFeedLinksJson(TypedDict):
    prev: NotRequired[DojoFeedLinkJson]
    next: NotRequired[DojoFeedLinkJson]


class DojoFeedResponseJson(TypedDict):
    _items: Sequence[DojoFeedItemJson]
    _links: NotRequired[DojoFeedLinksJson]
