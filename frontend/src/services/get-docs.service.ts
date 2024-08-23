import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({providedIn: 'root'})
export class GetDocsService {
    private readonly _apiUrl = environment.apiUrl + '/read'
    private readonly _http = inject(HttpClient)
    private readonly _docs$ = new BehaviorSubject<GetDocsState>([])
    readonly docs$ = this._docs$.asObservable()

    execute(): Observable<GetDocsState> {
        this._docs$.next('loading')
        const subscription = this._http.get<GetDocsAPIResponse>(this._apiUrl).subscribe({
            next: response => {
                const docOutput: GetDocsServiceOutput = response.map(docResponse => {
                    return {...docResponse, createdAt: new Date(docResponse.createdAt)}
                })
                this._docs$.next(docOutput)
            },
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
    createdAt: Date,
    createdBy: string,
    signers: {
        name: string,
        email: string,
        status: string,
        id: number
    }[]
}[]

type GetDocsAPIResponse = {
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
