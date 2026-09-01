// ==========================================
// DIVYA AI OFFLINE SYSTEM
// ==========================================


// ==========================================
// STORAGE KEYS
// ==========================================

const DIVYA_LOCATION_KEY =
    "divya_last_location";

const DIVYA_FACILITIES_KEY =
    "divya_emergency_facilities";


// ==========================================
// SAVE LOCATION
// ==========================================

function saveDivyaLocation(
    latitude,
    longitude
) {

    const location = {

        latitude:
            latitude,

        longitude:
            longitude,

        timestamp:
            Date.now()

    };


    localStorage.setItem(
        DIVYA_LOCATION_KEY,
        JSON.stringify(location)
    );


    console.log(
        "DIVYA location saved:",
        location
    );

}


// ==========================================
// GET SAVED LOCATION
// ==========================================

function getDivyaLocation() {

    const saved =
        localStorage.getItem(
            DIVYA_LOCATION_KEY
        );


    if (!saved) {

        return null;

    }


    try {

        return JSON.parse(saved);

    }

    catch (error) {

        console.error(
            "Unable to read saved location:",
            error
        );

        return null;

    }

}


// ==========================================
// SAVE FACILITIES
// ==========================================

function saveDivyaFacilities(
    facilities
) {

    const data = {

        facilities:
            facilities,

        timestamp:
            Date.now()

    };


    localStorage.setItem(
        DIVYA_FACILITIES_KEY,
        JSON.stringify(data)
    );


    console.log(
        "Emergency facilities saved locally:",
        facilities.length
    );

}


// ==========================================
// GET SAVED FACILITIES
// ==========================================

function getDivyaFacilities() {

    const saved =
        localStorage.getItem(
            DIVYA_FACILITIES_KEY
        );


    if (!saved) {

        return null;

    }


    try {

        return JSON.parse(saved);

    }

    catch (error) {

        console.error(
            "Unable to read saved facilities:",
            error
        );

        return null;

    }

}


// ==========================================
// CHECK ONLINE STATUS
// ==========================================

function isDivyaOnline() {

    return navigator.onLine;

}


// ==========================================
// OFFLINE STATUS UI
// ==========================================

function updateDivyaNetworkStatus() {

    const status =
        document.getElementById(
            "networkStatus"
        );


    if (!status) {

        return;

    }


    if (navigator.onLine) {

        status.innerHTML = `
            <i class="bi bi-wifi"></i>
            Online
        `;

        status.className =
            "badge bg-success";

    }

    else {

        status.innerHTML = `
            <i class="bi bi-wifi-off"></i>
            Offline Mode
        `;

        status.className =
            "badge bg-warning text-dark";

    }

}


// ==========================================
// ONLINE EVENT
// ==========================================

window.addEventListener(
    "online",
    function () {

        console.log(
            "DIVYA AI is back online."
        );

        updateDivyaNetworkStatus();

    }
);


// ==========================================
// OFFLINE EVENT
// ==========================================

window.addEventListener(
    "offline",
    function () {

        console.log(
            "DIVYA AI is now offline."
        );

        updateDivyaNetworkStatus();

    }
);


// ==========================================
// SERVICE WORKER REGISTRATION
// ==========================================

if ("serviceWorker" in navigator) {

    window.addEventListener(
        "load",
        function () {

            navigator.serviceWorker
                .register(
                    "/static/js/service-worker.js"
                )
                .then(function (registration) {

                    console.log(
                        "DIVYA Service Worker registered:",
                        registration.scope
                    );

                })
                .catch(function (error) {

                    console.error(
                        "Service Worker registration failed:",
                        error
                    );

                });

        }
    );

}


// ==========================================
// INITIAL STATUS
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        updateDivyaNetworkStatus();

    }
);