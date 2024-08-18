import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";

@Injectable({providedIn: 'root'})
export class DeleteDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/delete/';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);

    execute(docID: any) {
        if (!confirm('Tem certeza que deseja deletar o documento?')) return;
        const subscriber = this._http.delete<any>(`${this._apiUrl}${docID}`).subscribe({
            complete: () => {
                this._getDocsService.execute();
                subscriber.unsubscribe();
            }
        });
    }
}
