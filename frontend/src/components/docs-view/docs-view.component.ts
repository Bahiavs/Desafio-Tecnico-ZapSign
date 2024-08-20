import {Component, inject} from '@angular/core';
import {GetDocsService} from "../../services/get-docs.service";
import {AsyncPipe, JsonPipe, NgForOf} from "@angular/common";
import {DeleteDocService} from "../../services/delete-doc.service";
import {Dialog, DialogModule} from "@angular/cdk/dialog";
import {EditDocComponent} from "../edit-doc/edit-doc.component";

@Component({
    selector: 'docs-view',
    standalone: true,
    imports: [NgForOf, JsonPipe, AsyncPipe, DialogModule],
    templateUrl: './docs-view.component.html',
    styleUrl: 'docs-view.component.scss'
})
export class DocsViewComponent {
    private readonly _getDocsService = inject(GetDocsService);
    protected readonly deleteDocService = inject(DeleteDocService);
    protected readonly docs$ = this._getDocsService.execute();
    private readonly _dialog = inject(Dialog);

    update(doc: any) {
        this._dialog.open(EditDocComponent, {data: doc});
    }
}
