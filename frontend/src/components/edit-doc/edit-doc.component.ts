import {Component, inject} from "@angular/core";
import {DIALOG_DATA, DialogRef} from "@angular/cdk/dialog";
import {FormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {UpdateDocService} from "../../services/update-doc.service";

@Component({
    selector: 'edit-doc',
    templateUrl: './edit-doc.component.html',
    styleUrl: './edit-doc.component.scss',
    standalone: true,
    imports: [ReactiveFormsModule]
})
export class EditDocComponent {
    private readonly _dialogRef = inject(DialogRef);
    private readonly _updateDocService = inject(UpdateDocService);
    private readonly _data = inject<EditDocComponentInput>(DIALOG_DATA);
    readonly nameFormCtrl = new FormControl(this._data.name, Validators.required);

    save() {
        if (this.nameFormCtrl.invalid) return
        this._updateDocService.execute(this._data.id, {name: this.nameFormCtrl.value as string})
        this._dialogRef.close()
    }
}

export interface EditDocComponentInput {
    id: number, 
    name: string
}