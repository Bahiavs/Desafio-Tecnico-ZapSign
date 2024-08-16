import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {CreateDocFormComponent} from "../components/create-doc-form/create-doc-form.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CreateDocFormComponent],
  template: `<create-doc-form/>`,
})
export class AppComponent {
}
