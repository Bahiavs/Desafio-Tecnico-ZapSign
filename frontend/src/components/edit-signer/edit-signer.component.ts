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
    readonly data = inject(DIALOG_DATA);
    readonly dialogRef = inject(DialogRef);
    private readonly _updateSignerService = inject(UpdateSignerService);
    readonly nameFormCtrl = new FormControl(this.data.name, Validators.required);

    save() {
        if (this.nameFormCtrl.invalid) return
        this._updateSignerService.execute(this.data['id'], {'name': this.nameFormCtrl.value})
    }
}