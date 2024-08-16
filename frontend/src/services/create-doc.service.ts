import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({providedIn: 'root'})
export class CreateDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/create';
    private readonly _http = inject(HttpClient);

    execute(documentData: any): Observable<any> {
        return this._http.post<any>(this._apiUrl, JSON.stringify(documentData));
    }
}
