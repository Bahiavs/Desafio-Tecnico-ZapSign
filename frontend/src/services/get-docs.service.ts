import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';

@Injectable({providedIn: 'root'})
export class GetDocsService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/read'
    private readonly _http = inject(HttpClient)
    private readonly _docs$ = new BehaviorSubject<GetDocsState>([])
    readonly docs$ = this._docs$.asObservable()

    execute(): Observable<GetDocsState> {
        this._docs$.next('loading')
        const subscription = this._http.get<GetDocsServiceOutput>(this._apiUrl).subscribe({
            next: response => this._docs$.next(response),
            error: () => this._docs$.next('error'),
            complete: () => subscription.unsubscribe()
        })
        return this.docs$
    }
}

type GetDocsState = GetDocsServiceOutput | 'loading' | 'error'
type GetDocsServiceOutput = {
    documentID: number,
    name: string,
    status: string,
    createdAt: string,
    createdBy: string,
    signers: {
        name: string,
        email: string,
        status: string,
        id: number
    }[]
}[]
