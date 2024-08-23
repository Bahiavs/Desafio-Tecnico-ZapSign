import {Component, inject} from '@angular/core';
import {GetDocsService} from "../../services/get-docs.service";
import {AsyncPipe, JsonPipe} from "@angular/common";
import {DeleteDocService} from "../../services/delete-doc.service";
import {Dialog, DialogModule} from "@angular/cdk/dialog";
import {EditDocComponent, EditDocComponentInput} from "../edit-doc/edit-doc.component";
import {EditSignerComponent, EditSignerComponentInput} from "../edit-signer/edit-signer.component";
import {UpdateDocService} from '../../services/update-doc.service';
import { UpdateSignerService } from '../../services/update-signer.service';

@Component({
    selector: 'docs-view',
    standalone: true,
    imports: [JsonPipe, AsyncPipe, DialogModule],
    templateUrl: './docs-view.component.html',
    styleUrl: 'docs-view.component.scss'
})
export class DocsViewComponent {
    private readonly _dialog = inject(Dialog);
    private readonly _getDocsService = inject(GetDocsService);
    private readonly _deleteDocService = inject(DeleteDocService);
    private readonly _updateDocService = inject(UpdateDocService);
    private readonly _updateSignerService = inject(UpdateSignerService);
    readonly loadingDocDeletions$ = this._deleteDocService.loadingDocDeletions$;
    readonly loadingDocUpdates$ = this._updateDocService.loadingDocUpdates$;
    readonly loadingSignerUpdates$ = this._updateSignerService.loadingSignerUpdates$;
    readonly docs$ = this._getDocsService.execute();
    
    editDoc(id: number, name: string) {
        this._dialog.open<any, EditDocComponentInput>(EditDocComponent, {data: {id, name}});
    }
    
    editSigner(id: number, name: string) {
        this._dialog.open<any, EditSignerComponentInput>(EditSignerComponent, {data: {id, name}});
    }
    
    deleteDoc(id: number) {
        this._deleteDocService.execute(id);
    }
}
