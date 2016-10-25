import { Injectable }    from '@angular/core';
import { Headers, Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Route } from '../models/route';

@Injectable()
export class MockService {
    private endpointUrl = 'http://localhost:8000/polls/my-own-view/';  // URL to web api
    private mockResponse: string = `
        {"route":[{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.92940049943596,"order_id":"e1c895a7-94b2-4cd0-9681-addc34e5f4a2","order_long":77.62507283430563}],"route_distance":338582,"route_duration":20478},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.937726558052173,"order_id":"f8ba2906-8b7c-4eb9-b8f2-4772d6a57ea9","order_long":77.61873534930234}],"route_distance":339466,"route_duration":20677},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.937926214779678,"order_id":"e383135a-ff2a-4dca-a2cc-37b92bcdf542","order_long":77.61582324328607}],"route_distance":340034,"route_duration":20689},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.946015958544878,"order_id":"8acc18bf-e3e5-4758-901b-528ab35525e5","order_long":77.62195027580779}],"route_distance":340417,"route_duration":20939},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.953436810643643,"order_id":"9790fced-2def-4c24-89b9-0593cf6baeb8","order_long":77.62646066045268}],"route_distance":341662,"route_duration":21161},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.943462677652683,"order_id":"11bc4415-56ac-4f61-8957-7bf70d27dcae","order_long":77.61220753694022}],"route_distance":340350,"route_duration":20894},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.955975626653235,"order_id":"054f0f7e-9e1f-4bda-b46f-7674ad8608c7","order_long":77.61677429937389}],"route_distance":341999,"route_duration":21292},{"orders":[{"order_lat":12.9329359,"order_id":0,"order_long":80.2305887},{"order_lat":12.958243463575355,"order_id":"b493543d-f1a2-494e-803c-6bfc1e166931","order_long":77.61896019677037}],"route_distance":342254,"route_duration":21295}]}
    `
    constructor(private http: Http) { }

    getRoutes() {
        var data = JSON.parse(this.mockResponse)
        var routes = data['route'] as Route[]
        console.log(routes)
        return Promise.resolve(routes)
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

}

