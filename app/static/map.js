// start the map
function start_map() {
        // retrieve layers
        layers = arguments[0];
        for(var i=0; i<arguments[0].length; i++) {
            layers[i].active = true
        };

        // define layer variables
        // load a tile layer
        var osm = new L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                attribution: '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 17,
                minZoom: 6
            });

        // load the overlays
        geojsonLayers = [];
        for(var i=0; i<layers.length; i++) {
            geojsonLayers[i] = L.geoJSON();
        }

        // prepare the list of layers to initialize
        init_layers = [osm].concat(geojsonLayers)

        // start the map
        var map = new L.map('map', {
            center: [52.1552404, 5.3850295],
            zoom: 7,
            layers: init_layers
        });

        // define layers for control group
        var baseMaps = {
            "OpenStreetMap": osm
        };
        var overlayMaps = {}
        for(var i=0; i<layers.length; i++) {
            overlayMaps[layers[i].name] = geojsonLayers[i]
        };

        // initialize control group
        L.control.layers(baseMaps, overlayMaps, {'collapsed': false}).addTo(map);

        // fill with data
        for(var i=0; i<layers.length; i++) {
            fetch_layer(map, geojsonLayers[i], layers[i].url)
        };

        // set function for when map changes
        map.on('moveend', onMapMove);

        // set layers to inactive/active to prevent too much data traffic
        map.on('overlayremove', function(overlay) {
            for(var i=0; i<layers.length; i++) {
                if(layers[i].name == overlay.name) {
                    layers[i].active = false
                }
            }
        });
        map.on('overlayadd', function(overlay) {
            for(var i=0; i<layers.length; i++) {
                if(layers[i].name == overlay.name) {
                    layers[i].active = true
                }
            }
        });

        // reload the map data when the map is moved
        function onMapMove() {
            for(var i=0; i<layers.length; i++) {
                if (layers[i].active == true) {
                    fetch_layer(map, geojsonLayers[i], layers[i].url)
                }
            }
        };

}



// function to fetch new data from the database
function fetch_layer(map, layer, base_url) {
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
              layer.addData(data[0].features[i].feature)
            }
        });
}
