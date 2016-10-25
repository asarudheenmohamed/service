import { AppComponent }   from './components/app.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { NgModule }      from '@angular/core';
import {HttpModule} from '@angular/http';
import {RouteService} from "./services/route.service"
import {MockService} from "./services/mock.service"


@NgModule({
    imports: [BrowserModule, FormsModule, HttpModule ],
    declarations: [AppComponent],
    bootstrap: [AppComponent],
    providers: [RouteService, MockService]
})
export class AppModule { }
