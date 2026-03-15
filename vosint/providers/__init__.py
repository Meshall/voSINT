from vosint.providers.bing_visual import BingVisualAdapter
from vosint.providers.google_lens import GoogleLensAdapter
from vosint.providers.pinterest import PinterestAdapter
from vosint.providers.tineye import TinEyeAdapter
from vosint.providers.yandex import YandexAdapter

DEFAULT_PROVIDER_ORDER = ["pinterest", "google_lens", "bing_visual", "yandex", "tineye"]

PROVIDER_REGISTRY = {
    "pinterest": PinterestAdapter,
    "google_lens": GoogleLensAdapter,
    "bing_visual": BingVisualAdapter,
    "yandex": YandexAdapter,
    "tineye": TinEyeAdapter,
}
