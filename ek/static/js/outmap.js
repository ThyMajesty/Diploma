(function() {
    var mapElem = document.getElementById("outmap"),
        infowindow = new google.maps.InfoWindow(),
        actCat = document.getElementsByClassName('list-group-item active')[0].dataset.id,
        features = [],
        map = null;

    function processPoints(geometry, callback, thisArg) {
        if (geometry instanceof google.maps.LatLng) {
            callback.call(thisArg, geometry);
        } else if (geometry instanceof google.maps.Data.Point) {
            callback.call(thisArg, geometry.get());
        } else {
            geometry.getArray().forEach(function(g) {
                processPoints(g, callback, thisArg);
            });
        }
    }

    function loadGeoJsonString(geoString) {
        map.data.addGeoJson(geoString);
    }

    function initialize() {
        var mapProp = {
            center: new google.maps.LatLng(50, 30),
            zoom: 18,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(mapElem, mapProp);

        google.maps.event.addListener(map, 'click', function() {
            infowindow.close();
        });
        map.data.setStyle({
            fillOpacity: .8
        });
        // When the user clicks, open an infowindow
        map.data.addListener('click', function(event) {
            var title = event.feature.getProperty("title"),
                description = event.feature.getProperty("description");
            console.log(title, event.feature);
            infowindow.setContent('<div id="content">' +
                '<div id="siteNotice">' +
                '</div>' +
                '<h1 id="firstHeading" class="firstHeading">' + title + '</h1>' +
                '<div id="bodyContent">' +
                '<p>' + description + '</p>' +
                '</div>');
            infowindow.setPosition(event.feature.getGeometry().get());
            infowindow.setOptions({
                pixelOffset: new google.maps.Size(0, -30)
            });
            infowindow.open(map);
        });
        actCat = document.getElementsByClassName('list-group-item active')[0].dataset.id;
        $.get('/json/geopoints/' + actCat, function(data) {
            loadGeoJsonString(data);
        });

        // zoom to show all the features
        var bounds = new google.maps.LatLngBounds();
        map.data.addListener('addfeature', function(e) {
            processPoints(e.feature.getGeometry(), bounds.extend, bounds);
            map.fitBounds(bounds);
        });
    }


    google.maps.event.addDomListener(window, 'load', initialize);
})()