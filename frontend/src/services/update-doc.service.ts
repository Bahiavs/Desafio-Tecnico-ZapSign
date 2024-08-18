import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";

@Injectable({providedIn: 'root'})
export class UpdateDocService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/update-document';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);

    execute(documentID: any, documentData: any) {
        const url = `${this._apiUrl}${documentID}`;
        const body = JSON.stringify(documentData);
        /*const subscription = this._http.patch<any>(url, body).subscribe({
            complete: () => {
                this._getDocsService.execute()
                subscription.unsubscribe()
            }
        })*/
    }
}
