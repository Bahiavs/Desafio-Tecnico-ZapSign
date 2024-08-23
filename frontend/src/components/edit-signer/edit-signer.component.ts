import {Component, inject} from "@angular/core";
import {DIALOG_DATA, DialogRef} from "@angular/cdk/dialog";
import {FormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {UpdateSignerService} from "../../services/update-signer.service";

@Component({
    selector: 'edit-signer',
    templateUrl: './edit-signer.component.html',
    styleUrl: './edit-signer.component.scss',
    standalone: true,
    imports: [ReactiveFormsModule]
})
export class EditSignerComponent {
    private readonly _dialogRef = inject(DialogRef);
    private readonly _updateSignerService = inject(UpdateSignerService);
    private readonly _data = inject<EditSignerComponentInput>(DIALOG_DATA);
    readonly nameFormCtrl = new FormControl(this._data.name, Validators.required);

    save() {
        if (this.nameFormCtrl.invalid) return
        this._updateSignerService.execute(this._data.id, {name: this.nameFormCtrl.value as string})
        this._dialogRef.close()
    }
}

export interface EditSignerComponentInput {
    id: number, 
    name: string
}