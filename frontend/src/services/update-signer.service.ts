import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";
import {BehaviorSubject} from 'rxjs';

@Injectable({providedIn: 'root'})
export class UpdateSignerService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/update-signer';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _loadingSignerUpdates$ = new BehaviorSubject<Set<number>>(new Set())
    readonly loadingSignerUpdates$ = this._loadingSignerUpdates$.asObservable()

    execute(id: number, signerData: UpdateSignerServiceInput) {
        const url = `${this._apiUrl}/${id}`;
        const body = JSON.stringify(signerData);
        this._loadingSignerUpdates$.next(this._loadingSignerUpdates$.value.add(id))
        const subscription = this._http.patch(url, body).subscribe({
            next: () => {
                this._getDocsService.execute();
                alert(`Sucesso ao editar signatário`)
            },
            error: () => alert(`Erro ao editar signatário ${id}`),
            complete: () => {
                const loadingDocUpdates = this._loadingSignerUpdates$.value
                loadingDocUpdates.delete(id)
                this._loadingSignerUpdates$.next(loadingDocUpdates)
                subscription.unsubscribe()
            }
        })
    }
}

interface UpdateSignerServiceInput {
	name: string
}