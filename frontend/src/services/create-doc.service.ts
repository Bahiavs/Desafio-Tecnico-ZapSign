import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsAPIResponse, GetDocsService} from "./get-docs.service";
import {environment} from '../environments/environment';
import {Subject} from 'rxjs';

@Injectable({providedIn: 'root'})
export class CreateDocService {
    private readonly _apiUrl = environment.apiUrl + '/create';
    private readonly _http = inject(HttpClient);
    private readonly _onSuccessfulResponse$ = new Subject<GetDocsAPIResponse>()
    readonly onSuccessfulResponse$ = this._onSuccessfulResponse$.asObservable()

    execute(documentData: CreateDocServiceInput) {
        const subscription = this._http.post<GetDocsAPIResponse>(this._apiUrl, JSON.stringify(documentData)).subscribe({
            next: (response) => {
                this._onSuccessfulResponse$.next(response)
                console.log(`Sucesso ao criar documento ${documentData.name}`)
            },
            error: () => alert(`Erro ao criar documento ${documentData.name}`),
            complete: () => subscription.unsubscribe()
        })
    }
}

export interface CreateDocServiceInput {
    name: string,
    url: string,
    signers: {
        name: string
        email: string
    }[]
}