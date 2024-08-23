import {Component, inject} from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {CreateDocService} from "../../services/create-doc.service";

@Component({
    selector: 'create-doc-form',
    standalone: true,
    imports: [ReactiveFormsModule, NgForOf],
    templateUrl: './create-doc-form.component.html',
    styleUrl: './create-doc-form.component.scss'
})
export class CreateDocFormComponent {
    private readonly _createDocService = inject(CreateDocService);
    private readonly _fb = inject(FormBuilder);
    readonly signers: FormArray = this._fb.array([]);
    readonly documentForm: FormGroup = this._fb.group({
        name: ['', Validators.required],
        url: ['', [Validators.required, Validators.pattern('https?://.+')]],
        signers: this.signers
    });

    constructor() {
        this.addSigner()
    }

    addSigner() {
        const signerForm = this._fb.group({
            name: ['', Validators.required],
            email: ['', [Validators.required, Validators.email]]
        });
        this.signers.push(signerForm);
    }

    removeSigner(index: number) {
        this.signers.removeAt(index);
    }

    onSubmit() {
        if (this.documentForm.valid) this._createDocService.execute(this.documentForm.value)
    }

    autoFill() {
        const nameFormCtrl = this.documentForm.get('name') as FormControl;
        nameFormCtrl.setValue('Documento A');
        const urlFormCtrl = this.documentForm.get('url') as FormControl;
        urlFormCtrl.setValue('https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf');
        this.signers.clear()
        const signerA = this._fb.group({
            name: ['Signatário A', Validators.required],
            email: ['signatarioA@email.com', [Validators.required, Validators.email]]
        });
        const signerB = this._fb.group({
            name: ['Signatário B', Validators.required],
            email: ['signatarioB@email.com', [Validators.required, Validators.email]]
        });
        this.signers.push(signerA);
        this.signers.push(signerB);
    }
}
