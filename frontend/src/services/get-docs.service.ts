import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';

@Injectable({providedIn: 'root'})
export class GetDocsService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/read'
    private readonly _http = inject(HttpClient)
    private readonly _docs$ = new BehaviorSubject<any[]>([])
    readonly docs$ = this._docs$.asObservable()

    execute(): Observable<any[]> {
        const subscription = this._http.get<any[]>(this._apiUrl).subscribe({
            next: (response) => {
                this._docs$.next(response);
            },
            error: (error) => {
                this._docs$.next([])
            },
            complete: () => subscription.unsubscribe()
        })
        return this.docs$
    }
}