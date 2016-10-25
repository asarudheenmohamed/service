import { Injectable }    from '@angular/core';
import { Headers, Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Route } from '../models/route';

@Injectable()
export class RouteService {
    private endpointUrl = 'http://localhost:8000/polls/my-own-view/';  // URL to web api
    constructor(private http: Http) { }

    getRoutes() {
        return this.http.get(this.endpointUrl)
            .toPromise()
            .then(function(response) {
                console.log(response.json() as Route[])
                return response.json()['route'] as Route[]
            })
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

    //    save(task: Task): Promise<Response> {
    //        // if (task.id) {
    //        //   return this.put(hero);
    //        // }
    //        return this.post(task);
    //    }
    //
    //    private post(task: Task): Promise<Response> {
    //        let headers = new Headers({
    //            'Content-Type': 'application/json',
    //            // 'auth': ()
    //            'Authorization': 'Token 73a3ea98a8def774b12f71632764ca8d544b5acb',
    //            'Access-Control-Request-Method': "POST"
    //        })
    //        console.log(JSON.stringify(task))
    //        return this.http.post(this.endpointUrl,
    //            JSON.stringify(task),
    //            { headers: headers })
    //            .toPromise()
    //            .then(function(res) {
    //                console.log(res.json());
    //                return res.json()
    //            })
    //            .catch(this.handleError)
    //
    //    }
    //
}
