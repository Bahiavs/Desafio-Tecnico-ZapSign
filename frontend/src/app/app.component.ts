import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {CreateDocFormComponent} from "../components/create-doc-form/create-doc-form.component";
import {DocsViewComponent} from "../components/docs-view/docs-view.component";

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterOutlet, CreateDocFormComponent, DocsViewComponent],
    template: `
        <create-doc-form/>
        <hr>
        <docs-view/>
    `,
})
export class AppComponent {
}
