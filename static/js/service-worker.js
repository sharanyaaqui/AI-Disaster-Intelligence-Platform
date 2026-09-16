const CACHE_NAME = "divya-ai-offline-v3";

const FILES_TO_CACHE = [
    // Offline page
    "/offline",

    // Your custom CSS
    "/static/css/style.css",

    // Your logo
    "/static/images/divya-logo.png",

    // JavaScript
    "/static/js/script.js",
    "/static/js/offline.js",

    // MapLibre
    "/static/vendor/maplibre/maplibre-gl.js",
    "/static/vendor/maplibre/maplibre-gl.css",

    // PMTiles
    "/static/vendor/pmtiles/pmtiles.js",

    // Emergency facility database
    "/static/data/northern_zone_emergency_facilities.json",

    // Offline UP map
    "/static/maps/up.pmtiles"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(FILES_TO_CACHE))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => name !== CACHE_NAME)
                    .map(name => caches.delete(name))
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", event => {

    if (event.request.method !== "GET") {
        return;
    }

    const url = new URL(event.request.url);

    // Special handling for PMTiles byte-range requests
    if (url.pathname === "/static/maps/up.pmtiles") {

        event.respondWith(
            caches.open(CACHE_NAME).then(async cache => {

                const range = event.request.headers.get("Range");

                // If PMTiles asks for a specific byte range
                if (range) {

                    const cached = await cache.match(
                        "/static/maps/up.pmtiles"
                    );

                    if (cached) {

                        const match = range.match(/bytes=(\d+)-(\d*)/);

                        if (!match) {
                            return cached;
                        }

                        const start = Number(match[1]);
                        const requestedEnd = match[2]
                            ? Number(match[2])
                            : null;

                        const buffer = await cached.arrayBuffer();
                        const totalLength = buffer.byteLength;

                        const end = requestedEnd !== null
                            ? Math.min(requestedEnd, totalLength - 1)
                            : totalLength - 1;

                        if (start >= totalLength) {
                            return new Response(null, {
                                status: 416,
                                headers: {
                                    "Content-Range":
                                        `bytes */${totalLength}`
                                }
                            });
                        }

                        const chunk = buffer.slice(start, end + 1);

                        return new Response(chunk, {
                            status: 206,
                            statusText: "Partial Content",
                            headers: {
                                "Content-Type":
                                    "application/octet-stream",

                                "Content-Length":
                                    String(chunk.byteLength),

                                "Content-Range":
                                    `bytes ${start}-${end}/${totalLength}`,

                                "Accept-Ranges":
                                    "bytes"
                            }
                        });
                    }
                }

                // Normal request for PMTiles
                const cached = await cache.match(
                    "/static/maps/up.pmtiles"
                );

                if (cached) {
                    return cached;
                }

                return fetch(event.request);
            })
        );

        return;
    }

    // Normal caching for everything else
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {

            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(event.request)
                .then(response => {

                    if (response.ok) {

                        const responseClone = response.clone();

                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, responseClone);
                        });
                    }

                    return response;
                })
                .catch(() => {

                    // Only return offline page for navigation
                    if (event.request.mode === "navigate") {
                        return caches.match("/offline");
                    }

                    return new Response("", {
                        status: 503,
                        statusText: "Offline"
                    });
                });
        })
    );
});