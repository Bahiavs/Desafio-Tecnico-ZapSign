import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";
import {BehaviorSubject} from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({providedIn: 'root'})
export class DeleteDocService {
    private readonly _apiUrl = environment.apiUrl + '/delete';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _loadingDocDeletions$ = new BehaviorSubject<Set<number>>(new Set())
    readonly loadingDocDeletions$ = this._loadingDocDeletions$.asObservable()

    execute(id: number) {
        if (!confirm('Tem certeza que deseja deletar o documento?')) return;
        this._loadingDocDeletions$.next(this._loadingDocDeletions$.value.add(id))
        const subscriber = this._http.delete(`${this._apiUrl}/${id}`).subscribe({
            next: () => {
                this._getDocsService.execute();
                alert(`Sucesso ao deletar documento`)
            },
            error: () => alert(`Erro ao deletar documento ${id}`),
            complete: () => {
                const loadingDocDeletions = this._loadingDocDeletions$.value
                loadingDocDeletions.delete(id)
                this._loadingDocDeletions$.next(loadingDocDeletions)
                subscriber.unsubscribe()
            }
        });
    }
}