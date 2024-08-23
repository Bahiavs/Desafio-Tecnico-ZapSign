import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";
import {BehaviorSubject} from 'rxjs';

@Injectable({providedIn: 'root'})
export class DeleteDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/delete/';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _loadingDocDeletions$ = new BehaviorSubject<Set<any>>(new Set())
    readonly loadingDocDeletions$ = this._loadingDocDeletions$.asObservable()

    execute(docID: any) {
        if (!confirm('Tem certeza que deseja deletar o documento?')) return;
        this._loadingDocDeletions$.next(this._loadingDocDeletions$.value.add(docID))
        const subscriber = this._http.delete<any>(`${this._apiUrl}${docID}`).subscribe({
            next: () => {
                this._getDocsService.execute();
                alert(`Sucesso ao deletar documento`)
            },
            error: () => alert(`Erro ao deletar documento ${docID}`),
            complete: () => {
                const loadingDocDeletions = this._loadingDocDeletions$.value
                loadingDocDeletions.delete(docID)
                this._loadingDocDeletions$.next(loadingDocDeletions)
                subscriber.unsubscribe()
            }
        });
    }
}