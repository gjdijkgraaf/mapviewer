var map;
var geojsonLayer;

// start the map
function start_map() {
        map = new L.map('map');

        // load a tile layer
        var osm = new L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                attribution: '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 17,
                minZoom: 6
            });

        // set the right view
        map.setView([52.20936, 5.970745], 7);
        map.addLayer(osm);

        // initialize layers
        var geojsonLayer = L.geoJSON();
        fetch_layer(geojsonLayer, arguments[0])

        // set function for when map changes
        map.on('moveend', onMapMove);

        function onMapMove() {
            fetch_layer(geojsonLayer, "/data/1");
        }

        return geojsonLayer;
}



// function to fetch new data from the database
function fetch_layer(layer, base_url) {
        // clear existing data
        layer.clearLayers();
        // create url to fetch data
        var bounds = map.getBounds();
        var url = base_url.concat("?xmin=", bounds._southWest.lng,
                                  "&ymin=", bounds._southWest.lat,
                                  "&xmax=", bounds._northEast.lng,
                                  "&ymax=", bounds._northEast.lat)
        // fetch and add data
        $.getJSON(url, function(data) {
            for(var i=0; i<data[0].features.length; i++) {
              layer.addData(data[0].features[i].feature).addTo(map)
            }
        });
}
