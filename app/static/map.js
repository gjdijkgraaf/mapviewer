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
        setup_layer(geojsonLayer, arguments[0])
        
        // set function for when map changes
        map.on('moveend', onMapMove);
        
        function onMapMove() {
            update_layer(geojsonLayer, "/fetch/2");
        }
        
        return geojsonLayer;
}



function setup_layer(layer, url) {
        // load GeoJSON from an external URL
        $.getJSON(url, function(data) {
            layer.addData(data).addTo(map)
        });
}



// function to fetch new data from the database
function update_layer(layer, url) {
        layer.clearLayers();
        $.getJSON(url, function(data) {
            layer.addData(data).addTo(map)
        });
}