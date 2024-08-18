import {Component, inject} from '@angular/core';
import {GetDocsService} from "../../services/get-docs.service";
import {AsyncPipe, DatePipe, JsonPipe, NgForOf} from "@angular/common";
import {DeleteDocService} from "../../services/delete-doc.service";
import {UpdateDocService} from "../../services/update-doc.service";

@Component({
    selector: 'docs-view',
    standalone: true,
    imports: [NgForOf, JsonPipe, AsyncPipe],
    templateUrl: './docs-view.component.html',
    styleUrl: 'docs-view.component.scss'
})
export class DocsViewComponent {
    private readonly _getDocsService = inject(GetDocsService);
    protected readonly deleteDocService = inject(DeleteDocService);
    protected readonly updateDocService = inject(UpdateDocService);
    protected readonly docs$ = this._getDocsService.execute();

    update() {
        this.updateDocService.execute(null, null)
    }
}
