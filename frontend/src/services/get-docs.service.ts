import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {CreateDocService} from './create-doc.service';

@Injectable({providedIn: 'root'})
export class GetDocsService {
    private readonly _apiUrl = environment.apiUrl + '/read'
    private readonly _http = inject(HttpClient)
    private readonly _docs$ = new BehaviorSubject<GetDocsState>([])
    private readonly _createDocService = inject(CreateDocService)
    readonly docs$ = this._docs$.asObservable()

    constructor() {
        this._createDocService.onSuccessfulResponse$.subscribe({
            next: this._onReceivedResponse.bind(this)
        })
    }

    execute(): Observable<GetDocsState> {
        this._docs$.next('loading')
        const subscription = this._http.get<GetDocsAPIResponse>(this._apiUrl).subscribe({
            next: this._onReceivedResponse.bind(this),
            error: () => this._docs$.next('error'),
            complete: () => subscription.unsubscribe()
        })
        return this.docs$
    }

    private _parseResponseToOutput(response: GetDocsAPIResponse): GetDocsServiceOutput {
        return response.map(docResponse => {
            return {...docResponse, createdAt: new Date(docResponse.createdAt)}
        })
    }
    
    private _onReceivedResponse(response: GetDocsAPIResponse) {
        const docOutput = this._parseResponseToOutput(response)
        this._docs$.next(docOutput)
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

export type GetDocsAPIResponse = {
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
