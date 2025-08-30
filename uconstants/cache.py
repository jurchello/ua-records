DEFAULT_TTL_SEC_LISTS = 24 * 3600
DEFAULT_TTL_SEC_FORMSTATE = 3600

CODEC_JSON = "json"
CODEC_LISTS = "lists"
CODEC_FORMSTATE = "formstate"

CACHE_SCHEMA_VERSION = "1.0"

NAMESPACE_LISTS = "lists"
NAMESPACE_FORMSTATE = "formstate"
NAMESPACE_MISC = "misc"

META_SUFFIX = ".meta.json"

DEFAULT_METADATA = {
    "ttl": None,
    "codec": CODEC_JSON,
    "schema_version": None,
    "created_at": 0.0,
    "updated_at": 0.0,
}
