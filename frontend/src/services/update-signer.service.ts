import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GetDocsService} from "./get-docs.service";

@Injectable({providedIn: 'root'})
export class UpdateSignerService {
    private readonly _apiUrl = 'http://localhost:8000/documentapp/update-signer';
    private readonly _http = inject(HttpClient);
    private readonly _getDocsService = inject(GetDocsService);

    execute(id: any, signerData: any) {
        const url = `${this._apiUrl}/${id}`;
        const body = JSON.stringify(signerData);
        const subscription = this._http.patch<any>(url, body).subscribe({
            complete: () => {
                this._getDocsService.execute()
                subscription.unsubscribe()
            }
        })
    }
}
