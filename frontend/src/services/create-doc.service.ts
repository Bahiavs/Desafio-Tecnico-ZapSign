import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";

@Injectable({providedIn: 'root'})
export class CreateDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/create';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);

    execute(documentData: any) {
        const subscription = this._http.post<any>(this._apiUrl, JSON.stringify(documentData)).subscribe({
            next: () => alert(`Sucesso ao criar documento ${documentData.name}`),
            error: () => alert(`Erro ao criar documento ${documentData.name}`),
            complete: () => {
                this._getDocsService.execute()
                subscription.unsubscribe()
            }
        })
    }
}
