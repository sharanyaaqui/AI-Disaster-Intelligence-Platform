const CACHE_NAME = "divya-ai-v1";

const FILES_TO_CACHE = [
    "/",
    "/offline",
    "/static/css/style.css",
    "/static/js/script.js",
    "/static/js/offline.js",
    "/static/images/divya-logo.png",

    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
];


// ==========================================
// INSTALL
// ==========================================

self.addEventListener("install", function (event) {

    console.log("DIVYA AI Service Worker installing...");

    event.waitUntil(

        caches.open(CACHE_NAME)
            .then(function (cache) {

                return cache.addAll(FILES_TO_CACHE);

            })
            .then(function () {

                console.log(
                    "DIVYA AI offline files cached."
                );

                return self.skipWaiting();

            })

    );

});


// ==========================================
// ACTIVATE
// ==========================================

self.addEventListener("activate", function (event) {

    event.waitUntil(

        caches.keys()
            .then(function (cacheNames) {

                return Promise.all(

                    cacheNames.map(function (cacheName) {

                        if (
                            cacheName !== CACHE_NAME
                        ) {

                            console.log(
                                "Removing old cache:",
                                cacheName
                            );

                            return caches.delete(
                                cacheName
                            );

                        }

                    })

                );

            })
            .then(function () {

                return self.clients.claim();

            })

    );

});


// ==========================================
// FETCH
// ==========================================

self.addEventListener("fetch", function (event) {

    event.respondWith(

        caches.match(event.request)
            .then(function (cachedResponse) {

                if (cachedResponse) {

                    return cachedResponse;

                }


                return fetch(event.request)
                    .then(function (networkResponse) {

                        return networkResponse;

                    })
                    .catch(function () {

                        /*
                         * Internet unavailable.
                         * Return cached content if available.
                         */

                        return caches.match(
                            "/offline"
                        );

                    });

            })

    );

});