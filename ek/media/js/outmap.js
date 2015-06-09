(function() {
    var mapElem = document.getElementById("outmap"),
        actCat = document.getElementsByClassName('list-group-item active')[0].dataset.id,
        features = [],
        map = null,
        mc = null;

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

    function constructMarkerImg(categ) {
        var st = new google.maps.MarkerImage('/static/icons/' + categ + '.png',
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0));
        console.log(st, '/static/icons/' + categ + '.png');
        return st;
    }

    function initialize() {
        var mapProp = {
            center: new google.maps.LatLng(50, 30),
            zoom: 11,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(mapElem, mapProp);

        if (!mc && map)
            mc = new MarkerClusterer(map);
        map.data.setStyle({
            fillOpacity: .8
        });

        function bindInfoWindow(feature) {
            // When the user clicks, open an infowindow
            var infowindow = new google.maps.InfoWindow();

            google.maps.event.addListener(map, 'click', function() {
                infowindow.close();
            });

            google.maps.event.addListener(feature, 'click', function() {
                var title = feature.title,
                    description = feature.description;
                infowindow.setContent('<div id="content" style="color: #000;">' +
                    '<div id="siteNotice">' +
                    '</div>' +
                    '<h1 id="firstHeading" class="firstHeading">' + title + '</h1>' +
                    '<div id="bodyContent">' +
                    '<p>' + description + '</p>' +
                    '</div>');
                infowindow.setPosition(feature.position);
                infowindow.setOptions({
                    pixelOffset: new google.maps.Size(0, -30)
                });
                infowindow.open(map);
            });
        }

        actCat = document.getElementsByClassName('list-group-item active')[0].dataset.id;
        $.get('/json/geopoints/' + actCat, function(data) {
            loadGeoJsonString(data);
        });

        // zoom to show all the features
        var bounds = new google.maps.LatLngBounds();
        map.data.addListener('addfeature', function(e) {
            var geo = e.feature.getGeometry();
            var markerStyle = constructMarkerImg(e.feature.getProperty('category').toLowerCase());
            if (geo.getType() === 'Point') {
                var tmp = new google.maps.Marker({
                    position: geo.get(),
                    icon: markerStyle,
                    title: e.feature.getProperty('title'),
                    description: e.feature.getProperty('description'),
                    category: e.feature.getProperty('category')
                });
                mc.addMarker(tmp);
                map.data.remove(e.feature);
                bindInfoWindow(tmp);
            }
            processPoints(e.feature.getGeometry(), bounds.extend, bounds);
            map.fitBounds(bounds);
            console.log(e.feature);
        });
    }


    google.maps.event.addDomListener(window, 'load', initialize);
})()