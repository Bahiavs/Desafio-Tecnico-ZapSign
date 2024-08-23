import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";
import { BehaviorSubject } from 'rxjs';

@Injectable({providedIn: 'root'})
export class UpdateDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/update-document';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _loadingDocUpdates$ = new BehaviorSubject<Set<any>>(new Set())
    readonly loadingDocUpdates$ = this._loadingDocUpdates$.asObservable()

    execute(docID: any, documentData: any) {
        const url = `${this._apiUrl}/${docID}`;
        const body = JSON.stringify(documentData);
        this._loadingDocUpdates$.next(this._loadingDocUpdates$.value.add(docID))
        const subscription = this._http.patch<any>(url, body).subscribe({
            next: () => {
                this._getDocsService.execute();
                alert(`Sucesso ao editar documento`)
            },
            error: () => alert(`Erro ao editar documento ${docID}`),
            complete: () => {
                const loadingDocUpdates = this._loadingDocUpdates$.value
                loadingDocUpdates.delete(docID)
                this._loadingDocUpdates$.next(loadingDocUpdates)
                subscription.unsubscribe()
            }
        })
    }
}
