import {Component, inject} from "@angular/core";
import {DIALOG_DATA, DialogRef} from "@angular/cdk/dialog";
import {FormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {UpdateDocService} from "../../services/update-doc.service";

@Component({
    selector: 'edit-doc',
    templateUrl: './edit-doc.component.html',
    styleUrl: './edit-doc.component.scss',
    standalone: true,
    imports: [
        ReactiveFormsModule
    ]
})
export class EditDocComponent {
    readonly data = inject(DIALOG_DATA);
    readonly dialogRef = inject(DialogRef);
    private readonly _updateDocService = inject(UpdateDocService);
    readonly nameFormCtrl = new FormControl(this.data.name, Validators.required);

    save() {
        if (this.nameFormCtrl.invalid) return
        this._updateDocService.execute(this.data['documentID'], {'name': this.nameFormCtrl.value})
    }
}