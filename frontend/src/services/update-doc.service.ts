import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";
import {BehaviorSubject} from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({providedIn: 'root'})
export class UpdateDocService {
    private readonly _apiUrl = environment.apiUrl + '/update-document';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _loadingDocUpdates$ = new BehaviorSubject<Set<number>>(new Set());
    readonly loadingDocUpdates$ = this._loadingDocUpdates$.asObservable();

    execute(id: number, documentData: UpdateDocServiceInput) {
        const url = `${this._apiUrl}/${id}`;
        const body = JSON.stringify(documentData);
        this._loadingDocUpdates$.next(this._loadingDocUpdates$.value.add(id))
        const subscription = this._http.patch(url, body).subscribe({
            next: () => {
                this._getDocsService.execute();
                console.log(`Sucesso ao editar documento`)
            },
            error: () => alert(`Erro ao editar documento ${id}`),
            complete: () => {
                const loadingDocUpdates = this._loadingDocUpdates$.value
                loadingDocUpdates.delete(id)
                this._loadingDocUpdates$.next(loadingDocUpdates)
                subscription.unsubscribe()
            }
        })
    }
}

interface UpdateDocServiceInput {
	name: string
}