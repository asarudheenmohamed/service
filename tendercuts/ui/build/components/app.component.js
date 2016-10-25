"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var route_service_1 = require('../services/route.service');
var AppComponent = (function () {
    function AppComponent(routeService, zone) {
        this.routeService = routeService;
        this.renderers = [];
        this.zone = zone;
    }
    AppComponent.prototype.onChange = function (value) {
        this.selectedRenderer.setMap(null);
        console.log(value);
        this.selectedRenderer = this.renderers[value];
        this.selectedRenderer.setMap(this.map);
    };
    AppComponent.prototype.getRoute = function () {
        var that = this;
        var onMapsReady = this.onMapsReady.bind(this);
        this.routeService
            .getRoutes()
            .then(function (routes) { return onMapsReady(routes); })
            .catch(function (error) { that.error = error; console.log(error); });
    };
    AppComponent.prototype.ngOnInit = function () {
    };
    AppComponent.prototype.createRenderer = function (map, response) {
        var _this = this;
        var lineSymbol = {
            path: 'M 1.5 1 L 1 0 L 1 2 M 0.5 1 L 1 0',
            fillColor: 'black',
            strokeColor: 'black',
            strokeWeight: 2,
            strokeOpacity: 1
        };
        var directionsDisplay = new google.maps.DirectionsRenderer({
            polylineOptions: {
                icons: [{
                        icon: lineSymbol,
                        offset: '25px',
                        repeat: '100px'
                    }]
            }
        });
        directionsDisplay.setDirections(response);
        this.renderers.push(directionsDisplay);
        this.zone.run(function () { return _this.selectedRenderer = _this.renderers[0]; });
    };
    AppComponent.prototype.fetchMapsData = function () {
        this.getRoute();
    };
    AppComponent.prototype.onMapsReady = function (routes) {
        this.routes = routes;
        function get_coords(a) {
            return { lat: a.order_lat, lng: a.order_long };
        }
        var directionsService = new google.maps.DirectionsService();
        var source = null;
        var colors = ['red', 'purple', 'yellow'];
        for (var _i = 0, routes_1 = routes; _i < routes_1.length; _i++) {
            var route = routes_1[_i];
            var data = route.orders;
            if (source == null) {
                var source = get_coords(data[0]);
                this.map = new google.maps.Map(document.getElementById('map'), {
                    center: source,
                    scrollwheel: false,
                    zoom: 7
                });
            }
            var w_data = data.slice(1, data.length - 2);
            var waypoints = [];
            for (var _a = 0, w_data_1 = w_data; _a < w_data_1.length; _a++) {
                var coord = w_data_1[_a];
                waypoints.push({ location: get_coords(coord) });
            }
            // Set destination, origin and travel mode.
            var request = {
                destination: get_coords(data[data.length - 1]),
                origin: source,
                travelMode: 'DRIVING',
                waypoints: waypoints
            };
            // Pass the directions request to the directions service.
            var createRenderer = this.createRenderer.bind(this);
            var that = this;
            directionsService.route(request, function (response, status) {
                if (status == 'OK') {
                    // Display the route on the map.
                    createRenderer(that.map, response);
                }
            });
        }
    };
    AppComponent.prototype.ngAfterViewInit = function () {
        window.fetchMapsData = this.fetchMapsData.bind(this);
        var script = document.createElement("script");
        script.type = "text/javascript";
        document.getElementsByTagName("head")[0].appendChild(script);
        script.src = "http://maps.googleapis.com/maps/api/js?v=3&key=AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU&callback=fetchMapsData";
    };
    Object.defineProperty(AppComponent.prototype, "diagnostic", {
        get: function () {
            return 1;
        },
        enumerable: true,
        configurable: true
    });
    AppComponent = __decorate([
        core_1.Component({
            selector: 'my-app',
            template: "\n<select  *ngIf=\"selectedRenderer\" (change) = \"onChange($event.target.value)\">\n  <option *ngFor='let item of renderers;let i = index' value=\"{{i}}\">Route {{i}}</option>\n</select>\n\n<div id='map'></div>",
            styles: ['#map { height: 300px; }']
        }), 
        __metadata('design:paramtypes', [route_service_1.RouteService, core_1.NgZone])
    ], AppComponent);
    return AppComponent;
}());
exports.AppComponent = AppComponent;
;
//# sourceMappingURL=app.component.js.map