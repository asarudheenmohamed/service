import { Input, Component, OnInit, OnChanges, SimpleChange, AfterViewInit, NgZone } from '@angular/core';
import {RouteService} from '../services/route.service'
import {MockService} from '../services/mock.service'
import {Route} from '../models/route'

declare var google: any;

@Component({
    selector: 'my-app',
    template: `
<select  *ngIf="selectedRenderer" (change) = "onChange($event.target.value)">
  <option *ngFor='let item of renderers;let i = index' value="{{i}}">Route {{i}}</option>
</select>

<div id='map'></div>`,
    styles : [ '#map { height: 300px; }']
})
export class AppComponent implements OnInit, AfterViewInit {
    public routes: Route[];
    public selectedRoute: any;
    public renderers = <any>[];
    public selectedRenderer: string;
    public error: any;
    public map: any;

    constructor(private routeService: RouteService, zone:NgZone) {
        this.zone = zone
    }

    onChange(value) {
        this.selectedRenderer.setMap(null)
        console.log(value)
        this.selectedRenderer = this.renderers[value]
        this.selectedRenderer.setMap(this.map)
    }

    getRoute() {
        var that = this
        var onMapsReady = this.onMapsReady.bind(this)
        this.routeService
            .getRoutes()
            .then(routes => onMapsReady(routes))
            .catch(function(error) { that.error = error; console.log(error)});
    }

    ngOnInit() {
    }

    createRenderer(map, response) {
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
        this.renderers.push(directionsDisplay)
        this.zone.run(() => this.selectedRenderer = this.renderers[0])
    }

    fetchMapsData() {
        this.getRoute()
     }


    onMapsReady(routes) {
        this.routes = routes;

        function get_coords(a) {
        	return {lat: a.order_lat, lng: a.order_long}
        }

        var directionsService = new google.maps.DirectionsService();
        var source = null;
        let colors = ['red', 'purple', 'yellow']
        for (let route of routes) {
            var data = route.orders
            if (source == null) {
                var source = get_coords(data[0])
                this.map = new google.maps.Map(document.getElementById('map'), {
                  center: source,
                  scrollwheel: false,
                  zoom: 7
                });
            }

            var w_data = data.slice(1, data.length -2)
            var waypoints = []

            for (let coord of w_data) {
                waypoints.push({location: get_coords(coord)})
            }

            // Set destination, origin and travel mode.
            var request = {
              destination: get_coords(data[data.length - 1]),
              origin: source,
              travelMode: 'DRIVING',
              waypoints: waypoints
            };

            // Pass the directions request to the directions service.
            var createRenderer = this.createRenderer.bind(this)
            var that = this
            directionsService.route(request, function(response, status) {
              if (status == 'OK') {
                // Display the route on the map.
                    createRenderer(that.map, response)
              }
            });

        }



    }

    ngAfterViewInit() {
       (<any>window).fetchMapsData = this.fetchMapsData.bind(this);
       var script = document.createElement("script");
       script.type = "text/javascript";
       document.getElementsByTagName("head")[0].appendChild(script);
       script.src = "http://maps.googleapis.com/maps/api/js?v=3&key=AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU&callback=fetchMapsData";
    }

    get diagnostic() {
        return 1;
    }
}
;
