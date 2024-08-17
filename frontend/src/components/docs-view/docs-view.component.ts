import {Component, inject, OnInit} from '@angular/core';
import {GetDocsService} from "../../services/get-docs.service";
import {DatePipe, JsonPipe, NgForOf} from "@angular/common";
import {DeleteDocService} from "../../services/delete-doc.service";

@Component({
    selector: 'docs-view',
    standalone: true,
    imports: [
        NgForOf,
        DatePipe,
        JsonPipe
    ],
    templateUrl: './docs-view.component.html',
    styleUrl: 'docs-view.component.scss'
})
export class DocsViewComponent implements OnInit {
    private readonly _getDocsService = inject(GetDocsService);
    readonly _deleteDocService = inject(DeleteDocService);
    docs: any[] = [];

    ngOnInit() {
        this._getDocsService.execute().subscribe({
            next: docs => this.docs = docs
        })
    }
}
