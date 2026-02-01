from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache-directory',
    'CACHE_DEFAULT_TIMEOUT': 3600  #we make the cache expire after 1h, don't know if it's ok but we'll keep it like that for now
})
