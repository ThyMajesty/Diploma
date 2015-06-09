(function() {
    var mapElem = document.getElementById("inputmap"),
        data_geojson = document.getElementById("data_geojson");
    addMarker = false;

    function constructMarkerImg(categ) {
        var st = new google.maps.MarkerImage('/static/icons/' + categ + '.png',
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0));
        console.log(st, '/static/icons/' + categ + '.png');
        return st;
    }

    function initialize() {
        mapElem = document.getElementById("inputmap");
        data_geojson = document.getElementById("data_geojson");
        var mapProp = {
            center: new google.maps.LatLng(50, 30),
            zoom: 11,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(mapElem, mapProp);
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            map.setCenter(pos);
        });
        google.maps.event.addListener(map, "click", function(event) {
            if (!addMarker) {
                addMarker = !addMarker;
                //u'color': u'3e8', u'coordinates': [50.456465770398644, 30.41187286376953], u'icon': u'3e8'
                var data = {
                    color: '3e8',
                    icon: '3e8'
                }
                data['coordinates'] = Object.keys(event.latLng).map(function(key) {
                    return event.latLng[key]
                }).reverse();
                data_geojson.value = JSON.stringify(data);
                var marker = new google.maps.Marker({
                    position: event.latLng,
                    draggable: true,
                    animation: google.maps.Animation.DROP
                });

                marker.setMap(map);

                google.maps.event.addListener(marker, 'dragend', function() {
                    var lnglat = marker.getPosition();

                    data['coordinates'] = Object.keys(event.latLng).map(function(key) {
                        return event.latLng[key]
                    }).reverse();
                    data_geojson.value = JSON.stringify(data);
                });
            }
        });


    }

    google.maps.event.addDomListener(window, 'load', initialize);

})()